# class TSMC350nm_C4(StandardCell):
# 	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,VREF=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

# 		# Define variables
# 		self.circuit = circuit
# 		self.pins = []
# 		self.ports = []
import argparse
import json
from pathlib import Path


DIR_ORDER = ("W", "E", "N", "S")


def parse_pin(pin):
	if "[" in pin and "]" in pin:
		base, idx = pin.split("[", 1)
		idx = idx.rstrip("]")
		if ":" in idx:
			left, right = idx.split(":", 1)
			width = abs(int(left) - int(right)) + 1
		else:
			width = 1
		return base, width
	return pin, 1


def extract_class_name(json_path):
	stem = json_path.stem
	suffix = "_output_directions"
	if stem.endswith(suffix):
		return stem[: -len(suffix)]
	return stem


def load_spec(json_path):
	data = json.loads(json_path.read_text())
	if not data:
		raise ValueError("JSON is empty")
	top_key = next(iter(data.keys()))
	return data[top_key]


def gather_pins(spec):
	ordered_pins = []
	pin_meta = []
	seen = set()
	for direction in DIR_ORDER:
		for pin in spec.get(direction, []):
			name, width = parse_pin(pin)
			if name in seen:
				continue
			seen.add(name)
			ordered_pins.append(name)
			pin_meta.append((name, direction, width))
	return ordered_pins, pin_meta


def render_class(class_name, pin_order, pin_meta):
	args = ["self", "circuit", "island=None", "dim=(1,1)"]
	args.extend(f"{pin}=None" for pin in pin_order)
	args_str = ",".join(args)

	lines = []
	lines.append(f"class {class_name}(StandardCell):")
	lines.append(f"    def __init__({args_str}):")
	lines.append("        # Define variables")
	lines.append("        self.circuit = circuit")
	lines.append("        self.pins = []")
	lines.append("        self.ports = []")
	lines.append("        self.island = island")
	lines.append("        self.dim = dim")
	lines.append("")
	lines.append("        # Define cell information")
	lines.append(f"        self.name = '{class_name}'")

	for name, direction, width in pin_meta:
		axis = "0" if direction in ("W", "E") else "1"
		lines.append(
			f"        self.{name} = Port(circuit,self,'{name}','{direction}',{width}*self.dim[{axis}])"
		)

	lines.append("")
	lines.append("        # Initialize ports with given values")
	ports_init = ",".join(pin_order)
	lines.append(f"        portsInit = [{ports_init}]")
	lines.append("        i=0")
	lines.append("        for p in self.ports:")
	lines.append("            self.assignPort(p,portsInit[i])")
	lines.append("            i+=1")
	lines.append("")
	lines.append("        # Add cell to circuit")
	lines.append("        circuit.addInstance(self,self.island)")

	return "\n".join(lines) + "\n"


def generate_from_json(json_path: Path, output_path: Path | None = None, append: bool = False) -> Path:
	spec = load_spec(json_path)
	class_name = extract_class_name(json_path)
	pin_order, pin_meta = gather_pins(spec)
	class_text = render_class(class_name, pin_order, pin_meta)

	if output_path is None:
		output_path = json_path.with_name(f"{class_name}.py")

	if append:
		prefix = ""
		if output_path.exists() and output_path.stat().st_size > 0:
			prefix = "\n\n"
		with open(output_path, "a", encoding="utf-8") as f:
			f.write(prefix + class_text)
	else:
		output_path.write_text(class_text, encoding="utf-8")
	return output_path


def main():
	parser = argparse.ArgumentParser(description="Generate StandardCell classes from JSON.")
	parser.add_argument("json_path", help="Path to *_output_directions.json")
	parser.add_argument(
		"--out",
		dest="output_path",
		default=None,
		help="Output .py path (default: sibling file based on json name)",
	)
	args = parser.parse_args()

	json_path = Path(args.json_path)
	if not json_path.exists():
		raise FileNotFoundError(json_path)

	output_path = Path(args.output_path) if args.output_path else None
	generate_from_json(json_path, output_path)


if __name__ == "__main__":
	main()
#     file_content = f"""
# class {json_file}(StandardCell):
#         def __init__(self,circuit,island=None,): 
#             # Define variables
#             self.circuit = circuit
#             self.pins = []
#             self.ports = []
#             self.island = island
#             self.dim = dim

#             # Define cell information
#             #self.name = 'filename' """ 

#     for key in 
#     for values in key,
#         if direction 'W' or 'E' then the pin dim[0]
#             #append \n to file_content
#             file_content.append("self.{PIN_NAME} = Port(circuit,self,'{PIN_NAME}','{PIN_DIRECTION}',{Max_Wire}*self.dim[0])")
#         else 'N' or "S"
#             #append \n to file_content
#             write self.{PIN_NAME} = Port(circuit,self,'{PIN_NAME}','{PIN_DIRECTION}',{Max_Wire}*self.dim[1])
#         #add Pin to PINLIST

#             file_content_2 = f"""
#             Initialize ports with given values
#             portsInit = {PIN_LIST}
#             i=0
# 		    for p in self.ports:
# 			    self.assignPort(p,portsInit[i])
# 			    i+=1

# 		    # Add cell to circuit
# 		    circuit.addInstance(self,self.island)
#             """
            