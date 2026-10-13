"""Generate regular 16nm VMM programming chains entirely in Python.

Selected shared decoder algorithms own core/support cells, electrical nets
and their multicolumn/multirow layout. Switch/shifter bands
abut the core or its native edge/TAP boundary. GDS never synthesizes decoders.
"""
from dataclasses import dataclass, field
import inspect
from importlib import import_module
from .fg_peripherals import DecoderPlacementContext, prepare, _snapshot, _signature
from ..placement.companion_groups import union_boxes
from ..placement.algorithm_grid import AlgorithmGrid


def native_port(cell, name):
    ports = [p for p in cell.ports if p.native_name == name]
    if len(ports) != 1:
        raise ValueError(f'{cell.name}: expected native port {name}')
    return ports[0]


def connect(a, b):
    if a.net is not b.net:
        a.connect(b)


@dataclass
class Generated:
    gate: object
    drain: object
    supplies: dict = field(default_factory=dict)
    controls: dict = field(default_factory=dict)
    configuration: object = None
    instances: tuple = ()
    layout: object = None


@dataclass(frozen=True)
class PeripheralContext:
    """Inputs to a selected whole-peripheral algorithm for an already placed body."""
    island: object
    circuit: object
    cells: object
    plan: object
    placement: object
    process_coordinates: str
    options: dict


@dataclass(frozen=True)
class PeripheralPlacementContext:
    """Canonical XY footprints and opaque descriptors for a custom island layout."""
    island: object
    cells: dict
    entries: dict


def _algorithm(value):
    if isinstance(value, str) and '.' in value:
        module, _, name = value.rpartition('.')
        value = getattr(import_module(module), name)
    if value is not None and value is not False and not callable(value):
        raise ValueError('An algorithm must be callable or a dotted Python function path')
    return value


def _place(cell, location, descriptor):
    cell.fg_peripheral = True
    cell.physical_companion = True
    cell.fg_geometry = descriptor
    cell.place(location)


