"""Generate regular 16nm VMM programming chains entirely in Python.

Selected shared decoder algorithms own core/support cells, electrical nets
and their multicolumn/multirow layout. Switch/shifter bands
abut the core or its native edge/TAP boundary. GDS never synthesizes decoders.
"""
from dataclasses import dataclass, field
import inspect
from importlib import import_module
from .fg_peripherals import DecoderPlacementContext, prepare, _snapshot, _signature


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


def _place(cell, location, descriptor):
    cell.fg_peripheral = True
    cell.physical_companion = True
    cell.fg_geometry = descriptor
    cell.place(location)


def generate(island, *, cells=None, process_coordinates='columns_y_rows_minus_x', **options):
    """Materialize the regular VMM case; retain explicit errors for bridge cases."""
    config = (id(cells), process_coordinates, tuple(sorted(options.items())))
    if hasattr(island, 'fg_generated'):
        if island.fg_generated.configuration != config:
            raise ValueError('Reconfigure FG generation from the original circuit')
        return island.fg_generated
    if process_coordinates != 'columns_y_rows_minus_x':
        raise ValueError('Default 16nm generation requires columns_y_rows_minus_x')
    model, circuit = inspect.getmodule(type(island.circuit)), island.circuit
    snapshot = _snapshot(circuit)
    try:
        for role in ('gate', 'drain'):
            key = role + '_decoder'
            if options.get(key) is None:
                try:
                    algorithms = import_module('algorithms.Decoders')
                except ModuleNotFoundError as error:
                    if error.name not in ('algorithms', 'algorithms.Decoders'):
                        raise
                    raise ValueError('Add the shared library directory to sys.path or '
                                     'pass gate_decoder/drain_decoder builders') from error
                options[key] = getattr(algorithms, 'build_' + role + '_decoder')
        plan = prepare(island, cells=cells, process_coordinates=process_coordinates, **options)
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
            chain.switches = chain.switch(circuit, island, dim=dim)
            chain.level_shifters = chain.level_shifter(circuit, island, dim=dim)
            for step, cell in enumerate((chain.switches, chain.level_shifters)):
                position = ((row + core.dim[0] + step, col) if role == 'gate'
                            else (row, col + core.dim[1] + step))
                _place(cell, position, (role + ('_switch' if step == 0 else '_shifter'), 0, 0))
            plan.signature = _signature(island)
            result = chain.build_decoder()
            if role == 'gate':
                select, select_n = native_port(chain.switches, 'SEL_w'), native_port(chain.switches, 'SELN_w')
                x, xn = native_port(chain.level_shifters, 'X_w'), native_port(chain.level_shifters, 'XN_w')
                shifted = native_port(chain.level_shifters, 'X_VINJ_e')
                shifted_n = native_port(chain.level_shifters, 'XN_VINJ_e')
                bindings = [('Vg_', native_port(chain.switches, 'VG_e'))]
            else:
                select, select_n = native_port(chain.switches, 'Sel_s'), native_port(chain.switches, 'SelN_s')
                x, xn = native_port(chain.level_shifters, 'X_s'), None
                shifted = native_port(chain.level_shifters, 'X_VINJ_n')
                shifted_n = native_port(chain.level_shifters, 'XN_VINJ_n')
                bindings = [('Vd_P_', native_port(chain.switches, 'Vd_P_n')),
                            ('Vd_R_', native_port(chain.switches, 'Vd_R_n'))]
            for p in (select, select_n, x, shifted, shifted_n):
                if len(p) != chain.output_count:
                    raise ValueError(f'{role}: selected peripheral pin width mismatch')
            for index, output in enumerate(result.outputs):
                connect(output, x[index])
                if xn is not None:
                    connect(result.output_complements[index], xn[index])
                connect(shifted[index], select[index])
                connect(shifted_n[index], select_n[index])
            for prefix, switched in bindings:
                for p in core.ports:
                    if p.native_name.startswith(prefix):
                        if len(p) != len(switched):
                            raise ValueError(f'{prefix}: core/switch width mismatch')
                        for a, b in zip(p.pins, switched.pins):
                            connect(a, b)
            for name, pin in result.supplies.items():
                if name in generated.supplies:
                    connect(pin, generated.supplies[name])
                else:
                    generated.supplies[name] = pin
            for cell in (core, chain.switches, chain.level_shifters):
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
    if plans and not swapped:
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
        core_idx = next(idx for idx, g in entries.items() if g[0] == 'core')
        core, info = island['items'][core_idx], cells[island['items'][core_idx]['name']]
        w, h = info['width'], info['height']
        cols, rows = core['mat_info']['mat_col'], core['mat_info']['mat_row']
        boxes = {core_idx: [0, 0, w * cols, h * rows]}
        pending = [r for r in companions or () if r['island'] == number]
        while pending:
            progressed = False
            for relation in list(pending):
                parent, idx = find(relation['parent']), find(relation['cell'])
                if parent not in boxes:
                    continue
                item, info = island['items'][idx], cells[island['items'][idx]['name']]
                mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
                cw, ch = info['width'] * mat['mat_col'], info['height'] * mat['mat_row']
                p = boxes[parent]
                if cw != p[2] - p[0]:
                    raise ValueError('FG edge/TAP does not span its parent boundary')
                boxes[idx] = ([p[0], p[3], p[0] + cw, p[3] + ch] if relation['side'] == 'W'
                              else [p[0], p[1] - ch, p[0] + cw, p[1]])
                pending.remove(relation)
                progressed = True
            if not progressed:
                raise ValueError('Unresolved FG companion chain')
        top = max(b[3] for b in boxes.values())
        for role in ('gate', 'drain'):
            cursor = top if role == 'gate' else 0
            for kind in ('switch', 'shifter'):
                idx = next(i for i, g in entries.items() if g[0] == role + '_' + kind)
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
            decoder = next(d for d in plan['decoders'] if d['role'] == role)
            decoder_entries = {find(e['location']): e['geometry'] for e in decoder['entries']}
            context = DecoderPlacementContext(role, island, cells, decoder_entries,
                                              cursor, (w, h), (cols, rows))
            placed = decoder['layout'](context)
            if set(placed) != set(decoder_entries):
                raise ValueError('Decoder layout must place exactly its returned instances')
            if set(placed) & set(boxes):
                raise ValueError('Decoder layout cannot replace another peripheral')
            boxes.update(placed)
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
