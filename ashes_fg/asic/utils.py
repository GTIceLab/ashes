import numpy as np
from collections import defaultdict
import bisect
from shapely.geometry import Polygon, LineString, box, GeometryCollection
from shapely.ops import polygonize, unary_union

def update_output_layout(text, file_path):
    '''
    append to the final layout file 
    '''
    with open(file_path, 'a') as outfile:
        outfile.writelines(text)

def calculate_offset_row(row_heights, curr_row):
    #print(row_heights)
    offset = 0
    row_keys = list(row_heights.keys())
    row_keys.sort()
   # print(row_keys)
    for key in row_keys:
        if key == curr_row: break
        val = row_heights[key]
        if val[1] == 'matrix':
            offset += val[0]
        elif val[1] == 'cell':
            offset += val[0]
    return offset


def calculate_offset(col_widths, curr_col, cell_padding):
    '''
    Calculate the width offset for a given column
    '''
    offset = 0
    col_keys = list(col_widths.keys())
    col_keys.sort()
    for key in col_keys:
        if key == curr_col: break
        val = col_widths[key]
        if val[1] == 'matrix':
            offset += val[0]
        elif val[1] == 'cell':
            offset += val[0] + cell_padding
    return offset

def make_pin_list(layer_map, tech_process):
    ''' 
    Return a list of all pin layers in layer map file as a (layer, datatype) tuple
    eg [('131', '0'), ('132', '0'), ('133', '0')]
    '''
    pin_list = []
    for item, value in layer_map.items():
        if value['purpose'] == 'pin':
            layer, datatype = item.split(',')
            pin_list.append((layer, datatype))
    
    if not pin_list: 
        raise PinNotDefined(f'Cannot find any pin mapping in {tech_process}.json')
    
    return pin_list

def assign_pins_to_polygon(pin_names, pin_boxes, layer_map, pin_dt):
    '''
    Given a list of pin centers and pin boxes, match the pin centers to the right boxes
    '''
    assigned_pins = {}
    for pin in pin_names:
        pin_x, pin_y = pin[2], pin[3]
        for box in pin_boxes:
            if box[1] < pin_x < box[3] and box[2] < pin_y < box[4] and box[0] == pin[0]:
                assigned_pins.update({pin[1]: { "Layer": layer_map[f'{pin[0]},{pin_dt}']['pdk_name'], "RECT": (box[1], box[2], box[3], box[4])} })
                break
    return assigned_pins

def reverse_pdk_doc(layer_map):
    '''
    Use pdkname_purpose as key instead
    '''
    ret_doc = {}
    for ld_str, value in layer_map.items():
        key = value['pdk_name'] + '_' + value['purpose']
        ret_doc[key] = value
        ret_doc[key]['layer_type'] = ld_str
    return ret_doc

def count_metal_layers(layer_map, tech_process):
    '''
    Return a list of metal routing layers available in PDK
    '''
    metal_layers = []
    for item, value in layer_map.items():
        if value['layer'][:5] == 'metal':
            metal_layers.append(value['pdk_name'])
    
    if not metal_layers: 
        raise PinNotDefined(f'Cannot find any metal layers in {tech_process}.json')
    
    return metal_layers

# def count_metal_layers_drawing(layer_map, tech_process):
#     '''
#     Return a list of metal routing layers with purpose 'DRAWING' available in PDK
#     '''
#     metal_layers = []
#     for item, value in layer_map.items():
#         if value['layer'][:5] == 'metal' and value['purpose'] == 'drawing':
#             metal_layers.append(value['pdk_name'])
    
#     if not metal_layers: 
#         raise PinNotDefined(f'Cannot find any metal layers in {tech_process}.json')
    
#     return metal_layers

