#high level description 
#read text file, it will accept an output file as such:
#look for "Labels in {name_of_file_without_extension}" within the text and start parsing after that
#Ex:
# Labels in TSMC350nm_TGate_2nMirror:
#     Text: 'GND_b' at (15.39, 0.92) on layer 41
#     Text: 'VINJ_b' at (4.5200000000000005, 0.92) on layer 41
#     Text: 'GND' at (15.39, 21.52) on layer 41
#     Text: 'VINJ' at (4.5200000000000005, 21.52) on layer 41
#     Text: 'IN_CM<0>' at (1.18, 19.52) on layer 40
#     Text: 'IN_CM<1>' at (0.29, 13.52) on layer 40
#     Text: 'IN_TG' at (0.66, 0.9500000000000001) on layer 40
#     Text: 'SelN' at (0.5, 10.05) on layer 40
#     Text: 'OUT_TG' at (24.990000000000002, 3.7800000000000002) on layer 40
#     Text: 'OUT_CM<1>' at (25.22, 10.77) on layer 40
#     Text: 'OUT_CM<0>' at (25.2, 18.66) on layer 40

# we only want the Text and its position


#parse coordinates as a tuple
#in a single pass, find the greatest x,y
#store in a variable or return from function

#in another loop find the least x,y
#store in a variable or return from function

#take max_x - min_x to get total_width
#take max_y - min_y to get total_height

#now, for each label,  
#e.g a label coord with its distance from the max height being smaller than any other side, would be in the "North"
# if the store its text in a dictionary with a list as a key { direction:[label]}
# do this for each label

import argparse
import re
import os
import json


def process_text_output(file: str) -> str:
    if not os.path.exists(file):
        raise FileNotFoundError("File not found")

    with open(file, 'r') as f:
        content = f.read()

    # Extract base filename without extension and "_output" suffix
    base_filename = os.path.basename(file)
    name_without_ext = os.path.splitext(base_filename)[0]
    # Remove "_output" suffix if present
    if name_without_ext.endswith('_output'):
        name_without_ext = name_without_ext[:-7]

    # Extract directory name for type
    directory_name = os.path.basename(os.path.dirname(file))
    if not directory_name:
        directory_name = os.path.basename(os.getcwd())

    # Extract foundry (letters before first number) and process node
    foundry_match = re.match(r'^([A-Za-z]+)', name_without_ext)
    foundry = foundry_match.group(1) if foundry_match else ""

    # Extract process node (numbers after foundry)
    process_node_match = re.search(r'(\d+)', name_without_ext)
    process_node = f"{process_node_match.group(1)}nm" if process_node_match else ""

    # Find "Labels in {filename}:" section for this specific file
    labels_section_pattern = rf"Labels in {re.escape(name_without_ext)}:(.*?)(?=Labels in |\Z)"
    section_match = re.search(labels_section_pattern, content, re.DOTALL)

    if not section_match:
        raise ValueError(f"No 'Labels in {name_without_ext}:' section found in file")

    labels_content = section_match.group(1)

    # Parse labels - pattern: Text: 'label' at (x, y) on layer N
    pattern = r"Text: '([^']+)' at \(([^,]+), ([^)]+)\)"
    matches = re.findall(pattern, labels_content)

    if not matches:
        raise ValueError("No labels found in section")

    # Extract labels with coordinates
    labels = []
    for text, x, y in matches:
        if text.startswith("&"):
            continue
        labels.append({'text': text, 'x': float(x), 'y': float(y)})

    # Find max and min coordinates
    max_x = max(label['x'] for label in labels)
    min_x = min(label['x'] for label in labels)
    max_y = max(label['y'] for label in labels)
    min_y = min(label['y'] for label in labels)

    total_width = max_x - min_x
    total_height = max_y - min_y

    # Parse labels to extract base name and pin number
    def parse_label(text):
        match = re.match(r'(.+?)<(\d+)>$', text)
        if match:
            return match.group(1), int(match.group(2))
        return text, None

    # Categorize labels by direction and group by base name
    directions = {'N': {}, 'S': {}, 'E': {}, 'W': {}}

    for label in labels:
        x, y = label['x'], label['y']
        direction = None

        # Calculate distances to each edge
        dist_north = max_y - y
        dist_south = y - min_y
        dist_east = max_x - x
        dist_west = x - min_x

        # Find closest edge
        min_dist = min(dist_north, dist_south, dist_east, dist_west)

        # If any two distances are equally close, throw an error
        distances = [dist_north, dist_south, dist_east, dist_west]
        if distances.count(min_dist) > 1:
            # if contains _b, put in south
            if label['text'].endswith('_b') or '_b' in label['text']:
                direction = 'S'
            else:
                raise ValueError(
                    f"Ambiguous direction for label '{label['text']}' at ({x}, {y}): multiple edges are equally close."
                )

        # Parse label to get base name and pin
        base_name, pin_num = parse_label(label['text'])

        # Determine direction
        if direction is None:
            if min_dist == dist_north:
                direction = 'N'
            elif min_dist == dist_south:
                direction = 'S'
            elif min_dist == dist_east:
                direction = 'E'
            else:
                direction = 'W'

        # Group by base name
        if base_name not in directions[direction]:
            directions[direction][base_name] = []
        directions[direction][base_name].append(pin_num)

    # Format labels with pin ranges
    formatted_directions = {'N': [], 'S': [], 'E': [], 'W': []}

    for direction, label_groups in directions.items():
        for base_name, pins in label_groups.items():
            if None in pins:
                formatted_directions[direction].append(base_name)
            else:
                pins_sorted = sorted(pins)
                min_pin = pins_sorted[0]
                max_pin = pins_sorted[-1]
                if min_pin == max_pin:
                    try:
                        if (min_pin > 0 and max_pin > 0):
                            formatted_directions[direction].append(f"{base_name}[0:{max_pin}]")
                    except Exception as e:
                        print(f"{e}: bus ranges from {min_pin} to {max_pin}.")
                else:
                    formatted_directions[direction].append(f"{base_name}[{min_pin}:{max_pin}]")

    directions = formatted_directions

    # Save to JSON
    output_file = os.path.splitext(file)[0] + "_directions.json"

    # Remove everything before first underscore for the key
    key_name = name_without_ext.split('_', 1)[1] if '_' in name_without_ext else name_without_ext

    # Create nested dict and format it on one line
    nested_dict = {
        'type': directory_name,
        'foundry': foundry,
        'process_node': process_node,
        'W': directions['W'],
        'E': directions['E'],
        'N': directions['N'],
        'S': directions['S']
    }

    nested_json = json.dumps(nested_dict, separators=(',', ':'))
    output_json = '{\n"' + key_name + '":\n' + nested_json + '\n}'

    with open(output_file, 'w') as f:
        f.write(output_json)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Convert text output to directions JSON")
    parser.add_argument("file", nargs="?", help="Path to *_output.txt file")
    args = parser.parse_args()

    file = args.file
    if not file:
        file = str(input("Insert output file path: "))

    try:
        output_file = process_text_output(file)
        print(f"\nSaved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
