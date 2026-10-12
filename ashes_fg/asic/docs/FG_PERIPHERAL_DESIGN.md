# Island-owned FG peripherals

Proposed design, grounded in `physical_cell_placement.py`, `asic_compile.py`,
`placement_axes.py`, and the reference library
`C:/Users/prave/OneDrive/Desktop/VMM_Swcs_to_frame_old_node/cells_16nm.py`.
This document specifies the target abstraction. `fg_peripherals.py` implements
planning; `fg_generation.py` now materializes the regular swapped-axis VMM case
with explicit routed Python decoder trees. Bridge-dependent and arbitrary CAB
topologies remain future work. See `FG_PERIPHERALS_README.md` for verified scope.

## Assumptions and selection rules

1. A cell name starting with `SWC` identifies a switch candidate. Edge, TAP, and
   filler variants are support cells, not independently selectable functional
   switches. The prefix does not establish the switch's gate/drain role.
2. Use defaults without requiring switch registration or capability contracts:
   gate switch `SWC_Gate`, drain switch `SWC_Drain`, gate level shifter
   `LevelShift_2x_Gate`, drain level shifter `LevelShift_4x_Drain`, and Python
   decoder builders `GateDecoder` / `DrainDecoder` from the shared version of
   `CAB_NN/Decoders.py`. These defaults use the selected central cell library.
3. Designers may override any switch class, level-shifter class, or decoder
   callable independently. Omitted fields retain their defaults. Listing `SWC`
   classes is optional discovery, not compatibility filtering or registration.
   Overrides use the expected builder/pin interface, with explicit wiring
   overrides where needed; report missing pins or width mismatches when building.
4. Parent pin prefixes discover potential FG requirements. Cell metadata or an
   explicit designer override distinguishes programming pins from analog bias
   pins and declares aliases/shared lines. Already selected peripherals and
   support cells cannot recursively become FG parents.
5. There is at most one logical chain per role referenced by each island. By
   default the island owns its chain; explicitly grouped islands may reference
   the same switch array, level shifters, and decoder. Instantiate the shared
   group once, with one placement owner and one public input interface. A chain
   can contain arrays, decoder trees, bridges, and physical segments. Multiple independently
   addressed gate/drain banks require an explicit future bank extension or
   separate islands; the manager must not silently short them together.
6. Every connection is represented electrically in Python before either netlist
   writer. Abutment implements a connection physically; it does not replace the
   net graph. Preserve designer-provided nets and reject contradictory bindings.
7. Every requested channel has a stable identity and an explicit decoder-output
   mapping. Do not infer that physical row/column order equals address order.
8. Geometry and voltage compatibility come from the selected technology profile.
   Direct abutment requires compatible pin geometry, layers, pitch, and native
   side. A mismatch requires a declared bridge or routing strategy, or an error.
   The selected SWCs are assumed designed to abut `IndirectVMM_4x2`. This is the
   default direct-contact target. Every other FG cell enters bridge treatment by
   default; matching pin names or prefixes does not establish direct-contact
   compatibility. A profile may explicitly declare another cell compatible.
9. All decoder generation occurs at Python level. `verilog_to_gds.py` receives
   ordinary generated instances and placement; its decoder generator is outside
   this design and is not used or adapted.
10. Preparation is explicit during design so controls can be connected afterward.
    Repeated identical preparation is idempotent. Structural edits after
    preparation invalidate the plan and require rebuilding, avoiding stale ports.
11. Decoder input bits may be shared across islands. Per-island chain ownership
    does not imply separate address nets. Sharing address bits does not implicitly
    share enable signals, supplies, decoder outputs, or FG drain lines.

## Sharing switches and complete peripheral chains

The designer may group islands to share a drain chain, a gate chain, or both.
This means one physical peripheral group serves FG endpoints in multiple islands,
not just multiple local decoders connected to one address bus. The attached
shared-drain illustration motivates this mode, including intervening scanner
and double-pitch cells.

