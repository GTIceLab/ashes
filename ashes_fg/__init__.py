# Expose internal modules for external use
# from . import fpaa
# from . import asic
# from . import class_lib
# from . import test_class_lib

import json


META_KEYS = {"type", "board", "foundry", "process_node", "num_inputs", "num_outputs"}


def update_class_lib(json_file="cells.json", library="class_lib.py"):
    # Open the JSON file and load the data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Helper function for sanitizing the field name from cells.json
    def sanitize(field_name: str):
        clean_field =  field_name.strip().replace(" ", "_").replace("[", "_").replace("]", "")
        return clean_field

    # Open the Python library file for writing
    with open(library, "w") as t:
        # Add necessary imports
        t.write("from ashes_fg.fpaa.ir import Module, Instance, Port, Net\n")
        t.write("import math\n\n")

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
            "\t\tself.pad_number = pad_number\n"
            '\t\tself.name = f"inpad_{pad_number}"\n\n'
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
            "\t\tself.pad_number = pad_number\n"
            '\t\tself.name = f"outpad_{pad_number}"\n\n'
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
            "\t\tself.fix_loc_y = fix_loc[2]\n"
            '\t\tself.name = f"outpada_{pad_number}"\n\n'
        )

        # General blocks
        for block in data:
            num_inputs = data[block].get(
                "num_inputs", 1
            )  # retrieves num inputs, default = 1
            num_outputs = data[block].get(
                "num_outputs", 1
            )  # retrieves numb outputs, default = 1

            if data[block]["type"] == "ASIC":
                t.write(f"class {block}(std_cell):\n" "\tpass\n\n")
            elif block == "dc_in":
                t.write(
                    "class dc_in:\n"
                    "\tdef __init__(self, DC_value, fix_loc=[0, 0, 0]):\n"
                    "\t\tself.DC_value = DC_value\n"
                    "\t\tself.fix_loc_enabled = fix_loc[0]\n"
                    "\t\tself.fix_loc_x = fix_loc[1]\n"
                    "\t\tself.fix_loc_y = fix_loc[2]\n"
                    '\t\tself.name = f"dc_in_{id(self)}"\n\n'
                    "\tdef _voltage_to_n_bias(self, voltage):\n"
                    "\t\tn_bias_ln = 1.658236340989905 * voltage - 16.781129443839024\n"
                    "\t\tn_bias = round(math.exp(n_bias_ln), 10)\n"
                    "\t\treturn n_bias\n\n"
                    "\tdef build(self, top: Module) -> Net:\n"
                    '\t\tif "vcc" in top.nets:\n'
                    '\t\t\tvcc_net = top.nets["vcc"]\n'
                    "\t\telse:\n"
                    '\t\t\tvcc_net = Net(name="vcc", driver=None)\n'
                    '\t\t\ttop.nets["vcc"] = vcc_net\n'
                    "\t\tn_bias = self._voltage_to_n_bias(self.DC_value)\n"
                    '\t\tinst = Instance(name=self.name, model="fgota")\n'
                    '\t\tinst.attrs = {"fgota_bias": 2e-06, "fgota_p_bias": 2e-06, "fgota_n_bias": n_bias, "fgota_small_cap": 0, "fix_loc_enabled": self.fix_loc_enabled, "fix_loc_x": self.fix_loc_x, "fix_loc_y": self.fix_loc_y}\n'
                    "\t\ttop.instances[inst.name] = inst\n"
                    '\t\tout_port = Port(name="out", direction="output", owner=inst)\n'
                    '\t\tinst.ports["out"] = out_port\n'
                    '\t\tout_net = Net(name=f"net_{inst.name}_out", driver=out_port)\n'
                    "\t\tout_port.net = out_net\n"
                    "\t\ttop.nets[out_net.name] = out_net\n"
                    '\t\tin0_port = Port(name="in_0", direction="input", owner=inst, net=vcc_net)\n'
                    '\t\tinst.ports["in_0"] = in0_port\n'
                    "\t\tvcc_net.sinks.append(in0_port)\n"
                    '\t\tin1_port = Port(name="in_1", direction="input", owner=inst, net=out_net)\n'
                    '\t\tinst.ports["in_1"] = in1_port\n'
                    "\t\tout_net.sinks.append(in1_port)\n"
                    "\t\treturn out_net\n\n"
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
                    if key not in META_KEYS:
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
                    t.write('\t\t\t"fix_loc_enabled": self.fix_loc_enabled,\n')
                    t.write('\t\t\t"fix_loc_x": self.fix_loc_x,\n')
                    t.write('\t\t\t"fix_loc_y": self.fix_loc_y,\n')
                    t.write("\t\t}\n")
                    t.write("\t\ttop.instances[inst.name] = inst\n")

                    # --- Input ports: branch on num_inputs ---
                    if num_inputs == 1:
                        t.write(
                            '\t\tin_port = Port(name="in0", direction="input", '
                            "owner=inst, net=self.input)\n"
                        )
                        t.write("\t\tinst.ports[in_port.name] = in_port\n")
                        t.write("\t\tself.input.sinks.append(in_port)\n")
                    else:
                        t.write(
                            "\t\tinput_nets = self.input if isinstance("
                            "self.input, list) else [self.input]\n"
                        )
                        t.write(f"\t\tfor idx, net in enumerate(input_nets):\n")
                        t.write(f'\t\t\tport_name = f"in{{idx}}"\n')
                        t.write(
                            '\t\t\tin_port = Port(name=port_name, direction="input", '
                            "owner=inst, net=net)\n"
                        )
                        t.write("\t\t\tinst.ports[port_name] = in_port\n")
                        t.write("\t\t\tnet.sinks.append(in_port)\n")

                    # --- Output ports: branch on num_outputs ---
                    if num_outputs == 1:
                        t.write(
                            '\t\tout_port = Port(name="out", direction="output", '
                            "owner=inst)\n"
                        )
                        t.write("\t\tinst.ports[out_port.name] = out_port\n")
                        t.write(
                            "\t\tout_net = Net(name=f'net_{inst.name}_out', "
                            "driver=out_port)\n"
                        )
                        t.write("\t\tout_port.net = out_net\n")
                        t.write("\t\ttop.nets[out_net.name] = out_net\n")
                        t.write("\t\treturn out_net\n\n")
                    else:
                        t.write("\t\tout_nets = []\n")
                        t.write(f"\t\tfor idx in range({num_outputs}):\n")
                        t.write(f'\t\t\tport_name = f"out{{idx}}"\n')
                        t.write(
                            "\t\t\tout_port = Port(name=port_name, "
                            'direction="output", owner=inst)\n'
                        )
                        t.write("\t\t\tinst.ports[port_name] = out_port\n")
                        t.write(
                            "\t\t\tout_net = Net(name=f'net_{inst.name}_out{idx}', "
                            "driver=out_port)\n"
                        )
                        t.write("\t\t\tout_port.net = out_net\n")
                        t.write("\t\t\ttop.nets[out_net.name] = out_net\n")
                        t.write("\t\t\tout_nets.append(out_net)\n")
                        t.write("\t\treturn out_nets\n\n")


if __name__ == "__main__":
    update_class_lib(json_file="cells.json", library="test_class_lib.py")
