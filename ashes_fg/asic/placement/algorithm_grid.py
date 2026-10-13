"""Map algorithm XY grid indices to the circuit's staging row/column indices.

Algorithms use X for slots/columns and Y for rows/bands. These are grid indices,
not physical database coordinates. Physical layout callbacks separately return
Cartesian XY boxes. Mapping never rotates the underlying library cells.
"""
from dataclasses import dataclass
from operator import index


@dataclass(frozen=True)
class AlgorithmGrid:
    island: object
    origin: tuple = (0, 0)
    x_axis: tuple = (0, 1)
    y_axis: tuple = (1, 0)

    def __post_init__(self):
        if (self.x_axis, self.y_axis) not in (((0, 1), (1, 0)), ((1, 0), (0, 1))):
            raise ValueError('Algorithm grid axes must map XY to rows/columns or columns/rows')
        if len(self.origin) != 2:
            raise ValueError('Algorithm grid origin requires two staging indices')
        for value in self.origin:
            index(value)

    @classmethod
    def for_process(cls, island, process_coordinates='xy', *, origin=(0, 0)):
        """Adapt a canonical XY origin and points to the selected process grid."""
        if process_coordinates == 'xy':
            return cls(island, (index(origin[1]), index(origin[0])))
        if process_coordinates == 'columns_y_rows_minus_x':
            return cls(island, (index(origin[0]), index(origin[1])), (1, 0), (0, 1))
        raise ValueError('Invalid process_coordinates')

    def staging_point(self, xy):
        x, y = (index(value) for value in xy)
        return (self.origin[0] + x * self.x_axis[0] + y * self.y_axis[0],
                self.origin[1] + x * self.x_axis[1] + y * self.y_axis[1])

    def place(self, cell, xy):
        if cell.island is not self.island:
            raise ValueError('Algorithm grid and cell must belong to the same island')
        cell.place(self.staging_point(xy))
        cell.algorithm_xy = tuple(index(value) for value in xy)
        return cell


def grid_layout(context):
    """Return body XY boxes while reserving the shared companion grid strips.

    Suitable for a naturally abutting grid with variable row/column pitches.
    Custom algorithms may replace this callback for other physical arrangements.
    Companion items contribute pitch but are placed by the shared manager.
    """
    rows, columns = {}, {}
    for item in context.island['items'].values():
        if item['type'] not in ('cell', 'matrix'):
            continue
        info = context.cells[item['name']]
        mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
        for row in range(item['logical_row'], item['logical_row'] + mat['mat_row']):
            rows[row] = max(rows.get(row, 0), info['height'])
        for col in range(item['logical_col'], item['logical_col'] + mat['mat_col']):
            columns[col] = max(columns.get(col, 0), info['width'])
    total_height = sum(rows.values())
    boxes = {}
    for idx in context.entries:
        item = context.island['items'][idx]
        info = context.cells[item['name']]
        row, col = item['logical_row'], item['logical_col']
        mat = item.get('mat_info', {'mat_row': 1, 'mat_col': 1})
        if mat['mat_row'] > 1 and any(rows[r] != info['height'] for r in range(row, row + mat['mat_row'])):
            raise ValueError('Custom grid row pitch would stretch a matrix')
        if mat['mat_col'] > 1 and any(columns[c] != info['width'] for c in range(col, col + mat['mat_col'])):
            raise ValueError('Custom grid column pitch would stretch a matrix')
        x = sum(width for c, width in columns.items() if c < col)
        top = total_height - sum(height for r, height in rows.items() if r < row)
        boxes[idx] = [x, top - info['height'] * mat['mat_row'],
                      x + info['width'] * mat['mat_col'], top]
    return boxes
