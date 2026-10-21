"""Compatibility wrapper; process-independent implementation is in gds_to_celldef."""
import sys
from ashes_fg.gds_to_celldef.cli import add_arguments, run
import argparse

if __name__ == '__main__':
    parser = add_arguments(argparse.ArgumentParser(description='Use ashes cells prepare from Tools/lib'), 'prepare')
    args = parser.parse_args()
    args.cells_action = 'prepare'
    try:
        run(args)
    except (ValueError, OSError, SyntaxError, TypeError) as error:
        parser.error(str(error))
