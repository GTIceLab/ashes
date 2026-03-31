import os
import subprocess
import sys
import json
from lxml import etree
from io import StringIO, BytesIO
import re

simulation_log = []

# generalized paths
ASHESPATH = os.getenv("ASHESPATH","/home/ubuntu/ashes")
RASPPATH = os.getenv("RASPPATH", "/home/ubuntu/rasp30")

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
    if block_level != "1" and block_level != "2":
        raise ValueError(f"Block level must be either 1 or 2. Yours was {block_level}.")
    # check folder vs path
    #if os.path.exists(f"{ASHESPATH}/{path_name}"):
        #raise ValueError(f"Path {path_name} already exists.")
    
    subprocess.run([f"mkdir", f"{ASHESPATH}/{path_name}"])
    subprocess.run([f"cp", f"{ASHESPATH}/ashes_fg/fpaa/template.json", f"{ASHESPATH}/{path_name}/{block_name}.json"])

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



def is_routing_exception(data):
    """
    Checks if any active routing column is less than 15.
    Works for the new flattened JSON structure.
    """
    routing = data.get('routing', {})
    
    for key, content in routing.items():
        # 1. Skip the power_block as per original logic
        if key == 'power_block':
            continue
            
        # 2. Extract fg_address (New Format)
        # In your new JSON, content is a dict like {"fg_address": [[r,c]..], "bias":..}
        addresses = content.get('fg_address', [])
        
        # Ensure 'addresses' is a list we can iterate over
        if isinstance(addresses, list) and len(addresses) > 0:
            
            # Case A: List of lists [[row, col], [row, col]]
            if isinstance(addresses[0], list):
                for addr in addresses:
                    if len(addr) > 1: # Ensure [row, col] pair exists
                        if int(addr[1]) < 15:
                            return True
            
            # Case B: Single list [row, col]
            else:
                if len(addresses) > 1:
                    if int(addresses[1]) < 15:
                        return True
                        
    return False

def edit_xml(xml_file, macrocab_name, macrocab_num_inputs, macrocab_num_outputs, delete, routing_exception):
    root = etree.parse(xml_file).getroot()

    if delete:
        # 1. Remove from <models>
        models = root.find('models')
        if models is not None:
            model = models.find(f"model[@name='{macrocab_name}']")
            if model is not None:
                models.remove(model)

        # 2. Find the CAB and remove the pb_type
        cab = root.find(".//pb_type[@name='cab']")
        if cab is not None:
            pb = cab.find(f"pb_type[@name='{macrocab_name}']")
            if pb is not None:
                cab.remove(pb)

            # 3. SAFE DELETE for Interconnect (The part we just fixed)
            interconnect = cab.find(".//interconnect")
            if interconnect is not None:
                for tag in ('complete', 'direct'):
                    for elem in interconnect.findall(tag):
                        inp = elem.get('input', '')
                        out = elem.get('output', '')
                        
                        # Regex ensures we match "OTA0" but NOT "FGOTA0"
                        pattern = rf"(^|[\s\[.]){re.escape(macrocab_name)}([\s\[.]|$)"
                        
                        if re.search(pattern, inp) or re.search(pattern, out):
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
        
        interconnect = cab.find(".//interconnect")

        if macrocab_num_inputs == 1:
            in_pins = f'{macrocab_name}.in[0]'
        else:
            in_pins = f'{macrocab_name}.in[{macrocab_num_inputs - 1}:0]'

        if routing_exception:
            cab_in = 'cab.I[0]' if macrocab_num_inputs == 1 else f'cab.I[{macrocab_num_inputs - 1}:0]'
            etree.SubElement(interconnect, 'direct', name='crossbar', input=cab_in, output=in_pins)
        else:
            etree.SubElement(interconnect, 'complete', name='crossbar', input=f'cab.I[12:0]', output=in_pins)

        # output line: macrocab output drives cab.O[4]
        if macrocab_num_outputs == 1:
            etree.SubElement(interconnect, 'complete', name='crossbar', input=f'{macrocab_name}[0].out[0]', output='cab.O[4]')
        else:
            cab_out_end = 4 - (macrocab_num_outputs - 1)
            etree.SubElement(interconnect, 'direct', name='crossbar', input=f'{macrocab_name}[0].out[{macrocab_num_outputs - 1}:0]', output=f'cab.O[4:{cab_out_end}]')

    etree.ElementTree(root).write(xml_file, pretty_print=True,xml_declaration=True,encoding='UTF-8')