def count_metal_layers_drawing(layer_map, tech_process):
    '''
    Return a unique list of metal routing layers with purpose 'drawing' 
    available in PDK. Ignores M0/metal0 but includes M1/metal1 and higher.
    '''
    metal_layers = []
    seen_layers = set()  # Track names to avoid repetitions
    
    for item, value in layer_map.items():
        lname = value['layer'].lower()
        pdk_name = value['pdk_name']
        
        # 1. Basic metal check (starts with 'm' and has a digit)
        is_metal = lname.startswith('m') and any(c.isdigit() for c in lname)
        
        # 2. Purpose check
        is_drawing = value.get('purpose') == 'drawing'
        
        # 3. Exclusion check (ignore M0/metal0)
        is_ignored = lname.startswith('m0') or lname.startswith('metal0')

        if is_metal and is_drawing and not is_ignored:
            # 4. Repetition check
            if pdk_name not in seen_layers:
                metal_layers.append(pdk_name)
                seen_layers.add(pdk_name)
    
    if not metal_layers: 
        raise Exception(f'Cannot find any metal layers (M1+) in {tech_process}.json')
    
    # Optional: Sort the layers if they appear out of order in the JSON
    # metal_layers.sort() 
    
    return metal_layers

def find_pitch_in_lef(layer_name, lef_path, dbu=1000):
    '''
    Returns the routing pitch of layer_name from the LEF file (converted to DBU)
    '''
    pitch = None
    in_target_layer = False
    target_layer_upper = layer_name.upper()
    # Ensure file extension is handled
    path = f'{lef_path}.lef' if not lef_path.endswith('.lef') else lef_path

    try:
        with open(path, 'r') as f:
            for line in f:
                # Clean line and split into tokens
                tokens = line.strip().split()
                if not tokens:
                    continue
                
                # Check for start of the layer: LAYER METAL1
                if tokens[0].upper() == "LAYER" and len(tokens) > 1:
                    if tokens[1].upper() == target_layer_upper:
                        in_target_layer = True
                    continue

                if in_target_layer:
                    # Check for PITCH: PITCH 0.2 ;
                    if tokens[0].upper() == "PITCH" and len(tokens) > 1:
                        # Remove semicolon if it's attached to the number
                        val_str = tokens[1].rstrip(';')
                        pitch_microns = float(val_str)
                        
                        if pitch_microns > 0:
                            return pitch_microns * dbu
                        else:
                            pitch = 0.0

                    # Check for PROPERTY: PROPERTY routingPitch 0.2 ;
                    elif tokens[0].upper() == "PROPERTY" and len(tokens) > 2:
                        if tokens[1] == "routingPitch":
                            val_str = tokens[2].rstrip(';')
                            pitch_microns = float(val_str)
                            if pitch_microns > 0:
                                return pitch_microns * dbu

                    # Check for end of the layer: END METAL1
                    if tokens[0].upper() == "END" and len(tokens) > 1:
                        if tokens[1].upper() == target_layer_upper:
                            break
                            
    except Exception as e:
        print(f"An error occurred while reading LEF: {e}")
        return None

    return pitch


# def find_pitch_in_lef(layer_name, lef_path, dbu=1000):
#     '''
#     Returns the pitch of given layer_name from LEF file
#     This is using the general expression method
#     '''
        
#     lef_path = lef_path + '.lef' if not lef_path.endswith('.lef') else lef_path
#     if not os.path.exists(lef_path):
#         print(f"Error: LEF file not found at {lef_path}")
#         return None

#     pitch = None
#     in_target_layer = False
    
#     # 1. Matches "LAYER METAL1"
#     layer_pattern = re.compile(rf"^\s*LAYER\s+{layer_name}\s*$", re.IGNORECASE)
    
#     # 2. Matches "PITCH value ;" or "PROPERTY routingPitch value ;"
#     # Group 1 captures the first number. Group 2 captures the second optional number.
#     pitch_pattern = re.compile(
#         r"^\s*(?:PITCH|PROPERTY\s+routingPitch)\s+([\d\.]+)(?:\s+([\d\.]+))?\s*;", 
#         re.IGNORECASE
#     )
    
#     # 3. Matches "END METAL1"
#     end_pattern = re.compile(rf"^\s*END\s+{layer_name}\s*$", re.IGNORECASE)

#     try:
#         with open(lef_path, 'r') as f:
#             for line in f:
#                 if layer_pattern.match(line):
#                     in_target_layer = True
#                     continue
                
#                 if in_target_layer:
#                     match = pitch_pattern.search(line)
#                     if match:
#                         # FIX 1: Use group(1) for the primary value
#                         pitch_microns = float(match.group(1))
                        
