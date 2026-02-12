import os
import subprocess
import sys
import json
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

# python3 macrocab_generation.py path_name block_name block_level
# python3 macrocab_generation.py make_macrocab
if len(sys.argv) == 4:
    global path_name
    path_name = sys.argv[1]
    global block_name
    block_name = sys.argv[2]
    global block_level
    block_name = sys.argv[3]
elif len(sys.argv) == 2:
    if sys.argv[1] == "make_macrocab":
        # call make macrocab function
        pass
    elif sys.argv[1] == "delete_macrocab":
        # call delete macrocab function
        pass
    else:
        raise ValueError("Invalid command.")
else:
    raise ValueError("Commands: python3 macrocab_generation.py path_name block_name block_level \nOR python3 macrocab_generation.py make_macrocab \nOR python3 macrocab_generation.py delete_macrocab")






    

# data to specify: folder name, block name, block level
# assume this is in json/csv/txt/yaml/etc

# for the following arguments, either provided directly through command file or from txt file

def verify_starting_parameters():
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
    subprocess.run(f"touch {block_name}.filextension")  

    return path_name, block_name, block_level

with open("ashes_fg/fpaa/ex_format.json") as f:
    data = json.load(f); #loads user's data from json file
    
def create_mc_block():
    # parameters from macrocab design
    """
    Creates macrocab class using JSON data from user
    
    path_name (str): folder path to save macrocab
    block_name (str): macrocab name
    data (dict): JSON-loaded macrocab info
    """
    parameters =[]

    #build the parameters from the JSON data
    for name, block in data.items():
        #bias
        if "bias" in block:
            parameters.append((f"{name}_bias", block["bias"]["default"]))
        elif "biases" in block: 
            for b in block["biases"]:
                parameters.append((b["name"], b["default"]))
                if "capacitance" in b:
                    parameters.append((f"{b['name']}_cap", b["capacitance"]))

        #capacitance
        if "capacitance" in block:
            parameters.append((f"{name}_capacitance", block["capacitance"]))

        # FG addresses
        if "fg_address" in block:
            parameters.append((f"{name}_row", block["fg_address"]["row"]))
            parameters.append((f"{name}_col", block["fg_address"]["col"]))

        # Inputs/outputs
        if "inputs" in block:
            parameters.append((f"{name}_inputs", block["inputs"]))
        if "outputs" in block:
            parameters.append((f"{name}_outputs", block["outputs"]))

    with open("../class_lib.py", "r") as file:
        lines = file.readlines()

    lines.append(f"\nclass {block_name}:\n")
    lines.append("    def __init__(self):\n")

    # Write all parameters as self attributes
    for param_name, param_value in parameters:
        lines.append(f"        self.{param_name} = {repr(param_value)}\n")

    with open("../class_lib.py", "w") as file:
        file.writelines(lines)

    

def delete_macrocab():
    file_path = os.path.join(path_name, f"{block_name}.filextension")
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise ValueError(f"Macrocab {block_name} does not exist in the specified path.")