def generate(island, *, cells=None, process_coordinates='columns_y_rows_minus_x',
             algorithm=None, switches=True, level_shifters=True, decoders=True, **options):
    """Build a default VMM chain or call a selected algorithm around a placed body.

    Class/name overrides choose cells; False disables an individual stage.
    Whole-peripheral algorithms own mixed-layout/bridge placement and wiring.
    """
    if any(type(flag) is not bool for flag in (switches, level_shifters, decoders)):
        raise ValueError('switches, level_shifters and decoders must be booleans')
    algorithm = _algorithm(algorithm)
    if algorithm is False:
        raise ValueError('algorithm=False is invalid; use stage switches instead')
    config = (id(cells), process_coordinates, algorithm, switches, level_shifters,
              decoders, tuple(sorted(options.items())))
    if hasattr(island, 'fg_generated'):
        if island.fg_generated.configuration != config:
            raise ValueError('Reconfigure FG generation from the original circuit')
        return island.fg_generated
    if algorithm is None and process_coordinates != 'columns_y_rows_minus_x':
        raise ValueError('Default 16nm generation requires columns_y_rows_minus_x')
    model, circuit = inspect.getmodule(type(island.circuit)), island.circuit
    snapshot = _snapshot(circuit)
    try:
        for role in ('gate', 'drain'):
            for stage, enabled in (('switch', switches), ('level_shifter', level_shifters), ('decoder', decoders)):
                key = role + '_' + stage
                if options.get(key) is None and not enabled:
                    options[key] = False
            key = role + '_decoder'
            if isinstance(options.get(key), str) and '.' in options[key]:
                options[key] = _algorithm(options[key])
            if options.get(key) is None or options.get(key) is True:
                try:
                    algorithms = import_module('algorithms.decoders.folded_radix4')
                except ModuleNotFoundError as error:
                    if error.name not in ('algorithms', 'algorithms.decoders', 'algorithms.decoders.folded_radix4'):
                        raise
                    raise ValueError('Add the shared library directory to sys.path or '
                                     'pass gate_decoder/drain_decoder builders') from error
                options[key] = getattr(algorithms, 'GateDecoder' if role == 'gate' else 'DrainDecoder')
        plan = prepare(island, cells=cells, process_coordinates=process_coordinates, **options)
        if algorithm is not None:
            library = next((chain.cells for chain in (plan.gate, plan.drain) if chain is not None), None)
            if library is None:
                raise ValueError('The selected island has no discovered FG channels')
            context = PeripheralContext(island, circuit, library, plan,
                                        AlgorithmGrid.for_process(island, process_coordinates),
                                        process_coordinates, dict(options))
            generated = algorithm(context)
            if not isinstance(generated, Generated) or not callable(generated.layout):
                raise TypeError('A peripheral algorithm must return Generated with a layout callback')
            if generated.gate is not plan.gate or generated.drain is not plan.drain:
                raise ValueError('Generated must retain the context plan gate/drain chains')
            generated.instances = tuple(generated.instances or island.instances)
            if len(set(generated.instances)) != len(generated.instances) or set(generated.instances) != set(island.instances):
                raise ValueError('Custom layout instances must cover the complete placed island body')
            generated.configuration = config
            plan.signature = _signature(island)
            island.fg_generated = generated
            return generated
        parents = {pin.cell for chain in (plan.gate, plan.drain) if chain
                   for channel in chain.channels for pin in channel.targets}
        if len(parents) != 1 or next(iter(parents)).name != 'IndirectVMM_4x2':
            raise ValueError('Default generation needs one contiguous IndirectVMM_4x2; '
                             'other layouts need a bridge-aware generator')
        core = next(iter(parents))
        if plan.gate is None or plan.drain is None:
            raise ValueError('Regular VMM generation needs gate and drain channels')
        if plan.gate.members != [island] or plan.drain.members != [island]:
            raise ValueError('Extended groups require a bridge-aware generator')
        if any(cell is not core for cell in island.instances):
            raise ValueError('Generate peripherals before adding physical companions')
        island._fg_core = core
        core.fg_geometry = ('core', 0, 0)
        loc = island.getLocation(core)
        row, col = int(loc[0][0]), int(loc[1][0])
        generated = Generated(plan.gate, plan.drain, configuration=config)
        for role, chain in (('gate', plan.gate), ('drain', plan.drain)):
            dim = (1, core.dim[1]) if role == 'gate' else (core.dim[0], 1)
            chain.switches = None if chain.switch is False else chain.switch(circuit, island, dim=dim)
            chain.level_shifters = None if chain.level_shifter is False else chain.level_shifter(circuit, island, dim=dim)
            stages = [(kind, cell) for kind, cell in (('switch', chain.switches), ('shifter', chain.level_shifters))
                      if cell is not None]
            for step, (kind, cell) in enumerate(stages):
                position = ((row + core.dim[0] + step, col) if role == 'gate'
                            else (row, col + core.dim[1] + step))
                _place(cell, position, (role + '_' + kind, 0, 0))
            plan.signature = _signature(island)
            result = None if chain.decoder is False else chain.build_decoder()
            selections = result.outputs if result is not None else model.Bus(circuit, size=chain.output_count)
            complements = result.output_complements if result is not None else []
            if result is None:
                chain.external_inputs['select'] = selections
                generated.controls[role.upper() + '_SELECT'] = selections
            need_complements = (chain.level_shifters is not None and role == 'gate') or (
                chain.level_shifters is None and chain.switches is not None)
            if need_complements and not complements:
                complements = model.Bus(circuit, size=chain.output_count)
                chain.external_inputs['select_n'] = complements
                generated.controls[role.upper() + '_SELECT_N'] = complements
            if complements and len(complements) != chain.output_count:
                raise ValueError(f'{role}: complementary selection width mismatch')
            true_out, complement_out = selections, complements
            if chain.level_shifters is not None:
                shifter = chain.level_shifters
                x = native_port(shifter, 'X_w' if role == 'gate' else 'X_s')
                xn = native_port(shifter, 'XN_w') if role == 'gate' else None
                true_out = native_port(shifter, 'X_VINJ_e' if role == 'gate' else 'X_VINJ_n')
                complement_out = native_port(shifter, 'XN_VINJ_e' if role == 'gate' else 'XN_VINJ_n')
                for port in (x, true_out, complement_out):
                    if len(port) != chain.output_count:
                        raise ValueError(f'{role}: selected shifter pin width mismatch')
                for index, output in enumerate(selections):
                    connect(output, x[index])
                    if xn is not None:
                        connect(complements[index], xn[index])
            chain.selection_outputs = {'select': true_out, 'select_n': complement_out}
            if chain.switches is not None:
                switch = chain.switches
                select = native_port(switch, 'SEL_w' if role == 'gate' else 'Sel_s')
                select_n = native_port(switch, 'SELN_w' if role == 'gate' else 'SelN_s')
                if len(select) != chain.output_count or len(select_n) != chain.output_count:
                    raise ValueError(f'{role}: selected switch pin width mismatch')
                for index in range(chain.output_count):
                    connect(true_out[index], select[index])
                    connect(complement_out[index], select_n[index])
            for prefix, native_name, external_name in (
                    [('Vg_', 'VG_e', 'GATE_PROGRAM')] if role == 'gate' else
                    [('Vd_P_', 'Vd_P_n', 'DRAIN_PROGRAM_P'), ('Vd_R_', 'Vd_R_n', 'DRAIN_PROGRAM_R')]):
                for port in core.ports:
                    if not port.native_name.startswith(prefix):
                        continue
                    if chain.switches is None:
                        if external_name not in generated.controls:
                            generated.controls[external_name] = model.Bus(circuit, size=len(port))
                        switched = generated.controls[external_name]
                    else:
                        switched = native_port(chain.switches, native_name)
                    if len(port) != len(switched):
                        raise ValueError(f'{prefix}: core/switch width mismatch')
                    for a, b in zip(port.pins, switched):
                        connect(a, b)
            for name, pin in (result.supplies.items() if result is not None else ()):
                if name in generated.supplies:
                    connect(pin, generated.supplies[name])
                else:
                    generated.supplies[name] = pin
            for cell in (core, chain.switches, chain.level_shifters):
                if cell is None:
                    continue
                for p in cell.ports:
                    family = p.native_name.rsplit('_', 1)[0]
                    # Analog core tuning/source ports remain designer-owned.
                    # Some EdgeR variants do not expose VTUN pass-throughs.
                    if cell is core and family == 'VTUN':
                        continue
                    if family in ('GND', 'VINJ', 'VDD_CORE', 'VTUN'):
                        if family not in generated.supplies:
                            generated.supplies[family] = model.Wire(circuit)
                        for pin in p.pins:
                            connect(pin, generated.supplies[family])
                    elif cell is chain.switches and family in ('RUN', 'PROG', 'VGPROG', 'VGRUN',
                                                              'Drainline_Indirect', 'Drainline_Direct'):
                        if family not in generated.controls:
                            generated.controls[family] = model.Wire(circuit)
                        for pin in p.pins:
                            connect(pin, generated.controls[family])
                    elif cell is chain.switches and family in ('VG_RUN', 'VS'):
                        name = role.upper() + '_' + family
                        if name not in generated.controls:
                            generated.controls[name] = model.Bus(circuit, size=len(p))
                        generated.controls[name].connectPort(p)
        island.fg_generated = generated
        return generated
    except Exception:
        for obj, state in snapshot:
            obj.__dict__.clear()
            obj.__dict__.update(state)
        raise


