## Cell-library pin geometry validation

`ashes cells build` and `ashes cells generate` now check selected pin labels
against top-cell physical pin rectangles. Warnings are saved in
`cell_def/cell_generation.log`; unmatched labels are omitted from both Python and JSON pin definitions.
Each omitted label is explicitly logged; no geometry or replacement connections are invented.

Add `--strict-pin-geometry` to fail when any selected label has no usable pin
rectangle. Validation finishes before the batch commits prepared GDS or cell
definitions, so a strict failure preserves the previous outputs. Genuinely
pinless cells still succeed with the existing warning, including strict mode.

For example, from your Tools/lib folder:

```sh
ashes cells build --process-node 350 --foundry tsmc --process-coordinates xy --strict-pin-geometry
```

By default, if present, the generator uses the JSON layer map at
`layer_map/FOUNDRY_NODEnm.json`, matching the standard process file naming
convention. This convention is an explicit default, not a cell-name heuristic.
Override it with `--pin-layer-map PATH`, or supply repeated
`--pin-layer LAYER:DATATYPE` options. The JSON selection uses `purpose: pin`;
processes using label-purpose mappings must select their layers explicitly.
`--label-layer` continues to select label layers/texttypes independently.

Without an available map or explicit pin layers, normal mode warns and performs
a diagnostic check using all polygon datatypes on each label's layer. It does
not claim compatibility with physical export. Strict mode requires a physical
layer selection whenever labels exist.

The shared rectangle matcher reports edge labels, outside labels, and missing
selected rectangles. The library check additionally reports labels on layers
excluded by the physical parser. Diagnostics include cell, pin, native
coordinates, layer and selected datatype; the library diagnostic records also
include label texttype. Selected labels without usable rectangles are recorded in
the log, omitted in normal mode, and rejected in strict mode.

Current inherited physical-parser limitations remain explicit: strict interior
matching rejects labels on rectangle edges; one most-common pin datatype is
selected across layers; geometry is represented using the first and third
polygon vertices. The library validation checks top-cell polygons, not PATH
elements or hierarchical geometry, and is not a full shape/connectivity or DRC
check. Layouts using PATH-based pin shapes need further parser unification;
strict mode can conservatively reject those. No technology-specific exceptions
were added, and no user GDS or technology LEF was inspected or regenerated.

The physical-build connected-port check remains a second safeguard. Bus-width
validation and preserving unused bus positions remain separate pending fixes.
Verification: 77 unit tests using synthetic layouts and existing fixtures pass.


### Pin geometry modes

Default warning mode omits unmatched labels from cells.py and cells.json and logs each omission in cell_generation.log. With --strict-pin-geometry, the same issue stops generation before committing any batch outputs. Genuinely pinless cells remain supported. This supersedes any earlier statement that unmatched pins are retained. No cell-specific exceptions were added.
