"""Insert native-side physical companions before either Verilog writer."""
import ast
from copy import deepcopy
import importlib
import inspect
import re
import textwrap
from pathlib import Path
from .companion_groups import companion_names, prepare_groups, union_boxes
from ..library.cell_profiles import load_cell_library


def _catalog(circuit, libraries):
    modules = [importlib.import_module(name) for name in libraries]
    modules += [inspect.getmodule(type(cell)) for cell in circuit.Instances]
    result = {}
    modules = [load_cell_library(module) for module in
               dict.fromkeys(m for m in modules if m is not None)]
    configured_names = {
        profile[key] for module in modules for cls in vars(module).values()
        if inspect.isclass(cls)
        for profile in [getattr(cls, 'physical_companions', {})]
        for key in ('edge_left', 'edge_right', 'tap') if profile.get(key) is not None
    }
    for module in modules:
        for cls in vars(module).values():
            if not inspect.isclass(cls):
                continue
            master = vars(cls).get('library_master_name')
            if master is not None:
                if master in configured_names or re.search(r'_(?:EdgeL|EdgeR|TAP)(?:_|$)', master):
                    result[master] = cls
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
                if name in configured_names or re.search(r'_(?:EdgeL|EdgeR|TAP)(?:_|$)', name):
                    if name in result and result[name] is not cls:
                        raise ValueError(f'Ambiguous physical cell {name}')
                    result[name] = cls
    return result



