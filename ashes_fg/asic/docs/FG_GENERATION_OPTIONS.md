# Configurable FG peripheral generation

All options are Python arguments; no JSON registry or copied cell definitions
are required. The default path handles a regular 16nm VMM or supported registered local bands
across a mixed VMM body. See [gap-filler scope](PERIPHERAL_GAP_FILLERS.md).

```python
from algorithms.decoders import folded_radix4

fg = island.generate_fg_peripherals(
    cells=cells_16nm,
    gate_switch="SWC_Gate",            # A name in the selected cell module.
    drain_switch=cells_16nm.SWC_Drain,  # Or a Python cell class.
    gate_decoder=folded_radix4.GateDecoder,
    drain_decoder=folded_radix4.DrainDecoder,
    gate_level_shifter=False,           # Disable only the gate shifter stage.
)
```

`gate_switch="SWC_GorS"` selects that class when it exists in the chosen library.
The default VMM wiring requires its expected native pins and channel widths.
Use a whole-peripheral algorithm for a different interface or physical layout.
Changing the class selection does not rename a GDS master or copy its definition.

## Cell, algorithm and stage choices

| Argument | Accepted values | Default |
| --- | --- | --- |
| `gate_switch`, `drain_switch` | Cell class, library class name, False | SWC_Gate / SWC_Drain |
| `gate_level_shifter`, `drain_level_shifter` | Cell class, library class name, False | LevelShift_2x_Gate / LevelShift_4x_Drain |
| `gate_decoder`, `drain_decoder` | Callable, dotted Python function path, False | Folded radix-4 GateDecoder / DrainDecoder |
| `switches` | Boolean applying to both switch stages | True |
| `level_shifters` | Boolean applying to both shifter stages | True |
| `decoders` | Boolean applying to both decoder stages | True |
| `roles` | Tuple of distinct gate/drain roles | ('gate', 'drain') |
| `algorithm` | Whole-peripheral callable or dotted Python function path | Automatic regular/local-band generator |

None keeps the default. An explicit per-role choice overrides a global switch:
`level_shifters=False, gate_level_shifter=cells.LevelShift_2x_Gate` keeps only the
gate shifter. True as a per-role choice enables its default. False creates no
new cells for that stage; it does not remove cells already placed by the designer
or a body algorithm.

Configuration changes require an original ungenerated circuit. Repeating the
same arguments returns the existing Generated object without duplicating cells.
Failed generation restores the circuit state, including custom algorithm changes.


## Available decoder selections

`my_gate_decoder` and `my_drain_decoder` in custom examples are placeholders
for designer-supplied functions, not names exported by this library. Currently
the only supplied topology is `algorithms.decoders.folded_radix4`.

| Value of `gate_decoder` | Result |
| --- | --- |
| Omitted, None or True | Default `folded_radix4.GateDecoder`, unless `decoders=False` disables the omitted/None choice |
| `folded_radix4.GateDecoder` | Explicit selection of the supplied builder |
| `"algorithms.decoders.folded_radix4.GateDecoder"` | Import the builder by dotted function path |
| A custom callable | Call it with DecoderContext; it must return DecoderResult |
| False | Disable the decoder and expose external selection inputs |

The same choices apply to `drain_decoder`, using `DrainDecoder`. Explicit True
or a builder overrides `decoders=False`. This API does not discover a catalog
of additional decoder topologies automatically. The shared library directory
must be importable for default or dotted-path selections.

## Connections when stages are disabled

- Without a shifter, the default VMM generator directly connects decoded
  selections to the switch. Use cell interfaces and signals suitable for that
  voltage domain; this option supplies no conversion circuitry.
- The default drain decoder has no complementary output. When its shifter is
  bypassed, the designer must drive `fg.drain.external_inputs["select_n"]`, also
  exposed as `fg.controls["DRAIN_SELECT_N"]`. A selected decoder can provide
  output_complements instead; no inverter or complementary signal is invented.
