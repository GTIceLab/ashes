from __future__ import annotations
from .ir import Module
from pathlib import Path


def save_blif(blif_str: str, module_name: str, out_dir: str | Path):
    """Saves a provided BLIF string to the specified directory."""
    if isinstance(out_dir, str):
        out_dir = Path(out_dir)
    # Create the directory if it doesn't exist
    out_dir.mkdir(parents=True, exist_ok=True)

    blif_filepath = out_dir / f"{module_name}.blif"
    with open(blif_filepath, "w") as file:
        file.write(blif_str)


def emit_py_to_blif(top_module: Module, module_name: str = "DEFAULT") -> str:
    inputs = []
    outputs = []
    pad_comments = []
    subckts = []

    # Collect global supply nets (vcc, gnd) as inputs
    if "vcc" in top_module.nets:
        inputs.append("vcc")
    if "gnd" in top_module.nets:
        inputs.append("gnd")

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
            # Separate input and output ports, sort by name
            in_ports = sorted(
                [
                    (p_name, port)
                    for p_name, port in inst.ports.items()
                    if port.direction == "input" and port.net
                ],
                key=lambda x: x[0],
            )
            out_ports = sorted(
                [
                    (p_name, port)
                    for p_name, port in inst.ports.items()
                    if port.direction == "output" and port.net
                ],
                key=lambda x: x[0],
            )

            # Map ports
            port_mappings = []
            for idx, (p_name, port) in enumerate(in_ports):
                port_mappings.append(f"in[{idx}]={port.net.name}")
            for idx, (p_name, port) in enumerate(out_ports):
                port_mappings.append(f"out[{idx}]={port.net.name}")

            port_str = " ".join(port_mappings)

            # Build attrs string — skip fix_loc fields with value 0
            attr_str = ""
            if inst.attrs:
                attr_list = []
                for k, v in inst.attrs.items():
                    attr_list.append(f"{k} ={v}")
                attr_str = " #" + "&".join(attr_list)

            # Assemble subcircuit string
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

    # Adding trailing '\n' char so that VPR know when the BLIF file ends
    return "\n".join(lines) + "\n"
