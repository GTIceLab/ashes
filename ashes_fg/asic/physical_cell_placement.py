"""Insert native-side physical companions before either Verilog writer."""
import ast
from copy import deepcopy
import importlib
import inspect
import textwrap
from pathlib import Path


def _catalog(circuit, libraries):
    modules = [importlib.import_module(name) for name in libraries]
    modules += [inspect.getmodule(type(cell)) for cell in circuit.Instances]
    result = {}
    for module in dict.fromkeys(m for m in modules if m is not None):
        for cls in vars(module).values():
            if not inspect.isclass(cls):
                continue
            try:
                tree = ast.parse(textwrap.dedent(inspect.getsource(cls)))
            except (OSError, TypeError, IndentationError):
                continue
            names = [node.value.value for node in ast.walk(tree)
                     if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                     and isinstance(node.value.value, str)
                     and any(isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                             and t.value.id == 'self' and t.attr == 'name' for t in node.targets)]
            for name in names:
                if name.endswith(('_EdgeL', '_EdgeR', '_TAP')):
                    if name in result and result[name] is not cls:
                        raise ValueError(f'Ambiguous physical cell {name}')
                    result[name] = cls
    return result


def prepare_physical_cells(circuit, settings=None, process_coordinates='xy', log_path=None):
    """Prepare companions, optionally writing diagnostics to a per-run log."""
    if log_path is None:
        return _prepare_physical_cells(circuit, settings, process_coordinates)
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as log:
        def report(message):
            log.write(message + '\n')
            log.flush()
        try:
            return _prepare_physical_cells(circuit, settings, process_coordinates, report)
        except Exception as error:
            report(f'ERROR: {error}')
            raise


