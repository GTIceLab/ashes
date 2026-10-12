# Automatic edge and TAP placement

`physical_cell_placement.py` adds available edge and TAP companions to a Python
circuit before Verilog generation. It also moves the exposed routing endpoints
to those companions and creates an abutment plan for `verilog_to_gds.py`.

The feature has two outputs: an augmented circuit and a placement validation
plan. The augmented circuit supplies instances, grid locations, and nets. The
plan lets physical placement check that grid-generated coordinates abut; it
does not reposition any instances.

## Enable the feature

Add this object to `synthesis_settings.json`:

```json
{
  "physical_cells": {
    "edges": "both",
    "taps": "both",
    "scope": "matrix",
    "libraries": ["cells_16nm"]
  }
}
```

| Setting | Choices | Default | Effect |
| --- | --- | --- | --- |
| `edges` | `off`, `left`, `right`, `both` | `off` | Request EdgeL/EdgeR companions. |
| `taps` | `off`, `left`, `right`, `both` | `off` | Request TAP companions independently of edges. |
| `scope` | `matrix`, `all` | `matrix` | Process matrices only, or include single standard-cell instances. |
| `libraries` | List of importable Python module names | `[]` | Scan additional cell-definition modules. |

Modules defining existing circuit instances are scanned automatically.
Decoders and existing companion cells are excluded from parent selection.
Unknown settings and invalid option values raise errors.

Left/right always mean native West/East. They do not change meaning when
`process_coordinates` changes.

## Compile flow and handoff

```text
Designer Python circuit + physical_cells settings
                       |
                       v
asic.compile() in __init__.py
                       |
                       v
prepare_physical_cells()
             /                         \
  augmented circuit                physical_cells_plan
          |                                |
          +--> circuit.print()             |
          |    ASHES Verilog               |
          |                                |
          +--> print_conventional()        |
               external-tool Verilog       |
                       |                   |
                       v                   v
             gds_synthesis(..., physical_cells_plan=plan)
                       |
                       v
             generate_islands(..., physical_cells_plan=plan)
                       |
                       v
             validate_abutments() before island fitting
                       |
                       v
             Native coordinate conversion, when required
                       |
                       v
             Placement GDS and physical-tool DEF
```

The compile entry point performs this call before either Verilog writer:

```python
circuit, physical_cells_plan = prepare_physical_cells(
    circuit,
    physical_cells,
    process_coordinates,
    log_path=os.path.join(project_path, 'syn', 'physical_cells.log'),
)
```

The actual entry point supplies `log_path=None` when no physical-cell settings
are provided.

It passes the returned plan explicitly to the initial `gds_synthesis()` call
and the subsequent routed-output calls. `gds_synthesis()` forwards the same
plan into `generate_islands()`.

**The plan is an in-memory argument, not a hidden Verilog port or a file that
the parser loads automatically.** A separate caller invoking `gds_synthesis()`
on augmented Verilog must also supply the corresponding plan to obtain the
same companion validation. Placement coordinates themselves come from the grid.

## 1. Discover available companion classes

`_catalog()` reads class source with `inspect` and parses it with `ast`. It
looks for literal assignments such as:

```python
self.name = 'IndirectVMM_4x2_EdgeL'
```

The physical `self.name` is the lookup key; the Python class identifier does
not have to match it. Discovery does not instantiate every library class.
Class source must be accessible, and the cell name must be a literal string
assignment for this discovery mechanism to recognize it.

For parent `IndirectVMM_4x2`, the requested names are:

```text
IndirectVMM_4x2_EdgeL
IndirectVMM_4x2_EdgeR
IndirectVMM_4x2_TAP
```

Missing companions are logged and skipped. A TAP can directly abut the parent
when its edge cell is absent. An available edge remains the outermost cell
when its TAP is absent. Conflicting classes using the same companion name
raise an ambiguity error.

Companion constructors must support the generated library interface:

```python
Companion(circuit, island=island, dim=dim)
```

## 2. Copy the circuit and add companion strips

When insertion is enabled, the pass works on a deep copy of the circuit.
The designer's circuit, placement grid, and connections are preserved.

