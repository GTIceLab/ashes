# Python FG peripheral planning and generation

## Regular VMM generation

```python
import cells_16nm as cells
from algorithms.decoders import folded_radix4  # Put the shared 5_Tools/lib directory on sys.path.

vmm = cells.IndirectVMM_4x2(top, island, dim=(16, 16))
vmm.place((1, 1))
fg = island.generate_fg_peripherals(
    cells=cells, process_coordinates='columns_y_rows_minus_x',
    gate_decoder=folded_radix4.GateDecoder,
    drain_decoder=folded_radix4.DrainDecoder)
```

This creates `SWC_Gate`, `SWC_Drain`, `LevelShift_2x_Gate`, and
`LevelShift_4x_Drain` arrays, plus ordinary `GateDecode_2x4` and
`DrainDecode_2x4` instances. The default `GateDecoder` / `DrainDecoder`
builders in the shared `5_Tools/lib/algorithms/decoders/folded_radix4.py` construct electrically
explicit radix-four trees using the
central CAB placement topology: leaf cores, first connection band, packed upper
cores/fillers, then connection/tree bands. They also place `CON0`–`CON3`,
`CON1_ALT`, `CON_FILL`, `CON_TREE`, `CON_TREE_FILL`, and `2x4_FILL` where needed.
Builders declare each decoder band with `register_companion_group()`. The
shared physical-cell pass adds its edge/TAP cells according to `physical_cells`
settings and library metadata. Gate variants are not invented where the library
has none. Generation is Python-level; GDS does not synthesize decoders.

Straight and cross-direction bit buses inside tree helpers remain separate.
Every helper address, enable, selection, and supply endpoint is attached to its
actual Python net. Contact and complete routing still require physical signoff.

For 16x16 unit cells, there are 32 gate channels with 5 address bits and 64 drain
channels with 6 address bits. An unused high input in an odd-width radix-four
root is grounded. True/complementary gate selections and all decoder enables,
shifter controls, and switch-to-VMM nets are created before either netlist writer.
The sample contains 40 gate-decoder cells (11 active cores) and 80 drain-decoder
cells (21 active cores), including connectors and fillers. `instances` in each
decoder result includes its body cells. With both edge/TAP sides enabled, the
shared pass separately adds 20 drain-decoder companions across five bands.
The earlier algorithm added 15 boundary cells because it included TAPs only
on the left; both sides now follow the common settings.

The default physical generator currently supports one contiguous
`IndirectVMM_4x2` per island, using cell definitions generated for the logical
swapped-axis convention. Automatic edge/TAP preparation runs afterward and
includes generated switches/shifters and declared decoder bands. Actual GDS cell bounds determine the
placement, so double-pitch gate decoder leaves do not stretch VMM columns.
Native edge/TAP chains are included in this geometry. Placement validates array
pitch, companion contact spans, and overlap; it is not DRC/LVS signoff.
Decoder bands use complete physical slots and validate helper pitch, band
thickness, and drain boundary-cell spans. Single-level and partial trees avoid
the reference algorithm's negative-index and row-list typo cases. Circuit copying
preallocates model graph objects, avoiding recursion through dense shared buses.

## Signals and overrides

```python
fg.gate.inputs.bits
fg.gate.inputs.enable
fg.drain.inputs.bits
fg.drain.inputs.enable
fg.gate.switches
fg.gate.level_shifters
fg.supplies
fg.controls
```

The VMM-to-frame example brings all gate/drain bits and separate enables to
logical N/W frame sides, plus the generated supplies and operation controls.
Gate run/source inputs retain separate lanes; they are not implicitly shorted.
Core analog tuning/source inputs remain designer-owned. In particular, this
library's VMM EdgeR lacks a VTUN pass-through, so automatic core VTUN attachment
is deliberately omitted rather than breaking companion preparation.