def edit_rasp30(rasp30_file, macrocab_name, num_inputs, num_outputs, output_cells, input_cells, resource_cells, fg_cells, delete):

    with open(rasp30_file, 'r') as file:
        lines = file.read()
    
    if f"{macrocab_name}" in lines and not delete:
        raise ValueError(f"{macrocab_name} already registered")
    
    out_pin = f"'{macrocab_name}[0].out[0]'" if num_outputs == 1 else \
              f"'{macrocab_name}[0].out[0:{num_outputs-1}]'"
    in_pin  = f"'{macrocab_name}[0].in[0]'"  if num_inputs  == 1 else \
              f"'{macrocab_name}[0].in[0:{num_inputs-1}]'"

    if delete:

        lines = lines.replace(f",{out_pin}", "")  # li_sm_0b
        lines = lines.replace(f",{in_pin}",    "")     # li_sm_1
        lines = lines.replace(f"+['{macrocab_name}']*1", "")  # dev_types
        lines = lines.replace(f",'{macrocab_name}_in':{num_inputs}", "")   # dev_pins
        lines = lines.replace(f",'{macrocab_name}_out':{num_outputs}", "")  # dev_pins

        lines = "\n".join(
            l for l in lines.splitlines()
            if macrocab_name not in l
        )
    else:

        old_dev_fgs = "'vmm_offc[0]',[0,0],"
        new_dev_fgs = f"{old_dev_fgs}\n\t\t\t'{macrocab_name}[0]',[0,0]"
        lines = lines.replace(old_dev_fgs, new_dev_fgs) # checked

    # This anchor matches the exact spacing and line content in your rasp30.py
        # Note: the file uses spaces (8 or 12) here, not tabs.
        anchor = "			'cap_4x_cs[0:3]',[[28,29,28,29], 0]]\n		self.dev_fgs = smDictFromList(dev_fgs_sm)"

        # Build the new content
        new_entry = f"            '{macrocab_name}_ls[0]', {fg_cells}"

        if isinstance(resource_cells, dict):
            caps = resource_cells.get("CAP0", [])
            caps_nums = {1: 4, 2: 2, 3: 1}
            
            for i, cell in enumerate(caps):
                cap_val = caps_nums.get(i + 1, 1)
                # Match the 12-space indentation of the file
                new_entry += f",\n            '{macrocab_name}_cap0_{cap_val}x_cs[0]', {cell}"

        # Use a comma and newline to maintain the list structure
        replacement = f"{new_entry},\n{anchor}"

        if anchor in lines:
            lines = lines.replace(anchor, replacement)
        else:
            print("Error: Could not find any valid anchor in rasp30.py")

        old_dev_pins_1 = "'vmm_offc_in':13,"
        lines = lines.replace(old_dev_pins_1, f"{old_dev_pins_1}'{macrocab_name}_in':{num_inputs},") # checked

        old_dev_pins_2 = "'vmm_offc_out':2"
        lines = lines.replace(old_dev_pins_2, f"{old_dev_pins_2},'{macrocab_name}_out':{num_outputs}") # checked

        old_dev_types = "+['vmm_offc']*1"
        lines = lines.replace(old_dev_types, f"{old_dev_types}+['{macrocab_name}']*1") # checked

        old_li_sm_in = "'vmm_offc[0].in[0:12]',[[6,7,8,9,10,11,12,13,14,15,16,17,27],0],"
        lines = lines.replace(old_li_sm_in, f"{old_li_sm_in}\n\t\t\t{in_pin},{input_cells},")

        old_li_sm_out = "'vmm_offc[0].out[0:1]',[0,[17,18]],"
        lines = lines.replace(old_li_sm_out, f"{old_li_sm_out}\n\t\t\t{out_pin},{output_cells},")

        old_li_sm_0b = ",'vmm_offc[0].out[0:1]'"
        lines = lines.replace(old_li_sm_0b, f"{old_li_sm_0b},{out_pin}") # checked

        old_li_sm_1 = ",'vmm_offc[0].in[0:12]'"
        lines = lines.replace(old_li_sm_1, f"{old_li_sm_1},{in_pin}") #fgbias, pbias, etc? # checked

    with open(rasp30_file, 'w') as file:
        file.write(lines)

