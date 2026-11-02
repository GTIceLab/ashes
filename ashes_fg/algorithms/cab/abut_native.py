"""Native abutting CAB adapter selected by library metadata.

Builds a reviewable circuit model. Strict construction rejects incomplete
electrical contracts before returning a design to the synthesis driver.
"""
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
import json
import math

import ashes_fg.asic.model.asic_compile as ac
from ashes_fg.asic.library.cell_profiles import load_cell_library
from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid, grid_layout
from ashes_fg.asic.peripherals.fg_generation import Generated
from ashes_fg.algorithms.common import native_port
from ashes_fg.algorithms.system_build import CircuitBuilder, join, pins
from ashes_fg.algorithms.common import connect
from ashes_fg.algorithms.cab.a_bias import bind_connections
from ashes_fg.algorithms.cab import Interfaces, load, validate_dimensions
from ashes_fg.algorithms.cab.matrix_rows import build as matrix_rows
from ashes_fg.algorithms.sblock.sectioned import build as sectioned_sblock
from ashes_fg.algorithms.sblock.sectioned import gate_fillers
from ashes_fg.algorithms.cab.component_interfaces import bind_component, bind_activation
from ashes_fg.algorithms.decoders.bridged_radix4 import build as bridged_decoder
from ashes_fg.algorithms.decoders.bridged_radix4 import unresolved_pins
from ashes_fg.algorithms.cab.relative_layout import create as relative_layout
from ashes_fg.algorithms.cab.band_layout import column_sources, section_gates, decoder_bands, drain_offsets