Each group records member islands, its placement owner, selected components,
ordered channels, and an explicit channel-to-target map. Each target identifies
an island, cell, pin, and lane. A lane may fan out to several target endpoints
only when the designer explicitly declares them the same programming line.
Distinct target lines retain distinct switch channels; sharing a peripheral
array does not imply shorting all member islands' drain lines. Sharing one
switch channel also means its targets cannot be selected independently through
that channel; separate channels or additional selection circuitry are needed
for independent operation.

Proposed API (not implemented):

```python
shared_drain = peripherals.prepare_shared(
    circuit=Top,
    islands=[island_a, island_b],
    role="drain",
    placement_owner=peripheral_island,
    channel_map=drain_channel_map,
    # SWC_Drain, LevelShift_4x_Drain, and DrainDecoder are defaults.
)
# Both member islands reference this same chain.
```

Determine switch counts from the group's ordered distinct channels, not the sum
of per-island pin counts. Check actual endpoint geometry for every mapped target:
use direct contact where designed abutment provides continuity, and explicit
electrical ties plus bridge/routing treatment where it does not. Separated VMM
islands also require a connection strategy for the physical gap; VMM compatibility
does not make disconnected geometry electrically continuous. Other FG cells
retain bridge treatment by default. Intervening scanner/double-pitch/support
cells provide continuity only if their defined pass-through pins establish it.

Create every switch-to-target connection in Python. Keep non-abutting target
pins exposed to the chosen physical connection strategy. Plan the shared group
once, after considering the placement of all member islands, and validate full
group connectivity and voltage-appropriate geometry. Independent compilation
of member islands must not generate duplicate shared arrays.

## Sharing decoder inputs across islands

Shared gate bits and shared drain bits with independent island enables are an
explicit supported mode. Each island retains its own independently enabled
gate/drain decoding and switch paths; corresponding address inputs use common
nets. This allows the same address to be presented to both islands while enable
signals select the intended island. Do not merge enable nets when sharing bits.

Proposed interface:

```python
fg_a.gate.inputs.address.connectPort(gate_bits)
fg_b.gate.inputs.address.connectPort(gate_bits)
fg_a.drain.inputs.address.connectPort(drain_bits)
fg_b.drain.inputs.address.connectPort(drain_bits)

fg_a.gate.inputs.enable.connectPort(enable_a_gate)
fg_a.drain.inputs.enable.connectPort(enable_a_drain)
fg_b.gate.inputs.enable.connectPort(enable_b_gate)
fg_b.drain.inputs.enable.connectPort(enable_b_drain)
```

Optionally connect an island's gate and drain enables to one island-select signal
when their active polarity and programming protocol are compatible. Otherwise
keep both enable controls exposed or provide an explicit adapter. Record enable
polarity and disabled behavior in the decoder builder result. Verify that a
disabled island's programming paths are inactive for its selected circuit;
address sharing alone does not guarantee isolation. Selecting exactly one island
is a designer/control-circuit responsibility unless an explicit selector is
requested. No implicit cross-island enable shorting or selection logic is added.

This mode differs from physically sharing one switch channel: independently
selecting islands behind a common physical channel requires per-island gating
or equivalent isolation circuitry. A single shared decoder/switch path cannot
provide independent island enables merely by attaching two enable signals to
the same input. Preserve separate enabled branches where isolation is required.

Designers can connect both islands' drain address interfaces to the same Python
bus. This merges corresponding bit nets, retaining separate decoder instances
and per-island chains. The same rule applies to gate bits and explicitly shared
controls. Proposed API:

```python
# drain_bits is the designer's existing ordered address bus.
fg_a.drain.inputs.address.connectPort(drain_bits)
fg_b.drain.inputs.address.connectPort(drain_bits)
# Connect enables independently, or share them explicitly when intended.
```

The important operation is connecting both exposed interfaces to the same ordered bit nets.
For different address widths, require an explicit slice/bit mapping rather than
silently truncating, extending, or reversing either interface.

One logical bit may reach several physical decoder-cell input pins. Each decoder
builder must expose those endpoints and declare internal pass-through/contact
relationships; returning only one representative input pin is insufficient
unless continuity to all other consumers is established. The manager places
every consumer on the bit's net before either Verilog writer.