- Without a decoder, the designer drives `chain.external_inputs["select"]` and
  any required `"select_n"`. These are also in fg.controls as GATE_SELECT,
  DRAIN_SELECT and complementary names. `chain.inputs.bits/enable` are unavailable.
- Without a switch, the core programming buses are exposed in fg.controls as
  GATE_PROGRAM, DRAIN_PROGRAM_P and DRAIN_PROGRAM_R. The designer supplies those
  signals. The generator does not substitute decoded logic for analog programming
  voltages. `chain.selection_outputs` retains available decoder/shifter outputs.

Available stages abut compactly in physical layout. Disabled stages leave no
physical band or companion strip. Edge/TAP selection remains in physical_cells.

## Automatic local bands and advanced callbacks

For VMM spans separated by registered non-FG columns, no custom callback is
needed. The default path uses peripheral_fillers for switch/shifter bands and
decoder_fillers for the selected decoder topology. Use parents= to select the
VMM FG targets and roles=('gate',) when another role needs separate bridge or
interface treatment. Existing body cells remain. See
[profiles, examples and scope](PERIPHERAL_GAP_FILLERS.md).

For a layout outside that supported contract, select a custom **peripheral**
algorithm. The my_* names below are placeholders, not supplied implementations:

```python
fg = sblock_island.generate_fg_peripherals(
    cells=cells,
    algorithm=my_sblock_peripherals,
    gate_decoder=my_gate_decoder,
    drain_decoder=my_drain_decoder,
    gate_switch="SWC_Gate",
    level_shifters=False,
)
```

`algorithm` is not Sblock_gen: that function builds the body. The peripheral
callback receives PeripheralContext with:

- island, circuit and the selected cell module;
- plan.gate/plan.drain, including resolved cell/decoder/bridge choices, channel
  targets and layouts with spans, filler_coordinates and edge_coordinates;
- placement, the shared canonical XY grid adapter;
- process_coordinates and normalized options, including roles.

The callback owns new stage placement, electrical wiring and any gap/bridge
treatment, and must honor the resolved stage choices. A chain.decoder_placement
can be set to a chosen AlgorithmGrid region before chain.build_decoder(), allowing
the selected decoder builder to use canonical local XY inside a mixed layout.
Missing bridge names are available through context.plan.missing_cells.

Return `Generated(context.plan.gate, context.plan.drain, supplies=..., controls=...,
instances=..., layout=...)` from ashes_fg.asic.peripherals.fg_generation.
Instances must cover every body and newly added cell in the island. Omit
instances to capture all current island cells automatically. The layout callback
receives PeripheralPlacementContext (including companion relationships) and returns canonical island-local XY boxes
for exactly its entry indices. It must account for the shared companion strips.

For a natural variable-pitch abutting grid, use
`ashes_fg.asic.placement.algorithm_grid.grid_layout` as the callback. It reserves
pitch for all shared strips and returns only the algorithm-owned body boxes;
the shared pass places companions against those boxes. A different arrangement
can use its own callback and opaque fg_geometry descriptors.

The S-block library's core, routing and TopBot edge/TAP profiles are preserved.
Non-FG columns are passed to the algorithm as filler locations; no VMM-only
assumption is imposed on a custom callback. The shared grid helper does not
create filler or bridge cells. Arbitrary S-block FG interfaces, bridge/extension algorithms and
required bridge physical cells remain design/library responsibilities;
selecting a custom callback does not synthesize their implementation automatically.

## Verification

Checks cover 16 global/per-role/override configurations, external selection and
programming signals, custom mixed S-block layout and specialized companions,
idempotence and failed-callback rollback. The default VMM retains its physical
placement and functional net connectivity. Placement-only GDS/DEF compiles cover
the default, disabled stages and a custom S-block layout. These checks do not
constitute voltage-domain, routing, DRC, LVS or functional signoff.

See [decoder fillers across intervening cells](DECODER_GAPS.md) for gap discovery,
library profiles, variable-width bands and connection ownership.

Automatic mixed-band checks additionally cover all eight stage combinations,
profile-driven narrow/regular fillers and explicit separation from bridge ties.
