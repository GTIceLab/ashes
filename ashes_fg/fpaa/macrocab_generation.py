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
    subprocess.run([f"cp", f"{ASHESPATH}/{path_name}/template.json", f"{ASHESPATH}/{path_name}/{block_name}.json"])

#######
# Parser for new JSON:
#######

def load_design_json(json_path):
    """
    Loads macrocab JSON file
    """
    with open(json_path, "r") as f:
        return json.load(f)
    
def validate_io(io_block):
    """
    Validate macrocab I/O definition.
    Ex:
    {
        "inputs": [0, 1, 2],
        "outputs": [0, 1]
    }
    """
    if not isinstance(io_block, dict):
        raise ValueError("io must be a dictionary")

    if "inputs" not in io_block or "outputs" not in io_block:
        raise ValueError("io must contain 'inputs' and 'outputs'")

    inputs = io_block["inputs"]
    outputs = io_block["outputs"]

    if not isinstance(inputs, list):
        raise ValueError("io.inputs must be a list")
    if not isinstance(outputs, list):
        raise ValueError("io.outputs must be a list")

    for name, arr in [("inputs", inputs), ("outputs", outputs)]:
        for val in arr:
            if not isinstance(val, int):
                raise ValueError(f"io.{name} entries must be integers")
            if val < 0:
                raise ValueError(f"io.{name} entries must be >= 0")

        if len(arr) != len(set(arr)):
            raise ValueError(f"io.{name} cannot contain duplicates")

        if arr and sorted(arr) != list(range(max(arr) + 1)):
            raise ValueError(
                f"io.{name} must be contiguous starting at 0, got {arr}"
            )

def validate_connection_list(points, max_rows, max_cols, field_name):
    """
    Validate C/T entries in format:
    {
        "row": 0 or "",
        "col": 0 or "",
        "label": ""
    }
    """
    if not isinstance(points, list):
        raise ValueError(f"{field_name} must be a list")

    for point in points:
        if not isinstance(point, dict):
            raise ValueError(f"{field_name} entries must be dictionaries")

        if "row" not in point or "col" not in point or "label" not in point:
            raise ValueError(
                f"{field_name} entries must contain 'row', 'col', and 'label'"
            )

        row = point["row"]
        col = point["col"]
        label = point["label"]

        if not isinstance(label, str):
            raise ValueError(f"{field_name} label must be a string")

        # allow template placeholders ""
        if row != "":
            if not isinstance(row, int):
                raise ValueError(f"{field_name} row must be an integer or ''")
            if not (0 <= row < max_rows):
                raise ValueError(
                    f"{field_name}: row {row} out of bounds [0, {max_rows - 1}]"
                )

        if col != "":
            if not isinstance(col, int):
                raise ValueError(f"{field_name} col must be an integer or ''")
            if not (0 <= col < max_cols):
                raise ValueError(
                    f"{field_name}: col {col} out of bounds [0, {max_cols - 1}]"
                )
def validate_resources(resources):
    """
    Validate resource block in JSON
    """
    allowed_resources = {
        "FGOTA0", "FGOTA1", "OTA0", "OTA1",
        "CAP0", "CAP1", "CAP2", "CAP3",
        "NFET0", "NFET1", "PFET0", "PFET1",
        "TGATE0", "TGATE1", "TGATE2", "TGATE3",
        "NMIRROR0", "NMIRROR1"
    }

    if not isinstance(resources, dict):
        raise ValueError("resources must be a dictionary")

    for name, resource in resources.items():
        if name not in allowed_resources:
            raise ValueError(f"Unknown resource: {name}")

        if not isinstance(resource, dict):
            raise ValueError(f"Resource {name} must be a dictionary")

        if "enabled" not in resource:
            raise ValueError(f"Resource {name} missing 'enabled'")

        if not isinstance(resource["enabled"], bool):
            raise ValueError(f"Resource {name}.enabled must be a boolean")

        if "params" in resource and not isinstance(resource["params"], dict):
            raise ValueError(f"Resource {name}.params must be a dictionary")