After placement, inspect actual endpoint geometry and cell continuity for each
shared net. A connection may be implemented by abutment only where compatible
pin shapes/layers touch and the required pass-through path is established.
For endpoints that do not abut, retain exposed routing pins and emit a routable
net connecting them. Ordinary routing can connect low-voltage decoder address
bits between islands; this does not require an FG programming bridge by default.
FG/high-voltage lines continue to follow the separate bridge-treatment rules.

Treat each validated abutting group as one physical connected component. Route
between components when a shared bit has more than one component, including
branches for multiple islands/consumers. Do not hide all but one endpoint merely
because they share a logical net, and do not assume island adjacency guarantees
electrical contact. The connectivity must be equivalent in both emitted netlists;
physical verification must confirm every consuming decoder pin is reached.

## Shared library and manager

Use the existing `5_Tools/lib/stdcell_defs` and `5_Tools/lib/algorithms` as the
starting point for one importable shared library. Add package namespaces and
technology profiles there rather than copying definitions into every design.
Do not relocate or overwrite existing libraries as part of this design proposal.

Proposed package shape:

```text
ashes_fg/library/
    cells/tsmc16/          # canonical cell definitions
    algorithms/decoders/  # selectable Python builders
    profiles/             # technology defaults and coordinate settings
ashes_fg/peripherals/
    defaults.py           # default classes/builders and optional overrides
    manager.py            # discover channels, build, connect, place, validate
    models.py             # island-owned chains and builder results
```

Use a defaults configuration and the peripheral manager; no switch registration
layer is required. Use qualified classes/callables and profile identifiers. Record library/profile
and algorithm versions with generated designs for reproducibility. Legacy design
folders can temporarily import the canonical library through thin re-export
modules; those modules must not contain copied cell definitions.

Proposed design API (not currently implemented):

```python
# All switch, shifter, and Python decoder choices have defaults.
fg = island.prepare_fg_peripherals(profile=profiles.tsmc16)
fg.gate.inputs.address.connectPort(address_bus)

# On another island, override only the desired choices.
other_fg = other_island.prepare_fg_peripherals(
    profile=profiles.tsmc16,
    gate=GateSpec(switch=cells.SWC_GorS, decoder=my_gate_decoder),
)
```

This illustrates selectable objects, not a claim that `SWC_GorS` is already a
validated drop-in replacement. It exposes `VG_e` and `VS_e`, and its controls
include `SELN_w`, `SEL_S_w`, and `SEL_e`, unlike `SWC_Gate.SEL_w` / `SELN_w`.
An explicit wiring override can establish the intended gate/source mode and
selection mapping without registering a capability contract.
The library also contains `SWC_OutMtrx`, `SWC_VolSwc`, and `SWC_BMtrx`; their prefix
alone does not make them compatible alternatives for this gate chain.

## Ownership and public interface

Each island references at most one gate chain and one drain chain, owned locally
or by an explicitly shared peripheral group. Each chain contains
one switch array, one level-shifter array, and one decoder tree (possibly many
physical instances). All instances remain ordinary members of the circuit and
one placement-owning island so both Verilog writers see the same cells and nets.
Other member islands reference the group without duplicating its instances.

Proposed API:

```python
island.prepare_fg_peripherals(profile=fg_profile)
island.fg.gate.switches
island.fg.gate.level_shifters
island.fg.gate.decoder.instances
island.fg.gate.inputs.address
island.fg.gate.inputs.enable
island.fg.drain.inputs.address
island.fg.drain.inputs.enable
```

`prepare_fg_peripherals` must be callable before compilation, allowing designers
to connect the exposed ports to frame ports, wires, or other islands. Compilation
validates an existing preparation or prepares an unconfigured island before both
writers. Store instance and port references, not just names or placement indices.
Repeated preparation with the same configuration returns the existing chains;
changed configuration requires rebuilding from the unprepared circuit.

Each chain also records parent instances, ordered channel bindings, generated
nets, logical side, native side, and abutment relationships. Exposed controls and
supplies are actual ports; no implicit supply or unused-output tie-offs.

## Discovery and channel layout