Companions are added to the parent's existing island. They are separate
physical instances, not separate islands. The intended native order is:

```text
West                                                  East
TAP | EdgeL | original instance or matrix | EdgeR | TAP
```

Disabled or unavailable cells are omitted. For a matrix, companions cover its
outer boundary; they are not inserted between internal matrix members.

| Coordinate convention | Companion logical dimensions | Grid space reserved |
| --- | --- | --- |
| `xy` | `(parent rows, 1)` | Columns beside the parent. |
| `columns_y_rows_minus_x` | `(1, parent columns)` | Rows beside the parent. |

Native-left companions reserve the earlier grid boundary. Logical rows are
numbered top-to-bottom; in the alternate convention that ordering maps to
increasing native X.

An existing companion band can be shared by another aligned parent if the
required transverse grid slots are empty. Otherwise, a new band is inserted
and existing grid locations shift. Insertion that would split another matrix
raises an error; align those boundaries or use separate islands.

Each generated cell is marked `physical_companion=True`. Even a 1x1 companion
uses matrix placement metadata in ASHES Verilog, preventing the old ordinary
cell padding rule from adding unwanted gaps.

## 3. Transfer exposed net connections

The pass identifies parent ports on native West/East. It uses
`Port.native_location` when present; older definitions fall back to the
configured mapping of logical `Port.location` to native sides.
Matching uses `Port.native_name`, not the logical Python attribute name.

For each selected parent signal, the lookup order is:

1. Same native name on the requested side, such as `VTUN_w` on West.
2. Same base signal on the opposite side, such as `VTUN_e` on East.
3. Same base signal on North/South, such as `VTUN_n` and `VTUN_s`.

Opposite-side and North/South fallbacks produce log messages. Suffix fallback
requires the requested name to end in `_w` or `_e`.

West/East matches must have compatible total pin counts. Connected parent
pins are mapped to target pins in their existing order. The target pins join
the original net objects, retaining signal identity and NDR attributes.

North/South fallback is allowed only when the connected source pins share
one net. Available North/South ports must have compatible per-member pin
widths. The existing perimeter logic in both writers exposes native North
only at the topmost strip member and native South only at the bottommost
member. If only one of those ports exists, only that available endpoint is
used. Separate connected member nets are rejected rather than merged.

The original parent remains the reference for the signal's requested name
and connection ordering throughout the chain. Thus, after EdgeL uses a
`GND_e` fallback, a subsequent TAP still first tries the original `GND_w`.

Successful transfer marks the previous exposed ports `routing_hidden=True`.
Both Verilog writers omit those ports. The Python pins remain attached to
their original nets; omission changes the routing interface rather than
deleting the designer's connections. Only the final exposed companion ports
are emitted for routing.

If a signal has no compatible companion pin:

| Source state | Behavior |
| --- | --- |
| Unconnected | Log a warning and stop this signal's search. Continue inserting cells and processing other signals. |
| Connected | Raise an error because its net cannot be transferred. Do not bypass the failing edge to search a later TAP. |

Unconnected signals do not acquire fabricated net connections. Ambiguous pin
definitions remain errors. Internal electrical continuity through the cells
is assumed from the library design; this pass does not verify that continuity
from GDS geometry.

## 4. Build the placement plan

After all grid insertions, the pass records each companion's final logical
location and its immediate inner neighbor's location:

```python
{
    'island': 0,
    'cell': (1, 1),
    'parent': (2, 1),
    'side': 'W',
}
```

This is an illustrative relationship, not a fixed grid position.
`parent` here means the immediate inner neighbor, which can be the original
matrix or an edge cell. A TAP therefore relates to its edge when that edge
exists, and directly to the original parent otherwise.

Coordinates are collected after all shifts to avoid stale grid addresses.
Relations are ordered from inner to outer so edge geometry is resolved before
its TAP. The circuit stores the configuration and plan to avoid duplicate
insertion if the same augmented circuit is processed again. A different
configuration must start from the original circuit.

