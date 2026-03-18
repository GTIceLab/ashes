import argparse
import os

import gdstk

def get_bounding_box(cell: gdstk.Cell) -> tuple:
    # TODO This function is not used. Does built-in bounding_box() include hierarchy?
    copy = cell.copy("temp_name")
    copy.flatten()
    print(cell.bounding_box(), copy.bounding_box())
    return copy.bounding_box()

def get_pin_direction(label: gdstk.Label, box: tuple) -> str:
    (x_min, y_min), (x_max, y_max) = box
    pin_x, pin_y = label.origin
    
    distances = [
        abs(pin_y - y_max), # n
        abs(pin_y - y_min), # s
        abs(pin_x - x_max), # e
        abs(pin_x - x_min), # w
    ]

    min_distance = min(distances)
    if min_distance == distances[0]:
        return "n"
    elif min_distance == distances[1]:
        return "s"
    elif min_distance == distances[2]:
        return "e"
    else:
        return "w"
    # TODO what if a pin is directly in the middle?

def add_direction(pin_name: str, direction: str) -> str:
    if "[" in pin_name:
        base_name, index = pin_name.split("[", 1)
        return base_name + "_" + direction + "[" + index
    else:
        return pin_name + "_" + direction

def fix_pins(input_filename: str, output_filename):
    try:
        library = gdstk.read_gds(input_filename)
    except Exception as e:
        print(f"NOTE: Error reading file '{input_filename}'")
        raise # re-raise error after communicating the problematic filename
    # TODO is below an issue?
    if len(library.top_level()) != 1:
        raise ValueError(f"Found multiple ({len(library.top_level())}) top level cells in {input_filename}")
    
    cell = library.top_level()[0]
    box = cell.bounding_box()
    for label in cell.labels:
        direction = get_pin_direction(label, box)
        label.text = add_direction(label.text, direction)
    
    library.write_gds(output_filename)

def main():
    parser = argparse.ArgumentParser(description="Edit GDS layouts to add directions to duplicate pin names")
    parser.add_argument("files", nargs="+", help="Paths to .gds files")
    parser.add_argument("-o", "--output", help="Output directory for fixed GDS files", default=".")
    args = parser.parse_args()

    files = args.files
    if not files:
        files = [input("Insert input .gds file path: ")]
    
    output_dir = args.output
    
    for filename in files:
        output_filename = os.path.join(
            output_dir,
            os.path.basename(filename)
        )
        fix_pins(filename, output_filename)

    print("NOTE: Final GDS files are in directory", output_dir)
    
if __name__ == "__main__":
    main()