Detect `Vg_` for gates and `Vd_P_` / `Vd_R_` for drains using native pin identifiers.
The profile may explicitly support uppercase spellings such as `VD_P_s`.
Exclude switches, level shifters, decoders, edge/TAP cells, and fillers from parent
discovery. Provide explicit parent eligibility/overrides: the library also has
bias pins such as `Vg_p_w` and `Vg_m_w` that must not automatically select a gate
programming chain.

Aggregate requirements per island before constructing any arrays. Opposite-edge
copies of one physical line are aliases, not additional channels. Drain program
and run pins are separate bindings for the same drain channel. Distinct cells
share a channel only when their connectivity and physical alignment establish
that sharing; matching pin names alone is insufficient.

For the supplied `IndirectVMM_4x2` in its native library indexing:

* `R` native rows require `2R` gate channels and `R` `SWC_Gate` cells.
* `C` native columns require `4C` drain channels and `C` `SWC_Drain` cells.
* Gate shifters handle two channels and drain shifters handle four.
* A gate decoder leaf handles four outputs and spans two gate-switch pitches.
* A drain decoder leaf handles four outputs and spans one drain-switch pitch.

Derive dimensions from the normalized channel bindings and profile capacities;
do not apply these native row/column formulas directly to a transformed logical
grid. Validate partial groups, discontinuous boundaries, and mixed cell pitches.
An island that cannot use a single directly abutting array may use an explicitly
supported segmented/bridged chain. Otherwise report the incompatible parents;
do not silently create another independently addressed chain.

## Placement and wiring

| Chain | Logical side | Native side in xy | Native side in columns_y_rows_minus_x |
| --- | --- | --- | --- |
| Gate | N | N | W |
| Drain | W | W | S |

From core outward, place switch array, level-shifter array, then decoder tree.
Selection signals travel decoder -> level shifter -> switch -> core.
Use the existing coordinate mapping once; do not rotate native cells or rewrite
their pin identifiers. Each technology profile must supply cells with compatible
native pin sides and pitches for its coordinate convention. The supplied library
has gate outputs on E and drain outputs on N, matching the swapped convention.
An xy profile requires compatible cell geometry rather than assuming these same
unrotated cells can contact an N/W core boundary.

Reference gate connections:

* `SWC_Gate.VG_e` -> core `Vg_w` (or the exposed companion endpoint).
* `LevelShift_2x_Gate.X_VINJ_e` -> `SWC_Gate.SEL_w`.
* `LevelShift_2x_Gate.XN_VINJ_e` -> `SWC_Gate.SELN_w`.
* Decoder `SEL_e` / `SELN_e` -> shifter `X_w` / `XN_w`.

Reference drain connections:

* `SWC_Drain.Vd_P_n` / `Vd_R_n` -> core `Vd_P_s` / `Vd_R_s`.
* Shifter `X_VINJ_n` / `XN_VINJ_n` -> switch `Sel_s` / `SelN_s`.
* Decoder `SEL_n` -> shifter `X_s`.

Validate vector widths and preserve existing user connections before merging
nets. The sample VMM circuit places switches but does not explicitly connect
their core-facing pins; adjacency alone is not a complete electrical netlist.
Create internal electrical nets before writing either Verilog representation.
Hide an internal routing endpoint only when validated physical contact supports
it, while preserving the connection in conventional Verilog.

Compose FG bands with edge/TAP companions using one ordered boundary plan.
Recompute grid positions after all insertions. Extend contact validation to N/S
as well as W/E and validate actual boxes, complete contact spans, and overlaps.
Gate and drain corner regions need explicit profile fillers or empty reserved
space; independent placement loops must not overlap them.

## Decoder integration

Use designer-selected Python algorithms directly. A local copy of the requested
`CAB_NN/Decoders.py` exists under
`C:/Users/prave/Downloads/NNopt_FPAA_16nm-main/NNopt_FPAA_16nm-main/5_Tools/run_syn`.
It supplies `GateDecoder(circuit, island, numCols, ...)` and
`DrainDecoder(circuit, island, numRows, ...)`, creates/places ordinary cells, and
returns dictionaries containing `Bits`, `Enable`, `VDD`, and `GND`.

