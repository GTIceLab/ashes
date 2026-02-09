import argparse
import os
from pathlib import Path

from ashes_fg.gds_to_celldef import gds2text
from ashes_fg.gds_to_celldef import text2json
from ashes_fg.gds_to_celldef import json2python


def gen_stdcell_defs(file_path: str, single_file: Path | None, per_class: bool) -> Path:
	# Step 1: GDS -> text output
	txt_path = gds2text.process_gds(file_path)

	# Step 2: text output -> directions JSON
	json_path = text2json.process_text_output(txt_path)

	# Step 3: directions JSON -> Python class
	class_name = json2python.extract_class_name(Path(json_path))
	if per_class:
		output_py = Path.cwd() / f"{class_name}.py"
		final_path = json2python.generate_from_json(Path(json_path), output_py, append=False)
	else:
		output_py = (single_file if single_file else (Path.cwd() / "standard_cells.py"))
		final_path = json2python.generate_from_json(Path(json_path), output_py, append=True)
	return final_path


def main():
	parser = argparse.ArgumentParser(description="End-to-end: GDS -> Python StandardCell")
	parser.add_argument("file", help="Path to source GDS file")
	parser.add_argument(
		"--single-file",
		dest="single_file",
		default="standard_cells.py",
		help="Append generated classes to this file (default: standard_cells.py). Use --per-class to generate separate files instead.",
	)
	parser.add_argument(
		"--per-class",
		action="store_true",
		help="Generate a separate .py per class instead of appending",
	)
	args = parser.parse_args()

	file = args.file
	if not os.path.exists(file):
		raise FileNotFoundError(f"File not found: {file}")

	single_file = Path(args.single_file) if args.single_file and not args.per_class else None
	final_py = gen_stdcell_defs(file, single_file, args.per_class)
	print(f"Generated Python cell(s) written to: {final_py}")


if __name__ == "__main__":
	main()
