import os
import subprocess
import sys
import json
from lxml import etree
from io import StringIO, BytesIO
import new_macrocab_generation
import re

'''
NOTES 3/9

2 use cases: 
    1) user creates the macrocab (new file directory, copied json file, check naming conventions) - ONLY RUN ONCE
    2) macrocab generated + added to ashes (user json file is parsed, sent to "edit" functions)

todo:
    - fix create_mc_block (move class lib part to new function (Maithreyi), replace existing parser with new parser (Arya))
    - replace everything including and before create_mc_block with new stuff (Arya)
    - edit functions below create_mc_block to take parameters from internal representation (Maithreyi)
    - fix delete part (Maithreyi)
'''

# generalized paths
ASHESPATH = os.getenv("ASHESPATH","/home/ubuntu/ashes")
RASPPATH = os.getenv("RASPPATH", "/home/ubuntu/rasp30")



if len(sys.argv) == 3:
    path_name = sys.argv[1]
    block_name = sys.argv[2]
    block_level = sys.argv[3]
elif len(sys.argv) == 2:
    if sys.argv[1] == "make_macrocab":
        # call make macrocab function
        pass
    elif sys.argv[1] == "delete_macrocab":
        # call delete macrocab function

        # function calls with false

        pass
    else:
        raise ValueError("Invalid command.")
else:
    raise ValueError("Commands: python3 macrocab_generation.py block_name block_level \nOR python3 macrocab_generation.py make_macrocab \nOR python3 macrocab_generation.py delete_macrocab")


# data to specify: folder name, block name, block level
# assume this is in json/csv/txt/yaml/etc

# for the following arguments, either provided directly through command file or from txt file

def verify_starting_parameters(path_name, block_name, block_level):
    """
    Verifies starting parameters for generation: block name, folder name, block level.
    
    path_name (str): folder name to save macrocab
    block_name (str): macrocab name
    block_level (int): level of macrocab (1 or 2)
    """

    
        
    # name errors
    if block_name == "":
        raise ValueError("Macrocab name cannot be empty.")
    elif block_name and block_name[0].isdigit():
        raise ValueError("Macrocab name cannot start with a digit.")
    elif os.path.exists(f"{ASHESPATH}/{path_name}/{block_name}.json"):
        raise ValueError("Macrocab name already exists in the specified path.")
    # level errors
    if block_level != 1 and block_level != 2:
        raise ValueError("Block level must be either 1 or 2.")
    # check folder vs path
    if os.path.exists(f"{ASHESPATH}/{path_name}"):
        raise ValueError(f"Path {path_name} already exists.")
    
    subprocess.run(f"mkdir {ASHESPATH}/{path_name}")
    subprocess.run(f"mv {ASHESPATH}/ex_format.json {ASHESPATH}/{path_name}/{block_name}.json")
    subprocess.run(f"mkdir {ASHESPATH}/{block_name}_copy")
    subprocess.run(f"cp -r {ASHESPATH}/ashes_fg {ASHESPATH}/{block_name}_copy/ashes_fg")

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


def edit_class_libs(classlibfile, macrocab_name, parameters, delete):
    with open(classlibfile, 'r') as file:
        lines = file.read()
    if macrocab_name in classlibfile and not delete:
        raise ValueError(f"{macrocab_name} is already in class_lib")
    if delete:
        pattern = rf'^class {macrocab_name}:.*?(?=^class |\Z)'
        new_content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
        with open(classlibfile, 'w') as f:
            f.write(new_content)
    else:
        with open(classlibfile, "a") as file:
            file.writelines(f"\nclass {block_name}:\n")
            file.writelines("    def __init__(self,\ninput,\nnum_instances='1',\ntype='FPAA',\nboard=['3.0','3.0a'],\n")

            # Write all parameters as self attributes
            for param_name, param_value in parameters:
                file.writelines(f"\n{param_name}={param_value},")

            # Replace last comma with closing parenthesis
            file.seek(0)
            content = file.read()
            content = content[:-1] + ")"
            file.seek(0)
            file.write(content)

            for param_name, param_value in parameters:
                file.writelines(f"        self.{param_name} = {repr(param_value)}\n") # thought this was supposed to be param name? like self.common_source_ibias = common_source_ibias





