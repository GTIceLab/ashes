"""Inspect CAB parameters/model without opening layout or technology files."""
import argparse
import json
from pathlib import Path
import sys
from . import build


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--settings', type=Path)
    parser.add_argument('--draft', action='store_true', help='Inspect incomplete model; never invoke synthesis')
    args = parser.parse_args(argv)
    project = args.project.resolve()
    sys.path.insert(0, str(project.parent.parent / 'lib'))
    try:
        tile = build(project, args.settings, **({'strict': False} if args.draft else {}))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(dict(parameters=tile.CAB_Params,
        instances=len(tile.Top.Instances), islands=len(tile.islands),
        row_capacity=getattr(tile, 'row_capacity', {}),
        synthesis_ready=getattr(tile, 'synthesis_ready', True),
        review_notes=getattr(tile, 'review_notes', ()),
        implementation_issues=getattr(tile, 'implementation_issues', ())), indent=2))
    return 0


if __name__ == '__main__':
    main()