def _prepare_physical_cells(circuit, settings=None, process_coordinates='xy', report=print):
    """Return an isolated augmented circuit and exact abutment relationships.

    Library classes must support (circuit, island=None, dim=(rows, cols)).
    Same-name native E/W ports are assumed electrically continuous.
    """
    settings = dict(settings or {})
    unknown = set(settings) - {'edges', 'taps', 'scope', 'libraries'}
    if unknown:
        raise ValueError(f'Unknown physical_cells settings: {sorted(unknown)}')
    edges, taps = settings.get('edges', 'off'), settings.get('taps', 'off')
    allowed = ('off', 'left', 'right', 'both')
    if edges not in allowed or taps not in allowed:
        raise ValueError('physical_cells edges/taps must be off, left, right, or both')
    scope = settings.get('scope', 'matrix')
    if scope not in ('matrix', 'all'):
        raise ValueError('physical_cells scope must be matrix or all')
    if process_coordinates not in ('xy', 'columns_y_rows_minus_x'):
        raise ValueError('Invalid process_coordinates')
    configuration = (settings, process_coordinates)
    if hasattr(circuit, '_physical_cells_configuration'):
        if circuit._physical_cells_configuration != configuration:
            raise ValueError('Reconfigure physical cells using the original circuit')
        return circuit, deepcopy(circuit._physical_cells_plan)
    if edges == taps == 'off':
        return circuit, []
    libraries = settings.get('libraries', [])
    if not isinstance(libraries, list) or any(not isinstance(n, str) for n in libraries):
        raise ValueError('physical_cells libraries must be a list of Python module names')
    catalog = _catalog(circuit, libraries)
    work = deepcopy(circuit)
    work.cleanIslands()
    plan = []
    relationships = []
    swapped = process_coordinates != 'xy'
    native_sides = {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'} if swapped else {}
    # Reserve distinct grid bands; exact geometry is resolved before island fitting.
    for island_number, island in enumerate(work.Islands):
        for parent in list(island.instances):
            if parent.isDecoder() or parent.name.endswith(('_EdgeL', '_EdgeR', '_TAP')):
                continue
            if scope == 'matrix' and not parent.isMatrix():
                continue
            loc = island.getLocation(parent)
            if not len(loc[0]):
                raise ValueError(f'Physical cell parent {parent.name} is not placed')
            for side, native_side, suffix in [('left', 'W', '_EdgeL'), ('right', 'E', '_EdgeR')]:
                chain = []
                if edges in (side, 'both'):
                    chain.append(parent.name + suffix)
                if taps in (side, 'both'):
                    chain.append(parent.name + '_TAP')
                if not chain:
                    continue
                dim = (1, parent.dim[1]) if swapped else (parent.dim[0], 1)
                boundary = [(p.native_name, p, [p]) for p in parent.ports
                            if getattr(p, 'native_location', native_sides.get(p.location, p.location)) == native_side]
                previous = parent
                for name in chain:
                    if name not in catalog:
                        report(f'WARNING: {parent.name}: companion {name} on native {native_side} '
                               'not found in the library; skipping this cell.')
                        continue
                    companion = catalog[name](work, island=island, dim=dim)
                    companion.physical_companion = True
                    next_boundary = []
                    for requested_name, source, exposed_ports in boundary:
                        matches = [p for p in companion.ports if p.native_name == requested_name
                                   and getattr(p, 'native_location', native_sides.get(p.location, p.location)) == native_side]
                        fallback = False
                        opposite = 'E' if native_side == 'W' else 'W'
                        if not matches and requested_name.endswith('_' + native_side.lower()):
                            opposite_name = requested_name[:-1] + opposite.lower()
                            matches = [p for p in companion.ports if p.native_name == opposite_name
                                       and getattr(p, 'native_location', native_sides.get(p.location, p.location)) == opposite]
                            fallback = bool(matches)
                        if not matches and requested_name.endswith('_' + native_side.lower()):
                            vertical = []
                            for vertical_side in ('N', 'S'):
                                vertical_name = requested_name[:-1] + vertical_side.lower()
                                candidates = [p for p in companion.ports if p.native_name == vertical_name
                                              and getattr(p, 'native_location', native_sides.get(p.location, p.location)) == vertical_side]
                                if len(candidates) > 1:
                                    raise ValueError(f'{name}: ambiguous native {vertical_side} pin {vertical_name}')
                                vertical.extend(candidates)
                            if vertical:
                                nets = {p.net for p in source.pins if p.isConnected()}
                                if len(nets) > 1:
                                    raise ValueError(f'{parent.name} -> {name}: North/South fallback for '
                                                     f'{requested_name} requires one shared net')
                                if any(p.numPins() != source.numPins() for p in vertical):
                                    if not nets:
                                        report(f'WARNING: {parent.name} -> {name}: incompatible North/South '
                                              f'pin width for {requested_name}; signal is unconnected, '
                                              'so its companion pin search stops here.')
                                        continue
                                    raise ValueError(f'{parent.name} -> {name}: North/South fallback pin width '
                                                     f'does not match {requested_name}')
                                for target in vertical:
                                    for dst in target.pins:
                                        if nets:
                                            dst.net.removePin(dst)
                                            work.Nets.remove(dst.net)
                                            dst.move(next(iter(nets)))
                                for port in exposed_ports:
                                    port.routing_hidden = True
                                locations = ', '.join(f'{p.native_name} on native '
                                            f'{getattr(p, "native_location", native_sides.get(p.location, p.location))}'
                                            for p in vertical)
                                report(f'WARNING: {parent.name} -> {name}: {requested_name} and its '
                                      f'East/West alternative are unavailable; using {locations} '
                                      'at the top/bottom of the companion strip (one shared net).')
                                next_boundary.append((requested_name, source, vertical))
                                continue
                        if len(matches) != 1 or len(matches[0]) != len(source):
                            if not any(pin.isConnected() for pin in source.pins):
                                report(f'WARNING: {parent.name} -> {name}: no compatible pin for '
                                      f'{requested_name} on native {native_side}; signal is unconnected, '
                                      'so its companion pin search stops here.')
                                continue
                            raise ValueError(f'{parent.name} -> {name}: pin {requested_name} must match '
                                             f'on native {native_side} with {len(source)} pins; '
                                             'cannot transfer the connected net')
                        target = matches[0]
                        if fallback:
                            report(f'WARNING: {parent.name} -> {name}: {requested_name} on native '
                                  f'{native_side} is unavailable; using {target.native_name} on native {opposite}.')
                        for src, dst in zip(source.pins, target.pins):
                            if not src.isConnected():
                                continue
                            dst.net.removePin(dst)
                            work.Nets.remove(dst.net)
                            dst.move(src.net)
                        for port in exposed_ports:
                            port.routing_hidden = True
                        next_boundary.append((requested_name, source, [target]))
                    boundary = next_boundary
                    prev_loc = island.getLocation(previous)
                    row, col = int(prev_loc[0][0]), int(prev_loc[1][0])
                    axis = 0 if swapped else 1
                    # Logical rows are numbered top-to-bottom. In the swapped
                    # convention that order maps to increasing native X.
                    before = native_side == 'W'
                    cut = (row, col)[axis] + (0 if before else previous.dim[axis])
                    candidate = cut - 1 if before else cut
                    shared_band = any(
                        getattr(other, 'physical_companion', False) and other is not companion
                        and len(island.getLocation(other)[axis])
                        and int(island.getLocation(other)[axis][0]) == candidate
                        for other in island.instances)
                    candidate_location = (candidate, col) if swapped else (row, candidate)
                    r0, c0 = candidate_location
                    fits = (r0 >= 0 and c0 >= 0 and r0 + dim[0] <= island.getNumRows()
                            and c0 + dim[1] <= island.getNumCols())
                    if shared_band and fits and all(
                            island.placementGrid[r, c] == 0
                            for r in range(r0, r0 + dim[0]) for c in range(c0, c0 + dim[1])):
                        companion.place(candidate_location)
                        relationships.append((island_number, companion, previous, native_side))
                        previous = companion
                        continue
                    for other in island.instances:
                        if other is companion or other.isDecoder():
                            continue
                        other_loc = island.getLocation(other)
                        if len(other_loc[axis]):
                            start = int(other_loc[axis][0])
                            if start < cut < start + other.dim[axis]:
                                raise ValueError(f'{parent.name}: companion grid offset would split {other.name}; '
                                                 'align matrix boundaries or use a separate island')
                    if swapped:
                        island.insertRows(cut)
                        location = (cut, col)
                    else:
                        island.insertCols(cut)
                        location = (row, cut)
                    companion.place(location)
                    relationships.append((island_number, companion, previous, native_side))
                    previous = companion
    for number, cell, parent, side in relationships:
        island = work.Islands[number]
        def location(instance):
            loc = island.getLocation(instance)
            return (int(loc[0][0]), int(loc[1][0]))
        plan.append({'island': number, 'cell': location(cell), 'parent': location(parent), 'side': side})
    for island in work.Islands:
        def order(cell):
            if cell.isDecoder():
                return (float('inf'), float('inf'))
            loc = island.getLocation(cell)
            return (int(loc[0][0]), int(loc[1][0]))
        island.instances.sort(key=order)
    for net in work.Nets:
        net.number, net.index = -1, -1
        for pin in net.pins:
            pin.markDominant = False
    work._physical_cells_configuration = configuration
    work._physical_cells_plan = deepcopy(plan)
    return work, plan


def resolve_abutments(islands, cells, plan, swapped=False):
    """Resolve logical boxes using physical dimensions before native conversion."""
    for relation in plan:
        island = islands[relation['island']]
        def find(location):
            matches = [idx for idx, item in island['items'].items()
                       if (item.get('logical_row'), item.get('logical_col')) == tuple(location)]
            if len(matches) != 1:
                raise ValueError(f'Cannot resolve physical companion at {location}')
            return matches[0]
        idx, parent_idx = find(relation['cell']), find(relation['parent'])
        parent = island['coords'][parent_idx]
        box = island['coords'][idx]
        width, height = box[2] - box[0], box[3] - box[1]
        if swapped:
            if width != parent[2] - parent[0]:
                raise ValueError('Companion native height does not match parent boundary')
            bottom = parent[3] if relation['side'] == 'W' else parent[1] - height
            island['coords'][idx] = [parent[0], bottom, parent[0] + width, bottom + height]
        else:
            if height != parent[3] - parent[1]:
                raise ValueError('Companion native height does not match parent boundary')
            left = parent[0] - width if relation['side'] == 'W' else parent[2]
            island['coords'][idx] = [left, parent[1], left + width, parent[1] + height]
    for number in {r['island'] for r in plan}:
        island = islands[number]
        boxes = island['coords']
        # Grid bands reserve space, but a left/bottom boundary may need an offset.
        dx, dy = max(0, -min(b[0] for b in boxes)), max(0, -min(b[1] for b in boxes))
        island['coords'] = [[b[0]+dx, b[1]+dy, b[2]+dx, b[3]+dy] for b in boxes]
        physical_boxes = [island['coords'][idx] for idx, item in island['items'].items()
                          if item['type'] in ('cell', 'matrix')]
        for i, a in enumerate(physical_boxes):
            for b in physical_boxes[i+1:]:
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    raise ValueError(f'Physical companion placement overlaps another item in island {number}; '
                                     'reserve more space between parent groups')
