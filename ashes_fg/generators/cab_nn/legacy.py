#!/usr/bin/env python3
"""CAB composition in golden XY; shared ASHES APIs own FG and edge cells."""
from pathlib import Path
from types import SimpleNamespace
import json
import sys


from ashes_fg.algorithms.cab import Interfaces, load, validate_dimensions

# Designer knobs are physical column counts, not process dimensions in um.
DEVICE_GAP_COLUMNS = 1
ISLAND_GAP_UM = 4


# Assemble the tile circuit, its programming interfaces, and its layout recipe.
def build(project, settings_path=None, *, cells=None, process_coordinates=None, strict=True, design_limits=None):
    """Assemble the CAB circuit and return its objects and compile settings.

    Resolve matrix lane counts from settings, create cells and programming
    interfaces, wire the tile, and provide a measured-footprint layout callback.
    """
    ROOT = Path(project).resolve()
    import ashes_fg.asic.model.asic_compile as ac
    import ashes_fg.class_lib_mux as lib_mux
    from ashes_fg.asic.library.cell_profiles import load_cell_library
    from ashes_fg.asic.library.coordinate_library import for_coordinates
    from ashes_fg.asic.placement.algorithm_grid import AlgorithmGrid
    from ashes_fg.asic.placement.placement_axes import native_island_layout
    from ashes_fg.asic.peripherals.fg_extensions import append_drain_control
    from ashes_fg.algorithms.common import connect
    from ashes_fg.algorithms.system_build import CircuitBuilder, pins, join, port, gate_order
    from ashes_fg.algorithms.sblock.switch_matrix import Sblock_gen
    from ashes_fg.algorithms.cab.device_assembly import build_devices
    from ashes_fg.algorithms.cab.a_bias import bind_connections

    # Select the cell library and logical placement convention before creating cells.
    synthesis = json.loads((ROOT / 'synthesis_settings.json').read_text())
    coordinates = process_coordinates or synthesis.get('process_coordinates', 'xy')
    if coordinates not in ('xy', 'columns_y_rows_minus_x'):
        raise ValueError('process_coordinates must be xy or columns_y_rows_minus_x')
    library = load_cell_library(cells if cells is not None else 'cell_def.cells')
    profile = getattr(library, 'cab_profile', {})
    interfaces = Interfaces(getattr(library, 'native_library_file', library.__file__), profile.get('devices', {}))
    library = for_coordinates(library, coordinates)

    # Resolve electrical lane counts; validation below requires whole matrix cells.
    params = load(settings_path or ROOT / 'cab_settings.json', interfaces,
                  csc_gate_alignment=profile.get('csc_gate_alignment'), shared_gate_selection=True)
    rows_per_cell, cols_per_cell = profile.get('matrix_unit', (4, 2))
    validate_dimensions(params, row_unit=rows_per_cell, column_unit=cols_per_cell)
    if params.A_col_pwr not in (0, 2):
        raise ValueError('A_col_pwr must be zero or two (GND and VDD)')

    top = ac.Circuit()
    frame = lib_mux.frame(top)
    frame.defaultPinLayer = 'M3'
    # Generic build mechanics live in algorithms.system_build. Shared-net
    # choices below are this tile's circuit policy, not implicit library rules.
    builder = CircuitBuilder(
        top, frame=frame, cells=library, process_coordinates=coordinates,
        matrix_unit=(rows_per_cell, cols_per_cell), masters=profile.get('masters', {}),
        supply_names=('GND', 'VDD', 'VINJ', 'VTUN'),
        supply_aliases={'VDD_CORE': 'VDD'},
        static_families=('GND', 'VDD', 'VDD_CORE', 'VINJ', 'VTUN', 'RUN', 'PROG', 'VGRUN'),
        shared_controls=('RUN', 'PROG', 'VGPROG', 'VGRUN', 'Drainline_Indirect', 'Drainline_Direct'),
    )
    islands, matrices = builder.islands, builder.matrices
    generated, support = builder.generated, builder.support
    supplies, controls = builder.supplies, builder.controls
    decoder_inputs = builder.decoder_inputs
    pending = []

    # Only bodies and topology live here. No local decoder/edge/TAP recipes.

    # CNS, the S-block bands, and CEW share one placement island.
    csc_owner = builder.island('CSC')
    csc_grid = AlgorithmGrid.for_process(csc_owner, coordinates)
    master = profile.get('masters', {}).get('IndirectVMM_4x2', 'IndirectVMM_4x2')
    cns = csc_grid.create(getattr(library, master), top,
        dim=(params.CNS_Rows // rows_per_cell, params.CNS_Cols // cols_per_cell))
    csc_grid.place(cns, (0, 0))

    # Specify body order only; the S-block API computes its own complete extent.
    s_owner = csc_owner
    s_signals = Sblock_gen(top, s_owner, params.CSC_rows, cells=library,
                          below=cns, process_coordinates=coordinates, peripherals=False)
    cew = csc_grid.create(getattr(library, master), top,
        dim=(params.CEW_Rows // rows_per_cell, params.CEW_Cols // cols_per_cell))
    csc_grid.place_below(cew, s_signals['body'])
    matrices.update(CEW=cew, CNS=cns)

    # Include functional S bands in the shared CSC gate programming chain.
    functional_s = [cell for cell in csc_owner.instances
                    if cell.name in ('Sblock_N', 'Sblock_S_0', 'Sblock_S_1')]
    csc_fg = csc_owner.generate_fg_peripherals(cells=library, process_coordinates=coordinates,
        parents=[cns, cew, *functional_s], roles=('gate',))
    builder.register_fg('CSC', csc_fg)
    for cell in s_owner.instances:
        if cell not in (cns, cew):
            builder.static(cell)
    for key, value in s_signals['supplies'].items():
        builder.common(key, value)
    builder.common('VGRUN', s_signals['VGRUN'])
    s_indices = [channel.index for channel in csc_fg.gate.channels
                 if any(target.cell in functional_s for target in channel.targets)]
    join(s_signals['VSEL'], [csc_fg.gate.selection_outputs['select_n'][index] for index in s_indices])

    # A/B keep local gate switches and use CSC decoder/shifter selections.
    # Local drain generation is disabled: the separate extension serves A and Out;
    # B connects through the B-cutoff bank below.
    a, a_fg = builder.matrix('A', params.AMatrix_Rows, params.AMatrix_Cols,
                     gate_level_shifter=False, gate_decoder=False,
                     drain_switch=False, drain_level_shifter=False, drain_decoder=False)
    b, b_fg = builder.matrix('B', params.BMatrix_Rows, params.BMatrix_Cols,
                     gate_level_shifter=False, gate_decoder=False,
                     drain_switch=False, drain_level_shifter=False, drain_decoder=False)
    out, out_fg = builder.matrix('Out', params.OutMatrix_Rows, params.OutMatrix_Cols,
                         gate_switch=False, gate_level_shifter=False, gate_decoder=False,
                         drain_switch=False, drain_level_shifter=False, drain_decoder=False)
    ab_drain = builder.drain_extension('AB_Drain', [a, out])

    # Legacy CAB_VSEL = [SELN_A, SELN_B] shares a CSC selection prefix.
    # Select the level-shifted outputs, rather than adding A/B decoders/shifters.

    # Collect CSC selections in CEW/S/CNS order, then connect A followed by B.
    csc_gate_indices = []
    for parents in ((cew,), tuple(functional_s), (cns,)):
        indices = [channel.index for channel in csc_fg.gate.channels
                   if any(target.cell in parents for target in channel.targets)]
        csc_gate_indices.extend(gate_order(indices))
    shared_gate_selections = {}
    for polarity in ('select', 'select_n'):
        outputs = csc_fg.gate.selection_outputs[polarity]
        source = [outputs[index] for index in csc_gate_indices]
        targets = gate_order(a_fg.gate.selection_outputs[polarity]) + gate_order(b_fg.gate.selection_outputs[polarity])
        if len(source) < len(targets):
            raise ValueError('CSC gate selections do not cover A and B')
        join(targets, source[:len(targets)])
        shared_gate_selections[polarity] = tuple(source[:len(targets)])

    # GorS banks connect matrix source/gate interfaces to their input lanes.
    # Queue source-selection controls for configuration-memory wiring later.
    a_switch = builder.bank('A_GorS', 'SWC_GorS', params.AMatrix_Cols // cols_per_cell)
    b_switch = builder.bank('B_GorS', 'SWC_GorS', params.BMatrix_Cols // cols_per_cell)
    for name, body, fg, switch in (('A', a, a_fg, a_switch), ('B', b, b_fg, b_switch)):
        join(port(switch, 'VG_e'), fg.controls['GATE_VG_RUN'])
        join(port(switch, 'VS_e'), port(body, 'Vs_w'))
        join(fg.controls['GATE_VS'], port(body, 'Vs_w'))
        join(port(body, 'Vs_w'), port(body, 'Vs_e'))
        join(port(switch, 'SEL_e'), port(body, 'Vsel_w'))
        join(port(body, 'Vsel_w'), port(body, 'Vsel_e'))
        join(port(switch, 'SELN_w'), fg.gate.selection_outputs['select_n'])
        # A/B matrix bodies and their terminations are entirely native.
        body.routing_export = 'native_abutment'
        for native in ('VG_e', 'VS_e', 'SEL_e'):
            port(switch, native).native_abutment = True
        pending.append((name + '_source_select', port(switch, 'SEL_S_w')))

    # B reaches the A drain interface through this cutoff switch bank.
    cutoff = builder.bank('B_cutoff', 'SWC_BMtrx', 1, params.BMatrix_Rows // rows_per_cell)
    join(port(cutoff, 'EXT_VD_R_n'), port(a, 'Vd_R_n'))
    join(port(cutoff, 'VD_P_n'), port(a, 'Vd_P_n'))
    join(port(cutoff, 'VD_R_s'), port(b, 'Vd_R_n'))
    join(port(cutoff, 'VD_P_s'), port(b, 'Vd_P_n'))
    # These interfaces are native continuations through the abutting A/B stack.
    for body in (a, b):
        for name in ('Vd_P_n', 'Vd_P_s', 'Vd_R_n', 'Vd_R_s'):
            port(body, name).native_abutment = True
    for name in ('EXT_VD_R_n', 'VD_P_n', 'VD_R_s', 'VD_P_s'):
        port(cutoff, name).native_abutment = True
    # A occupies the native part of the shared extension. Out remains routed.
    for channel in ab_drain.drain.channels:
        if any(target.cell is a for target in channel.targets):
            for name in ('Vd_P_n', 'Vd_R_n'):
                port(ab_drain.drain.switches, name)[channel.index].native_abutment = True


    # Connect B to Out through the output switch; its source selection is shared with B.
    output_switch = builder.bank('Out_switch', 'SWC_OutMtrx', params.OutMatrix_Cols // cols_per_cell)
    for source, target in (('Vs_B_w', 'Vs_e'), ('Vg_B_w', 'Vg_e'), ('Vsel_w', 'Vsel_e')):
        join(port(output_switch, source), port(b, target))
    for source, target in (('Vs_Out_e', 'Vs_w'), ('Vg_Out_e', 'Vg_w'), ('Vsel_e', 'Vsel_w')):
        join(port(output_switch, source), port(out, target))
    join(port(output_switch, 'SEL_S_w'), port(b_switch, 'SEL_S_w'))

    # Profile-owned assembly distinguishes signal cells from bottom support cells.
    # The recipe makes the old abutting activation rails explicit in the netlist.
    device_assembly = build_devices(builder, params.devices, profile.get('devices', {}))
    device_instances = device_assembly.instances
    device_inputs, device_outputs = device_assembly.inputs, device_assembly.outputs
    activation_groups = device_assembly.activation_groups
    if device_instances:
        join(device_inputs, port(cutoff, 'CAB_IN_n')[:len(device_inputs)])
        join(device_outputs, port(b_switch, 'VMM_IN_w'))
    else:
        builder.expose('CAB_DEVICE_IN', port(cutoff, 'CAB_IN_n'), 'E')
        builder.expose('CAB_DEVICE_OUT', port(b_switch, 'VMM_IN_w'), 'E')
    input_count = len(device_inputs)
    if input_count and input_count < params.AMatrix_Rows:
        builder.expose('AB_extra', port(cutoff, 'CAB_IN_n')[input_count:], 'E')

    # Exact, named A-column allocation replaces the legacy fixed offsets.

    # Allocate A input lanes in order: optional GND/VDD, CEW, CNS, then biases.
    a_inputs = pins(port(a_switch, 'VMM_IN_w'))
    offset = 0
    if params.A_col_pwr:
        connect(a_inputs[0], supplies['GND'])
        connect(a_inputs[1], supplies['VDD'])
        offset = 2
    join(port(cew, 'Vs_w')[:params.C_EW_to_A], a_inputs[offset:offset + params.C_EW_to_A])
    offset += params.C_EW_to_A
    join(port(cns, 'Vs_w')[:params.C_NS_to_A], a_inputs[offset:offset + params.C_NS_to_A])
    offset += params.C_NS_to_A
    a_bias_inputs = a_inputs[offset:]
    for name, body in (('CEW', cew), ('CNS', cns)):
        join(port(body, 'Vs_w'), port(body, 'Vs_e'))
        join(port(body, 'Vsel_w'), port(body, 'Vsel_e'))
        indices = [channel.index for channel in csc_fg.gate.channels
                   if any(target.cell is body for target in channel.targets)]
        join([csc_fg.gate.selection_outputs['select_n'][index] for index in indices], port(body, 'Vsel_w'))
        indices = [channel.index for channel in csc_fg.gate.channels
                   if any(target.cell is body for target in channel.targets)]
        join([csc_fg.controls['GATE_VS'][index] for index in indices], port(body, 'Vs_w'))
    builder.common('VGRUN', csc_fg.controls['GATE_VG_RUN'])

    # Preserve the scanner and its volatile switch; ASHES handles the companions.
    scan_units = max(0, params.AMatrix_Cols // cols_per_cell - 2)
    if scan_units:
        scanner = builder.bank('Scanner', 'Scanner_VOL_SWC', scan_units)
        volatile = builder.bank('Volatile', 'SWC_VolSwc', scan_units)
        join(port(scanner, 'SEL_w'), port(volatile, 'SEL_VolSWC_e'))
        join(port(scanner, 'SELN_w'), port(volatile, 'SELN_VolSWC_e'))
        join(port(volatile, 'Vs_w'), port(a, 'Vs_e')[2:-2])
        join(port(volatile, 'Vg_w'), port(a, 'Vg_e')[2:-2])
        join(port(volatile, 'SEL_S_w'), port(a_switch, 'SEL_S_w')[2:-2])
        pending.append(('Scanner_enable', port(volatile, 'ENBLN_VolSWC_e')))
        join(port(scanner, 'CLK_n'), port(scanner, 'CLK_s'))
        join(port(scanner, 'RSTN_n'), port(scanner, 'RSTN_s'))
        # COM/Din/Dout use the design-owned A-bias bindings below, not frame IO.

    # Resolve declarative signal references after all scanner/support cells exist.
    # Unassigned extra columns remain external A_bias inputs.
    a_bias_bindings = bind_connections(
        builder, a_bias_inputs, params.A_bias_connections,
        blocks={**matrices, **support}, activation_groups=activation_groups,
    )
    if activation_groups:
        # Retain the old memory allocation order and its spare lane before WTA.
        targets = dict(pending)
        pending = [(name, targets.pop(name)) for name in
                   ('A_source_select', 'Scanner_enable', 'B_source_select') if name in targets]
        pending.extend(targets.items())
        pending.append(('Activation_reserved', ac.Wire(top)))
        for index, group in enumerate(activation_groups):
            pending.append((f'Activation_{index}_WTA', group.rails['WTA']))
            pending.append((f'Activation_{index}_WTA_B', group.rails['WTA_B']))

    # CEW/S/CNS form the original abutting CSC path; no CNS drain chain.
    for body in (cew, cns):
        join(port(body, 'Vd_P_n'), port(body, 'Vd_P_s'))
    join(port(cew, 'Vd_P_n'), port(cns, 'Vd_P_s'))
    # The S-block API exposes electrical lane slices; no grid-column arithmetic
    # or reserved peripheral columns are needed to find programming contacts.
    for cell, lanes in s_signals['drain_programming']:
        program = pins(port(cew, 'Vd_P_n'))[lanes]
        for pin_group in cell.ports:
            if pin_group.native_name in ('Vd_P_n', 'Vd_P_s'):
                join(pin_group, program)

    # One full-height memory strip per C block. Spare memory bits are allowed.
    memory_bits, configuration_banks, memory_hosts = [], [], {}
    for host_name, host in (('CEW', cew), ('CNS', cns)):
        name = 'Configuration_' + host_name
        units = AlgorithmGrid.for_process(host.island, coordinates).shape(host)[0]
        memory = builder.bank(name, 'VMM_DigMem', units)
        configuration_banks.append(name)
        memory_hosts[name] = host_name
        for family in ('Vg', 'Vs', 'Vsel'):
            join(port(host, family + '_e'), port(memory, family + '_w'))
            join(port(memory, family + '_w'), port(memory, family + '_e'))
        join(port(memory, 'Vd_P_n'), port(memory, 'Vd_P_s'))
        west, east = pins(port(memory, 'B_w')), pins(port(memory, 'B_e'))
        for index in range(len(west) - 2, -1, -2):
            memory_bits.extend(west[index:index + 2] + east[index:index + 2])

    # Both memory strips share programming drains. Their B ports supply configuration
    # bits for source selection and scanner enable; CSC gate selections use the decoder.
    ew_memory, ns_memory = (support[name] for name in configuration_banks)
    join(port(ew_memory, 'Vd_P_n'), port(ns_memory, 'Vd_P_n'))
    builder.drain_extension('CEW_Drain', [cew], program_only=(ew_memory,))
    ab_bits = len(port(a_switch, 'SEL_S_w')) + len(port(b_switch, 'SEL_S_w'))
    if len(memory_bits) < ab_bits:
        raise ValueError(f'C-block memory capacity {len(memory_bits)} is below A/B GorS demand {ab_bits}')
    bit_count = sum(len(pins(value)) for _, value in pending)
    if len(memory_bits) < bit_count:
        raise ValueError(f'C-block memory capacity {len(memory_bits)} is below configuration demand {bit_count}')
    offset = 0

    # Assign consecutive memory-bit slices to the queued configuration consumers.
    configuration_slices = {}
    for name, target in pending:
        size = len(pins(target))
        join(target, memory_bits[offset:offset + size])
        configuration_slices[name] = (offset, offset + size)
        offset += size

    # Legacy low-voltage control buffers: gate address, shared drain address,
    # independent enables, PROG/RUN level shifting, and scanner clock/reset.
    buffered = {}
    for (name, role), inputs in decoder_inputs.items():
        if role == 'gate':
            buffered[name + '_gate_bits'] = [[pin] for pin in pins(inputs.bits)]

    # Broadcast each drain address bit to every decoder that uses it.
    # Decoder enable signals remain independent.
    drains = [inputs for (name, role), inputs in decoder_inputs.items() if role == 'drain']
    buffered['Drain_bits'] = [[pins(inputs.bits)[i] for inputs in drains if i < len(pins(inputs.bits))]
                              for i in range(max(len(pins(inputs.bits)) for inputs in drains))]
    for (name, role), inputs in decoder_inputs.items():
        buffered[name + '_' + role + '_enable'] = [[pin] for pin in pins(inputs.enable)]
    # Ask the extension API to attach the PROG/RUN shifter. It owns the band
    # position, geometry metadata, and physical companions; this file owns nets.
    control_shifter = append_drain_control(
        ab_drain, library.LevelShift_4x_Drain, supplies=supplies,
    )
    support['Control_level_shifter'] = control_shifter
    builder.static(control_shifter)
    buffered['PROG_IN'] = [[port(control_shifter, 'X_s')[1]]]
    for i, pin in enumerate(port(control_shifter, 'X_s')):
        if i != 1:
            connect(pin, supplies['GND'])
    builder.common('PROG', port(control_shifter, 'X_VINJ_n')[1])
    builder.common('RUN', port(control_shifter, 'XN_VINJ_n')[1])
    if scan_units:
        buffered['Scanner_CLK_n'] = [[pin] for pin in pins(port(scanner, 'CLK_n'))]
        buffered['Scanner_RSTN_n'] = [[pin] for pin in pins(port(scanner, 'RSTN_n'))]

    # Route external low-voltage controls through buffers before their internal targets.
    digital_count = sum(len(lanes) for lanes in buffered.values())
    digital = builder.bank('Digital_buffers', 'DIG_BUF_LV', (digital_count + 1) // 2)
    digital_in, digital_out = pins(port(digital, 'IN_w')), pins(port(digital, 'OUT_e'))
    digital_slices = {}
    offset = 0
    for name, lanes in buffered.items():
        for index, targets in enumerate(lanes, offset):
            for target in targets:
                connect(digital_out[index], target)
        builder.expose(name, digital_in[offset:offset + len(lanes)])
        digital_slices[name] = (offset, offset + len(lanes))
        offset += len(lanes)

    # Tie unused inputs to GND when buffer capacity rounds up to a whole cell.
    for pin in digital_in[offset:]:
        connect(pin, supplies['GND'])

    # Export fabric links and CAB analog interfaces at the tile boundary.
    north = csc_fg.gap_connections.get(('gate', 'decoder', 'Sblock_N'), s_signals['Sblock_N'])
    if ('gate', 'decoder', 'Sblock_N') in csc_fg.gap_connections:
        for wire in s_signals['Sblock_N']:
            for pin in wire.net.pins:
                if pin.cell in functional_s:
                    pin.port.native_abutment = True
    if len(north) != params.CSC_rows:
        raise ValueError('S-block north frame access must match CSC_rows')
    builder.expose('N', north, 'N')
    builder.expose('E', s_signals['Sblock_W'], 'E')
    builder.expose('S', port(cns, 'Vd_R_n'), 'S')
    builder.expose('W', port(cew, 'Vd_R_n'), 'W')
    half = params.OutMatrix_Rows // 2
    builder.expose('CAB_IN_N', port(cew, 'Vs_w')[params.C_EW_to_A:params.C_EW_to_A + half], 'N')
    builder.expose('CAB_IN_E', port(cns, 'Vs_w')[params.C_NS_to_A:params.C_NS_to_A + params.OutMatrix_Rows - half], 'E')
    builder.expose('CEW_spare_inputs', port(cew, 'Vs_w')[params.C_EW_to_A + half:], 'N')
    builder.expose('CNS_spare_inputs', port(cns, 'Vs_w')[params.C_NS_to_A + params.OutMatrix_Rows - half:], 'N')
    builder.expose('CAB_OUT_S', port(out, 'Vd_R_n')[:half], 'S')
    builder.expose('CAB_OUT_W', port(out, 'Vd_R_n')[half:], 'W')
    # The S-block's other native endpoints remain available to the fabric.
    builder.expose('Sblock_S', s_signals['Sblock_S'], 'S')
    builder.expose('Sblock_W', s_signals['Sblock_E'], 'W')
    for name, value in supplies.items():
        builder.expose(name, value)
    for name, value in controls.items():
        if name not in ('PROG', 'RUN'):
            builder.expose(name, value)

    # Restore the original directional tile-control paths using actual buffer
    # inputs/outputs; never short a buffered input to its output.
    frame_controls = []
    for role, keys, side in (
            ('GateBits', [k for k in buffered if k.endswith('_gate_bits')], 'N'),
            ('GateEnable', [k for k in buffered if k.endswith('_gate_enable')], 'N'),
            ('DrainBits', ['Drain_bits'], 'W'),
            ('DrainEnables', [k for k in buffered if k.endswith('_drain_enable')], 'W'),
            ('PROG', ['PROG_IN'], 'W'),
            ('Scanner_CLK', ['Scanner_CLK_n'] if scan_units else [], 'N'),
            ('Scanner_RSTN', ['Scanner_RSTN_n'] if scan_units else [], 'N')):
        incoming, outgoing = [], []
        for key in keys:
            start, stop = digital_slices[key]
            incoming.extend(digital_in[start:stop])
            outgoing.extend(digital_out[start:stop])
        frame_controls.append((role, incoming, outgoing, side, keys))
    from ashes_fg.algorithms.cab.tile_frame import finish as finish_tile_frame
    finish_tile_frame(builder, digital=frame_controls)

    # Preserve insertion order: the backend expects one layout origin per island in this order.
    names = list(islands)

    def layout(blocks, cell_info, area):
        """Place islands in golden XY using materialized cell footprints.

        Align active cores and companion boundaries using measured local boxes.
        Return one origin per island in creation order, including the core-area
        offset. The surrounding adapter handles the native coordinate convention.
        """
        bounds = {name: (max(box[2] for box in blocks[i]['coords']),
                         max(box[3] for box in blocks[i]['coords']))
                  for i, name in enumerate(names)}

        # Use golden XY coordinates in nanometers; the outer adapter handles native axes.
        origins = {}
        margin, gap = 10000, ISLAND_GAP_UM * 1000

        # Record an island origin, rather than an individual cell position.
        def put(name, x, y):
            """Record a rounded integer origin for one placement island.
            """
            origins[name] = (int(round(x)), int(round(y)))

        # Global right edge = island origin + measured local extent.
        def right(name):
            """Return the global right edge from the island origin and local extent.
            """
            return origins[name][0] + bounds[name][0]
        def upper(name):
            """Return the global upper edge from the island origin and local extent.
            """
            return origins[name][1] + bounds[name][1]

        # Find an active master box so alignment follows the core, including local offsets.
        def core_box(name, master):
            """Return the first local box matching a physical master in an island.
            """
            block = blocks[names.index(name)]
            return next(block['coords'][idx] for idx, item in block['items'].items() if item['name'] == master)

        # CSC contains two matrix bodies with the same physical master.
        def all_boxes(name, master):
            """Return all matching local master boxes, including both CSC matrices.
            """
            block = blocks[names.index(name)]
            return [block['coords'][idx] for idx, item in block['items'].items() if item['name'] == master]

        # Use measured materialized boxes, including peripheral and companion offsets.
        a_core = core_box('A', matrices['A'].name)
        b_core = core_box('B', matrices['B'].name)
        out_core = core_box('Out', matrices['Out'].name)
        cutoff_core = core_box('B_cutoff', support['B_cutoff'].name)
        ew_core, ns_core = sorted(all_boxes('CSC', matrices['CEW'].name), key=lambda box: box[1])
        ew_drain = core_box('CEW_Drain', 'SWC_Drain')
        ab_program = core_box('AB_Drain', 'SWC_Drain')
        csc_y = margin + max(0, bounds['CEW_Drain'][1] - ew_core[1])
        put('CSC', margin, csc_y)
        put('CEW_Drain', margin + ew_core[0] - ew_drain[0],
            csc_y + ew_core[1] - bounds['CEW_Drain'][1])

        # Place the CAB beside CSC, with the shared drain strip below A.
        column = right('CSC') + gap
        a_x = column + bounds['A_GorS'][0]
        a_y = margin + max(0, bounds['AB_Drain'][1] - a_core[1])
        put('AB_Drain', a_x + a_core[0] - ab_program[0],
            a_y + a_core[1] - bounds['AB_Drain'][1])
        put('A', a_x, a_y)
        put('A_GorS', origins['A'][0] - bounds['A_GorS'][0],
            origins['A'][1] + a_core[1])
        # Align the core columns across A and B, rather than
        # their outer boxes. Both shared core boundaries meet without a split.
        put('B', origins['A'][0] + a_core[0] - b_core[0],
            origins['A'][1] + a_core[3] - b_core[1])
        put('B_GorS', origins['B'][0] - bounds['B_GorS'][0],
            origins['B'][1] + b_core[1])
        put('B_cutoff', origins['B'][0] + b_core[0] - cutoff_core[0],
            origins['B'][1] + b_core[3] - cutoff_core[1])
        if 'Devices' in bounds:
            # Abut controls boundary spacing, not automatic electrical contact.
            # Explicit nets remain valid regardless of native pin-side labels.
            pitch = cell_info[params.devices[0].std_cell]['width']
            space = 0 if params.cab_device_cfg == 'abut' else DEVICE_GAP_COLUMNS * pitch
            # Item enumeration can reverse under axis mapping. Align the
            # leftmost active body, not the first item encountered in the dict.
            device_core = min(all_boxes('Devices', device_instances[0].name),
                              key=lambda box: box[0])
            put('Devices', origins['B_cutoff'][0] + cutoff_core[0] - device_core[0],
                origins['B_cutoff'][1] + cutoff_core[3] + space - device_core[1])
        put('Out_switch', right('B'), origins['B'][1] + b_core[1])
        # Output and B have equal gate counts. Align those active rows even
        # though Out has a drain-programming band below its core.
        put('Out', right('Out_switch'),
            origins['B'][1] + b_core[1] - out_core[1])
        if 'Scanner' in bounds:
            volatile_box = core_box('Volatile', support['Volatile'].name)
            scanner_box = core_box('Scanner', support['Scanner'].name)
            centre = origins['A'][1] + (a_core[1] + a_core[3]) / 2
            put('Volatile', right('A'), centre - (volatile_box[1] + volatile_box[3]) / 2)
            put('Scanner', right('Volatile'), centre - (scanner_box[1] + scanner_box[3]) / 2)
        # Keep buffers by the scanner bottom, above the drain decoder strip.
        if 'Scanner' in origins:
            put('Digital_buffers', right('Scanner') + 1000,
                origins['Scanner'][1] + 4000)
        else:
            put('Digital_buffers', right('A') + gap, margin)
        csc_block = blocks[names.index('CSC')]
        for name in configuration_banks:
            host = ew_core if memory_hosts[name] == 'CEW' else ns_core
            # Find the host's outer EdgeR/TAP boundary from measured boxes.
            boundary = max(box[2] for idx, box in enumerate(csc_block['coords'])
                           if abs(box[1] - host[1]) < 1 and abs(box[3] - host[3]) < 1
                           and csc_block['items'][idx]['name'] in
                           (matrices['CEW'].name, 'IndirectVMM_4x2_EdgeR', 'IndirectVMM_4x2_TAP'))
            put(name, origins['CSC'][0] + boundary, origins['CSC'][1] + host[1])

        # Add the backend core-area offset and return origins in the expected island order.
        return [(origins[name][0] + area[0], origins[name][1] + area[1]) for name in names]

    # Return the circuit, inspection handles, and placement/settings needed by compile().
    return SimpleNamespace(Top=top, CAB_Params=params.as_dict(), parameters=params,
        islands=islands, matrices=matrices, generated=generated, support=support,
        devices=device_instances, device_inputs=device_inputs, device_outputs=device_outputs,
        activation_groups=activation_groups, a_bias_bindings=a_bias_bindings,
        configuration_slices=configuration_slices, configuration_bits=tuple(memory_bits),
        configuration_banks=tuple(configuration_banks), memory_hosts=memory_hosts, frame=frame,
        shared_gate_selections=shared_gate_selections,
        digital_slices=digital_slices, decoder_inputs=decoder_inputs,
        process_coordinates=coordinates, physical_cells=synthesis.get('physical_cells'),
        location_islands=native_island_layout(layout, coordinates),
        design_limits=design_limits if design_limits is not None else synthesis.get('design_limits', [500000, 500000]))