def collect_layout(circuit):
    plans = []
    for number, island in enumerate(circuit.Islands):
        if not hasattr(island, 'fg_generated'):
            if hasattr(island, 'fg'):
                raise ValueError('FG plan is not materialized; call generate_fg_peripherals() '
                                 'or use a complete custom generator before compiling')
            continue
        if island.fg_generated.layout is not None:
            entries = []
            for cell in island.fg_generated.instances:
                loc = island.getLocation(cell)
                if not len(loc[0]):
                    raise ValueError('Custom peripheral algorithm left an instance unplaced')
                entries.append({'location': (int(loc[0][0]), int(loc[1][0])),
                                'geometry': getattr(cell, 'fg_geometry', None)})
            plans.append({'island': number, 'entries': entries, 'layout': island.fg_generated.layout})
            continue
        entries = []
        peripherals = {island._fg_core}
        for role in ('gate', 'drain'):
            chain = getattr(island.fg_generated, role)
            peripherals.update((chain.switches, chain.level_shifters))
        for cell in island.instances:
            if cell in peripherals:
                loc = island.getLocation(cell)
                entries.append({'location': (int(loc[0][0]), int(loc[1][0])),
                                'geometry': cell.fg_geometry})
        decoders = []
        for role in ('gate', 'drain'):
            result = getattr(island.fg_generated, role).decoder_result
            if result is None:
                continue
            if not callable(result.layout):
                raise ValueError(f'{role}: decoder algorithm must return a layout callback')
            decoder_entries = []
            for cell in result.instances:
                loc = island.getLocation(cell)
                decoder_entries.append({'location': (int(loc[0][0]), int(loc[1][0])),
                                        'geometry': getattr(cell, 'fg_geometry', None)})
            decoders.append({'role': role, 'layout': result.layout, 'entries': decoder_entries})
        plans.append({'island': number, 'entries': entries, 'decoders': decoders})
    return plans


