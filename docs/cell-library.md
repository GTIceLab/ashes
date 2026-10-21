# Shared standard-cell library generation

The generator is part of ASHES and is shared by all process nodes. Install ASHES
from `ashes_2p0` with `python -m pip install -e .`, then activate that environment.
Use Linux, WSL/Ubuntu, or a Linux VM. There is no need to copy Python or shell
helper implementations into a public or private technology repository.

## Project layout

Run the commands from your own project's `Tools/lib` directory:

```text
project/
  Tools/
    lib/                     # current working directory
      gds_source/            # original Cadence, Magic, or other editor exports
      gds/                   # prepared GDS with native directional pin names
      cell_def/              # generated Python + JSON
        cells.py
        cells.json
        cell_histories/      # previous versions of changed classes
    run_syn/
      example/
        design.py
```

`gds_source` describes what the files are, without coupling the folder name to a
layout editor. The older `gds_cadence` name remains accepted automatically.
If both original-export folders exist, select one with `--source-dir`.
The commands never search parent directories for missing GDS inputs.

## Choose a workflow

If you already have prepared GDS:

```bash
cd /path/to/project/Tools/lib
ashes cells generate --process-node 130 --foundry sky --process-coordinates xy
```

For original exports without pin directions:

```bash
ashes cells prepare
ashes cells generate --process-node 130 --foundry sky --process-coordinates xy
```

Or prepare and generate as one validated batch:

```bash
ashes cells build --process-node 130 --foundry sky --process-coordinates xy
```

The source folder must already exist for `prepare` or `build`. `generate`
requires an existing, nonempty `gds/` directory; it does not require the original
exports. Missing directories, empty input sets, and unknown selected cells are
errors. Correct your working directory or provide explicit path overrides.

Process node, foundry, and coordinate convention are explicit for `generate` and
`build`; none are guessed from cell names or hardcoded to a process. For example,
a different library can use:

```bash
ashes cells generate --process-node 16 --foundry tsmcN \
  --process-coordinates columns_y_rows_minus_x
```

No technology files are fetched or bundled by these commands. Outputs stay in
the project, regardless of where ASHES is installed.

## Cells and directories

By default every `.gds` file is processed. Select specific filename stems with:

```bash
ashes cells generate --cells IndirectVMM_4x2 TA_FGbias_1x2 \
  --process-node 130 --foundry sky --process-coordinates xy
```

Each GDS must contain exactly one cell matching its filename stem. Only that
cell's direct pin labels and geometry bounds are interpreted; unrelated cells
stored in the same GDS do not inflate its dimensions. References inside the
selected cell still contribute to its bounding box.

Overrides are resolved from the current directory; absolute paths are allowed:

```bash
ashes cells build --source-dir original_layouts --gds-dir prepared_layouts \
  --output-dir cell_def --process-node 130 --foundry sky --process-coordinates xy
```

Original and prepared GDS folders must be separate. The output definition folder
must be separate from the prepared GDS folder and, during `build`, the originals.
Existing generated classes not selected for update are preserved. Changed
classes are archived in `cell_histories/`.

## Geometry, boundaries, and labels

The default dimension source is the selected cell's bounding box. If the process
uses an explicit placement boundary, supply its layer and datatype:

```bash
ashes cells generate --process-node 16 --foundry tsmcN \
  --process-coordinates columns_y_rows_minus_x --boundary-layer 108:0
```

The number above is an example, not a default. A requested boundary absent from
the selected top cell is an error. Boundaries are not inferred from the process
node. GDS user units are normalized to microns while preserving physical dimensions.
Dimensions in `cells.json` and generated `size` values are in microns.
They describe geometry; they do not certify an abutment pitch or DRC/LVS.

`prepare` adds `_n`, `_e`, `_s`, or `_w` before a bus index. Existing direction
suffixes are preserved, so repeating preparation does not append them again.
Directions are native physical sides, and geometry is not rotated. With no
suffix, the nearest edge determines the side. Ties require an explicit override
rather than a hardcoded routing-layer assumption.

