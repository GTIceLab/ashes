## Full flow
See make_library.sh

*This file README not be up to date. The .sh file above will be a better resource*
## How to run mag2gds
```bash
python  mag2gds.py -o <output_dir> --files <magic files...>
```
Or, if .mag files are organized into a library of subdirectories with matching names:
```bash
python  mag2gds.py -o <output_dir> --dir <library dir>
```
### Example
```bash
python  mag2gds.py -o ./gds_output/ ../../../ASHES-Skywater130nm/sky130_cells/
```