def build(project, settings_path=None, *, cells, process_coordinates='xy', strict=True, design_limits=None):
    project = Path(project)
    library = load_cell_library(cells)
    profile = library.cab_profile
    if design_limits is None:
        synthesis_path = project / 'synthesis_settings.json'
        synthesis = json.loads(synthesis_path.read_text()) if synthesis_path.is_file() else {}
        design_limits = synthesis.get('design_limits', profile.get('design_limits'))
    if design_limits is None:
        raise ValueError('Set design_limits in the design build call or synthesis_settings.json')
    if process_coordinates != profile['process_coordinates']:
        raise ValueError('The selected CAB recipe requires its declared native coordinates')
    interfaces = Interfaces(library.__file__, profile.get('devices', {}))
    params = load(settings_path or project / 'cab_settings.json', interfaces,
                  shared_gate_selection=True, sblock_gate_channels=profile['sblock_gate_channels'])
    validate_dimensions(params, row_unit=profile['matrix_unit'][0], column_unit=profile['matrix_unit'][1],
                        sblock_unit=profile['sblock']['lane_unit'])
    top = ac.Circuit()
    top.routing_access_contract = deepcopy(profile.get('routing_access'))
    from ashes_fg.class_lib_mux import frame as Frame
    frame = Frame(top)
    builder = CircuitBuilder(top, frame=frame, cells=library, process_coordinates=process_coordinates,
        matrix_unit=profile['matrix_unit'], supply_names=profile['supply_names'],
        supply_aliases=profile.get('supply_aliases', {}),
        static_families=profile['static_families'], shared_controls=())
    masters = profile['masters']
    matrices, assemblies = {}, {}
    for name, rows, columns in (
            ('A', params.AMatrix_Rows, params.AMatrix_Cols),
            ('B', params.BMatrix_Rows, params.BMatrix_Cols),
            ('Out', params.OutMatrix_Rows, params.OutMatrix_Cols),
            ('CEW', params.CEW_Rows, params.CEW_Cols),
            ('CNS', params.CNS_Rows, params.CNS_Cols)):
        assembly = matrix_rows(top, builder.island(name), cells=library, master=masters['matrix'],
            rows=rows, columns=columns, unit=profile['matrix_unit'],
            recipe=profile['matrix_rows'].get(name, {}), coordinates=process_coordinates)
        matrices[name], assemblies[name] = assembly.core or assembly.body[0], assembly
        for cell in assembly.body:
            builder.static(cell)
    builder.matrices.update(matrices)
    device_input_count = sum(len(d.inputs) * d.count for d in params.devices)
    for name in ('A', 'B'):
        capacity = len(assemblies[name].usable_read_drains)
        if device_input_count > capacity:
            raise ValueError(f'{name}: {device_input_count} required device lanes exceed {capacity} usable '
                             f'read lanes in {assemblies[name].nominal_rows} nominal rows; '
                             f'reserved slots: {assemblies[name].reserved_read_lanes}')

    def mapped(cell, role, key):
        if isinstance(cell, tuple):
            return [pin for member in cell for pin in mapped(member, role, key)]
        return [pin for name in profile['ports'][role][key] for pin in native_port(cell, name).pins]

    # Exact native role mappings come from the library, including case-sensitive names.
    gors = {}
    for name in ('A', 'B'):
        columns = getattr(params, name + 'Matrix_Cols')
        switch = builder.bank(name + '_GorS', masters['gors'], 1, columns // profile['matrix_unit'][1])
        gors[name] = switch
        for switch_role, body_role in (('matrix_sources', 'source_top'), ('matrix_gates', 'gate_top'),
                                       ('selection', 'selection_top')):
            join(mapped(switch, 'gors', switch_role), mapped(matrices[name], 'matrix', body_role))
            for port_name in profile['ports']['gors'][switch_role]:
                native_port(switch, port_name).native_abutment = True
        # Owner-approved abutting memory contract: top fgmem -> GorS pull-up controls.
        join(mapped(assemblies[name].before[0], 'ab_top', 'memory'), mapped(switch, 'gors', 'memory_controls'))
    output_switch = builder.bank('Out_switch', masters['output_switch'], 1,
                                 params.OutMatrix_Cols // profile['matrix_unit'][1])
    for key, host, role in (('sources_in', 'B', 'source_bottom'), ('gates_in', 'B', 'gate_bottom'),
                            ('sources_out', 'Out', 'source_top'), ('gates_out', 'Out', 'gate_top')):
        join(mapped(output_switch, 'output_switch', key), mapped(matrices[host], 'matrix', role))
        for port_name in profile['ports']['output_switch'][key]:
            native_port(output_switch, port_name).native_abutment = True
    join(mapped(assemblies['B'].after[0], 'b_bottom', 'memory'),
         mapped(output_switch, 'output_switch', 'memory_controls'))
    join(mapped(output_switch, 'output_switch', 'selection'), mapped(matrices['B'], 'matrix', 'selection_bottom'))
    join(mapped(matrices['Out'], 'matrix', 'selection_top'), mapped(matrices['B'], 'matrix', 'selection_bottom'))
    # This bank's north face abuts B; none of its contacts need routing.
    for port in output_switch.ports:
        if getattr(port, 'native_location', port.location) == 'N':
            port.native_abutment = True

    sblock = sectioned_sblock(top, builder.island('Sblock'), params.CSC_rows,
                              cells=library, profile=profile['sblock'])
    for cell in sblock.body:
        builder.static(cell)
    # Match TILE_NN grouping. Matrix side ports serialize at the final
    # physical column; opposite native copies are not additional targets.
    builder.expose('N', sblock.north, 'N')
    builder.expose('E', sblock.east, 'E')
    builder.expose('S', assemblies['CNS'].usable_read_drains, 'S')
    builder.expose('W', assemblies['CEW'].usable_read_drains, 'W')
    builder.expose('Sblock_S', sblock.south, 'S')
    builder.expose('Sblock_W', sblock.west, 'W')

    s_columns = column_sources(sblock.body)
    s_slots = [cell.algorithm_xy[0] for cell in sblock.sections]
    addresses = {
        'CEW': list(range(params.CEW_Cols)),
        'Sblock': list(range(params.CEW_Cols, params.CEW_Cols + len(sblock.gates))),
        'CNS': list(range(params.CEW_Cols + len(sblock.gates),
                          params.CEW_Cols + len(sblock.gates) + params.CNS_Cols)),
    }
    gate_count = params.CEW_Cols + len(sblock.gates) + params.CNS_Cols
    active_addresses = [i for group in addresses.values() for i in group]
    gate = bridged_decoder(top, builder.island('Gate_decoder'), gate_count, cells=library,
                           master=masters['gate_decoder'], role='gate',
                           auxiliary_contract=profile.get('decoder_auxiliary', {}).get('gate'),
                           active_outputs=active_addresses, family=profile['decoder_cells']['gate'],
                           interface=profile['decoder_interface']['gate'])
    custom_layouts = {'Gate_decoder': decoder_bands()}
    for cell in gate.instances:
        cell.fg_geometry = ('gate_decoder', *cell.algorithm_xy)
    gate_bodies = (('CEW', mapped(matrices['CEW'], 'matrix', 'gate_top'),
                   mapped(matrices['CEW'], 'matrix', 'selection_top')),
                  ('Sblock', list(sblock.gates), list(sblock.selections)),
                  ('CNS', mapped(matrices['CNS'], 'matrix', 'gate_top'),
                   mapped(matrices['CNS'], 'matrix', 'selection_top')))
    gate_selection = []
    sblock_gate_fillers = ()
    for name, gates, selects in gate_bodies:
        owner = builder.island(name + '_gate_switch')
        grid = AlgorithmGrid.for_process(owner, process_coordinates)
        if name == 'Sblock':
            switches = []
            for band in s_slots:
                cell = grid.create(getattr(library, masters['gate_switch']), top)
                grid.place(cell, (band, 0))
                cell.fg_geometry = ('section_gate', band)
                switches.append(cell)
            switch = tuple(switches)
            if profile['sblock'].get('gate_fillers'):
                sblock_gate_fillers = gate_fillers(top, owner, cells=library, sblock=sblock,
                                                  specifications=profile['sblock']['gate_fillers'])
                for filler in sblock_gate_fillers:
                    builder.static(filler)
            custom_layouts[name + '_gate_switch'] = section_gates(s_columns)
        else:
            unit = profile['gate_switch_unit']
            if len(gates) % unit:
                raise ValueError('Gate channels do not fit the selected switch lane unit')
            switch = grid.create(getattr(library, masters['gate_switch']), top, dim=(1, len(gates) // unit))
            grid.place(switch, (0, 0))
        builder.support[name + '_gate_switch'] = switch
        join(mapped(switch, 'gate_switch', 'selection'), [gate.outputs[i] for i in addresses[name]])
        join(mapped(switch, 'gate_switch', 'gates'), gates)
        shifted = mapped(switch, 'gate_switch', 'body_selection')
        join(shifted, selects)
        gate_selection.extend(shifted)
        join(mapped(switch, 'gate_switch', 'run_output'), [gate.run_outputs[i] for i in addresses[name]])
        builder.common(profile['gate_switch_run_net'], mapped(switch, 'gate_switch', 'run_input'))
        # VPWR/VDD on this cell can carry analog paths; never blanket-tie them.
        for member in switch if isinstance(switch, tuple) else (switch,):
            for net, names in profile['gate_switch_shared_ports'].items():
                for native in names:
                    builder.common(net, native_port(member, native))
    # The shared CAB selection prefix serves the already integrated A/B switches.
    targets = mapped(gors['A'], 'gors', 'selection') + mapped(gors['B'], 'gors', 'selection')
    join(gate_selection[:len(targets)], targets)
    builder.expose('Gate_bits', gate.bits)
    builder.expose('Gate_enable', gate.enable)
    if gate.run_inputs:
        run_net = profile.get('gate_analog_input_net')
        if run_net is not None:
            if not isinstance(run_net, str) or not run_net.strip():
                raise ValueError('gate_analog_input_net must name the shared run rail')
            builder.common(run_net, gate.run_inputs)
        else:
            builder.expose('Gate_analog_in', gate.run_inputs, 'N')
    for family, rail in gate.supplies.items():
        builder.common(family, rail)

    # Opposite core-edge terminals are explicit copies of the same signal lanes.
    for body in matrices.values():
        for first, second in profile['matrix_continuity']:
            names = {p.native_name for p in body.ports}
            if first in names and second in names:
                join(native_port(body, first), native_port(body, second))

    scan_slice = slice(*profile['volatile']['body_lane_slice'])
    volatile_lanes = len(mapped(matrices['A'], 'matrix', 'source_bottom')[scan_slice])
    volatile_unit = profile['volatile']['lane_unit']
    if not volatile_lanes or volatile_lanes % volatile_unit:
        raise ValueError('Selected A lanes do not fit the volatile cell lane unit')
    volatile = builder.bank('Volatile', profile['volatile']['master'], 1, volatile_lanes // volatile_unit)
    # Intentionally no FG generator call for the volatile block.
    for role, key in profile['volatile']['body_bindings']:
        join(mapped(volatile, 'volatile', role), mapped(matrices['A'], 'matrix', key)[scan_slice])
    # The volatile bank's north face abuts A, including its supply contacts.
    for port in volatile.ports:
        if getattr(port, 'native_location', port.location) == 'N':
            port.native_abutment = True
    volatile_interfaces = bind_component(builder, volatile, profile['volatile']['interface'])

    # Programming drains share the legacy AB and C-block groups. Reserved read
    # positions stay empty; their valid programming positions remain connected.
    for hosts in profile['shared_programming_groups']:
        for host in hosts[1:]:
            join(assemblies[hosts[0]].programming_drains, assemblies[host].programming_drains)
    join(assemblies[profile['sblock_programming_host']].programming_drains, sblock.programming_drains)
    drains, drain_switches, host_y_offsets = {}, {}, {}
    for name, hosts in profile['drain_groups'].items():
        count = sum(a.nominal_rows for a in (assemblies[host] for host in hosts))
        owner = builder.island(name)
        drain_switches[name] = {}
        offsets = {}
        for host, reference in profile.get('drain_host_x_offsets', {}).get(name, {}).items():
            assembly = assemblies[reference]
            member = assembly.body[0]
            offsets[host] = (member.name, member.dim[1])
        if offsets:
            custom_layouts[name] = drain_offsets(offsets)
        row_gaps = {}
        cursor = 0
        for host in hosts[:-1]:
            cursor += assemblies[host].physical_rows
            reference = profile.get('drain_group_gaps', {}).get(name, {}).get(host)
            if reference:
                contract = reference if isinstance(reference, dict) else {'reference': reference}
                body = builder.support[contract['reference']]
                pitch = assemblies[host].body[0].size[1]
                reference_height = body.size[1] * body.dim[0]
                gap_height = reference_height
                clearance_reference = contract.get('clearance_reference')
                if clearance_reference:
                    clearance_body = builder.support[clearance_reference]
                    gap_height = max(gap_height, clearance_body.size[1] * clearance_body.dim[0]
                                     + contract.get('clearance_um', 0))
                gap_rows = math.ceil(gap_height / pitch - 1e-9)
                row_gaps[cursor] = gap_rows
                next_host = hosts[hosts.index(host) + 1]
                host_y_offsets[next_host] = -(gap_rows * pitch - reference_height) * profile['placement_units_per_um']
        decode = bridged_decoder(top, owner, count, cells=library,
                                 master=masters['drain_decoder'], role='drain',
                                 auxiliary_contract=profile.get('decoder_auxiliary', {}).get('drain'),
                                 row_gaps=row_gaps, family=profile['decoder_cells']['drain'],
                                 interface=profile['decoder_interface']['drain'])
        # Drain leaf outputs meet SELECT contacts by native abutment.
        output_name = profile['decoder_interface']['drain']['outputs']
        for cell in decode.instances:
            for port in cell.ports:
                if port.native_name == output_name:
                    port.native_abutment = True
        grid = AlgorithmGrid.for_process(owner, process_coordinates)
        last_column = max(cell.algorithm_xy[0] for cell in decode.instances) + 1
        lane = 0
        for host in hosts:
            assembly = assemblies[host]
            switch = grid.create(getattr(library, masters['drain_switch']), top,
                                  dim=(assembly.physical_rows, 1))
            row = lane // profile['matrix_unit'][0]
            row += sum(size for start, size in row_gaps.items() if start <= row)
            grid.place(switch, (last_column, row))
            switch.fg_geometry = ('drain_switch', host)
            drain_switches[name][host] = switch
            join(mapped(switch, 'drain_switch', 'selection'), decode.outputs[lane:lane + assembly.nominal_rows])
            for port_name in profile['ports']['drain_switch']['selection']:
                native_port(switch, port_name).native_abutment = True
            join(mapped(switch, 'drain_switch', 'program'), assembly.programming_drains)
            placement = profile['island_layout'][name]
            if placement.get('reference') == host and placement.get('gap', 0) == 0:
                # Direct host contact is native; remote extension paths still route.
                for role in ('program', 'read'):
                    for port_name in profile['ports']['drain_switch'][role]:
                        native_port(switch, port_name).native_abutment = True
            for source, target in zip(mapped(switch, 'drain_switch', 'read'), assembly.read_slots):
                if target is not None:
                    connect(source, target)
            builder.static(switch)
            lane += assembly.nominal_rows
        for family, rail in decode.supplies.items():
            builder.common(family, rail)
        builder.expose(name + '_enable', decode.enable)
        drains[name] = decode
    address_width = max(len(d.bits) for d in drains.values())
    drain_bits = ac.Bus(top, size=address_width)
    for decode in drains.values():
        join(decode.bits, drain_bits[:len(decode.bits)])
    builder.expose('Drain_bits', drain_bits)

    # A/B read paths and programming contacts remain separate at the cutoff.
    cutoff = builder.bank('B_cutoff', masters['cutoff'], params.BMatrix_Rows // profile['matrix_unit'][0])
    for p, target in zip(mapped(cutoff, 'cutoff', 'b_read'), assemblies['B'].read_slots):
        if target is not None:
            connect(p, target)
    for p, target in zip(mapped(cutoff, 'cutoff', 'a_read'), assemblies['A'].read_slots):
        if target is not None:
            connect(p, target)
    join(mapped(cutoff, 'cutoff', 'program'), assemblies['B'].programming_drains)
    # Read/program paths continue through the abutting matrix/cutoff row.
    for names in profile['ports']['cutoff'].values():
        for name in names:
            native_port(cutoff, name).native_abutment = True

    inputs = mapped(gors['A'], 'gors', 'inputs')
    offset = 0
    if params.A_col_pwr:
        power_names = profile['power_input_order']
        if params.A_col_pwr != len(power_names):
            raise ValueError('A_col_pwr must match the profile power-input list or be zero')
        for pin, name in zip(inputs, power_names):
            connect(pin, builder.supplies[name])
        offset = len(power_names)
    for host, count in (('CEW', params.C_EW_to_A), ('CNS', params.C_NS_to_A)):
        join(mapped(matrices[host], 'matrix', 'source_top')[:count], inputs[offset:offset + count])
        offset += count
    bias_inputs = inputs[offset:]

    devices, device_inputs, device_outputs, activation_members = [], [], [], []
    if params.devices:
        owner = builder.island('Devices')
        grid = AlgorithmGrid.for_process(owner, process_coordinates)
        slot = 0
        for descriptor in params.devices:
            for _ in range(descriptor.count):
                cell = getattr(library, descriptor.std_cell)(top, owner)
                grid.place(cell, (0, slot))
                cell.markAbut()
                slot += 1
                devices.append(cell)
                builder.static(cell)
                if descriptor.role == 'support':
                    # Support/bias terminals never add functional matrix lanes.
                    continue
                activation_members.append(cell)
                for identifiers, destination in ((descriptor.inputs, device_inputs),
                                                  (descriptor.outputs, device_outputs)):
                    for identifier in identifiers:
                        native, lane = identifier[:-1].rsplit('[', 1)
                        port = native_port(cell, native)
                        destination.append(port[int(lane)])
                        # Functional device inputs/outputs meet adjoining banks
                        # by native abutment; bias/control interfaces stay explicit.
                        port.native_abutment = True
    available_cutoff = [mapped(cutoff, 'cutoff', 'a_read')[i]
                        for i, pin in enumerate(assemblies['B'].read_slots) if pin is not None]
    if device_inputs:
        join(device_inputs, available_cutoff[:len(device_inputs)])
        join(device_outputs, mapped(gors['B'], 'gors', 'inputs'))
        for name in profile['ports']['gors']['inputs']:
            native_port(gors['B'], name).native_abutment = True
    activation_groups = ([bind_activation(builder, devices, profile.get('devices', {}),
                                         profile['activation_interface'])] if activation_members else [])
    a_bias_bindings = bind_connections(builder, bias_inputs, params.A_bias_connections,
        blocks={**matrices, **builder.support}, activation_groups=activation_groups,
        aliases=profile.get('bias_aliases', {}))
    half = params.OutMatrix_Rows // 2
    for host, prefix, count in (('CEW', 'CAB_IN_N', params.C_EW_to_A),
                                ('CNS', 'CAB_IN_E', params.C_NS_to_A)):
        builder.expose(prefix, mapped(matrices[host], 'matrix', 'source_top')[count:count + half],
                       'N' if prefix.endswith('_N') else 'E')
    output_drains = assemblies['Out'].usable_read_drains
    if len(output_drains) != params.OutMatrix_Rows:
        raise ValueError('Output frame requires one usable read drain per output row')
    builder.expose('CAB_OUT_S', output_drains[:half], 'S')
    builder.expose('CAB_OUT_W', output_drains[half:], 'W')
    for name, rail in {**builder.supplies, **builder.controls}.items():
        builder.expose(name, rail)

    # Native 350nm control pass-throughs have no invented level shifters or
    # buffers. Their same-net opposite ports are distinct physical accesses.
    frame_controls = [
        ('GateBits', gate.bits, gate.bits, 'N', ('Gate_bits',)),
        ('GateEnable', gate.enable, gate.enable, 'N', ('Gate_enable',)),
        ('DrainBits', drain_bits, drain_bits, 'W', ('Drain_bits',)),
        ('DrainEnables', [p for d in drains.values() for p in pins(d.enable)],
                         [p for d in drains.values() for p in pins(d.enable)], 'W',
                         tuple(name + '_enable' for name in drains)),
    ]
    for name, side in (('PROG', 'W'), ('RUN', 'W')):
        rail = builder.controls.get(name)
        if rail is not None:
            frame_controls.append((name, [rail], [rail], side, (name,)))
    for name in ('Scanner_CLK_n', 'Scanner_RSTN_n'):
        if name in builder.exposed:
            value = builder.exposed[name]
            frame_controls.append((name.removesuffix('_n'), value, value, 'N', (name,)))
    from ashes_fg.algorithms.cab.tile_frame import finish as finish_tile_frame
    finish_tile_frame(builder, digital=frame_controls)

    # Keep incomplete contracts visible. Never publish this draft for synthesis.
    issues = []
    if unresolved_pins(gate):
        issues.append('Unconnected gate decoder auxiliary pins after CAB wiring: ' + ', '.join(sorted(
            {cell.name + '.' + port.native_name + str(lanes) for cell, port, lanes in unresolved_pins(gate)})))
    for name, decoder in drains.items():
        missing = unresolved_pins(decoder)
        if missing:
            issues.append(name + ': unconnected native auxiliary pins: ' + ', '.join(sorted(
                {cell.name + '.' + port.native_name + str(lanes) for cell, port, lanes in missing})))
    for name, owner in builder.islands.items():
        for index, cell in enumerate(owner.instances):
            if not hasattr(cell, 'fg_geometry'):
                cell.fg_geometry = ('body', index)
        owner.fg_generated = Generated(None, None, instances=tuple(owner.instances),
                                       layout=custom_layouts.get(name, grid_layout))
    placement_rules = deepcopy(profile['island_layout'])
    for host, dy in host_y_offsets.items():
        placement_rules[host]['dy'] = placement_rules[host].get('dy', 0) + dy
    for name, rule in placement_rules.items():
        selector = rule.get('own_anchor', {})
        host = selector.pop('host', None)
        if host is not None:
            switch = drain_switches[name][host]
            row, column = (int(axis[0]) for axis in switch.island.getLocation(switch))
            selector.update(logical_row=row, logical_col=column)
            selector.pop('occurrence', None)
    location_islands = relative_layout(list(builder.islands), placement_rules,
        gap=profile['default_island_gap'], margin=profile['layout_margin'])
    if strict and issues:
        raise ValueError('CAB electrical preflight is incomplete:\n- ' + '\n- '.join(issues))
    return SimpleNamespace(Top=top, frame=frame, parameters=params, CAB_Params=params.as_dict(),
        matrices=matrices, assemblies=assemblies, support=builder.support,
        islands=builder.islands, devices=tuple(devices), device_inputs=tuple(device_inputs),
        device_outputs=tuple(device_outputs), a_bias_bindings=a_bias_bindings,
        activation_groups=tuple(activation_groups), volatile_interfaces=volatile_interfaces,
        sblock_gate_fillers=sblock_gate_fillers,
        sblock=sblock, gate_decoder=gate, drain_decoders=drains, drain_switches=drain_switches,
        gate_address_map=addresses,
        implementation_issues=tuple(issues), synthesis_ready=not issues,
        review_notes=tuple(profile.get('review_notes', ())),
        location_islands=location_islands, design_limits=design_limits,
        row_capacity={name: dict(nominal=a.nominal_rows, usable=len(a.usable_read_drains),
                                reserved=a.reserved_read_lanes) for name, a in assemblies.items()},
        process_coordinates=process_coordinates, physical_cells=dict(profile['physical_cells']))
