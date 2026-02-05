import os
import subprocess

'''
Macrocab generation transferred from rasp30.

High level (macrocab_gen_fcn.sce):
- MC_folder_name_callback: read folder name
- MC_block_name_callback: read macrocab name
- MC_b1_level_callback: read mixed sp, lvl1, lvl2 (what do the other levels mean?)
- start_MC_design_callback: checks macroname + workspace folder w/ xcos template
- delete_MC_callback: deletes macrocab + associated files
- generate_MC_callback: 
    - saved xcos
'''

# data to specify: folder name, block name, block level
# assume this is in json/csv/txt/yaml/etc

# for the following arguments, either provided directly through command file or from txt file

def verify_starting_parameters(path_name, block_name, block_level):
    # check folder vs path
    if os.path.exists(path_name):
        raise ValueError(f"Path {path_name} does not exist.")
    # name errors
    if block_name == "":
        raise ValueError("Macrocab name cannot be empty.")
    elif block_name and block_name[0].isdigit():
        raise ValueError("Macrocab name cannot start with a digit.")
    elif f"{path_name}/{block_name}.filextension".exists():
        raise ValueError("Macrocab name already exists in the specified path.")
    # level errors
    if block_level != 1 and block_level != 2:
        raise ValueError("Block level must be either 1 or 2.")
    
    subprocess.run(f"mkdir {RASPPATH}/{path_name}")
    subprocess.run(f"cd {RASPPATH}/{path_name}")
    subprocess.run("touch {block_name}.filextension")  

    return path_name, block_name, block_level

    
def create_mc_block(path_name, block_name, block_level):
    # parameters from macrocab design
    with open("../class_lib.py", "r") as file:
        lines = file.readlines()


    # needs fleshing out
    lines.append(f"class {block_name}:\n")
    lines.append("    def __init__(self):\n")
    for p in parameters:
        lines.append(f"        {p},\n")
    
    for p in parameters:
        lines.append(f"    self.{p} = {p}\n")
    
    with open ("../class_lib.py", "w") as file:
        file.writelines(lines)


    

def delete_macrocab(block_name, path_name):
    file_path = os.path.join(path_name, f"{block_name}.filextension")
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise ValueError(f"Macrocab {block_name} does not exist in the specified path.")
