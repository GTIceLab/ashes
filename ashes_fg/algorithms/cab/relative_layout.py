"""Resolve profile-selected island relationships from measured island boxes."""
from collections.abc import Mapping


def create(names, rules, *, gap=4000, margin=10000):
    names = tuple(names)
    if set(rules) != set(names):
        raise ValueError('Island placement rules must cover every constructed island exactly once')

    # A scalar preserves legacy symmetric padding; a mapping configures each side.
    if isinstance(margin, Mapping):
        unknown = set(margin) - {'left', 'right', 'bottom', 'top'}
        if unknown:
            raise ValueError(f'Unknown layout margin sides: {sorted(unknown)}')
        left, right, bottom, top = (margin.get(side, 0) for side in ('left', 'right', 'bottom', 'top'))
    else:
        left = right = bottom = top = margin
    import math
    if any(isinstance(value, bool) or not isinstance(value, (int, float))
           or not math.isfinite(value) or value < 0 for value in (left, right, bottom, top)):
        raise ValueError('Layout margins must be finite nonnegative database-unit distances')

    def layout(blocks, cell_info, area):
        # The physical backend passes {island_number: block}. Model callers may
        # pass a sequence. Island numbers, not insertion order, identify names.
        if isinstance(blocks, Mapping):
            if set(blocks) != set(range(len(names))):
                raise ValueError('Island layout requires contiguous numeric island IDs matching the model')
            blocks = [blocks[number] for number in range(len(names))]
        else:
            blocks = list(blocks)
        if len(blocks) != len(names):
            raise ValueError(f'Island layout expected {len(names)} blocks, got {len(blocks)}')
        boxes = {}
        by_name = dict(zip(names, blocks))
        def anchor(name, selector):
            if not selector:
                return boxes[name]
            block = by_name[name]
            matches = [index for index, item in sorted(block['items'].items())
                       if item['name'] == selector['master']
                       and all(item.get(key) == selector[key]
                               for key in ('logical_row', 'logical_col') if key in selector)]
            if not matches:
                raise ValueError(f'Cannot find island anchor for {name}: {selector}')
            return block['coords'][matches[selector.get('occurrence', 0)]]
        for name, block in zip(names, blocks):
            coords = block['coords']
            boxes[name] = (min(b[0] for b in coords), min(b[1] for b in coords),
                           max(b[2] for b in coords), max(b[3] for b in coords))
        origins, pending = {}, dict(rules)
        while pending:
            progress = False
            for name, rule in list(pending.items()):
                reference = rule.get('reference')
                if reference is not None and reference not in origins:
                    continue
                own = boxes[name]
                x, y = -own[0], -own[1]
                if reference is not None:
                    parent = boxes[reference]
                    px, py = origins[reference]
                    x, y = px + parent[0] - own[0], py + parent[1] - own[1]
                    distance = rule.get('gap', gap)
                    side = rule['side']
                    if side == 'right':
                        x = px + parent[2] + distance - own[0]
                    elif side == 'left':
                        x = px + parent[0] - distance - own[2]
                    elif side == 'above':
                        y = py + parent[3] + distance - own[1]
                    elif side == 'below':
                        y = py + parent[1] - distance - own[3]
                    else:
                        raise ValueError(f'Invalid island relationship: {side}')
                    if 'align_y' in rule:
                        edge = {'bottom': 1, 'top': 3}[rule['align_y']]
                        a = anchor(name, rule.get('own_anchor'))
                        b = anchor(reference, rule.get('reference_anchor'))
                        y = py + b[edge] - a[edge]
                    if 'align_x' in rule:
                        a = anchor(name, rule.get('own_anchor'))
                        b = anchor(reference, rule.get('reference_anchor'))
                        def horizontal(box, edge):
                            return (box[0] + box[2]) / 2 if edge == 'center' else box[{'left': 0, 'right': 2}[edge]]
                        x = px + horizontal(b, rule.get('reference_x', rule['align_x'])) - horizontal(a, rule['align_x'])
                origins[name] = (x + rule.get('dx', 0), y + rule.get('dy', 0))
                del pending[name]
                progress = True
            if not progress:
                raise ValueError('Island layout has unknown references or a dependency cycle')
        placed = {name: (origins[name][0] + box[0], origins[name][1] + box[1],
                         origins[name][0] + box[2], origins[name][1] + box[3])
                  for name, box in boxes.items()}
        for index, name in enumerate(names):
            a = placed[name]
            for other in names[index + 1:]:
                b = placed[other]
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    # Shared peripheral banks can be sparse/L-shaped. Their
                    # enclosing rectangles may overlap without macros touching.
                    for first in by_name[name]['coords']:
                        for second in by_name[other]['coords']:
                            ax, ay = origins[name]
                            bx, by = origins[other]
                            if (min(first[2] + ax, second[2] + bx) > max(first[0] + ax, second[0] + bx)
                                    and min(first[3] + ay, second[3] + by) > max(first[1] + ay, second[1] + by)):
                                raise ValueError(f'Island placement overlaps: {name} and {other}')
        x0, y0 = min(b[0] for b in placed.values()), min(b[1] for b in placed.values())
        width = max(b[2] for b in placed.values()) - x0 + left + right
        height = max(b[3] for b in placed.values()) - y0 + bottom + top
        if len(area) >= 4 and (width > area[2] - area[0] or height > area[3] - area[1]):
            raise ValueError(f'CAB island layout needs at least {width} x {height} database units')
        return [(round(origins[n][0] - x0 + left + area[0]),
                 round(origins[n][1] - y0 + bottom + area[1])) for n in names]

    return layout
