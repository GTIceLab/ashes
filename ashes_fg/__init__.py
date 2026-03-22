# Expose internal modules for external use
from . import fpaa
from . import asic
from . import class_lib


import json
import os
import sys


def update_class_lib(json_file="cells.json", library="class_lib.py"):
    # Open the JSON file and load the data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Helper function for sanitizing the field name from cells.json
    def sanitize(field_name: str):
        return (
            field_name.strip()
            .lower()
            .replace(" ", "_")
            .replace("[", "_")
            .replace("]", "")
        )

    # Open the Python library file for writing
    with open(library, "w") as t:
        # Add necessary imports
        t.write("from ir import Module, Instance, Port, Net\n\n")

        # Base ASIC class
        t.write(
            "class std_cell:\n"
            "\tdef __init__(self, input, num_instances, cell_type):\n"
            "\t\tself.input = input\n"
            "\t\tself.num_instances = num_instances\n"
            "\t\tself.cell_type = cell_type\n\n"
        )

        # IO Pads
        t.write(
            "class inpad:\n"
            "\tdef __init__(self, pad_number):\n"
            "\t\tself.pad_number = pad_number\n\n"
            "\tdef build(self, top: Module) -> Net:\n"
            '\t\tinst = Instance(name=self.name, model="inpad")\n'
            '\t\tinst.attrs = {"pad_number": self.pad_number}\n'
            "\t\ttop.instances[inst.name] = inst\n"
            '\t\tout_port = Port(name="out", direction="output", owner=inst)\n'
            '\t\tinst.ports["out"] = out_port\n'
            "\t\tout_net = Net(name=f'net_{inst.name}', driver=out_port)\n"
            "\t\tout_port.net = out_net\n"
            "\t\ttop.nets[out_net.name] = out_net\n"
            "\t\treturn out_net\n\n"
        )
        t.write(
            "class outpad:\n"
            "\tdef __init__(self,input, pad_number):\n"
            "\t\tself.input=input\n"
            "\t\tself.pad_number = pad_number\n\n"
            "\tdef build(self, top: Module):\n"
            '\t\tinst = Instance(name=self.name, model="outpad")\n'
            '\t\tinst.attrs = {"pad_number": self.pad_number}\n'
            "\t\ttop.instances[inst.name] = inst\n"
            '\t\tin_port = Port(name="in", direction="output", owner=inst, net=self.input)\n'
            '\t\tinst.ports["in"] = in_port\n'
            "\t\tself.input.sinks.append(in_port)\n\n"
        )
        t.write(
            "class outpada:\n"
            "\tdef __init__(self,input, pad_number, fix_loc=[0, 0, 0]):\n"
            "\t\tself.input=input\n"
            "\t\tself.pad_number = pad_number\n"
            "\t\tself.fix_loc_enabled = fix_loc[0]\n"
            "\t\tself.fix_loc_x = fix_loc[1]\n"
            "\t\tself.fix_loc_y = fix_loc[2]\n\n"
        )

        # General blocks
        for block in data:
            if data[block]["type"] == "ASIC":
                t.write(f"class {block}(std_cell):\n" "\tpass\n\n")
            elif block == "dc_in":
                t.write(
                    "class dc_in:\n"
                    "\tdef __init__(self, DC_value, fix_loc=[0, 0, 0]):\n"
                    "\t\tself.DC_value = DC_value\n"
                    "\t\tself.fix_loc_enabled = fix_loc[0]"
                    "\t\tself.fix_loc_x = fix_loc[1]"
                    "\t\tself.fix_loc_y = fix_loc[2]\n\n"
                )
            elif block == "gnd":
                t.write("class gnd:\n" "\tdef __init__(self):\n" "\t\tpass\n\n")
            elif block == "vdd":
                t.write("class vdd:\n" "\tdef __init__(self):\n" "\t\tpass\n\n")
            elif block == "GENARB_f":
                t.write(
                    "class GENARB_f:\n"
                    "\tdef __init__(self,input):\n"
                    "\t\tself.input=input\n"
                    "\n"
                )
            elif block == "meas_volt":
                t.write(
                    "class meas_volt:\n"
                    "\tdef __init__(self,input):\n"
                    "\t\tself.input=input\n\n"
                )
            elif block == "gpio_in":
                t.write("class gpio_in:\n" "\tdef __init__(self):\n" "\t\tpass\n\n")
            elif "?" not in block:
                t.write(f"class {block}:\n")

                # Generate __init__() function
                t.write("\tdef __init__(self, input, num_instances='1'")
                for key, value in data[block].items():
                    field_name = sanitize(str(key))
                    if type(value) != list:
                        t.write(f", {field_name}='{str(value)}'")
                    else:
                        t.write(f", {field_name} ={str(value)}")

                # Add field for fix location down the line
                t.write(", fix_loc=[0, 0, 0]")

                t.write("):\n")
                t.write("\t\tself.input=input\n")
                t.write("\t\tself.num_instances=num_instances\n")

                tracked_attrs = []

                for key, value in data[block].items():
                    if (
                        "type" not in key
                        and "board" not in key
                        and "foundry" not in key
                        and "process_node" not in key
                    ):
                        field_name = sanitize(str(key))
                        t.write(f"\t\tself.{field_name} = {field_name}\n")
                        tracked_attrs.append(field_name)
                t.write(
                    "\t\tself.fix_loc_enabled = fix_loc[0]\n"
                    "\t\tself.fix_loc_x = fix_loc[1]\n"
                    "\t\tself.fix_loc_y = fix_loc[2]\n"
                )
                # Add unique self.name using instance ID
                t.write(f'\t\tself.name = f"{block}_{{id(self)}}"\n\n')

                # Generate __build__()
                if data[block]["type"] == "FPAA":
                    t.write("\tdef build(self, top: Module):\n")
                    t.write(f'\t\tinst = Instance(name=self.name, model="{block}")\n')
                    t.write("\t\tinst.attrs = {\n")
                    for attr in tracked_attrs:
                        t.write(f'\t\t\t"{attr}": self.{attr},\n')
                    t.write("\t\t}\n")
                    t.write(
                        "\t\ttop.instances[inst.name] = inst\n"
                        '\t\tin_port = Port(name="in", direction="input", owner=inst, net=self.input)\n'
                        "\t\tinst.ports[in_port.name] = in_port\n"
                        "\t\tself.input.sinks.append(in_port)\n"
                        '\t\tout_port = Port(name="out", direction="output", owner=inst)\n'
                        "\t\tinst.ports[out_port.name] = out_port\n"
                        "\t\tout_net = Net(name=f'net_{inst.name}_out', driver=out_port)\n"
                        "\t\tout_port.net = out_net\n"
                        "\t\ttop.nets[out_net.name] = out_net\n"
                        "\t\treturn out_net\n\n"
                    )


if __name__ == "__main__":
    update_class_lib(json_file="cells.json", library="test_class_lib.py")