def validate_row_map(row_map_b):
    """
    Valid matrix_b row mapping
    """
    if not isinstance(row_map_b, list):
        raise ValueError("row_map.matrix_b must be a list")

    if len(row_map_b) != 30:
        raise ValueError("row_map.matrix_b must contain exactly 30 entries")

    seen_rows = set()
    for entry in row_map_b:
        if not isinstance(entry, dict):
            raise ValueError("Each row_map.matrix_b entry must be a dictionary")

        if "row" not in entry or "resource" not in entry or "pin" not in entry:
            raise ValueError(
                "Each row_map.matrix_b entry must contain row, resource, and pin"
            )

        row = entry["row"]
        if row in seen_rows:
            raise ValueError(f"Duplicate row_map.matrix_b row: {row}")
        seen_rows.add(row)

    if seen_rows != set(range(30)):
        raise ValueError("row_map.matrix_b must cover rows 0 through 29 exactly")

def validate_design_json(data):
    """
    Validate full JSON template.
    """
    required_top_keys = ["metadata", "defaults", "io", "resources", "routing", "row_map"]
    for key in required_top_keys:
        if key not in data:
            raise ValueError(f"Missing top-level key: {key}")

    validate_io(data["io"])
    validate_resources(data["resources"])

    routing = data["routing"]
    required_blocks = {
        "power_block": (30, 2),
        "matrix_a": (30, 13),
        "matrix_b": (30, 18)
    }

    for block_name, dims in required_blocks.items():
        if block_name not in routing:
            raise ValueError(f"Missing routing block: {block_name}")

        block = routing[block_name]

        if "dimensions" not in block:
            raise ValueError(f"{block_name} missing 'dimensions'")

        if block["dimensions"] != [dims[0], dims[1]]:
            raise ValueError(
                f"{block_name}.dimensions must be {[dims[0], dims[1]]}"
            )

        if block_name == "power_block":
            validate_connection_list(
                block.get("C", []), dims[0], dims[1], f"{block_name}.C", require_label=False
            )
            validate_connection_list(
                block.get("T", []), dims[0], dims[1], f"{block_name}.T", require_label=True
            )
        else:
            validate_connection_list(
                block.get("C", []), dims[0], dims[1], f"{block_name}.C", require_label=True
            )
            validate_connection_list(
                block.get("T", []), dims[0], dims[1], f"{block_name}.T", require_label=True
            )

    if "matrix_b" not in data["row_map"]:
        raise ValueError("row_map must contain 'matrix_b'")

    validate_row_map(data["row_map"]["matrix_b"])


def apply_defaults(data):
    """
    Fill missing parameter values from defaults.
    """
    default_value = data["defaults"].get("value", "1e-9")

    for name, resource in data["resources"].items():
        params = resource.setdefault("params", {})

        if name.startswith("CAP"):
            params.setdefault("value", default_value)

    return data


def build_internal_representation(data):
    row_lookup_b = {}
    for entry in data["row_map"]["matrix_b"]:
        row_lookup_b[entry["row"]] = {
            "resource": entry["resource"],
            "pin": entry["pin"]
        }

    routing_ir = {}
    all_connections = []
    connection_lookup = {}

    for block_name, block in data["routing"].items():
        routing_ir[block_name] = {
            "dimensions": block["dimensions"],
            "column_labels": block.get("column_labels", []),
            "C": [],
            "T": []
        }

        for kind in ["C", "T"]:
            for entry in block.get(kind, []):
                row = None if entry["row"] == "" else entry["row"]
                col = None if entry["col"] == "" else entry["col"]

                conn = {
                    "block": block_name,
                    "kind": kind,
                    "row": row,
                    "col": col,
                    "label": entry["label"],
                    "default": entry.get("default"),
                    "default_in+": entry.get("default_in+"),
                    "default_in-": entry.get("default_in-"),
                    "row_info": None
                }

                if block_name == "matrix_b" and row is not None:
                    conn["row_info"] = row_lookup_b.get(row)

                routing_ir[block_name][kind].append(conn)
                all_connections.append(conn)

                if row is not None and col is not None:
                    key = (block_name, kind, row, col)
                    if key in connection_lookup:
                        raise ValueError(f"Duplicate connection at {key}")
                    connection_lookup[key] = conn

    ir = {
        "metadata": data["metadata"],
        "defaults": data["defaults"],
        "resources": data["resources"],
        "io": data["io"],
        "routing": routing_ir,
        "row_lookup_b": row_lookup_b,
        "connections": all_connections,
        "connection_lookup": connection_lookup
    }

    return ir

def parse_design(json_path):
    """
    Full parser path for template
    """
    data = load_design_json(json_path)
    validate_design_json(data)
    data = apply_defaults(data)
    ir = build_internal_representation(data)
    return ir