#                         # FIX 2: Logic to handle "PITCH 0". 
#                         # If PITCH is 0, keep looking for "routingPitch". 
#                         # If value is > 0, we found our valid pitch.
#                         if pitch_microns > 0:
#                             pitch = pitch_microns * dbu
#                             break 
#                         else:
#                             # If we found 0, store it but keep looking for a better one 
#                             # inside the same LAYER block.
#                             pitch = 0.0
                    
#                     if end_pattern.match(line):
#                         in_target_layer = False
#                         break
#     except Exception as e:
#         print(f"An error occurred while reading LEF: {e}")
#         return None

#     return pitch




def sanitize_island_info(island_info):
    '''
    Return a dictionary of island info with instnce name as key. 
    - collapse deques and merge all islands into one structure
    '''
    ret_doc = {}
    for island in island_info:
        mod_list = island_info[island]['deq']
        for inst in mod_list:
            ret_doc[inst.instance_name] = inst.ports
            ret_doc[inst.instance_name]['module_name'] = inst.module_name
    return ret_doc

# def find_via_in_lef(via_name, file_name, dbu):
#     '''
#     Given a via name and file name, return the via definition from the lef file
#     '''
#     print(f'############################# {via_name} ########################')
#     lef_file = open(f'{file_name}.lef')
#     store_via, rect_toggle, leave_file = False, False, False
#     temp_via = None
#     ret_val = []
#     for line in lef_file:
#         line = line.split(' ')
#         print(f'############################# {line} ########################')
#         if len(line) > 1 and line[1] == f'{via_name}\n' and line[0] == 'VIA': 
#             store_via = True
#         elif store_via:
#             if line[0] == 'END': 
#                 store_via = False
#                 lef_file.close()
#                 return ret_val
#             elif ~rect_toggle: temp_via = line[3]
#             elif rect_toggle: ret_val.append((temp_via, float(line[5])*dbu, float(line[6])*dbu, float(line[7])*dbu, float(line[8])*dbu))
#             rect_toggle = ~rect_toggle

def find_via_in_lef(via_name, file_name, dbu):
    '''
    Given a via name and file name, return the via definition from the lef file
    '''
    via_name = via_name.upper()
    #print(f'############################# {via_name} ########################')
    lef_file = open(f'{file_name}.lef')
    store_via = False
    temp_via = None
    ret_val = []
    
    for line in lef_file:
        # Change 1: Use strip().split() to remove '\n' and empty '' elements from your log
        tokens = line.strip().split()
        if not tokens: 
            continue
        
        # Change 2: Match tokens[0] and tokens[1] (this ignores 'DEFAULT' at the end)
        if tokens[0] == 'VIA' and tokens[1] == via_name.upper(): 
            store_via = True
            continue
            
        elif store_via:
            # Change 3: Cleanly check for keywords
            if tokens[0] == 'END': 
                store_via = False
                lef_file.close()
                return ret_val
            
            # Change 4: Detect LAYER and RECT directly (safer than toggling)
            if tokens[0] == 'LAYER':
                temp_via = tokens[1].rstrip(';')
            
            elif tokens[0] == 'RECT':
                # rstrip(';') handles cases where the semicolon is touching the number
                v1 = float(tokens[1].rstrip(';')) * dbu
                v2 = float(tokens[2].rstrip(';')) * dbu
                v3 = float(tokens[3].rstrip(';')) * dbu
                v4 = float(tokens[4].rstrip(';')) * dbu
                ret_val.append((temp_via, v1, v2, v3, v4))
                
    lef_file.close()
    return ret_val

def get_island_adjacent(island_place, neighbors):
    '''
    Return a dictionary of right adjacent islands for all placed islands.
    i.e. What island is to the right of the current island? This helps determine vertical channels
    '''
    matrix = np.array(island_place)
    bottoms = matrix[:, 1] # get bottom y locations of all placed islands
    for idx, item in enumerate(island_place):
        if idx in neighbors: # skip islands whose adjacent were already assigned
            continue
        else:
            same_row = [i for i,n in enumerate(bottoms) if n == item[1]] # get islands on the same row
            if len(same_row) <= 1: # if only one on the row, then no adjacent islands
                neighbors[idx] = None
            else:
                same_row = list(set(same_row) - set(neighbors.keys())) # for islands on the same row, remove already processed items
                if len(same_row) > 1:
                    neighbors[idx] = same_row[1]
                else:
                    neighbors[idx] = None