def apply_layout(islands, cells, plans, companions=(), swapped=True):
    """Use actual GDS bounds; decoder double pitch must not stretch VMM columns."""
    if not swapped and any('layout' not in plan for plan in plans or ()):
        raise ValueError('Default FG layout requires the swapped convention')
    for plan in plans or ():
        number, island = plan['island'], islands[plan['island']]
        def find(location):
            matches = [idx for idx, item in island['items'].items()
                       if (item.get('logical_row'), item.get('logical_col')) == tuple(location)]
            if len(matches) != 1:
                raise ValueError(f'Cannot find FG item at {location}')
            return matches[0]
        entries = {find(e['location']): e['geometry'] for e in plan['entries']}
        if 'layout' in plan:
            context = PeripheralPlacementContext(island, cells, entries)
            boxes = plan['layout'](context)
            if set(boxes) != set(entries):
                raise ValueError('Custom peripheral layout must place exactly its declared instances')
            pending = [r for r in companions or () if r['island'] == number]
            while pending:
                progressed = False
                for relation in list(pending):
                    parents = [find(loc) for loc in relation.get('parents', [relation['parent']])]
                    if any(parent not in boxes for parent in parents):
                        continue
                    idx = find(relation['cell'])
                    item = island['items'][idx]
                    info = cells[item['name']]
                    mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
                    cw, ch = info['width'] * mat['mat_col'], info['height'] * mat['mat_row']
                    p = union_boxes([boxes[parent] for parent in parents])
                    if swapped:
                        if cw != p[2] - p[0]:
                            raise ValueError('Companion does not span its custom parent boundary')
                        boxes[idx] = ([p[0], p[3], p[2], p[3] + ch] if relation['side'] == 'W'
                                      else [p[0], p[1] - ch, p[2], p[1]])
                    else:
                        if ch != p[3] - p[1]:
                            raise ValueError('Companion does not span its custom parent boundary')
                        boxes[idx] = ([p[0] - cw, p[1], p[0], p[3]] if relation['side'] == 'W'
                                      else [p[2], p[1], p[2] + cw, p[3]])
                    pending.remove(relation)
                    progressed = True
                if not progressed:
                    break
        else:
            core_idx = next(idx for idx, g in entries.items() if g[0] == 'core')
            core, info = island['items'][core_idx], cells[island['items'][core_idx]['name']]
            w, h = info['width'], info['height']
            cols, rows = core['mat_info']['mat_col'], core['mat_info']['mat_row']
            boxes = {core_idx: [0, 0, w * cols, h * rows]}
            pending = [r for r in companions or () if r['island'] == number]
            def place_companions():
                while pending:
                    progressed = False
                    for relation in list(pending):
                        parents = [find(loc) for loc in relation.get('parents', [relation['parent']])]
                        idx = find(relation['cell'])
                        if any(parent not in boxes for parent in parents):
                            continue
                        item, info = island['items'][idx], cells[island['items'][idx]['name']]
                        mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
                        cw, ch = info['width'] * mat['mat_col'], info['height'] * mat['mat_row']
                        p = union_boxes([boxes[parent] for parent in parents])
                        if cw != p[2] - p[0]:
                            raise ValueError('FG edge/TAP does not span its parent boundary')
                        boxes[idx] = ([p[0], p[3], p[0] + cw, p[3] + ch] if relation['side'] == 'W'
                                      else [p[0], p[1] - ch, p[0] + cw, p[1]])
                        pending.remove(relation)
                        progressed = True
                    if not progressed:
                        break
            place_companions()
            top = max(b[3] for b in boxes.values())
            for role in ('gate', 'drain'):
                cursor = top if role == 'gate' else 0
                for kind in ('switch', 'shifter'):
                    idx = next((i for i, g in entries.items() if g[0] == role + '_' + kind), None)
                    if idx is None:
                        continue
                    item, info = island['items'][idx], cells[island['items'][idx]['name']]
                    mat = item['mat_info']
                    cw, ch = info['width'] * mat['mat_col'], info['height'] * mat['mat_row']
                    if role == 'gate':
                        if cw != w * cols:
                            raise ValueError('Gate peripheral pitch differs from VMM')
                        boxes[idx] = [0, cursor, cw, cursor + ch]
                        cursor += ch
                    else:
                        if ch != h * rows:
                            raise ValueError('Drain peripheral pitch differs from VMM')
                        boxes[idx] = [cursor - cw, 0, cursor, ch]
                        cursor -= cw
                    before = set(boxes)
                    place_companions()
                    if role == 'gate':
                        # Include both sides of this band before placing the next one.
                        group = (set(boxes) - before) | {idx}
                        bottom = min(boxes[i][1] for i in group)
                        shift = boxes[idx][1] - bottom
                        for i in group:
                            boxes[i][1] += shift
                            boxes[i][3] += shift
                        cursor = max(boxes[i][3] for i in group)
                decoder = next((d for d in plan['decoders'] if d['role'] == role), None)
                if decoder is None:
                    continue
                decoder_entries = {find(e['location']): e['geometry'] for e in decoder['entries']}
                # The algorithm sees a local XY block with horizontal slots and
                # vertical bands. Convert footprints and the final pose here only.
                canonical_cells = cells if role == 'gate' else {
                    name: dict(info, width=info['height'], height=info['width'])
                    for name, info in cells.items()}
                context = DecoderPlacementContext(
                    role, island, canonical_cells, decoder_entries, 0,
                    (w, h) if role == 'gate' else (h, w),
                    (cols, rows) if role == 'gate' else (rows, cols),
                    slot_pitch=2 * w if role == 'gate' else h)
                local_boxes = decoder['layout'](context)
                placed = {
                    idx: ([box[0], cursor + box[1], box[2], cursor + box[3]]
                          if role == 'gate' else
                          [cursor - box[3], rows * h - box[2],
                           cursor - box[1], rows * h - box[0]])
                    for idx, box in local_boxes.items()}

                if set(placed) != set(decoder_entries):
                    raise ValueError('Decoder layout must place exactly its returned instances')
                if set(placed) & set(boxes):
                    raise ValueError('Decoder layout cannot replace another peripheral')
                boxes.update(placed)
                place_companions()
        if pending:
            raise ValueError('Unresolved FG companion chain')
        if set(boxes) != set(island['items']):
            raise ValueError('Unplanned item in regular FG island')
        dx, dy = -min(b[0] for b in boxes.values()), -min(b[1] for b in boxes.values())
        for idx, box in boxes.items():
            island['coords'][idx] = [box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy]
        values = list(boxes.values())
        for index, a in enumerate(values):
            for b in values[index + 1:]:
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    raise ValueError('Generated FG cells overlap')