def emit_matrix_b_connections(ir):
    """
    Emit resolved matrix_b connections in a normalized form.
    Returns:list[dict]
    """
    emitted = []

    for kind in ["C", "T"]:
        for conn in ir["routing"]["matrix_b"][kind]:
            if conn["row"] is None or conn["col"] is None:
                continue

            row_info = conn.get("row_info") or {}

            emitted.append({
                "block": "matrix_b",
                "kind": kind,
                "row": conn["row"],
                "col": conn["col"],
                "label": conn["label"],
                "resource": row_info.get("resource"),
                "pin": row_info.get("pin"),
                "default": conn.get("default"),
                "default_in+": conn.get("default_in+"),
                "default_in-": conn.get("default_in-")
            })

    return emitted
def emit_matrix_a_connections(ir):
    """
    Emit resolved matrix_a connections in a normalized form.
    Returns:list[dict]
    """
    emitted = []

    for kind in ["C", "T"]:
        for conn in ir["routing"]["matrix_a"][kind]:
            if conn["row"] is None or conn["col"] is None:
                continue

            emitted.append({
                "block": "matrix_a",
                "kind": kind,
                "row": conn["row"],
                "col": conn["col"],
                "label": conn["label"],
                "default": conn.get("default"),
                "default_in+": conn.get("default_in+"),
                "default_in-": conn.get("default_in-")
            })
    
    return emitted

def emit_io_definition(ir):
    """
    Emit logical macrocab input/output definition.
    """
    inputs = ir["io"].get("inputs", [])
    outputs = ir["io"].get("outputs", [])

    return {
        "inputs": inputs,
        "outputs": outputs,
        "num_inputs": len(inputs),
        "num_outputs": len(outputs)
    }

def emit_power_block_connections(ir):
    """
    Emit resolved power_block connections in a normalized form.

    Returns:
        list[dict]
    """
    emitted = []

    column_labels = ir["routing"]["power_block"].get("column_labels", [])

    for kind in ["C", "T"]:
        for conn in ir["routing"]["power_block"][kind]:
            if conn["row"] is None or conn["col"] is None:
                continue

            col_label = None
            if 0 <= conn["col"] < len(column_labels):
                col_label = column_labels[conn["col"]]

            emitted.append({
                "block": "power_block",
                "kind": kind,
                "row": conn["row"],
                "col": conn["col"],
                "column_label": col_label,
                "label": conn["label"],
                "default": conn.get("default"),
                "default_in+": conn.get("default_in+"),
                "default_in-": conn.get("default_in-")
            })

    return emitted

def emit_resource_parameters(ir):
    """
    Emit enabled resource parameters in a form similar to what the old
    create_mc_block() wanted: a flat parameter list plus structured resource info.

    Returns: dict with: enabled_resources, class_parameters
    """
    enabled_resources = []
    class_parameters = []

    for resource_name, resource_data in ir["resources"].items():
        if not resource_data.get("enabled", False):
            continue

        params = resource_data.get("params", {})

        enabled_resources.append({
            "resource": resource_name,
            "params": params
        })

        # flatten parameters into name/value pairs
        for param_name, param_value in params.items():
            class_parameters.append({
                "name": f"{resource_name}_{param_name}",
                "value": param_value
            })

    return {
        "enabled_resources": enabled_resources,
        "class_parameters": class_parameters
    }


