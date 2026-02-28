import argparse
import json
import os
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
	sys.path.insert(0, str(SCRIPT_DIR))

import gds2text
import text2json
import json2python


def _load_json_dict_lenient(path: Path) -> dict:
	text = path.read_text(encoding="utf-8").strip()
	if not text:
		return {}

	try:
		data = json.loads(text)
		if not isinstance(data, dict):
			raise ValueError(f"JSON must be an object at top-level: {path}")
		return data
	except json.JSONDecodeError:
		pass

	decoder = json.JSONDecoder()
	idx = 0
	merged = {}
	while idx < len(text):
		while idx < len(text) and text[idx].isspace():
			idx += 1
		if idx >= len(text):
			break

		obj, end = decoder.raw_decode(text, idx)
		if not isinstance(obj, dict):
			raise ValueError(f"Found non-object JSON block in {path} near char {idx}")
		merged.update(obj)
		idx = end

	return merged


def merge_into_json_library(generated_json_path: Path, json_library_path: Path) -> Path:
	generated_data = _load_json_dict_lenient(generated_json_path)
	if not generated_data:
		raise ValueError(f"Generated JSON is empty: {generated_json_path}")

	if not json_library_path.exists():
		print(f"Warning: JSON library file not found, creating: {json_library_path}")
		json_library_path.parent.mkdir(parents=True, exist_ok=True)
		json_library_path.write_text("{}\n", encoding="utf-8")

	existing_data = _load_json_dict_lenient(json_library_path)
	existing_data.update(generated_data)
	json_library_path.write_text(json.dumps(existing_data, indent=2) + "\n", encoding="utf-8")
	return json_library_path


def ensure_py_defs_file(py_defs_path: Path) -> None:
	if not py_defs_path.exists():
		print(f"Warning: Python defs file not found, creating: {py_defs_path}")
		py_defs_path.parent.mkdir(parents=True, exist_ok=True)
		py_defs_path.write_text("", encoding="utf-8")


def orchestrate(
	gds_path: Path,
	json_library_path: Path,
	py_defs_path: Path,
	process_node_override: str | None = None,
	foundry_override: str | None = None,
) -> tuple[Path, Path]:
	txt_path: Path | None = None
	json_path: Path | None = None
	try:
		# Step 1: GDS -> text output
		txt_path = Path(gds2text.process_gds(str(gds_path)))

		# Step 2: text output -> directions JSON
		json_path = Path(
			text2json.process_text_output(
				str(txt_path),
				process_node_override=process_node_override,
				foundry_override=foundry_override,
			)
		)
		merged_json_lib = merge_into_json_library(json_path, json_library_path)

		# Step 3: directions JSON -> Python class
		ensure_py_defs_file(py_defs_path)
		history_dir = py_defs_path.parent / "cell_histories"
		final_py = json2python.generate_from_json(
			json_path,
			py_defs_path,
			append=True,
			history_dir=history_dir,
		)
		return merged_json_lib, final_py
	finally:
		protected_paths = {
			json_library_path.resolve(),
			py_defs_path.resolve(),
			gds_path.resolve(),
		}
		for intermediate in (json_path, txt_path):
			if intermediate is None:
				continue
			try:
				resolved = intermediate.resolve()
				if intermediate.exists() and resolved not in protected_paths:
					intermediate.unlink()
			except OSError as err:
				print(f"Warning: could not remove intermediate file {intermediate}: {err}")


def main():
	parser = argparse.ArgumentParser(description="End-to-end: GDS -> Python StandardCell")
	parser.add_argument("gds_path", help="Path to source GDS file")
	parser.add_argument("json_lib_path", help="Path to JSON library file to upsert generated cell definitions")
	parser.add_argument("py_defs_path", help="Path to Python file to upsert generated cell class definitions")
	parser.add_argument("-pn", "--process-node", dest="process_node", default=None, help="Override process node (e.g. 350 or 350nm)")
	parser.add_argument("-foundry", "--foundry", dest="foundry", default=None, help="Override foundry (e.g. TSMC)")
	args = parser.parse_args()

	gds_path = Path(args.gds_path)
	if not gds_path.exists():
		raise FileNotFoundError(f"File not found: {gds_path}")

	json_lib_path = Path(args.json_lib_path)
	py_defs_path = Path(args.py_defs_path)
	json_lib_written, final_py = orchestrate(
		gds_path,
		json_lib_path,
		py_defs_path,
		process_node_override=args.process_node,
		foundry_override=args.foundry,
	)
	print(f"JSON library updated: {json_lib_written}")
	print(f"Python definitions updated: {final_py}")


if __name__ == "__main__":
	main()
