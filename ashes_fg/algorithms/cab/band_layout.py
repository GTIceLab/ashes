"""Place sparse programming bands using their host body's physical columns."""
from ashes_fg.asic.placement.algorithm_grid import grid_layout


def column_sources(body):
    result = {}
    for cell in body:
        x, _ = cell.algorithm_xy
        for column in range(x, x + cell.dim[1]):
            result.setdefault(column, []).append(cell.name)
    return tuple(tuple(result[index]) for index in range(max(result) + 1))


def section_gates(sources):
    def layout(context):
        widths = [max(context.cells[name]['width'] for name in names) for names in sources]
        boxes = {}
        for index, descriptor in context.entries.items():
            _, column = descriptor
            cell = context.cells[context.island['items'][index]['name']]
            if cell['width'] > widths[column] + 1e-6:
                raise ValueError('Programming-band cell is wider than its S-block host column')
            x = sum(widths[:column])
            boxes[index] = [x, 0, x + cell['width'], cell['height']]
        return boxes
    return layout


def decoder_columns(sources, active_columns=None):
    """Compatibility entry point; host gaps never split native decoder bands."""
    active_columns = tuple(range(len(sources)) if active_columns is None else active_columns)
    if len(set(active_columns)) != len(active_columns) or any(not 0 <= c < len(sources) for c in active_columns):
        raise ValueError('Decoder active columns must identify distinct host columns')
    return decoder_bands()


def decoder_bands():
    """Abut decoder cells independently of the switch-bank/body column pitch."""
    def layout(context):
        groups = sorted({descriptor[1] for descriptor in context.entries.values()})
        x_positions, right = {}, 0
        for group in groups:
            members = [index for index, d in context.entries.items() if d[1] == group]
            widths = [context.cells[context.island['items'][i]['name']]['width'] for i in members]
            if max(widths) - min(widths) > 1e-6:
                raise ValueError('Decoder stage widths differ; provide matching native pass-through cells')
            x_positions[group] = right
            right += max(widths)
        heights = {}
        for index, (_, group, stage) in context.entries.items():
            cell = context.cells[context.island['items'][index]['name']]
            heights[stage] = max(heights.get(stage, 0), cell['height'])
        total = sum(heights.values())
        boxes = {}
        for index, (_, group, stage) in context.entries.items():
            cell = context.cells[context.island['items'][index]['name']]
            x = x_positions[group]
            top = total - sum(height for row, height in heights.items() if row < stage)
            boxes[index] = [x, top - cell['height'], x + cell['width'], top]
        return boxes
    return layout


def drain_offsets(offsets):
    """Keep a shared decoder while aligning offset host switch strips."""
    def layout(context):
        boxes = grid_layout(context)
        for index, descriptor in context.entries.items():
            if descriptor[0] != 'drain_switch' or descriptor[1] not in offsets:
                continue
            master, columns = offsets[descriptor[1]]
            dx = context.cells[master]['width'] * columns
            box = boxes[index]
            boxes[index] = [box[0] + dx, box[1], box[2] + dx, box[3]]
        return boxes
    return layout
