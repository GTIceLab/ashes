# class TSMC350nm_C4(StandardCell):
# 	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,VREF=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

# 		# Define variables
# 		self.circuit = circuit
# 		self.pins = []
# 		self.ports = []
import argparse
import json
from pathlib import Path
import re
from datetime import datetime, timezone


DIR_ORDER = ("W", "E", "N", "S")


def parse_pin(pin):
	if "[" in pin and "]" in pin:
		base, idx = pin.split("[", 1)
		idx = idx.rstrip("]")
		if ":" in idx:
			left, right = idx.split(":", 1)
			lo, hi = sorted((int(left), int(right)))
			return base, set(range(lo, hi + 1))
		else:
			return base, {int(idx)}
	return pin, None


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
	seen = {}
	for direction in DIR_ORDER:
		for pin in spec.get(direction, []):
			name, bits = parse_pin(pin)
			if name not in seen:
				ordered_pins.append(name)
				seen[name] = {"direction": direction, "bits": set() if bits is not None else None}

			if bits is not None:
				if seen[name]["bits"] is None:
					seen[name]["bits"] = set()
				seen[name]["bits"].update(bits)

	pin_meta = []
	for name in ordered_pins:
		bits = seen[name]["bits"]
		width = len(bits) if bits else 1
		pin_meta.append((name, seen[name]["direction"], width))
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


def upsert_class_text(existing_text: str, class_name: str, class_text: str) -> str:
	class_header = f"class {class_name}(StandardCell):"
	start = existing_text.find(class_header)
	if start == -1:
		if existing_text and not existing_text.endswith("\n"):
			existing_text += "\n"
		prefix = "\n" if existing_text.strip() else ""
		return existing_text + prefix + class_text

	next_class_match = re.search(r"^class\s+\w+\(StandardCell\):", existing_text[start + len(class_header):], re.MULTILINE)
	if next_class_match:
		end = start + len(class_header) + next_class_match.start()
	else:
		end = len(existing_text)

	before = existing_text[:start].rstrip()
	after = existing_text[end:].lstrip()

	parts = []
	if before:
		parts.append(before)
	parts.append(class_text.rstrip())
	if after:
		parts.append(after)

	return "\n\n".join(parts) + "\n"


def extract_existing_class_text(existing_text: str, class_name: str) -> str | None:
	class_header = f"class {class_name}(StandardCell):"
	start = existing_text.find(class_header)
	if start == -1:
		return None

	next_class_match = re.search(r"^class\s+\w+\(StandardCell\):", existing_text[start + len(class_header):], re.MULTILINE)
	if next_class_match:
		end = start + len(class_header) + next_class_match.start()
	else:
		end = len(existing_text)

	return existing_text[start:end].strip() + "\n"


def append_history(history_path: Path, class_name: str, previous_text: str) -> None:
	timestamp = datetime.now(timezone.utc).isoformat()
	entry = (
		f"===== {class_name} overwrite @ {timestamp} =====\n"
		f"{previous_text.rstrip()}\n"
		"===== end =====\n\n"
	)
	with open(history_path, "a", encoding="utf-8") as history_file:
		history_file.write(entry)


ASHES_IMPORT = "from ashes_fg.asic.asic_compile import *"
def ensure_import(content: str) -> str:
    """Ensure the required import is at the top of the file."""
    if ASHES_IMPORT not in content:
        return ASHES_IMPORT + "\n\n" + content
    return content


def generate_from_json(
	json_path: Path,
	output_path: Path | None = None,
	append: bool = False,
	history_dir: Path | None = None,
) -> Path:
	spec = load_spec(json_path)
	class_name = extract_class_name(json_path)
	pin_order, pin_meta = gather_pins(spec)
	class_text = render_class(class_name, pin_order, pin_meta)
	if history_dir is None:
		history_path = json_path.with_name(f"{class_name}_history.txt")
	else:
		history_dir.mkdir(parents=True, exist_ok=True)
		history_path = history_dir / f"{class_name}_history.txt"

	if output_path is None:
		output_path = json_path.with_name(f"{class_name}.py")

	if append:
		if output_path.exists():
			existing_text = output_path.read_text(encoding="utf-8")
			previous_class_text = extract_existing_class_text(existing_text, class_name)
			if previous_class_text is not None and previous_class_text.strip() != class_text.strip():
				append_history(history_path, class_name, previous_class_text)
			updated_text = upsert_class_text(existing_text, class_name, class_text)
			updated_text = ensure_import(updated_text)
			output_path.write_text(updated_text, encoding="utf-8")
		else:
			class_text = ensure_import(class_text)
			output_path.write_text(class_text, encoding="utf-8")
	else:
		if output_path.exists():
			existing_text = output_path.read_text(encoding="utf-8")
			if existing_text.strip() != class_text.strip():
				append_history(history_path, class_name, existing_text)
		class_text = ensure_import(class_text)
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
            