def edit_xml(xml_file, generated, delete):
    macrocab_name = generated["macrocab"]["block_name"]

    root = etree.parse(xml_file).getroot()

    if delete:
        models = root.find('models')
        model = models.find(f"model[@name='{macrocab_name}']")
        if model is not None:
            models.remove(model)

        cab = root.find(".//pb_type[@name='cab']")
        pb = cab.find(f"pb_type[@name='{macrocab_name}']")
        if pb is not None:
            cab.remove(pb)

        interconnect = cab.find('interconnect')
        for elem in interconnect.findall('complete'):
            if macrocab_name in elem.get('output', '') or macrocab_name in elem.get('input', ''):
                interconnect.remove(elem)
    else:


        models = root.find('models')
        model = etree.SubElement(models, 'model', name=macrocab_name)
        inn = etree.SubElement(model, 'input_ports')
        etree.SubElement(inn,'port',name='in')
        out = etree.SubElement(model, 'output_ports')
        etree.SubElement(out, 'port', name='out')
        
        cab = root.find(".//pb_type[@name='cab']")
        pb = etree.SubElement(cab, "pb_type", name=macrocab_name,blif_model=f".{macrocab_name}",num_pb="1")

        etree.SubElement(pb, 'input', name='in', num_pins=str(macrocab_num_inputs))
        etree.SubElement(pb, 'output', name='out', num_pins=str(macrocab_num_outputs))

        etree.SubElement(pb, "delay_constant",max="1.667e-9",in_port=f"{macrocab_name}.in",out_port=f"{macrocab_name}.out")
        
        interconnect = cab.find("interconnect")

        if macrocab_num_inputs == 1:
            in_pins = f'{macrocab_name}.in[0]'
        else:
            in_pins = f'{macrocab_name}.in[{macrocab_num_inputs - 1}:0]'

        etree.SubElement(interconnect, 'complete', name='crossbar',input='cab.I[12:0]',output=in_pins)

        # output line: macrocab output drives cab.O[4]
        etree.SubElement(interconnect, 'complete',name='crossbar',input=f'{macrocab_name}[0].out[0]',output='cab.O[4]')

        # write
        etree.ElementTree(root).write(xml_file, pretty_print=True,xml_declaration=True,encoding='UTF-8')

        # routing

        #etree.write(xml_file,pretty_print=True,xml_declaration=True,encoding='UTF-8')

# needs to be updated
def edit_rasp30(rasp30_file, generated, delete):

    macrocab_name = generated["macrocab"]["block_name"]

    with open(rasp30_file, 'r') as file:
        lines = file.read()
    
    if f"{macrocab_name}" in lines and not delete:
        raise ValueError(f"{macrocab_name} already registered")

    old_dev_fgs = "'vmm_offc[0]',[0,0],"
    new_dev_fgs = f"{old_dev_fgs}\n'{macrocab_name}[0]',[0,0]"
    lines = lines.replace(old_dev_fgs, new_dev_fgs)

    old_self_dev_pins_1 = "'vmm_offc_in':13,"
    new_self_dev_pins_1 = f"{old_self_dev_pins_1}'{macrocab_name}_in':1,"
    lines = lines.replace(old_self_dev_pins_1, new_self_dev_pins_1)

    old_self_dev_pins_2 = "'vmm_offc_out':2"
    new_self_dev_pins_2 = f"{old_self_dev_pins_2},'{macrocab_name}_out':1}}"
    lines = lines.replace(old_self_dev_pins_2, new_self_dev_pins_2)

    old_self_dev_types = "+['current_ref']*1"
    new_self_dev_types = f"{old_self_dev_types}+['{macrocab_name}']*1"
    lines = lines.replace(old_self_dev_types, new_self_dev_types)

    old_li_sm_in = "'vmm_offc[0].in[0:12]',[[6,7,8,9,10,11,12,13,14,15,16,17,27],0],"
    new_li_sm_in = f"{old_li_sm_in}\n'{macrocab_name}[0].in[0]',[33,0],"
    lines = lines.replace(old_li_sm_in, new_li_sm_in)

    old_li_sm_out = "'vmm_offc[0].out[0:1]',[0,[17,18]],"
    new_li_sm_out = f"{old_li_sm_out}\n'{macrocab_name}[0].out[0]',[0,0],"
    lines = lines.replace(old_li_sm_out, new_li_sm_out)

    old_li_sm_0b = "'vmm_offc[0].out[0:1]'"
    new_li_sm_0b = f"{old_li_sm_0b},'{macrocab_name}[0].out[0]']"
    lines = lines.replace(old_li_sm_0b, new_li_sm_0b)

    old_li_sm_1 = "'vmm_offc[0].in[0:12]'"
    new_li_sm_1 = f"{old_li_sm_1},'{macrocab_name}[0].in[0]'"
    lines = lines.replace(old_li_sm_1, new_li_sm_1)

    old_cell_list = "'cap_4x_cs[0:3]',[[28,29,28,29], 0]"
    new_cell_list = f"{old_cell_list},\n'{macrocab_name}[0]',[[25,24],[25,25],[etc]],"
    lines = lines.replace(old_cell_list, new_cell_list)

    with open(rasp30_file, 'w') as file:
        file.write(lines)

def edit_genswcs(genswcs_file, block_name, num_inputs, num_outputs, delete):
    with open(genswcs_file, 'r') as file:
        lines = file.read()
    
    old_if_subckt = "else\n\t\t\t\t\tkey = ports[2]"
    new_if_subckt = f"elif subckt in [{block_name}]:\n\t\t\t\t\tkey = ports[{num_inputs}]\n{old_if_subckt}"
    lines = lines.replace(old_if_subckt, new_if_subckt)

    if num_outputs > 1:
        old_if_nsb = "if nsb.name in ["
        new_if_nsb = f"{old_if_nsb}{block_name}[0], "
        lines = lines.replace(old_if_nsb, new_if_nsb)

        old_if_from_sub_name = "elif from_sub_name in ["
        new_if_from_sub_name = f"{old_if_from_sub_name}'{block_name}[0]', "
        lines = lines.replace(old_if_from_sub_name, new_if_from_sub_name)





    