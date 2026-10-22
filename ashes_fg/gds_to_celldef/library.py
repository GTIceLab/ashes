"""Process-independent GDS handling, using the NNopt/Sky130 class renderer."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import json
import keyword
import logging
import os
from pathlib import Path
import re
import tempfile

import gdstk
from . import json2python

COORDINATES = ("xy", "columns_y_rows_minus_x")
HEADER = "from ashes_fg.asic.asic_compile import StandardCell, Port\n\n"
PIN = re.compile(r"^(.*?)(?:[<\[]([0-9]+)(?::([0-9]+))?[>\]])?$")
SIDES = re.compile(r"_([nesw])$", re.I)


def identifier(name, what):
    if not name.isidentifier() or keyword.iskeyword(name):
        raise ValueError(f"{what} {name!r} is not a Python identifier; correct the source or provide --pin-map for a logical pin")


def load_object(path):
    if path is None:
        return {}
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def files_in(directory, cells=None):
    if not directory.is_dir():
        raise ValueError(f"Missing GDS directory: {directory}. Run this command from your project's Tools/lib directory, or set the directory option.")
    files = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.gds')
    names = [p.stem for p in files]
    if len(names) != len(set(names)):
        raise ValueError(f"Duplicate GDS filename stems in {directory}")
    if cells:
        missing = set(cells) - set(names)
        if missing:
            raise ValueError(f"Cells not found in {directory}: {', '.join(sorted(missing))}")
        files = [p for p in files if p.stem in cells]
    if not files:
        raise ValueError(f"No .gds files in {directory}")
    return files


def source_directory(root, explicit=None):
    if explicit:
        return root / explicit
    candidates = [root / name for name in ('gds_source', 'gds_cadence') if (root / name).is_dir()]
    if len(candidates) > 1:
        raise ValueError("Both gds_source/ and gds_cadence/ exist; select one with --source-dir")
    if not candidates:
        raise ValueError(f"Missing gds_source/ (or legacy gds_cadence/) in {root}. Run from Tools/lib; export the original GDS there first.")
    return candidates[0]


def selected_cell(library, name):
    matches = [c for c in library.cells if c.name == name]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one GDS cell named {name!r}, matching the filename")
    return matches[0]


def bounds(cell, boundary=None):
    if boundary:
        layer, datatype = boundary
        polygons = [p for p in cell.polygons if (p.layer, p.datatype) == (layer, datatype)]
        if not polygons:
            raise ValueError(f"Cell {cell.name}: no top-cell boundary polygons on {layer}/{datatype}")
        boxes = [p.bounding_box() for p in polygons]
        box = ((min(b[0][0] for b in boxes), min(b[0][1] for b in boxes)),
               (max(b[1][0] for b in boxes), max(b[1][1] for b in boxes)))
    else:
        box = cell.bounding_box()
    if box is None or box[1][0] <= box[0][0] or box[1][1] <= box[0][1]:
        raise ValueError(f"Cell {cell.name}: missing or degenerate geometry")
    return box


def label_parts(text):
    match = PIN.fullmatch(text)
    if not match or not match[1]:
        raise ValueError(f"Invalid pin label {text!r}")
    base, a, b = match.groups()
    bits = None if a is None else set(range(min(int(a), int(b or a)), max(int(a), int(b or a)) + 1))
    return base, bits


def pin_side(label, box, overrides, cell_name="<unknown>", corner_layers=None, corner_distance=0.25):
    base, _ = label_parts(label.text)
    override = overrides.get(label.text, overrides.get(base))
    if override is not None:
        if not isinstance(override, str) or override.upper() not in ('N', 'S', 'E', 'W'):
            raise ValueError(f"Invalid direction override for {label.text!r}: {override!r}")
        return override.upper()
    suffix = SIDES.search(base)
    if suffix:
        return suffix[1].upper()
    (xmin, ymin), (xmax, ymax) = box
    x, y = label.origin
    distances = {'N': abs(ymax-y), 'S': abs(y-ymin), 'E': abs(xmax-x), 'W': abs(x-xmin)}
    if corner_layers:
        vertical, horizontal = corner_layers
        ns = min(('N', 'S'), key=distances.get)
        ew = min(('E', 'W'), key=distances.get)
        if distances[ns] < corner_distance and distances[ew] < corner_distance:
            if label.layer in vertical:
                return ns
            if label.layer in horizontal:
                return ew
    minimum = min(distances.values())
    closest = [side for side, value in distances.items() if abs(value-minimum) <= 1e-9]
    if len(closest) != 1:
        logging.getLogger(__name__).warning(
            "Cell %s: ambiguous side for pin %r at %s; tied sides %s; "
            "using %s (tie priority N, S, E, W). Set --direction-map to override.",
            cell_name, label.text, label.origin, ", ".join(closest), closest[0])
    return closest[0]


def labels_for(cell, label_layers):
    labels = [label for label in cell.labels if not label.text.startswith('&')
              and (not label_layers or any(label.layer == layer and (datatype is None or label.texttype == datatype)
                                          for layer, datatype in label_layers))]
    if not labels:
        raise ValueError(f"Cell {cell.name}: no selected top-cell pin labels")
    return labels


def prepare(library, name, boundary=None, label_layers=None, directions=None, corner_layers=None, corner_distance=0.25):
    cell = selected_cell(library, name)
    box = bounds(cell, boundary)
    for label in labels_for(cell, label_layers):
        base, bits = label_parts(label.text)
        side = pin_side(label, box, directions or {}, cell.name, corner_layers, corner_distance)
        if not SIDES.search(base):
            # Preserve the original bus notation and indices verbatim.
            label.text = base + '_' + side.lower() + label.text[len(base):]
    return library


def specification(library, name, process_node, foundry, coordinates='xy', boundary=None,
                  label_layers=None, directions=None, pin_map=None, corner_layers=None, corner_distance=0.25):
    identifier(name, 'Cell name')
    cell = selected_cell(library, name)
    box = bounds(cell, boundary)
    groups = {}
    for label in labels_for(cell, label_layers):
        base, bits = label_parts(label.text)
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_$]*', base):
            raise ValueError(f"Cell {name}: native label {base!r} is not a supported Verilog pin identifier. Review internal annotations or explicitly select pin-label layers; no labels were silently removed.")
        side = pin_side(label, box, directions or {}, name, corner_layers, corner_distance)
        if base in groups:
            old_side, old_bits = groups[base]
            if old_side != side or (old_bits is None) != (bits is None):
                raise ValueError(f"Cell {name}: conflicting labels for {base!r}; prepare directional GDS first")
            if bits is not None:
                old_bits.update(bits)
        else:
            groups[base] = (side, None if bits is None else set(bits))
    spec = {'type': 'ASIC', 'foundry': foundry, 'process_node': process_node.removesuffix('nm') + 'nm',
            **{side: [] for side in ('W', 'E', 'N', 'S')},
            'width': round(box[1][0]-box[0][0], 6), 'height': round(box[1][1]-box[0][1], 6)}
    for base, (side, bits) in groups.items():
        if bits is not None and bits != set(range(max(bits)+1)):
            logging.getLogger(__name__).warning(
                "Cell %s: bus %r is not contiguous and zero-based, got %s; "
                "continuing with %s declared bits. JSON preserves the source indices, "
                "but compiler ports use zero-based numbering; review before physical synthesis.",
                name, base, sorted(bits), len(bits))
        # Keep [0] for a physical one-bit indexed pin in metadata.
        if bits is None:
            labels = [base]
        elif bits == set(range(min(bits), max(bits)+1)):
            labels = [f'{base}[{min(bits)}:{max(bits)}]']
        else:
            labels = [f'{base}[{bit}:{bit}]' for bit in sorted(bits)]
        spec[side].extend(labels)
    order, meta = json2python.gather_pins(spec)
    order, meta, native = json2python.logical_pin_interface(order, meta, coordinates, pin_map)
    for logical in order:
        identifier(logical, f'Logical pin in {name}')
    text = json2python.render_class(name, order, meta, [spec['width'], spec['height']], native)
    ast.parse(text)
    spec['process_coordinates'] = coordinates
    spec['logical_to_native'] = native
    return spec, text


def library_outputs(generated, json_path, python_path):
    data = load_object(json_path) if json_path.exists() else {}
    text = python_path.read_text() if python_path.exists() else HEADER
    ast.parse(text, filename=str(python_path))
    text = re.sub(r'^from ashes_fg[.]asic[.]model[.]asic_compile import ',
                  'from ashes_fg.asic.asic_compile import ', text, flags=re.M)
    if 'from ashes_fg.asic.asic_compile import' not in text and 'from ashes_fg.asic.model.asic_compile import' not in text:
        text = HEADER + text
    histories = []
    for name, spec, class_text in generated:
        previous = json2python.extract_existing_class_text(text, name)
        if previous and previous.strip() != class_text.strip():
            histories.append((name, previous))
        data[name] = spec
        text = json2python.upsert_class_text(text, name, class_text)
    ast.parse(text, filename=str(python_path))
    return json.dumps(data, indent=2) + '\n', text, histories


def write_outputs(contents):
    """Stage every output before replacements; roll back if a replacement fails."""
    originals = {Path(path): Path(path).read_bytes() if Path(path).exists() else None for path in contents}
    staged, replaced = {}, []
    try:
        for path, content in contents.items():
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
                staged[path] = Path(stream.name)
                stream.write(content)
        for path, temp in staged.items():
            os.replace(temp, path)
            replaced.append(path)
    except Exception:
        for path in replaced:
            if originals[path] is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(originals[path])
        raise
    finally:
        for temp in staged.values():
            temp.unlink(missing_ok=True)


def commit_library(generated, json_path, python_path, extra=None):
    json_text, python_text, histories = library_outputs(generated, json_path, python_path)
    contents = {json_path: json_text.encode(), python_path: python_text.encode(), **(extra or {})}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name, text in histories:
        contents[python_path.parent / 'cell_histories' / f'{name}.{stamp}.py.txt'] = text.encode()
    write_outputs(contents)
