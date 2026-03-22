from __future__ import annotations
from .ir import Module
from pathlib import Path


def save_blif(blif_str: str, module_name: str, out_dir: str|Path):
    """Saves a provided BLIF string to the specified directory."""
    if isinstance(out_dir, str):
        out_dir = Path(out_dir)
    # Create the directory if it doesn't exist
    out_dir.mkdir(parents=True, exist_ok=True)

    blif_filepath = out_dir / f"{module_name}.blif"
    with open(blif_filepath, "w") as file:
        file.write(blif_str)


def emit_py_to_blif(top_module: Module, module_name: str = "ors_buffer") -> str:
    inputs = []
    outputs = []
    pad_comments = []
    subckts = []

    # Iterate through all instances in the IR
    for inst_name, inst in top_module.instances.items():

        # Handle Input Pads
        if inst.model == "inpad":
            # Find the net driven by this pad
            out_port = inst.ports.get("out")
            if out_port and out_port.net:
                inputs.append(out_port.net.name)

            # Extract pad number
            pad_num = inst.attrs.get("pad_number", "?")
            if isinstance(pad_num, list):
                pad_num = pad_num[0]
            pad_comments.append(f"# {pad_num} pad_in")

        # Handle Output Pads
        elif inst.model in ("outpad", "outpada"):
            # Find the net driving this pad
            in_port = inst.ports.get("in")
            if in_port and in_port.net:
                outputs.append(in_port.net.name)

            # Extract pad number
            pad_num = inst.attrs.get("pad_number", "?")
            if isinstance(pad_num, list):
                pad_num = pad_num[0]
            pad_comments.append(f"# {pad_num} pad_out")

        # Handle Standard Primitives
        else:
            # 1. Map ports
            port_mappings = []
            for p_name, port in inst.ports.items():
                if port.net:
                    # Append [0] to match the FPAA backend's vector expectation
                    port_mappings.append(f"{p_name}[0]={port.net.name}")

            port_str = " ".join(port_mappings)

            # 2. Map attributes / location constraints
            attr_str = ""
            if inst.attrs:
                # Format: #param1 =value1&param2 =value2
                attr_list = [f"{k} ={v}" for k, v in inst.attrs.items()]
                attr_str = " #" + "&".join(attr_list)

            # 3. Assemble subcircuit string
            subckts.append(f"#{inst.model}")
            subckts.append(f".subckt {inst.model} {port_str}{attr_str}")

    # Assemble the final BLIF file
    lines = []
    lines.append(f".model {module_name}")
    lines.append(f".inputs {' '.join(inputs)}")
    lines.append(f".outputs {' '.join(outputs)}")
    lines.extend(pad_comments)
    lines.append("")
    lines.extend(subckts)
    lines.append("")
    lines.append(".end")

    # Currently only return string and not save to .blif file
    # Adding trailing '\n' char so that VPR know when the BLIF file ends
    return "\n".join(lines) + "\n"