def add_guide_to_def(file_path, blocks, nets, guide):
    '''
    Append the global router guide polygons to the def file for viewing in klayout
    '''
    with open(file_path, 'a') as def_file:
        def_file.write(blocks)
        def_file.write(f';\n  - LAYER M1\n')
        for idx, box in enumerate(guide):
            if idx < ( len(guide) - 1):  
                def_file.write(f'    RECT ( {box[0]} {box[1]} ) ( {box[2]} {box[3]} ) \n')
            else:
                def_file.write(f'    RECT ( {box[0]} {box[1]} ) ( {box[2]} {box[3]} ) ;\n')
        def_file.write(f'END BLOCKAGES\n\n')
        def_file.write(nets)

def find_metal_in_lef(metal, file_name, dbu):
    lef_file = open(f'{file_name}.lef')
    store_metal = False
    ret_val = None
    for line in lef_file:
        line = line.split(' ')
        if len(line) > 1 and line[1] == f'{metal}\n' and line[0] == 'LAYER': 
            store_metal = True
        elif store_metal:
            if line[2] == 'WIDTH': 
                ret_val = float(line[3])*dbu
                store_metal = False
                lef_file.close()
                return ret_val
    lef_file.close()
    return ret_val


class Rectangle:
    def __init__(self, x1, y1, x2, y2, layer):
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        self.layer = layer

class EdgeEvent:
    def __init__(self, coord, start, end, is_start, rect, is_vertical):
        self.coord = coord
        self.start = start
        self.end = end
        self.is_start = is_start
        self.rect = rect
        self.is_vertical = is_vertical

class HoleDetector:
    def __init__(self, metal_width):
        self.metal_width = metal_width
        self.rectangles = []
        self.layers = defaultdict(list)

    def add_rectangle(self, x1, y1, x2, y2, layer):
        rect = Rectangle(x1, y1, x2, y2, layer)
        self.rectangles.append(rect)
        self.layers[layer].append(rect)

    def find_holes(self):
        holes = []
        for layer, rects in self.layers.items():
            vertical_holes = self._find_direction_holes(rects, is_vertical=True)
            horizontal_holes = self._find_direction_holes(rects, is_vertical=False)
            holes.extend([(hole, layer, "vertical") for hole in vertical_holes])
            holes.extend([(hole, layer, "horizontal") for hole in horizontal_holes])
        return holes

    def _find_direction_holes(self, rects, is_vertical):
        events = []
        for rect in rects:
            if is_vertical:
                events.append(EdgeEvent(rect.x1, rect.y1, rect.y2, True, rect, is_vertical))
                events.append(EdgeEvent(rect.x2, rect.y1, rect.y2, False, rect, is_vertical))
            else:
                events.append(EdgeEvent(rect.y1, rect.x1, rect.x2, True, rect, is_vertical))
                events.append(EdgeEvent(rect.y2, rect.x1, rect.x2, False, rect, is_vertical))
        events.sort(key=lambda e: e.coord)

        active_edges = []
        holes = []

        for i, event in enumerate(events):
            if event.is_start:
                self._insert_edge(active_edges, event)
            else:
                self._remove_edge(active_edges, event)

            if i < len(events) - 1 and events[i+1].coord - event.coord <= self.metal_width:
                new_holes = self._check_for_holes(active_edges, event.coord, events[i+1].coord, is_vertical)
                holes.extend(new_holes)

        return holes

    def _insert_edge(self, active_edges, event):
        bisect.insort(active_edges, (event.start, event.end, event.rect), key=lambda e: e[0])

    def _remove_edge(self, active_edges, event):
        active_edges.remove((event.start, event.end, event.rect))

    def _check_for_holes(self, active_edges, coord1, coord2, is_vertical):
        holes = []
        for i in range(len(active_edges) - 1):
            _, end1, _ = active_edges[i]
            start2, _, _ = active_edges[i+1]
            gap = start2 - end1
            if 0 < gap < self.metal_width:
                if is_vertical:
                    hole = ((coord1, end1), (coord2, start2))
                else:
                    hole = ((end1, coord1), (start2, coord2))
                
                # Ensure the hole has non-zero width and height
                if hole[0][0] != hole[1][0] and hole[0][1] != hole[1][1]:
                    holes.append(hole)
        return holes
    