Use `--direction-map directions.json` to resolve ambiguous sides:

```json
{
  "MyCell": {
    "INPUT": "W",
    "ENABLE[0]": "N"
  }
}
```

By default, direct top-cell labels are considered, except markers beginning with
`&` (the existing helper convention). To explicitly select pin-label layers:

```bash
ashes cells build --process-node 130 --foundry sky --process-coordinates xy \
  --label-layer 68:5 --label-layer 69:5
```

`LAYER` selects all texttypes on that layer; `LAYER:TEXTTYPE` selects one pair.
Layer numbers are supplied by the user; no process stack is assumed. Hierarchical
annotation names containing dots are not silently discarded or rewritten. If
such labels are selected, generation reports an error. Review the source pin
interface or explicitly select the intended pin-label layers.

Repeated scalar labels remain one physical pin. Indexed buses must be contiguous
and zero-based; missing indices or scalar/bus conflicts produce errors rather
than generating pins that do not exist.

## Logical coordinate conventions and pin maps

`xy` keeps native pin names and sides. `columns_y_rows_minus_x` maps native sides
to the logical interface used by the NNopt library:

| Native side | Logical side |
| --- | --- |
| W | N |
| E | S |
| N | E |
| S | W |

The Python interface can therefore expose `VG_n` while storing native identifier
`VG_w`. ASHES `Port.native_name` retains that physical identifier for netlist
export. The coordinate option changes the generated interface; it does not rotate
GDS or add a physical-placement transformation to the compiler. Use a placement
mode supported by the compiler revision when building a complete design. Do not
copy this metadata field into synthesis settings on versions that do not accept it.

Explicit overrides use `--pin-map pins.json`:

```json
{
  "MyCell": {
    "gate_n": "VG_w"
  }
}
```

The mapping is logical Python name to an existing native base name (without bus
indices). Logical override names must end in a side suffix. Missing targets,
multiple native pins collapsing onto one logical name, and invalid identifiers
produce errors. The JSON library retains native pin-side metadata and records
the selected logical-to-native mapping.

## Use the library in a design

For a design in `Tools/run_syn/example/design.py`:

```python
from pathlib import Path
import sys

# Older ASHES CLI revisions execute designs without defining __file__.
# Run ashes from the design directory in that case.
design_dir = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
sys.path.insert(0, str(design_dir.parents[1] / 'lib' / 'cell_def'))
import cells as lib_cells
import ashes_fg.asic.asic_compile as ac

Top = ac.Circuit()
island = ac.Island(Top)
# Instantiate the generated class required by your design:
# instance = lib_cells.MyCell(Top, island, dim=(1, 1))
```

Add the usual `design_limits`, `location_islands`, frame, and connections for a
complete algorithm. `lib_path` in synthesis settings points to `Tools/lib`,
which contains prepared `gds/`; it does not point to `cell_def`.

## Failure behavior

Input, naming, mapping, and syntax validation finishes for the entire selected
batch before generated outputs are replaced. An invalid cell leaves existing
GDS/Python/JSON outputs unchanged. File replacements are staged; a normal I/O
replacement failure rolls back already replaced outputs. This is not a filesystem
transaction across a machine crash. No requested cell is silently skipped.

Validate generated Python before synthesis:

```bash
python -m py_compile cell_def/cells.py
```

This is interface generation, not cell-level electrical, DRC, or LVS validation.

## Help and migration

```bash
ashes --help
ashes cells --help
ashes cells prepare --help
ashes cells generate --help
ashes cells build --help
```

The existing single-file command remains available, with explicit metadata and
project-local defaults:

```bash
gen_stdcell_defs gds/MyCell.gds -pn 130 -foundry sky \
  --process-coordinates xy -json cell_def/cells.json -pydef cell_def/cells.py
```

Old ASHES shell helpers delegate to these shared commands. They no longer prompt
for folders or embed a process node. Existing project-local scripts are not
modified automatically; replace their use with `ashes cells` after reviewing the
new outputs. Keep original exports and generated definitions under your project's
own access controls; the shared code contains no private process data.
