import argparse
import os
import subprocess

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
    parser.add_argument("files", nargs="+", help="Path to .mag files")
    parser.add_argument("-o", "--output", help="Output directory for GDS files", default=".")
    args = parser.parse_args()

    files = args.files
    if not files:
        files = [input("Insert input .mag file path: ")]
    
    output_dir = args.output

    commands_file = generate_magic_commands(files, output_dir)
    
    run_magic(commands_file)
    
if __name__ == "__main__":
    main()
