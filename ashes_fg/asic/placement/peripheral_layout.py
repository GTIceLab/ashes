"""Compose automatic local peripheral bands using actual logical XY footprints.

Bridge routing, cross-island extension and electrical ties are not performed
by this placement callback. Native conversion remains in PlacementAxes.
"""
from ..peripherals.fg_generation import PeripheralPlacementContext
from ..peripherals.fg_peripherals import DecoderPlacementContext
from .algorithm_grid import grid_layout
from .companion_groups import union_boxes


def layout_mixed(context):
    """Compose body, active stages, filler columns and selected decoder boxes.

    All boxes use logical XY; the existing backend performs native conversion.
    Only the swapped 16nm convention is enabled by the automatic generator.
    """
    items, entries, cells = context.island['items'], context.entries, context.cells
    by_location = {(item['logical_row'], item['logical_col']): idx
                   for idx, item in items.items()}
    relationships = []
    for relation in context.companions:
        child = by_location[tuple(relation['cell'])]
        parents = [by_location[tuple(loc)] for loc in relation.get('parents', [relation['parent']])]
        relationships.append((child, parents, relation['side']))

    def closure(indices):
        indices = set(indices)
        changed = True
        while changed:
            changed = False
            for child, parents, side in relationships:
                if child not in indices and set(parents) <= indices:
                    indices.add(child)
                    changed = True
        return indices

    def size(idx):
        item = items[idx]
        info = cells[item['name']]
        mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
        return info['width'] * mat['mat_col'], info['height'] * mat['mat_row']

    def companions(boxes, indices):
        pending = [r for r in relationships if r[0] in indices and r[0] not in boxes]
        while pending:
            progress = False
            for relation in list(pending):
                child, parents, side = relation
                if not set(parents) <= boxes.keys():
                    continue
                p = union_boxes([boxes[parent] for parent in parents])
                width, height = size(child)
                if width != p[2] - p[0]:
                    raise ValueError('Mixed-band companion cannot span the variable-pitch body')
                boxes[child] = ([p[0], p[3], p[2], p[3] + height] if side == 'W'
                                else [p[0], p[1] - height, p[2], p[1]])
                pending.remove(relation)
                progress = True
            if not progress:
                raise ValueError('Unresolved mixed-band companion chain')

    body = {idx: desc for idx, desc in entries.items() if desc[0] == 'mixed_body'}
    component = closure(body)
    body_island = dict(context.island, items={idx: items[idx] for idx in component})
    boxes = grid_layout(PeripheralPlacementContext(body_island, cells, body))
    companions(boxes, component)
    body_box = union_boxes(list(boxes.values()))
    columns, rows = {}, {}

    def edge(mapping, coordinate, interval):
        if coordinate in mapping and mapping[coordinate] != interval:
            raise ValueError('Mixed body has inconsistent projected pitch; use a custom layout')
        mapping[coordinate] = interval

    for idx, desc in body.items():
        _, row, col, nr, nc = desc
        box = boxes[idx]
        info = cells[items[idx]['name']]
        for offset in range(nc):
            edge(columns, col + offset, (box[0] + offset * info['width'],
                                        box[0] + (offset + 1) * info['width']))
        for offset in range(nr):
            edge(rows, row + offset, (box[3] - (offset + 1) * info['height'],
                                     box[3] - offset * info['height']))

    def append_component(local, cursor, gate):
        indices = closure(local)
        companions(local, indices)
        bound = union_boxes(list(local.values()))
        shift = cursor - (bound[1] if gate else bound[2])
        for idx, b in local.items():
            boxes[idx] = ([b[0], b[1] + shift, b[2], b[3] + shift] if gate else
                          [b[0] + shift, b[1], b[2] + shift, b[3]])
        return (bound[3] + shift if gate else bound[0] + shift)

    for role in ('gate', 'drain'):
        gate = role == 'gate'
        cursor = body_box[3] if gate else body_box[0]
        axis = columns if gate else rows
        for stage in ('switch', 'level_shifter'):
            band = {idx: desc for idx, desc in entries.items()
                    if desc[:3] == ('peripheral_band', role, stage)}
            if not band:
                continue
            local = {}
            for idx, desc in band.items():
                coordinate = desc[3]
                width, height = size(idx)
                mat = items[idx].get('mat_info', {'mat_row': 1, 'mat_col': 1})
                length = mat['mat_col'] if gate else mat['mat_row']
                if any(coordinate + offset not in axis for offset in range(length)):
                    raise ValueError('Peripheral band extends beyond a known body pitch')
                low = min(axis[coordinate + offset][0] for offset in range(length))
                high = max(axis[coordinate + offset][1] for offset in range(length))
                if (width if gate else height) != high - low:
                    raise ValueError(f'{role}/{stage}: filler or active span does not match body pitch')
                local[idx] = ([low, 0, high, height] if gate else [-width, low, 0, high])
            # Every member must share one band thickness and touch its neighbors.
            thickness = {size(idx)[1 if gate else 0] for idx in band}
            if len(thickness) != 1:
                raise ValueError('Peripheral filler thickness differs from the selected active stage')
            cursor = append_component(local, cursor, gate)

        decoder = {idx: desc for idx, desc in entries.items()
                   if desc[:2] == ('mixed_decoder', role)}
        if not decoder:
            continue
        # Algorithms remain selected at generation time. Callback references are
        # attached to their descriptors below, avoiding closure over live models.
        first = next(iter(decoder.values()))
        callback, target_origin = first[2], first[4]
        if not callable(callback) or any(desc[2] is not callback or desc[4] != target_origin
                                         for desc in decoder.values()):
            raise ValueError('Missing or inconsistent selected decoder layout in mixed generation')
        decoder = {idx: desc[3] for idx, desc in decoder.items()}
        canonical = cells if gate else {name: dict(info, width=info['height'], height=info['width'])
                                       for name, info in cells.items()}
        core = next((idx for idx in body if items[idx]['name'] == 'IndirectVMM_4x2'), None)
        if core is None:
            raise ValueError('Cannot determine VMM decoder slot pitch')
        core_info = cells[items[core]['name']]
        pitch = 2 * core_info['width'] if gate else core_info['height']
        mat = items[core].get('mat_info', {'mat_row': 1, 'mat_col': 1})
        core_size = ((core_info['width'], core_info['height']) if gate else
                     (core_info['height'], core_info['width']))
        core_shape = ((mat['mat_col'], mat['mat_row']) if gate else
                      (mat['mat_row'], mat['mat_col']))
        local = callback(DecoderPlacementContext(role, context.island, canonical, decoder,
                                                 0, core_size, core_shape, pitch))
        if set(local) != set(decoder):
            raise ValueError('Decoder layout must cover exactly its mixed-body instances')
        # Use the selected chain's first coordinate even for decoder-only
        # generation around a subset of the body's VMM matrices.
        origin = axis[target_origin][0 if gate else 1]
        local = {idx: ([b[0] + origin, b[1], b[2] + origin, b[3]] if gate else
                       [-b[3], origin - b[2], -b[1], origin - b[0]])
                 for idx, b in local.items()}
        cursor = append_component(local, cursor, gate)
    return {idx: boxes[idx] for idx in entries}