## 5. Validate grid-generated geometry in verilog_to_gds.py

`generate_islands()` first parses the augmented ASHES Verilog and constructs
the usual logical placement items. Each core item retains `logical_row` and
`logical_col`, allowing the plan to locate the correct instances.

Before island dimension checks and island fitting, it calls:

```python
validate_abutments(
    cell_order_in_island,
    physical_cells_plan,
    swapped=bool(placement_axes and placement_axes.swapped),
)
```

The validator reads already-generated placement boxes without modifying them.
It verifies that each companion band has one native cell width, that companion
and parent boundary heights align, and that their boundaries touch exactly.
For `xy`, contact is checked along logical X; for the alternate convention,
contact is checked along logical Y before native conversion. Native West/East
semantics are preserved in either case.

A mixed-width companion band or an unexpected gap fails validation instead of
silently moving cells. Overlapping cell or matrix boxes also fail. Polygon
items are excluded from the cell-overlap check because they can intentionally
overlap device geometry. No companion-specific coordinate correction or
negative-coordinate offset is performed.

After fitting, `PlacementAxes.map_islands()` converts alternate-convention
boxes and matrix member positions to native coordinates. The downstream GDS
and DEF writers consume the grid-generated positions. Cell geometry is not rotated.

## Verilog and DEF instance names

Matrix placement metadata and external-tool naming are separate decisions:

| Physical instance | Conventional Verilog and external DEF name |
| --- | --- |
| One member, including a 1x1 companion | `I_<island>_<row>_<col>` |
| Multiple members | `I_<island>_<absolute-row>_<absolute-col>_<member-row>_<member-col>` |

A drain TAP named `I_0_20_0` belongs to island 0. Its shorter name indicates
one member, not a separate island. Both the conventional writer and external
DEF writer use this same rule. Adding `_0_0` only to Verilog would cause
OpenROAD to report undefined DEF components.

## Logs and checks

Normal compilation writes diagnostics to:

```text
<design project>/syn/physical_cells.log
```

With physical-cell settings supplied, the log is replaced on each compile.
It contains missing-cell skips, pin fallbacks, unconnected-pin warnings, and
exceptions raised during preparation. Later geometry failures are raised by
the physical stage and are not captured by this preparation log.

For direct Python use:

```python
augmented, plan = prepare_physical_cells(
    circuit,
    settings={'edges': 'both', 'taps': 'both'},
    process_coordinates='columns_y_rows_minus_x',
    log_path='syn/physical_cells.log',
)
```

Without `log_path`, direct calls print diagnostic messages.

`check_physical_cells.py` exercises circuit copying, discovery, grid sharing,
pin transfer, shared-net fallbacks, non-mutating geometry validation, logging, and naming.
It requires NumPy. Its production-island-function test supplies lightweight
helpers rather than running a complete physical-tool flow.

During development, the NNopt VMM/switch design was also regenerated in the
installed WSL ASHES environment. Its 356 generated DEF components matched all
356 conventional Verilog instances, and its placement GDS contained the VMM
and drain edge/TAP references. This verifies that design's handoff; other
library geometries and external routing runs still require their own checks.

## Files that cooperate

| File | Responsibility |
| --- | --- |
| `physical_cell_placement.py` | Discovery, circuit augmentation, pin translation, logging, plan creation, and abutment validation. |
| `__init__.py` | Calls preparation before netlist generation and forwards the plan to every physical synthesis call. |
| `asic_compile.py` | Omits hidden routing ports, emits companion placement metadata, and preserves external-tool names. |
| `verilog_to_gds.py` | Generates coordinates from the grid, validates companion geometry before island fitting, and generates physical outputs. |
| `placement_axes.py` | Converts logical placement and matrix members to native coordinates. |
| `json2python.py` | Generates ports with native names and explicit native-side metadata where needed. |
| `update_generated_pin_interfaces.py` | Preserves native-side metadata when updating generated interfaces. |

Install cooperating runtime changes together. An older compile entry point
rejects `physical_cells`; an older physical writer cannot consume the plan;
inconsistent naming between writers causes missing external-tool components.