def _insert_companion(island, companion, previous, native_side, swapped, dim):
    """Reserve one strip outside a single cell or an explicitly grouped band."""
    parents = previous if isinstance(previous, tuple) else (previous,)
    locations = [island.getLocation(cell) for cell in parents]
    row = min(int(loc[0][0]) for loc in locations)
    col = min(int(loc[1][0]) for loc in locations)
    axis = 0 if swapped else 1
    before = native_side == 'W'
    cut = ((row, col)[axis] if before else
           max(int(loc[axis][0]) + cell.dim[axis] for cell, loc in zip(parents, locations)))
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
        return
    for other in island.instances:
        if other is companion or other.isDecoder():
            continue
        loc = island.getLocation(other)
        if len(loc[axis]) and int(loc[axis][0]) < cut < int(loc[axis][0]) + other.dim[axis]:
            raise ValueError(f'{parents[0].name}: companion grid offset would split {other.name}; '
                             'align matrix boundaries or use a separate island')
    if swapped:
        island.insertRows(cut)
        companion.place((cut, col))
    else:
        island.insertCols(cut)
        companion.place((row, cut))


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
    """Return an isolated augmented circuit and companion validation relationships.

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
        if any(group.endpoints for island in circuit.Islands
               for group in getattr(island, '_companion_groups', ())):
            raise ValueError('Companion-only endpoints require physical_cells edges or taps')
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
    # Reserve pure grid bands; validate their natural contact before island fitting.
    for island_number, island in enumerate(work.Islands):
        # Decoder cores/connectors/fillers are handled as declared bands below,
        # rather than giving every internal cell its own termination strips.
        decoder_cells = {
            cell for role in ('gate', 'drain')
            for chain in [getattr(getattr(island, 'fg', None), role, None)]
            if chain is not None and chain.decoder_result is not None
            for cell in chain.decoder_result.instances
        }
        grouped = {cell for group in getattr(island, '_companion_groups', ()) for cell in group.members}
        for parent in list(island.instances):
            if (parent.isDecoder() or parent in decoder_cells or parent in grouped
                    or parent.name in catalog):
                continue
            if scope == 'matrix' and not parent.isMatrix():
                continue
            loc = island.getLocation(parent)
            if not len(loc[0]):
                raise ValueError(f'Physical cell parent {parent.name} is not placed')
            profile = companion_names(parent)
            for side, native_side, suffix in [('left', 'W', 'edge_left'), ('right', 'E', 'edge_right')]:
                chain = []
                if edges in (side, 'both'):
                    chain.append(profile[suffix])
                if taps in (side, 'both'):
                    chain.append(profile['tap'])
                if not chain:
                    continue
                dim = (1, parent.dim[1]) if swapped else (parent.dim[0], 1)
                boundary = [(p.native_name, p, [p]) for p in parent.ports
                            if getattr(p, 'native_location', native_sides.get(p.location, p.location)) == native_side]
                # Explicit library endpoints remain on the body even when the
                # shared boundary family has no corresponding pass-through pin.
                body_ports = set(profile.get('body_ports', ()))
                unknown = body_ports - {p.native_name for p in parent.ports}
                if unknown:
                    raise ValueError(f'{parent.name}: unknown companion body_ports {sorted(unknown)}')
                boundary = [entry for entry in boundary if entry[0] not in body_ports]
                previous = parent
                for name in chain:
                    if name is None:
                        continue
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
                    # Companion-only well/supply pins are absent from some switches.
                    # Bind them to the same explicitly generated FG supply nets.
                    generated = getattr(island, 'fg_generated', None)
                    if generated is not None and getattr(parent, 'fg_peripheral', False):
                        for port in companion.ports:
                            supply = generated.supplies.get(port.native_name.rsplit('_', 1)[0])
                            if supply is not None:
                                for pin in port.pins:
                                    if pin.net is not supply.net:
                                        pin.connect(supply)
                    boundary = next_boundary
                    _insert_companion(island, companion, previous, native_side, swapped, dim)
                    relationships.append((island_number, companion, previous, native_side))
                    previous = companion
        for companion, previous, side in prepare_groups(
                work, island, catalog, edges, taps, swapped, report, _insert_companion):
            relationships.append((island_number, companion, previous, side))
    for number, cell, parent, side in relationships:
        island = work.Islands[number]
        def location(instance):
            loc = island.getLocation(instance)
            return (int(loc[0][0]), int(loc[1][0]))
        parents = parent if isinstance(parent, tuple) else (parent,)
        relation = {'island': number, 'cell': location(cell), 'parent': location(parents[0]), 'side': side}
        if len(parents) > 1:
            relation['parents'] = [location(each) for each in parents]
        plan.append(relation)
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


def validate_abutments(islands, plan, swapped=False, custom_layout_islands=()):
    """Validate contact and overlap; require pure bands only for grid layouts.

    Custom layouts use logical locations as identifiers, not shared row pitches.
    Their actual companion boxes must still align and touch their parents.
    """
    for relation in plan:
        island = islands[relation['island']]
        def find(location):
            matches = [idx for idx, item in island['items'].items()
                       if (item.get('logical_row'), item.get('logical_col')) == tuple(location)]
            if len(matches) != 1:
                raise ValueError(f'Cannot locate physical companion at {location}')
            return matches[0]
        idx, parent_idx = find(relation['cell']), find(relation['parent'])
        parent = union_boxes([island['coords'][find(loc)]
                              for loc in relation.get('parents', [relation['parent']])])
        box = island['coords'][idx]
        width, height = box[2] - box[0], box[3] - box[1]
        band_axis = 'logical_row' if swapped else 'logical_col'
        dimension = 'mat_row' if swapped else 'mat_col'
        thickness = height if swapped else width
        band = island['items'][idx][band_axis]
        if relation['island'] not in custom_layout_islands:
            for other_idx, other in island['items'].items():
                if other['type'] not in ('cell', 'matrix') or band_axis not in other:
                    continue
                count = other.get('mat_info', {}).get(dimension, 1)
                if other[band_axis] <= band < other[band_axis] + count:
                    other_box = island['coords'][other_idx]
                    other_thickness = ((other_box[3] - other_box[1]) if swapped
                                       else (other_box[2] - other_box[0])) / count
                    if other_thickness != thickness:
                        raise ValueError(f'Companion band {band} in island {relation["island"]} is not pure: '
                                         f'{island["items"][idx]["name"]} and {other["name"]} have different widths')
        if swapped:
            aligned = box[0] == parent[0] and box[2] == parent[2]
            touching = (box[1] == parent[3] if relation['side'] == 'W' else box[3] == parent[1])
        else:
            aligned = box[1] == parent[1] and box[3] == parent[3]
            touching = (box[2] == parent[0] if relation['side'] == 'W' else box[0] == parent[2])
        if not aligned or not touching:
            raise ValueError(f'Grid placement does not abut {island["items"][idx]["name"]} to '
                             f'{island["items"][parent_idx]["name"]} on native {relation["side"]}; '
                             'check companion widths, boundary heights, and grid alignment')
    for number in {r['island'] for r in plan}:
        island = islands[number]
        physical_boxes = [island['coords'][idx] for idx, item in island['items'].items()
                          if item['type'] in ('cell', 'matrix')]
        for i, a in enumerate(physical_boxes):
            for b in physical_boxes[i+1:]:
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    raise ValueError(f'Physical companion placement overlaps another item in island {number}; '
                                     'reserve more space between parent groups')