def sort_pins_and_detect_steps(cell_pins, loc, pin_threshold):
    """
    Sort pins into sides and detect steps along each side.
    
    Parameters:
        cell_pins : dict
            Dictionary of pins with 'RECT' info: {pin_name: {'RECT': [x1,y1,x2,y2]}}
        loc : list or tuple
            Cell bounding box: [x_min, y_min, x_max, y_max]
        pin_threshold : float
            Minimum distance between pins to consider a step
    
    Returns:
        sides : dict
            Each side has 'pins' and 'steps'. Steps are (start_coord, end_coord) along the side.
            keys: 'left', 'right', 'top', 'bottom'
    """
    left_side, right_side, top_side, bottom_side = [], [], [], []

    # Assign pins to sides
    for pin_item in cell_pins.values():
        pin_left, pin_bot, pin_right, pin_top = (
            loc[0] + int(pin_item['RECT'][0]),
            loc[1] + int(pin_item['RECT'][1]),
            loc[0] + int(pin_item['RECT'][2]),
            loc[1] + int(pin_item['RECT'][3])
        )
        # distance to each side
        extension_dirs = [
            abs(loc[0] - pin_left),   # left
            abs(loc[1] - pin_bot),    # bottom
            abs(loc[2] - pin_right),  # right
            abs(loc[3] - pin_top)     # top
        ]
        index_min = min(range(len(extension_dirs)), key=extension_dirs.__getitem__)
        if index_min == 0:
            left_side.append([pin_left, pin_bot, pin_right, pin_top])
        elif index_min == 1:
            bottom_side.append([pin_left, pin_bot, pin_right, pin_top])
        elif index_min == 2:
            right_side.append([pin_left, pin_bot, pin_right, pin_top])
        elif index_min == 3:
            top_side.append([pin_left, pin_bot, pin_right, pin_top])

    sides = {}

    # Helper function for step detection
    def detect_steps(sorted_pins, side, axis_start, axis_end):
        steps = []
        prev_end = axis_start
        for pin in sorted_pins:
            start_coord = pin[1] if side in ['left','right'] else pin[0]
            end_coord = pin[3] if side in ['left','right'] else pin[2]
            if (start_coord - prev_end) > pin_threshold:
                steps.append((prev_end, start_coord))
            prev_end = end_coord
        # gap from last pin to edge
        if (axis_end - prev_end) > pin_threshold:
            steps.append((prev_end, axis_end))
        return steps

    # Sort and detect steps
    sides['left'] = {'pins': sorted(left_side, key=lambda x: x[1]), 
                     'steps': detect_steps(sorted(left_side, key=lambda x: x[1]), 'left', loc[1], loc[3])}

    sides['right'] = {'pins': sorted(right_side, key=lambda x: x[1]), 
                      'steps': detect_steps(sorted(right_side, key=lambda x: x[1]), 'right', loc[1], loc[3])}

    sides['bottom'] = {'pins': sorted(bottom_side, key=lambda x: x[0]), 
                       'steps': detect_steps(sorted(bottom_side, key=lambda x: x[0]), 'bottom', loc[0], loc[2])}

    sides['top'] = {'pins': sorted(top_side, key=lambda x: x[0]), 
                    'steps': detect_steps(sorted(top_side, key=lambda x: x[0]), 'top', loc[0], loc[2])}

    return sides