Wrap these builders to normalize their result; do not reuse the GDS decoder
generator. Normalize requested size to *output count*, because local algorithms
do not all use the same convention: the central `lib/algorithms/Decoders.py`
accepts a `bits` parameter whereas the CAB_NN builders calculate bits internally.

The common algorithm contract takes a context (circuit, target island, selected
cell library, coordinate/pitch contract), ordered requested outputs, and a local
placement origin. It returns instances, local placement/extent, output bindings,
address bus with declared bit order, enable/controls, supplies, and abutment
relationships. An algorithm may instantiate connection/filler/TAP cells, but
must declare them in its result. The manager translates local placement into the
island and owns integration with neighboring chains. Existing builders that
insert rows/columns need an adapter documenting those mutations or a refactor
to local placement, rather than hidden changes to the final island grid.

Expose address and enable through the island chain. Track valid outputs and
unused leaves explicitly. Confirm the intended one-channel case and partial
leaf behavior rather than allowing a zero-column decoder from a generic formula.

## Bridge abstraction for complex macros

The attached figure distinguishes a regular memory array, where matching unit
cells permit direct abutment, from an MLP macro with termination cells and
discontinuous programming endpoints. Represent both through one channel-to-core
connection plan. Keep the bridge separate from the decoder algorithm so any
decoder choice can serve either macro geometry.

Connection strategies:

* `abut`: verified direct contact for every required endpoint.
* `bridge`: registered passive bridge cells with declared input/output lane maps.
* `route`: explicit routed programming channels, using declared corridors and
  technology constraints.
* `auto`: choose direct contact when compatible, otherwise a configured validated
  bridge, otherwise a permitted routing strategy; report unsupported cases.

A bridge contract includes channel count, lane permutation, port layers/shapes,
voltage-rated geometry, extent, orientation, pass-through nets, and obstructions.
Start with a small straight pass-through bridge, a pitch adapter, and an optional
turn cell rather than assuming one universal bridge can connect every topology.
For a termination block, a pass-through strip or reserved corridor can carry FG
lines past the block to a common peripheral boundary. For fragmented groups,
segmented switch arrays within one logical chain can keep local contact while
sharing the decoder interface through an explicit output map.

Default endpoint classification is per parent, not per island: an
`IndirectVMM_4x2` endpoint uses direct abutment, while another FG cell's endpoint
requires bridge treatment. A mixed island therefore retains one gate/drain chain
while recording different connection strategies for its endpoints. A missing
bridge implementation leaves the affected connection unresolved and must produce
a clear error during generation; do not silently assume contact or substitute
ordinary routing. Explicitly permitted routing remains a designer-selected
alternative. Edge/TAP companions preserve the declared VMM boundary chain and
must not cause a VMM parent to be reclassified as an unrelated FG cell.

Alternatives to a dedicated bridge are a reserved upper-metal programming
corridor, standardized boundary-access adapter cells, or local peripheral strips
for each aligned segment. These are architectural options to evaluate, not
verified DRC-clean solutions. A passive bridge does not provide voltage isolation
or remove loading constraints. Full-macro DRC/LVS, voltage suitability, and
parasitic/loading checks remain needed at bridge-to-cell and routed interfaces.

## Implementation sequence and verification

1. Add island chain records, eligibility rules, channel discovery, and a library
   profile using native identifiers.
2. Adapt the selected Python decoder algorithms to the common result contract.
3. Instantiate and wire complete chains before either Verilog writer.
4. Reserve abutting grid bands and compose their validation with edge/TAP plans.
5. Carry chain identity and exposed signal references into physical island details.

Check gate-only, drain-only, and combined parents; aliases on opposite sides;
shared and independent channels; existing manual peripherals; duplicate
preparation; transformed coordinates; odd gate groups; partial decoder leaves;
and incompatible pitches. Verify both netlists describe the same electrical
connections and GDS/DEF placement has complete abutment without overlaps.
Also check shared decoder bits across separated and abutting islands, multiple
physical consumers per bit, independent enables, and explicit unequal-width
bit mappings; non-abutting consumers must remain visible to routing.
Check both gate and drain address sharing together, distinct island enable nets,
enable polarity, and inactive programming paths for the deselected island.
