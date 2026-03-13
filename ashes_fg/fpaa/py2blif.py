from ir import Module

def emit_blif(top_module: Module, module_name: str = "ors_buffer") -> str:
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
            if isinstance(pad_num, list): pad_num = pad_num[0]
            pad_comments.append(f"# {pad_num} pad_in")
            
        # Handle Output Pads
        elif inst.model in ("outpad", "outpada"):
            # Find the net driving this pad
            in_port = inst.ports.get("in")
            if in_port and in_port.net:
                outputs.append(in_port.net.name)
            
            # Extract pad number
            pad_num = inst.attrs.get("pad_number", "?")
            if isinstance(pad_num, list): pad_num = pad_num[0]
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
    return "\n".join(lines)