Switch, shifter, and decoder choices can be overridden with `gate_switch=`,
`drain_switch=`, `gate_level_shifter=`, `drain_level_shifter=`, `gate_decoder=`,
and `drain_decoder=`. No registration or JSON file is needed. False disables a stage; global switches/level_shifters/decoders booleans are
also available. See [generation options](FG_GENERATION_OPTIONS.md) for external
signals and custom algorithms around placed S-blocks. Different pin
interfaces report a missing-port/width error; automatic alternative pin mapping
is not implemented. Decoder callables use `DecoderContext` / `DecoderResult`.
The selected algorithm owns decoder core/CON/FILL names, connections, and
multirow/multicolumn placement. Edge/TAP names are cell-library metadata;
the shared companion pass owns their instantiation, wiring and placement.
ASHES contains no decoder tree or CON/FILL selection. Omitting decoder overrides selects `algorithms.decoders.folded_radix4`' normalized
builders; put the shared library directory on `sys.path` once in the design.
The unified `GateDecoder(context)` / `DrainDecoder(context)` functions return
DecoderResult objects. The old positional decoder entry points were removed;
standalone filler utilities are retained in `decoders/cell_helpers.py`.

`DecoderContext.placement` is an ASHES AlgorithmGrid adapted to the chosen
chain region. Builders place cells with canonical `(x=slot, y=band)` indices;
they do not calculate process-specific staging rows/columns. The standard
DecoderGrid helper records these points as `cell.algorithm_xy`. Declared
companion bands continue to retain live cell references.

`DecoderResult.layout` receives DecoderPlacementContext with canonical cell
footprints, slot_pitch, core size/shape and opaque entry descriptors. It returns
`{item_index: [x0, y0, x1, y1]}` in **local Cartesian XY**, for exactly the returned
body instances. The local anchor is zero. The FG manager supplies gate/drain
orientation and the chain's physical anchor, resolves companions, validates
coverage/overlap, translates the island and converts to native coordinates.
Alternate callbacks must follow this local XY contract; callbacks using the old
absolute anchor or implementing drain-axis conversion must remove that mapping.

Builders must reserve unique staging locations through the supplied grid and
retain `fg_peripheral` / `physical_companion` metadata for compact placement.
Use `register_companion_group()` for body bands. The optional `fg_geometry`
descriptors remain algorithm-owned. The current 16nm FG materializer still
requires its selected swapped process convention; canonical algorithm XY does
not add physical-library support for another process convention.

Generation is idempotent for the same configuration. A failed generation restores
the circuit-model state. Reconfiguration requires the original circuit. Library
modules remain shared during the compile flow's deep copy.

## Sharing and bridge cases

After generating two separate islands, `island_a.share_fg_bits(island_b)` connects
both address buses and leaves their enable nets separate. `role='gate'` or
`role='drain'` shares only one bus. Unequal widths require explicit designer slices.
All non-abutting endpoints remain electrical routing endpoints.

`add_fg_peripherals()` remains the planning API for layouts containing gaps,
non-VMM FG cells, or extended groups. Plans record filler coordinates, edge
boundaries, target channels, and bridge requirements. Compile rejects an
unmaterialized plan rather than quietly omitting its peripherals.

Default materialization of bridge-dependent extensions, segmented arrays,
gap fillers, xy libraries, and gate program/run isolation is not implemented.
The assumed missing bridge names remain `FG_RoutingBridge_Gate` and
`FG_RoutingBridge_Drain`; they require physical views and defined lane mappings.
The shared address/separate-enable mode works with regular generated islands.

## Compile handoff and verification

Compilation collects an in-memory `fg_layout_plan` after edge/TAP insertion.
Every GDS synthesis call passes it to `generate_islands()`, which applies actual
FG geometry before island fitting and native conversion. Verilog retains ordinary
cell instances; no new cell ports or GDS decoder synthesis are used.

Tests and generated verification artifacts are kept in the Windows workspace,
not in the ASHES or project directories. Verification covers the real 16nm
library, both Verilog forms, sharing, rollback, companion preparation, geometry,
and placement-only GDS/DEF generation. Routing, DRC, LVS, and electrical simulation
have not been run.

See [configurable generation](FG_GENERATION_OPTIONS.md) for cell-name/class overrides,
stage switches and the whole-peripheral algorithm contract.