def generate_macrocab_from_ir(ir, path_name, block_name, block_level):
    """
    Generate macrocab specification from parsed IR.

    Returns: dict
    """
    resource_emit = emit_resource_parameters(ir)
    power_emit = emit_power_block_connections(ir)
    matrix_a_emit = emit_matrix_a_connections(ir)
    matrix_b_emit = emit_matrix_b_connections(ir)

    all_connections = power_emit + matrix_a_emit + matrix_b_emit

    # flat parameter list
    class_parameters = list(resource_emit["class_parameters"])

    for idx, conn in enumerate(all_connections):
        base = f"{conn['block']}_{conn['kind']}_{idx}"

        class_parameters.append({
            "name": f"{base}_row",
            "value": conn["row"]
        })
        class_parameters.append({
            "name": f"{base}_col",
            "value": conn["col"]
        })
        class_parameters.append({
            "name": f"{base}_label",
            "value": conn["label"]
        })

        if conn.get("default") is not None:
            class_parameters.append({
                "name": f"{base}_default",
                "value": conn["default"]
            })
        if conn.get("default_in+") is not None:
            class_parameters.append({
                "name": f"{base}_default_in_plus",
                "value": conn["default_in+"]
            })
        if conn.get("default_in-") is not None:
            class_parameters.append({
                "name": f"{base}_default_in_minus",
                "value": conn["default_in-"]
            })

        if conn["block"] == "matrix_b":
            if conn.get("resource") is not None:
                class_parameters.append({
                    "name": f"{base}_resource",
                    "value": conn["resource"]
                })
            if conn.get("pin") is not None:
                class_parameters.append({
                    "name": f"{base}_pin",
                    "value": conn["pin"]
                })

        if conn["block"] == "power_block" and conn.get("column_label") is not None:
            class_parameters.append({
                "name": f"{base}_column_label",
                "value": conn["column_label"]
            })

    generated = {
        "metadata": ir["metadata"],
        "macrocab": {
            "path_name": path_name,
            "block_name": block_name,
            "block_level": block_level
        },
        "resources": resource_emit["enabled_resources"],
        "routing": {
            "power_block": power_emit,
            "matrix_a": matrix_a_emit,
            "matrix_b": matrix_b_emit
        },
        "class_parameters": class_parameters,
        "summary": {
            "num_enabled_resources": len(resource_emit["enabled_resources"]),
            "num_power_connections": len(power_emit),
            "num_matrix_a_connections": len(matrix_a_emit),
            "num_matrix_b_connections": len(matrix_b_emit),
            "num_total_connections": len(all_connections)
        }
    }

    return generated

   
def create_mc_block(json_path, path_name, block_name, block_level, class_lib_path="../class_lib.py"):
    """
    Creates macrocab class using new JSON parser / IR flow.

    json_path (str): path to user JSON template
    path_name (str): folder path to save macrocab
    block_name (str): macrocab name
    block_level (int): level of macrocab
    class_lib_path (str): file to append generated class into
    """
    verify_starting_parameters(path_name, block_name, block_level)

    ir = parse_design(json_path)
    generated = generate_macrocab_from_ir(ir, path_name, block_name, block_level)

    target_dir = os.path.join(ASHESPATH, path_name)
    target_json = os.path.join(target_dir, f"{block_name}.json")

    with open(target_json, "w") as f:
        json.dump(generated, f, indent=2)

    parameters = generated["class_parameters"]


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



def is_routing_exception(json):
    for matrix in json['routing'].values():
        if matrix == json['routing']['power_block']:
            continue
        for entry in matrix.get('C', []) + matrix.get('T', []):
            col = entry.get('col', '')
            if col != '' and int(col) < 15:
                return True
    return False

def edit_xml(xml_file, macrocab_name, macrocab_num_inputs, macrocab_num_outputs, delete, routing_exception):
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
        for tag in ('complete', 'direct'):
            for elem in interconnect.findall(tag):
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

        if routing_exception:
            cab_in = 'cab.I[0]' if macrocab_num_inputs == 1 else f'cab.I[{macrocab_num_inputs - 1}:0]'
            etree.SubElement(interconnect, 'direct', name='crossbar', input=cab_in, output=in_pins)
        else:
            etree.SubElement(interconnect, 'complete', name='crossbar', input='cab.I[12:0]', output=in_pins)

        # output line: macrocab output drives cab.O[4]
        if macrocab_num_outputs == 1:
            etree.SubElement(interconnect, 'complete', name='crossbar', input=f'{macrocab_name}[0].out[0]', output='cab.O[4]')
        else:
            cab_out_end = 4 - (macrocab_num_outputs - 1)
            etree.SubElement(interconnect, 'direct', name='crossbar', input=f'{macrocab_name}[0].out[{macrocab_num_outputs - 1}:0]', output=f'cab.O[4:{cab_out_end}]')

    etree.ElementTree(root).write(xml_file, pretty_print=True,xml_declaration=True,encoding='UTF-8')



