"""Map logical ASHES placement to native geometry without rotating cells."""
from copy import deepcopy


class PlacementAxes:
    def __init__(self, process_coordinates="xy"):
        if process_coordinates not in ("xy", "columns_y_rows_minus_x"):
            raise ValueError("process_coordinates must be 'xy' or 'columns_y_rows_minus_x'")
        self.swapped = process_coordinates != "xy"

    def native_side(self, side):
        """Map a logical frame edge without changing its pin identifier."""
        return {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'}[side] if self.swapped else side

    def native_pin_groups(self, groups):
        """Copy logical pin groups to native edges; native edge settings stay intact."""
        return {self.native_side(side): list(pins) for side, pins in groups.items()}

    def logical_cells(self, cells):
        """Only placement extents change; pin coordinates and identifiers stay native."""
        result = deepcopy(cells)
        if self.swapped:
            for cell in result.values():
                cell['width'], cell['height'] = cell['height'], cell['width']
        return result

    def logical_area(self, area):
        if not self.swapped:
            return area
        x0, y0, x1, y1, dx, dy = area
        return (0, 0, y1 - y0, x1 - x0, dy, dx)

    def native_box(self, box, area):
        if not self.swapped:
            return list(box)
        left, bottom, right, top = box
        x0, y0, x1, y1 = area[:4]
        # Float-valued design limits (e.g. 120e3) must not propagate decimal
        # coordinates into frame generation. Snap to integer database units.
        return [int(round(value)) for value in
                (x1 - top, y0 + left, x1 - bottom, y0 + right)]

    def map_islands(self, islands, cells, area):
        """Preserve logical matrix indexing while caching native member positions."""
        for island in islands.values():
            for idx, item in island['items'].items():
                box = island['coords'][idx]
                if item['type'] == 'matrix':
                    cell = cells[item['name']]
                    logical_w, logical_h = cell['height'], cell['width']
                    rows, cols = item['mat_info']['mat_row'], item['mat_info']['mat_col']
                    positions = {}
                    for row in range(rows):
                        for col in range(cols):
                            left = box[0] + col * logical_w
                            bottom = box[1] + (rows - 1 - row) * logical_h
                            positions[row, col] = self.native_box(
                                [left, bottom, left + logical_w, bottom + logical_h], area)[:2]
                    item['native_positions'] = positions
                island['coords'][idx] = self.native_box(box, area)


def matrix_position(item, row, col, box, cell):
    """One source of matrix positions for both DEF writers and GDS output."""
    if 'native_positions' in item:
        return item['native_positions'][row, col]
    return (box[0] + col * cell['width'],
            box[1] + (item['mat_info']['mat_row'] - 1 - row) * cell['height'])


def native_island_text(islands, cells, layer_map, frame_module=None):
    """Write unrotated native references; expand matrices to preserve logical order."""
    output = []
    if frame_module:
        output += ['SREF\n', f'SNAME: "{frame_module.module_name}"\n', 'XY: 0, 0\n', 'ENDEL\n']
    for island in islands.values():
        for idx, item in island['items'].items():
            box = island['coords'][idx]
            if item['type'] == 'polygon':
                layer, datatype = layer_map[item['layer'] + '_drawing']['layer_type'].split(',')
                left, bottom, right, top = (int(round(value)) for value in box)
                output += ['BOUNDARY\n', f'LAYER: {layer}\n', f'DATATYPE: {datatype}\n',
                           f'XY: {left}, {bottom}, {right}, {bottom}, {right}, {top}, {left}, {top}, {left}, {bottom}\n', 'ENDEL\n']
                continue
            cell = cells[item['name']]
            positions = (item['native_positions'].values() if item['type'] == 'matrix' else [box[:2]])
            for x, y in positions:
                # GDS references locate the cell origin, not its bounding-box corner.
                ox, oy = cell['origin']
                output += ['SREF\n', f'SNAME: "{item["name"]}"\n',
                           f'XY: {int(x - ox)}, {int(y - oy)}\n', 'ENDEL\n']
    return ''.join(output)