def layout_mixed_xy(context):
    """Run the existing canonical mixed-band solver for native Cartesian cells."""
    from copy import deepcopy
    island = deepcopy(context.island)
    for item in island['items'].values():
        item['logical_row'], item['logical_col'] = item['logical_col'], item['logical_row']
        if 'mat_info' in item:
            m = item['mat_info']
            m['mat_row'], m['mat_col'] = m['mat_col'], m['mat_row']
    cells = {name: dict(info, width=info['height'], height=info['width'])
             for name, info in context.cells.items()}
    entries = {}
    for idx, desc in context.entries.items():
        if desc[0] == 'mixed_body':
            _, row, col, nr, nc = desc
            desc = ('mixed_body', col, row, nc, nr)
        entries[idx] = desc
    relations = []
    for original in context.companions:
        relation = dict(original)
        for key in ('cell', 'parent'):
            if key in relation:
                relation[key] = tuple(reversed(relation[key]))
        if 'parents' in relation:
            relation['parents'] = [tuple(reversed(loc)) for loc in relation['parents']]
        relations.append(relation)
    boxes = layout_mixed(PeripheralPlacementContext(island, cells, entries, tuple(relations)))
    top = max(box[3] for box in boxes.values())
    right = max(box[2] for box in boxes.values())
    return {idx: [top - box[3], right - box[2], top - box[1], right - box[0]] for idx, box in boxes.items()}


def layout_mixed_swapped(context):
    """Preserve native top-down band order in the swapped staging space."""
    boxes = layout_mixed(context)
    right = max(box[2] for box in boxes.values())
    return {idx: [right - box[2], box[1], right - box[0], box[3]]
            for idx, box in boxes.items()}