def generate_side_blockages_with_pin_dist(sides, loc, block_ext_len, pin_spacing, pin_threshold):
    """
    Generate rectilinear blockages along all sides of a cell and update pin_dist for each gap.

    Args:
        sides (dict): output from sort_pins_and_detect_steps, 
                      each side has 'pins' (sorted list) and 'steps' (list of gaps)
        loc (tuple): cell bounding box (x_min, y_min, x_max, y_max)
        block_ext_len (float): extension length beyond cell boundary for large blockage
        pin_spacing (float): spacing to keep around pins for small blockages
        pin_threshold (float): minimum distance to be considered a step

    Returns:
        List of RECT strings defining blockages
    """
    rect_string = []

    for side_name, side_info in sides.items():
        pin_list = side_info['pins']
        step_list = side_info['steps']

        # Initialize previous coordinate and pin_dist
        prev_coord = None
        pin_dist = None

        # If no pins on this side → one large rectangle covering the side
        if not pin_list:
            if side_name in ['left', 'right']:
                rect_string.append(
                    f"RECT ({loc[0]-block_ext_len if side_name=='left' else loc[2]+block_ext_len} {loc[1]}) "
                    f"({loc[0] if side_name=='left' else loc[2]} {loc[3]})\n"
                )
            else:
                rect_string.append(
                    f"RECT ({loc[0]} {loc[1]-block_ext_len if side_name=='bottom' else loc[3]+block_ext_len}) "
                    f"({loc[2]} {loc[1] if side_name=='bottom' else loc[3]})\n"
                )
            continue

        # Determine the bounding rectangle for large blockage spanning the side
        if side_name == 'left':
            block_x1 = loc[0] - block_ext_len
            block_x2 = min(pin[0] for pin in pin_list) - pin_spacing
            rect_y1 = pin_list[0][1]
            rect_y2 = pin_list[-1][3]
            rect_string.append(f"RECT ({block_x1} {rect_y1}) ({block_x2} {rect_y2})\n")

        elif side_name == 'right':
            block_x1 = max(pin[2] for pin in pin_list) + pin_spacing
            block_x2 = loc[2] + block_ext_len
            rect_y1 = pin_list[0][1]
            rect_y2 = pin_list[-1][3]
            rect_string.append(f"RECT ({block_x1} {rect_y1}) ({block_x2} {rect_y2})\n")

        elif side_name == 'bottom':
            block_y1 = loc[1] - block_ext_len
            block_y2 = min(pin[1] for pin in pin_list) - pin_spacing
            rect_x1 = pin_list[0][0]
            rect_x2 = pin_list[-1][2]
            rect_string.append(f"RECT ({rect_x1} {block_y1}) ({rect_x2} {block_y2})\n")

        elif side_name == 'top':
            block_y1 = max(pin[3] for pin in pin_list) + pin_spacing
            block_y2 = loc[3] + block_ext_len
            rect_x1 = pin_list[0][0]
            rect_x2 = pin_list[-1][2]
            rect_string.append(f"RECT ({rect_x1} {block_y1}) ({rect_x2} {block_y2})\n")

        # Generate smaller blockages between pins and edges, updating pin_dist
        for ind, pin_coord in enumerate(pin_list):
            if prev_coord is None:
                # First pin → distance from edge
                if side_name in ['left', 'right']:
                    pin_dist = abs(pin_coord[1] - loc[1])
                    temp_start = loc[1]
                else:
                    pin_dist = abs(pin_coord[0] - loc[0])
                    temp_start = loc[0]
            else:
                if side_name in ['left', 'right']:
                    pin_dist = abs(pin_coord[1] - prev_coord[3])
                    temp_start = prev_coord[3] + pin_spacing
                else:
                    pin_dist = abs(pin_coord[0] - prev_coord[2])
                    temp_start = prev_coord[2] + pin_spacing

            prev_coord = pin_coord

            # Only insert small blockage if distance exceeds threshold
            if pin_dist > pin_threshold:
                if side_name == 'left':
                    rect_string.append(f"RECT ({loc[0]-block_ext_len} {temp_start}) ({block_x2} {pin_coord[1]-pin_spacing})\n")
                elif side_name == 'right':
                    rect_string.append(f"RECT ({block_x1} {temp_start}) ({loc[2]+block_ext_len} {pin_coord[1]-pin_spacing})\n")
                elif side_name == 'bottom':
                    rect_string.append(f"RECT ({temp_start} {loc[1]-block_ext_len}) ({pin_coord[0]-pin_spacing} {block_y2})\n")
                elif side_name == 'top':
                    rect_string.append(f"RECT ({temp_start} {block_y1}) ({pin_coord[0]-pin_spacing} {loc[3]+block_ext_len})\n")

        # Handle gap from last pin to edge
        if side_name in ['left', 'right']:
            pin_dist = abs(loc[3] - prev_coord[3])
            if pin_dist > pin_threshold:
                if side_name == 'left':
                    rect_string.append(f"RECT ({loc[0]-block_ext_len} {prev_coord[3]+pin_spacing}) ({block_x2} {loc[3]})\n")
                else:
                    rect_string.append(f"RECT ({block_x1} {prev_coord[3]+pin_spacing}) ({loc[2]+block_ext_len} {loc[3]})\n")
        else:
            pin_dist = abs(loc[2] - prev_coord[2])
            if pin_dist > pin_threshold:
                if side_name == 'bottom':
                    rect_string.append(f"RECT ({prev_coord[2]+pin_spacing} {loc[1]-block_ext_len}) ({loc[2]} {block_y2})\n")
                else:
                    rect_string.append(f"RECT ({prev_coord[2]+pin_spacing} {block_y1}) ({loc[2]} {loc[3]+block_ext_len})\n")

    return rect_string

