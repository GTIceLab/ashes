"""Class rendering and logical pin mapping adapted from the working NNopt generator."""
import re

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


def logical_pin_interface(pin_order, pin_meta, process_coordinates="xy", pin_map=None):
	"""Return logical API pins and their original native identifiers.

	An optional explicit map is {logical_pin_name: native_pin_name}.
	Unspecified pins use the configured native-to-logical side mapping.
	"""
	if process_coordinates not in ('xy', 'columns_y_rows_minus_x'):
		raise ValueError('Invalid process_coordinates')
	sides = {'W': 'N', 'E': 'S', 'N': 'E', 'S': 'W'}
	overrides = {native: logical for logical, native in (pin_map or {}).items()}
	if len(overrides) != len(pin_map or {}):
		raise ValueError('Each native pin must map to one logical pin')
	missing = set(overrides) - set(pin_order)
	if missing:
		raise ValueError(f'Pin map references missing native pins: {sorted(missing)}')
	logical_order, logical_meta, native_names = [], [], {}
	for native, direction, width in pin_meta:
		logical_side = sides[direction] if process_coordinates != 'xy' else direction
		logical = re.sub(r'_[nesw]$', '_' + logical_side.lower(), native) if process_coordinates != 'xy' else native
		if native in overrides:
			logical = overrides[native]
			match = re.search(r'_([nesw])$', logical)
			if not match:
				raise ValueError(f'Logical pin {logical} must end in _n, _e, _s, or _w')
			logical_side = match.group(1).upper()
		if logical in native_names:
			raise ValueError(f'Multiple native pins map to {logical}; provide an explicit pin map')
		logical_order.append(logical)
		logical_meta.append((logical, logical_side, width))
		native_names[logical] = native
	return logical_order, logical_meta, native_names


def render_class(class_name, pin_order, pin_meta, cell_dimension, native_names=None):
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
	lines.append("        self.size = [" + str(cell_dimension[0]) + "," + str(cell_dimension[1]) + "]")
	lines.append("")
	lines.append("        # Define cell information")
	lines.append(f"        self.name = '{class_name}'")

	for name, direction, width in pin_meta:
		axis = "0" if direction in ("W", "E") else "1"
		native = (native_names or {}).get(name, name)
		mapping_arg = f",native_name={native!r}" if native != name else ''
		lines.append(
			f"        self.{name} = Port(circuit,self,{name!r},{direction!r},{width}*self.dim[{axis}]{mapping_arg})"
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
