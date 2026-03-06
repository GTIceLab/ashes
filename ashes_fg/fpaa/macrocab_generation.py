import os
import subprocess
import sys
import json
from lxml import etree
from io import StringIO, BytesIO

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

NOTES 3/3
CONFIRMED - in the xml, model/pb_type/crossbar is edited
'''

ASHESPATH = os.getenv("ASHESPATH","/home/ubuntu/ashes")
RASPPATH = os.getenv("RASPPATH", "/home/ubuntu/rasp30")


if len(sys.argv) == 4:
    path_name = sys.argv[1]
    block_name = sys.argv[2]
    block_level = sys.argv[3]
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

def verify_starting_parameters(path_name, block_name, block_level):
    """
    Verifies starting parameters for generation: block name, folder name, block level.
    
    path_name (str): folder name to save macrocab
    block_name (str): macrocab name
    block_level (int): level of macrocab (1 or 2)
    """
    # check folder vs path
    if os.path.exists(f"{ASHESPATH}/{path_name}"):
        raise ValueError(f"Path {path_name} already exists.")
        
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
    
    subprocess.run(f"mkdir {ASHESPATH}/{path_name}")
    subprocess.run(f"mv {ASHESPATH}/ex_format.json {ASHESPATH}/{path_name}/{block_name}.json")

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

    with open("../class_lib.py", "a") as file:

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

     

def delete_macrocab(path_name, block_name):
    if os.path.exists(f"{ASHESPATH}/{path_name}/{block_name}.json"):
        os.remove(f"{ASHESPATH}/{path_name}/{block_name}.json")
        os.rmdir(f"{ASHESPATH}/{path_name}")
    else:
        raise ValueError(f"Macrocab {block_name} does not exist in the specified path.")
    
    with open("../class_lib.py", "r") as file:
        lines = file.readlines()
        removeline = False
        for line in lines:
            if f"class {block_name}:" in line:
                removeline = True
            if removeline:
                lines.remove(line)

    with open("../class_lib.py", "w") as file:
        file.writelines(lines)



'''
rasp3a_arch.xml example for hh neuron
</model>
		<model name="hhneuron"> 
			<input_ports>
				<port name="in"/>
			</input_ports>
			<output_ports>
				<port name="out"/>
			</output_ports>

            
 </pb_type>
			<pb_type name="hhneuron" num_pb="1" blif_model=".hhneuron">
				<input name="in" num_pins="4"/>
				<output name="out" num_pins="3"/>
				<delay_matrix type="max" in_port="hhneuron.in" out_port="hhneuron.out"> 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10 2.69e-10</delay_matrix>
			           

<complete name="direct" input="hhneuron[0].out[2:0]" output="cab.O[3:1] "/>
				<complete name="crossbar" input="cab.I[11:8]" output="hhneuron.in[3:0] c4_sp.in[1:0] fgota.in[1:0]"/>                
                
                '''


'''
for generic macrocab:
- model defines name, input, output
- device: transistor sizing, timing, area, switch block
- routing fabric
- segment list (wire definition)
- complexblocklist
= cab type
    - instantiate model, physical block

'''

def edit_xml(xml_file, macrocab):
    root = etree.parse(xml_file).getroot()
    models = root.find('models')
    model = etree.SubElement(models, 'model', name=macrocab.name)
    inn = etree.SubElement(model, 'input_ports')
    etree.SubElements(inn,'port',name='in')
    out = etree.SubElement(model, 'output_ports')
    etree.SubElement(out, 'port', name=out)
    
    cab = root.find(".//pb_type[@name='cab']")
    pb = etree.SubElement(cab, "pb_type", name=macrocab.name,blif_model=f".{macrocab.name}",num_pb="1")

    etree.SubElement(pb, 'input', name='in', num_pins=str(macrocab.num_inputs))
    etree.SubElement(pb, 'output', name='out', num_pins=str(macrocab.num_outputs))

    etree.SubElement(pb, "delay_constant",max="1.667e-9",in_port=f"{macrocab.name}.in",out_port=f"{macrocab.name}.out")
    
    interconnect = cab.find("interconnect")

    if macrocab.num_inputs == 1:
        in_pins = f'{macrocab.name}.in[0]'
    else:
        in_pins = f'{macrocab.name}.in[{macrocab.num_inputs - 1}:0]'

    etree.SubElement(interconnect, 'complete', name='crossbar',input='cab.I[12:0]',output=in_pins)

    # output line: macrocab output drives cab.O[4]
    etree.SubElement(interconnect, 'complete',name='crossbar',input=f'{macrocab.name}[0].out[0]',output='cab.O[4]')

    # write
    etree.ElementTree(root).write(xml_file, pretty_print=True,xml_declaration=True,encoding='UTF-8')

    # routing

    #etree.write(xml_file,pretty_print=True,xml_declaration=True,encoding='UTF-8')

def edit_rasp30(rasp30_file, block_name):
    with open(rasp30_file, 'r') as file:
        lines = file.read()
    
    if f"'{block_name}[0]'" in lines:
        print(f"{block_name} already registered")

    old_dev_fgs = "'vmm_offc[0]',[0,0],"
    new_dev_fgs = f"{old_dev_fgs}\n'{block_name}[0]',[0,0]"
    lines.replace(old_dev_fgs, new_dev_fgs)

    old_self_dev_pins_1 = "'vmm_offc_in':13,"
    new_self_dev_pins_1 = f"{old_self_dev_pins_1}'{block_name}_in':1,"
    lines.replace(old_self_dev_pins_1, new_self_dev_pins_1)

    old_self_dev_pins_2 = "'vmm_offc_out':2"
    new_self_dev_pins_2 = f"{old_self_dev_pins_2},'{block_name}_out':1}}"
    lines.replace(old_self_dev_pins_2, new_self_dev_pins_2)

    old_self_dev_types = "+['current_ref']*1"
    new_self_dev_types = f"{old_self_dev_types}+['{block_name}']*1"
    lines.replace(old_self_dev_types, new_self_dev_types)

    old_li_sm_in = "'vmm_offc[0].in[0:12]',[[6,7,8,9,10,11,12,13,14,15,16,17,27],0],"
    new_li_sm_in = f"{old_li_sm_in}\n'{block_name}[0].in[0]',[33,0],"
    lines.replace(old_li_sm_in, new_li_sm_in)

    old_li_sm_out = "'vmm_offc[0].out[0:1]',[0,[17,18]],"
    new_li_sm_out = f"{old_li_sm_out}\n'{block_name}[0].out[0]',[0,0],"
    lines.replace(old_li_sm_out, new_li_sm_out)

    old_li_sm_0b = "'vmm_offc[0].out[0:1]'"
    new_li_sm_0b = f"{old_li_sm_0b},'{block_name}[0].out[0]']"
    lines.replace(old_li_sm_0b, new_li_sm_0b)

    old_li_sm_1 = "'vmm_offc[0].in[0:12]'"
    new_li_sm_1 = f"{old_li_sm_1},'{block_name}[0].in[0]'"
    lines.replace(old_li_sm_1, new_li_sm_1)

    old_cell_list = "'cap_4x_cs[0:3]',[[28,29,28,29], 0]"
    new_cell_list = f"{old_cell_list},\n'{block_name}[0]',[[25,24],[25,25],[etc]],"
    lines.replace(old_cell_list, new_cell_list)

    with open(rasp30_file, 'w') as file:
        file.write(lines)

    