def edit_rasp30(rasp30_file, macrocab_name, num_inputs, num_outputs, output_cols, input_rows, all_cells, delete):

    with open(rasp30_file, 'r') as file:
        lines = file.read()
    
    if f"{macrocab_name}" in lines and not delete:
        raise ValueError(f"{macrocab_name} already registered")
    
    out_pin = f"'{macrocab_name}[0].out[0]'" if num_outputs == 1 else \
              f"'{macrocab_name}[0].out[0:{num_outputs-1}]'"
    in_pin  = f"'{macrocab_name}[0].in[0]'"  if num_inputs  == 1 else \
              f"'{macrocab_name}[0].in[0:{num_inputs-1}]'"
    in_loc  = str(input_rows[0])  if num_inputs  == 1 else str(input_rows)
    out_loc = str(output_cols[0]) if num_outputs == 1 else str(output_cols) 

    if delete:

        lines = lines.replace(f",{out_pin}']", f"']")  # li_sm_0b
        lines = lines.replace(f",{in_pin}",    "")     # li_sm_1
        lines = lines.replace(f"+['{macrocab_name}']*1", "")  # dev_types
        lines = lines.replace(f",'{macrocab_name}_in':{num_inputs}", "")   # dev_pins
        lines = lines.replace(f",'{macrocab_name}_out':{num_outputs}}}", "}}")  # dev_pins

        lines = "\n".join(
            l for l in lines.splitlines()
            if macrocab_name not in l
        )
    else:

        old_dev_fgs = "'vmm_offc[0]',[0,0],"
        new_dev_fgs = f"{old_dev_fgs}\n'{macrocab_name}[0]',[0,0]"
        lines = lines.replace(old_dev_fgs, new_dev_fgs) # checked

        old_dev_fgs_2 = "self.dev_fgs ="
        new_dev_fgs_2 = f"'{macrocab_name}_ls[0]',[{all_cells[0]}"
        for cell in all_cells[1:]:
            new_dev_fgs_2 += f",{str(cell)}"
        lines = lines.replace(old_dev_fgs_2, new_dev_fgs_2+"\n"+old_dev_fgs_2)

        old_dev_pins_1 = "'vmm_offc_in':13,"
        lines = lines.replace(old_dev_pins_1, f"{old_dev_pins_1},'{macrocab_name}_in':{num_inputs},") # checked

        old_dev_pins_2 = "'vmm_offc_out':2"
        lines = lines.replace(old_dev_pins_2, f"{old_dev_pins_2},'{macrocab_name}_out':{num_outputs}}}") # checked

        old_dev_types = "+['vmm_offc']*1"
        lines = lines.replace(old_dev_types, f"{old_dev_types}+['{macrocab_name}']*1") # checked

        old_li_sm_in = "'vmm_offc[0].in[0:12]',[[6,7,8,9,10,11,12,13,14,15,16,17,27],0],"
        lines = lines.replace(old_li_sm_in, f"{old_li_sm_in}\n{in_pin},[{in_loc},0],")

        old_li_sm_out = "'vmm_offc[0].out[0:1]',[0,[17,18]],"
        lines = lines.replace(old_li_sm_out, f"{old_li_sm_out}\n{out_pin},[0,{out_loc}],")

        old_li_sm_0b = ",'vmm_offc[0].out[0:1]'"
        lines = lines.replace(old_li_sm_0b, f"{old_li_sm_0b},{out_pin}']") # checked

        old_li_sm_1 = "'vmm_offc[0].in[0:12]'"
        lines = lines.replace(old_li_sm_1, f"{old_li_sm_1},{in_pin}") #fgbias, pbias, etc? # checked

    with open(rasp30_file, 'w') as file:
        file.write(lines)

def edit_genswcs(genswcs_file, block_name, num_inputs, num_outputs, delete):
    with open(genswcs_file, 'r') as file:
        lines = file.read()

    if delete:
        lines = re.sub(
        rf"elif subckt in \['{re.escape(block_name)}'\]:\n\t\t\t\t\tkey = ports\[\d+\]\n",
        "",
        lines
    )
    else:
        
        old_if_subckt = "else\n\t\t\t\t\tkey = ports[2]"
        new_if_subckt = f"elif subckt in [{block_name}]:\n\t\t\t\t\tkey = ports[{num_inputs}]\n{old_if_subckt}"
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


if len(sys.argv) == 4:
    block_name = sys.argv[1]
    block_level = sys.argv[2]
    json_path = sys.argv[3]

    verify_starting_parameters(json_path, block_name, block_level)
    
    sys.exit(0)


if len(sys.argv) == 2:
    if sys.argv[1] == "make_macrocab":
        ir = parse_design(json_path)
        emits = emit_io_definition(ir)
        params = emit_resource_parameters(ir)

    elif sys.argv[1] == "delete_macrocab":
        # call delete macrocab function

        # function calls with false

        pass
    else:
        raise ValueError("Invalid command.")
else:
    raise ValueError("Commands: python3 macrocab_generation.py block_name block_level json_path \nOR python3 macrocab_generation.py make_macrocab \nOR python3 macrocab_generation.py delete_macrocab")






    