def edit_genswcs(genswcs_file, block_name, num_inputs, num_outputs, delete):
    with open(genswcs_file, 'r') as file:
        lines = file.read()
    if num_outputs == 1:
        four_spaces = "    " 
        indent_4 = four_spaces * 4
        indent_5 = four_spaces * 5
        if delete:
            pattern = rf"{indent_4}elif subckt in \['{re.escape(block_name)}'\]:\n{indent_5}key = ports\[\d+\]\n"
            lines = re.sub(pattern, "", lines)
        
        else:
            

            old_if_subckt = f"{indent_4}else:\n{indent_5}key = ports[2]"

            new_if_subckt = (
                f"{indent_4}elif subckt in ['{block_name}']:\n"
                f"{indent_5}key = ports[{num_inputs}]\n"
                f"{old_if_subckt}"
            )

            lines = lines.replace(old_if_subckt, new_if_subckt)
    

    if num_outputs > 1:
        if delete:
            lines = re.sub(rf"'{re.escape(block_name)}\[\d+\]',\s*", "", lines)
            lines = re.sub(rf"{re.escape(block_name)}\[\d+\],\s*", "", lines)
        else:
            old_if_nsb = "if nsb.name in ["
            new_if_nsb = f"{old_if_nsb}{block_name}[0], "
            lines = lines.replace(old_if_nsb, new_if_nsb)

            old_if_from_sub_name = "elif from_sub_name in ["
            new_if_from_sub_name = f"{old_if_from_sub_name}'{block_name}[0]', "
            lines = lines.replace(old_if_from_sub_name, new_if_from_sub_name)
    
    with open(genswcs_file, 'w') as file:
        file.write(lines)


if len(sys.argv) == 4:
    block_name = sys.argv[1]
    block_level = sys.argv[2]
    json_path = sys.argv[3]

    verify_starting_parameters(json_path, block_name, block_level)

if len(sys.argv) == 5:
    block_name = sys.argv[1]
    block_level = sys.argv[2]
    json_file = sys.argv[3] # from ashes/ashes_fg/fpaa
    make_or_delete = sys.argv[4]

    # assume already verified
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    num_inputs = data['io']['inputs']['num_inputs']
    num_outputs = data['io']['outputs']['num_outputs']

    categorized_addresses = {
        "resources": {},  # Changed to a dictionary
        "io": [],
        "routing": []
    }

    # 1. Process Resources with specific names
    for name, info in data['resources'].items():
        if info.get("sel", False) or info.get("enabled", False):
            addr = info.get('fg_address')
            if addr:
                # We create a entry for each specific resource name (e.g., 'CAP0')
                if name not in categorized_addresses["resources"]:
                    categorized_addresses["resources"][name] = []
                
                if isinstance(addr[0], list):
                    categorized_addresses["resources"][name].extend(addr)
                else:
                    categorized_addresses["resources"][name].append(addr)

    # 2. Process IO (using keys for clarity)
    categorized_addresses["io"] = {
        "input": data['io']['inputs']['fg_address'],
        "output": data['io']['outputs']['fg_address']
    }

    # 3. Process Routing
    categorized_addresses["routing"] = data['routing']['C']['fg_address']

    resources = categorized_addresses["resources"]

    io = categorized_addresses["io"]

    routing = categorized_addresses["routing"]

    print(categorized_addresses)

    if make_or_delete == "make":
        edit_genswcs(f"{ASHESPATH}/ashes_fg/fpaa/genswcs.py", block_name, num_inputs, num_outputs, delete=False)
        edit_xml(f"{ASHESPATH}/ashes_fg/fpaa/arch/rasp3_arch.xml", block_name, num_inputs, num_outputs, delete=False, routing_exception=is_routing_exception(data))
        edit_xml(f"{ASHESPATH}/ashes_fg/fpaa/arch/rasp3a_arch.xml", block_name, num_inputs, num_outputs, delete=False, routing_exception=is_routing_exception(data))

        edit_rasp30(f"{ASHESPATH}/ashes_fg/fpaa/rasp30.py", block_name, num_inputs, num_outputs, io["output"], io["input"], resources, routing, delete=False)
        edit_rasp30(f"{ASHESPATH}/ashes_fg/fpaa/rasp30a.py", block_name, num_inputs, num_outputs, io["output"], io["input"], resources, routing, delete=False)
        #edit_class_libs
    elif make_or_delete == "delete":
        edit_genswcs(f"{ASHESPATH}/ashes_fg/fpaa/genswcs.py", block_name, num_inputs, num_outputs, delete=True)
        edit_xml(f"{ASHESPATH}/ashes_fg/fpaa/arch/rasp3_arch.xml", block_name, num_inputs, num_outputs, delete=True, routing_exception=is_routing_exception(data))
        edit_xml(f"{ASHESPATH}/ashes_fg/fpaa/arch/rasp3a_arch.xml", block_name, num_inputs, num_outputs, delete=True, routing_exception=is_routing_exception(data))
        edit_rasp30(f"{ASHESPATH}/ashes_fg/fpaa/rasp30.py", block_name, num_inputs, num_outputs, io["output"], io["input"], resources, routing, delete=True)
        edit_rasp30(f"{ASHESPATH}/ashes_fg/fpaa/rasp30a.py", block_name, num_inputs, num_outputs, io["output"], io["input"], resources, routing, delete=True)