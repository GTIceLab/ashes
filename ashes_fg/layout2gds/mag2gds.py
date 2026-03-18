import argparse
import os
import subprocess

def read_lib_dir(directory: str) -> list[str]:
    mag_files = []
    for cell_dir in os.listdir(directory):
        mag_filename = os.path.basename(cell_dir) + ".mag"
        mag_file_path = os.path.join(directory, cell_dir, mag_filename)
        if not os.path.isfile(mag_file_path):
            print(f"mag2gds WARNING: Magic file '{mag_filename}' was not found in subdirectory '{cell_dir}'")
        else:
            mag_files.append(mag_file_path)
    return mag_files

def generate_magic_commands(mag_files: str, output_dir: str):
    commands_file = os.path.join(output_dir, "mag2gds.tcl")
    with open(commands_file, "w") as f:
        f.write("grid 0.05um 0.05um\n")
        f.write("snap user\n")
        for mag_path in mag_files:
            if not mag_path.endswith(".mag"):
                raise ValueError(f"File {mag_path} is not a .mag file")
            gds_filename = os.path.basename(mag_path.replace(".mag", ".gds"))
            gds_path = os.path.join(output_dir, gds_filename)
            f.write(f"load \"{mag_path}\"\n")
            f.write(f"gds write \"{gds_path}\"\n")
        f.write("quit -noprompt\n")
    return commands_file

def run_magic(commands_file: str):
    magic_rc = "/srv/cadsp/pdks/open_pdks/sky130/sky130A/libs.tech/magic/sky130A.magicrc" 
    subprocess.run(["magic", "-rcfile", magic_rc, "-dnull", "-noconsole", commands_file])

def main():
    parser = argparse.ArgumentParser(description="Convert Magic layouts to GDS")
    parser.add_argument("-o", "--output", help="Output directory for GDS files", default=".")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-d", "--dir", help="Directory containing subdirectories, each with a .mag file of the same name")
    input_group.add_argument("-f", "--files", nargs="+", help="Paths to .mag files. Not allowed when also inputting DIR")
    parser.add_argument("-k", "--keep-tcl", action="store_true", help="Keep the generated TCL file after conversion (default: delete it)")
    args = parser.parse_args()

    if args.dir:
        mag_files = read_lib_dir(args.dir)
    else: # args.files
        mag_files = args.files
        if not mag_files:
            mag_files = [input("Enter an input .mag file path: ")]
        for file in mag_files:
            if not os.path.isfile(file):
                parser.error(f"File '{file}' does not exist")

    output_dir = args.output
    
    commands_file = generate_magic_commands(mag_files, output_dir)
    
    print("\nmag2gds: Running Magic...")
    run_magic(commands_file)
    print("\nmag2gds: Exited Magic\n")
    
    if not args.keep_tcl:
        os.remove(commands_file)
    else:
        print("NOTE: TCL file it at", commands_file)

if __name__ == "__main__":
    main()
