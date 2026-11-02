"""Run with python -m ashes_fg.algorithms.cab --settings ... --cells ..."""
import argparse
import json
from pathlib import Path
import sys
from . import Interfaces, load, validate_dimensions


def main(argv=None):
    parser = argparse.ArgumentParser(description='Resolve and validate CAB dimensions without generating layout')
    parser.add_argument('--settings', type=Path, default=Path('cab_settings.json'))
    parser.add_argument('--cells', type=Path, default=Path('cells_16nm.py'))
    parser.add_argument('--interfaces', type=Path, help='Optional golden-coordinate device interface profiles')
    parser.add_argument('--shared-gate-selection', action='store_true')
    parser.add_argument('--row-unit', type=int, default=4)
    parser.add_argument('--column-unit', type=int, default=2)
    parser.add_argument('--sblock-unit', type=int, default=4)
    args = parser.parse_args(argv)
    try:
        profiles = json.loads(args.interfaces.read_text()) if args.interfaces else None
        alignment = None
        sblock_gate_channels = 6  # Compatibility for libraries predating this profile field.
        # Matrix mode deliberately never opens/loads the device cell library.
        settings = json.loads(args.settings.read_text(encoding='utf-8'))
        if settings.get('mode') in ('cab_devices', 'matrix'):
            profile_path = args.cells.with_name(args.cells.stem + '_profiles.py')
            if profile_path.exists():
                from ashes_fg.asic.library.cell_profiles import load_cell_library
                sys.path.insert(0, str(args.cells.resolve().parent))
                library = load_cell_library(args.cells.stem)
                cab_profile = getattr(library, 'cab_profile', {})
                alignment = cab_profile.get('csc_gate_alignment')
                sblock_gate_channels = cab_profile.get('sblock_gate_channels', sblock_gate_channels)
                if profiles is None:
                    profiles = cab_profile.get('devices', {})
        interfaces = Interfaces(args.cells, profiles) if settings.get('mode') == 'cab_devices' else None
        params = load(args.settings, interfaces, csc_gate_alignment=alignment,
                      shared_gate_selection=args.shared_gate_selection,
                      sblock_gate_channels=sblock_gate_channels)
        validate_dimensions(params, row_unit=args.row_unit,
                            column_unit=args.column_unit, sblock_unit=args.sblock_unit)
    except (ValueError, OSError, SyntaxError) as error:
        parser.error(str(error))
    print(json.dumps(params.as_dict(), indent=2))


if __name__ == '__main__':
    main()
