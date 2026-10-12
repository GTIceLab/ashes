# Python FG peripheral planning and generation

## Regular VMM generation

```python
import cells_16nm as cells
from algorithms import Decoders  # Put the shared 5_Tools/lib directory on sys.path.

vmm = cells.IndirectVMM_4x2(top, island, dim=(16, 16))
vmm.place((1, 1))
fg = island.generate_fg_peripherals(
    cells=cells, process_coordinates='columns_y_rows_minus_x',
    gate_decoder=Decoders.build_gate_decoder,
    drain_decoder=Decoders.build_drain_decoder)
```

This creates `SWC_Gate`, `SWC_Drain`, `LevelShift_2x_Gate`, and
`LevelShift_4x_Drain` arrays, plus ordinary `GateDecode_2x4` and
`DrainDecode_2x4` instances. The default `build_gate_decoder` / `build_drain_decoder`
builders in the shared `5_Tools/lib/algorithms/Decoders.py` construct electrically
explicit radix-four trees using the
central CAB placement topology: leaf cores, first connection band, packed upper
cores/fillers, then connection/tree bands. They also place `CON0`–`CON3`,
`CON1_ALT`, `CON_FILL`, `CON_TREE`, `CON_TREE_FILL`, and `2x4_FILL` where needed.
Drain bands include left/right edges and left TAP cells, with matching connection
edge/TAP fillers. Gate edge/TAP variants are not invented where the library has
none. Generation is Python-level; GDS does not synthesize decoders.

Straight and cross-direction bit buses inside tree helpers remain separate.
Every helper address, enable, selection, and supply endpoint is attached to its
actual Python net. Contact and complete routing still require physical signoff.

For 16x16 unit cells, there are 32 gate channels with 5 address bits and 64 drain
channels with 6 address bits. An unused high input in an odd-width radix-four
root is grounded. True/complementary gate selections and all decoder enables,
shifter controls, and switch-to-VMM nets are created before either netlist writer.
The sample contains 40 gate-decoder cells (11 active cores) and 95 drain-decoder
cells (21 active cores), including fillers and boundary cells. `instances` in
each decoder result includes all those cells, not only functional cores.

The default physical generator currently supports one contiguous
`IndirectVMM_4x2` per island, using cell definitions generated for the logical
swapped-axis convention. Automatic edge/TAP preparation runs afterward and
skips the already-generated peripherals. Actual GDS cell bounds determine the
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
and `drain_decoder=`. No registration or JSON file is needed. Different pin
interfaces report a missing-port/width error; automatic alternative pin mapping
is not implemented. Decoder callables use `DecoderContext` / `DecoderResult`.
The selected algorithm owns all decoder core/CON/FILL/edge/TAP names, connections,
and multirow/multicolumn placement. ASHES contains no decoder tree or support-cell
selection. Omitting decoder overrides selects `algorithms.Decoders`' normalized
builders; put the shared library directory on `sys.path` once in the design.
The existing legacy `GateDecoder(...)` / `DrainDecoder(...)` functions remain
available for old scripts; their old return dictionaries do not satisfy the new
interface without adaptation.

`DecoderResult.layout` is a callback receiving `DecoderPlacementContext`, with
actual GDS dimensions, the chain's outer anchor, core size/shape, and entries
indexed by placement item. Entry descriptors are opaque to ASHES. The callback
returns `{item_index: [x0, y0, x1, y1]}` in the logical placement plane for exactly
its returned decoder instances. ASHES checks coverage/overlap, translates the
whole island, and converts to native coordinates. Alternate algorithms can use
different layouts and descriptors without changing the FG manager. Builders
must place their instances at unique staging grid coordinates and flag them as
`fg_peripheral` and `physical_companion` to bypass automatic core companions and
matrix padding. The optional `fg_geometry` attribute is passed to the callback.

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
