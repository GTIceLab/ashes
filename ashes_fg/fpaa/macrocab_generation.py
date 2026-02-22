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

    # routing

    etree.write(xml_file,pretty_print=True,xml_declaration=True,encoding='UTF-8')
    










    


    
