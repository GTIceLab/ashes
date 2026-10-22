"""Project-local `ashes cells` commands; no installed-package output files."""
import argparse
import io
import logging
import tempfile
from pathlib import Path
import re

from . import library as lib


def layer_spec(value):
    try:
        parts = value.split(':')
        if len(parts) not in (1, 2):
            raise ValueError
        layer = int(parts[0])
        datatype = int(parts[1]) if len(parts) == 2 else None
        if layer < 0 or (datatype is not None and datatype < 0):
            raise ValueError
        return layer, datatype
    except ValueError:
        raise argparse.ArgumentTypeError('Use nonnegative LAYER or LAYER:DATATYPE')


def node(value):
    value = value.strip()
    if not re.fullmatch(r'[0-9]+(?:[.][0-9]+)?(?:nm)?', value, re.I):
        raise argparse.ArgumentTypeError('Use a process node such as 130, 16, or 180nm')
    return re.sub('nm$', '', value, flags=re.I)


def add_arguments(parser, action):
    parser.add_argument('--cells', nargs='+', metavar='CELL', help='Select filename stems; default: every GDS cell (errors are never skipped)')
    parser.add_argument('--gds-dir', type=Path, default=Path('gds'), help='Prepared GDS directory relative to current Tools/lib (default: gds)')
    if action in ('prepare', 'build'):
        parser.add_argument('--source-dir', type=Path, help='Original editor GDS (default: gds_source, with legacy gds_cadence fallback)')
    if action in ('generate', 'build'):
        parser.add_argument('--output-dir', type=Path, default=Path('cell_def'), help='Python/JSON library directory (default: cell_def)')
        parser.add_argument('--process-node', '-pn', required=True, type=node, help='Process metadata, e.g. 130 or 16; never inferred from filenames')
        parser.add_argument('--foundry', '-foundry', required=True, help='Foundry identifier; no process-specific default')
        parser.add_argument('--process-coordinates', required=True, choices=lib.COORDINATES, help='Logical pin interface; geometry remains native')
        parser.add_argument('--pin-map', type=Path, help='JSON object: cell -> {logical_pin: existing_native_pin}')
    parser.add_argument('--boundary-layer', type=layer_spec, help='Optional top-cell boundary LAYER:DATATYPE; default: named-cell bounding box')
    parser.add_argument('--label-layer', type=layer_spec, action='append', default=[], help='Explicit pin-label LAYER[:TEXTTYPE]; repeat to select layers (default: all top-cell labels except & markers)')
    parser.add_argument('--vertical-pin-layers', nargs='+', type=int, default=[], help='Pin-label layers routed vertically near corners; choose N/S')
    parser.add_argument('--horizontal-pin-layers', nargs='+', type=int, default=[], help='Pin-label layers routed horizontally near corners; choose E/W')
    parser.add_argument('--corner-distance', type=float, default=0.25, help='Corner proximity in microns for layer-aware inference (default: 0.25)')
    parser.add_argument('--direction-map', type=Path, help='JSON object: cell -> {label_or_base: N|S|E|W}; overrides ambiguous sides (otherwise warns and uses N/S/E/W tie priority)')
    return parser


def add_parser(subparsers):
    parser = subparsers.add_parser('cells', help='Prepare a process-independent GDS library and generate cell_def/cells.py + cells.json',
        description='Run from any project Tools/lib directory. Inputs are local GDS files; no PDK is bundled.')
    actions = parser.add_subparsers(dest='cells_action', required=True)
    for action, help_text in (
        ('prepare', 'Add physical direction suffixes: gds_source/ (or gds_cadence/) -> gds/'),
        ('generate', 'Generate cell_def/cells.py and cells.json from existing gds/'),
        ('build', 'Prepare original GDS and generate definitions as one validated batch')):
        add_arguments(actions.add_parser(action, help=help_text, description=help_text), action)
    return parser


def run(args):
    # Capture library diagnostics without propagating warnings to the terminal.
    messages = io.StringIO()
    handler = logging.StreamHandler(messages)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger = logging.getLogger(lib.__name__)
    old_handlers, old_propagate, old_level = logger.handlers[:], logger.propagate, logger.level
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.WARNING)
    log_path = (Path.cwd() / getattr(args, 'output_dir', Path('cell_def')) / 'cell_generation.log').resolve()
    try:
        result = _run(args)
    except Exception as error:
        logger.error('%s', error)
        # Validation errors still fail the command; diagnostics live in the log.
        raise ValueError(f'Check log: {log_path}') from None
    else:
        return result
    finally:
        logger.handlers, logger.propagate, logger.level = old_handlers, old_propagate, old_level
        handler.close()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(messages.getvalue() or 'Generation completed without warnings.\n')
        print(f'Check log: {log_path}')


def _run(args):
    root = Path.cwd()
    boundary = args.boundary_layer
    if boundary and boundary[1] is None:
        raise ValueError('--boundary-layer requires LAYER:DATATYPE')
    directions = lib.load_object(args.direction_map)
    action = args.cells_action
    prepared = (root / args.gds_dir).resolve()
    if action in ('prepare', 'build'):
        source = lib.source_directory(root, args.source_dir).resolve()
        if source == prepared:
            raise ValueError('Source and prepared GDS directories must differ; original editor exports are never overwritten')
        if source in prepared.parents or prepared in source.parents:
            raise ValueError('Source and prepared GDS directories must not contain each other')
        files = lib.files_in(source, args.cells)
    else:
        files = lib.files_in(prepared, args.cells)
    pin_maps = lib.load_object(getattr(args, 'pin_map', None))
    vertical = set(args.vertical_pin_layers)
    horizontal = set(args.horizontal_pin_layers)
    if vertical & horizontal:
        raise ValueError('Vertical and horizontal pin layers must not overlap')
    if not 0 < args.corner_distance < float('inf'):
        raise ValueError('--corner-distance must be finite and positive')
    corner_layers = (vertical, horizontal)
    extra, generated = {}, []
    for path in files:
        library = lib.gdstk.read_gds(str(path), unit=1e-6)
        per_cell_directions = directions.get(path.stem, {})
        if action in ('prepare', 'build'):
            lib.prepare(library, path.stem, boundary, args.label_layer, per_cell_directions, corner_layers, args.corner_distance)
            with tempfile.TemporaryDirectory() as temporary:
                temporary_gds = Path(temporary) / path.name
                library.write_gds(temporary_gds)
                extra[prepared / path.name] = temporary_gds.read_bytes()
        if action in ('generate', 'build'):
            if not args.foundry.strip():
                raise ValueError('--foundry must not be empty')
            spec, text = lib.specification(library, path.stem, args.process_node, args.foundry.strip(),
                args.process_coordinates, boundary, args.label_layer, per_cell_directions, pin_maps.get(path.stem), corner_layers, args.corner_distance)
            generated.append((path.stem, spec, text))
    if action == 'prepare':
        lib.write_outputs(extra)
        print(f'Prepared {len(files)} GDS files in {prepared}; original exports unchanged.')
    else:
        output = (root / args.output_dir).resolve()
        # Generated code belongs in a separate project folder, never among input GDS.
        if output == prepared or prepared in output.parents or output in prepared.parents:
            raise ValueError('--output-dir must be separate from the prepared GDS directory')
        if action == 'build' and (output == source or source in output.parents or output in source.parents):
            raise ValueError('--output-dir must be separate from the original GDS directory')
        lib.commit_library(generated, output / 'cells.json', output / 'cells.py', extra)
        print(f'Generated {len(files)} classes: {output / "cells.py"} and {output / "cells.json"}')
    return 0
