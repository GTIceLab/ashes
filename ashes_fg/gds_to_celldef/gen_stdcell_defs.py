"""Compatibility entry point for generating one explicit GDS cell."""
import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from ashes_fg.gds_to_celldef import library as lib
    from ashes_fg.gds_to_celldef.cli import layer_spec, node
else:
    from . import library as lib
    from .cli import layer_spec, node


def orchestrate(gds_path, json_library_path, py_defs_path, process_node_override=None,
                foundry_override=None, process_coordinates='xy', pin_map=None,
                boundary=None, label_layers=None):
    if not process_node_override or not foundry_override:
        raise ValueError('Explicit process node and foundry are required; use ashes cells generate --help')
    gds_path = Path(gds_path)
    if not gds_path.is_file() or gds_path.suffix.lower() != '.gds':
        raise ValueError(f'Missing .gds input file: {gds_path}')
    json_library_path, py_defs_path = Path(json_library_path), Path(py_defs_path)
    if json_library_path.suffix != '.json' or py_defs_path.suffix != '.py':
        raise ValueError('Library outputs must have .json and .py extensions')
    if json_library_path.resolve() == gds_path.resolve() or py_defs_path.resolve() == gds_path.resolve():
        raise ValueError('Output files must not overwrite the GDS input')
    library = lib.gdstk.read_gds(str(gds_path), unit=1e-6)
    spec, text = lib.specification(library, gds_path.stem, node(str(process_node_override)),
                                  foundry_override, process_coordinates, boundary, label_layers, pin_map=pin_map)
    lib.commit_library([(gds_path.stem, spec, text)], json_library_path, py_defs_path)
    return json_library_path, py_defs_path


def main():
    parser = argparse.ArgumentParser(description='Generate one explicit GDS cell. For directory workflows use ashes cells --help.')
    parser.add_argument('gds_path', type=Path)
    parser.add_argument('-json', '--json', dest='json_path', type=Path, default=Path('cell_def/cells.json'))
    parser.add_argument('-pydef', '--pydef', dest='python_path', type=Path, default=Path('cell_def/cells.py'))
    parser.add_argument('-pn', '--process-node', required=True, type=node)
    parser.add_argument('-foundry', '--foundry', required=True)
    parser.add_argument('--process-coordinates', choices=lib.COORDINATES, default='xy')
    parser.add_argument('--pin-map', type=Path)
    parser.add_argument('--boundary-layer', type=layer_spec)
    parser.add_argument('--label-layer', type=layer_spec, action='append', default=[])
    args = parser.parse_args()
    try:
        if args.boundary_layer and args.boundary_layer[1] is None:
            raise ValueError('--boundary-layer requires LAYER:DATATYPE')
        pin_map = lib.load_object(args.pin_map).get(args.gds_path.stem)
        outputs = orchestrate(args.gds_path, args.json_path, args.python_path, args.process_node,
                              args.foundry, args.process_coordinates, pin_map, args.boundary_layer, args.label_layer)
    except (ValueError, OSError, SyntaxError, TypeError) as error:
        parser.error(str(error))
    print('Updated:', *outputs)


if __name__ == '__main__':
    main()