# Rectilinear Blockages Functions

def rectangle(origin = None, vert2 = None, size = None):
    if size != None:
        x1, y1 = origin
        w, h = size
        return Polygon([(x1, y1), (x1+w, y1), (x1+w, y1+h), (x1, y1+h)])
    elif vert2 != None:
        x1, y1 = origin
        x2, y2 = vert2
        return Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    else:
        return(print(f"Undefined Shape"))

def subtract_and_polygonize(large, cutouts):
    # merge all cutouts into one geometry
    all_cutouts = unary_union(cutouts)
    print(f'Cutout Union: {all_cutouts}')

    # Subtract small from large
    diff = large.difference(all_cutouts)

    # Collect boundary lines: exterior + interiors
    lines = [LineString(diff.exterior.coords)]
    for interior in diff.interiors:
        lines.append(LineString(interior.coords))

    # Polygonize the boundary lines
    pieces = list(polygonize(lines))
    return pieces, diff  # list of polygons (should usually be one L-shaped polygon)

def shrink_polygon(diff, margin):
    """Shrink an L-shaped or axis-aligned polygon by margin using sharp corners."""
    shrinked = diff.buffer(-margin, join_style=2)  # join_style=2 => sharp corners
    # If shrinked is MultiPolygon, unify it
    if shrinked.is_empty:
        return None
    elif shrinked.geom_type == 'Polygon':
        return shrinked
    elif shrinked.geom_type == 'MultiPolygon':
        return unary_union(shrinked)
    else:
        return None
    
def extract_polygons(geom):
    """Return a list of Polygon objects from any geometry."""
    if geom.is_empty:
        return []
    if geom.geom_type == 'Polygon':
        return [geom]
    elif geom.geom_type == 'MultiPolygon':
        return list(geom.geoms)
    elif geom.geom_type == 'GeometryCollection':
        polygons = []
        for g in geom.geoms:
            if g.geom_type == 'Polygon':
                polygons.append(g)
            elif g.geom_type == 'MultiPolygon':
                polygons.extend(list(g.geoms))
        return polygons
    else:
        return []

def generate_rectangles(diff_polygon, vertical_splits):
    rectangles = []

    # Ensure vertical splits are sorted and unique
    vertical_splits = sorted(set(vertical_splits))

    for i in range(len(vertical_splits) - 1):
        x_left = vertical_splits[i]
        x_right = vertical_splits[i + 1]

        # Skip zero-width strips
        if x_left >= x_right:
            continue

        # Create a tall rectangle covering full polygon Y-range
        miny, maxy = diff_polygon.bounds[1], diff_polygon.bounds[3]
        strip = box(x_left, miny, x_right, maxy)

        # Intersect strip with the polygon
        intersection = diff_polygon.intersection(strip)

        # Extract polygons from intersection
        polys = extract_polygons(intersection)
        for poly in polys:
            ys = [pt[1] for pt in poly.exterior.coords]
            rectangles.append((x_left, min(ys), x_right, max(ys)))

    return rectangles
