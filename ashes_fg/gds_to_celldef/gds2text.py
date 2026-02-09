import argparse
import gdstk
import os


def process_gds(file: str) -> str:
    if not os.path.exists(file):
        raise FileNotFoundError("File not found")

    library = gdstk.read_gds(file)
    output_file = os.path.splitext(file)[0] + "_output.txt"

    with open(output_file, 'w') as f:
        f.write(str(library))
        f.write("\n\n")
        for cell in library.cells:
            f.write(f"{cell}\n")

            # Extract labels (text) from each cell
            if cell.labels:
                f.write(f"  Labels in {cell.name}:\n")
                for label in cell.labels:
                    f.write(
                        f"    Text: '{label.text}' at ({label.origin[0]}, {label.origin[1]}) on layer {label.layer}\n"
                    )
                f.write("\n")

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Convert GDS to text output")
    parser.add_argument("file", nargs="?", help="Path to GDS file")
    args = parser.parse_args()

    file = args.file
    if not file:
        file = str(input("Insert GDS file path: "))

    try:
        output_file = process_gds(file)
        print(f"Saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()