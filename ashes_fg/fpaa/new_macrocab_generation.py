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


#######
# Parser for new JSON (merge with create_mc block after):
#######

def load_design_json(json_path):
    """
    Loads macrocab JSON file
    """
    with open(json_path, "r") as f:
        return json.load(f)

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
    required_top_keys = ["metadata", "defaults", "resources", "routing", "row_map"]
    for key in required_top_keys:
        if key not in data:
            raise ValueError(f"Missing top-level key: {key}")

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

        validate_connection_list(block.get("C", []), dims[0], dims[1], f"{block_name}.C")
        validate_connection_list(block.get("T", []), dims[0], dims[1], f"{block_name}.T")

    if "matrix_b" not in data["row_map"]:
        raise ValueError("row_map must contain 'matrix_b'")

    validate_row_map(data["row_map"]["matrix_b"])


# def apply_defaults(data):
#     """
#     Fill missing parameter values from defaults.
#     """
#     default_value = data["defaults"].get("value", "1e-9")

#     for name, resource in data["resources"].items():
#         params = resource.setdefault("params", {})

#         if name.startswith("CAP"):
#             params.setdefault("value", default_value)

#     return data


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

