# CAB cell-library profiles

Profiles are hand-maintained metadata beside a generated cell library. They
describe which cells/pins implement electrical roles and which placement rules
the selected CAB recipe should use. They do not create GDS cells or establish
physical continuity by themselves.

## Files and loading

- `cells.py`: generated definitions. Regenerate it when layout pin labels change.
- `cells_profiles.py`: hand-maintained metadata with `register_profiles(cells)`.
- `README_CAB_PROFILES.md`: this guide.
- Project `run_syn/CAB_NN_global/cab_settings.json`: dimensions, devices and logical connections.
- Project `synthesis_settings.json`: process/backend and library selection.

`load_cell_library('cell_def.cells')` looks for the adjacent `cells_profiles.py`
and invokes its registration function. Registration is repeatable and preserves
already-loaded overrides. Start a fresh Python process after editing profile
files to avoid cached modules. Cell generation does not replace the profile.

The common `ashes_fg.generators.cab_nn` entry point selects `cab_profile.builder`.
The 350nm profile selects `ashes_fg.algorithms.cab.abut_native.build`. Libraries
without that field use the existing packaged 16nm recipe. Do not copy a complete
350nm profile over a 16nm profile: their selected recipes have different contracts.

## What belongs in the profile

| Field | Purpose |
| --- | --- |
| `builder` | Shared CAB recipe to invoke |
| `masters` | Physical cell classes implementing matrix, switch, decoder and boundary roles |
| `ports` | Exact, case-sensitive native pin names for each electrical role |
| `matrix_unit`, `gate_switch_unit`, `volatile.lane_unit` | Electrical capacity of selected cells |
| `matrix_rows` | Boundary-row selection and reserved read-lane positions |
| `matrix_continuity` | Explicit opposite-edge pin pairs representing the same matrix signal |
| `shared_programming_groups` | Matrix programming drains connected together |
| `sblock_programming_host` | Matrix drain group serving the S-block |
| `sblock.sections`, `section_ports`, `routing_ports` | Functional and passive S-block interfaces |
| `sblock.gate_fillers` | Filler choices and carried signal connections, by passive-band role |
| `sblock_gate_channels` | S-block contribution to shared gate-selection capacity |
| `decoder_cells` | Explicit core/bridge/spacing master for each topology slot kind |
| `decoder_interface` | Address/enable/output/run/supply terminal names |
| `decoder_auxiliary` | Explicit internal/pass-through versus external terminal interpretation |
| `supply_names`, `supply_aliases`, `static_families` | Common supply/control policies |
| `gate_switch_shared_ports` | Exact gate-switch supply/RUN/PROG contacts; avoids blanket analog-rail ties |
| `power_input_order` | Optional A-input power lanes, in declared order |
| `volatile.interface`, `body_bindings`, `body_lane_slice` | Combined volatile/scan interface and connected A lanes |
| `devices`, `activation_interface` | Signal/support roles, known rails, bias roles and native-abutment assumptions |
| `bias_aliases` | Translate old logical CAB references to current native terminals |
| `island_layout` | Relative island placement and exact host anchors |
| `layout_margin`, `default_island_gap`, `design_limits` | Designer-selected placement policy and area limits |
| `placement_units_per_um` | Conversion between generated micron dimensions and placement units |
| `physical_cells` | Edge/TAP insertion policy |
| `review_notes` | Assumptions and unresolved physical/electrical verification limits |

Example native-role mapping from the current 350nm profile:

```python
PROFILE['ports']['drain_switch'] = {
    'selection': ('SELECT_w',),
    'program': ('Vd_P_e',),
    'read': ('Vd_R_e',),
}
PROFILE['ports']['cutoff'] = {
    'b_read': ('In_w',),
    'a_read': ('A_e',),
    'program': ('P_e',),
}
```

These strings are intentional library data. Pin renaming requires a profile
update, not a spelling-based alias guessed in the algorithm. A test library
using different master and pin names verifies decoder resolution follows its
contract. Missing decoder contracts fail rather than silently selecting a family.

## S-block fillers and compact decoder addressing

Current 350nm filler selections:

- `buffer` -> `S_BLOCK_BUFFER_FILL_GSWCS`.
- `connector_23` -> `S_BLOCK_23CONN_FILL_GSWCS`.
- `routing` -> `S_BLOCK_FILL_GSWCS`, with its `n_n` pins bound to that column's north tracks.

Only the functional SEC1/SEC2/SEC3 interfaces contribute decoder channels.
Passive columns and fillers consume no addresses. The current configuration is
12 CEW + 6 S-block + 12 CNS = 30 outputs, requiring five address bits. These are
results for the current parameters, not dimensions fixed in the implementation.

The decoder's native bands are packed consecutively using the dimensions
supplied by the layout context. They do not follow sparse S-block column
positions. This removes the former 31.18 um internal gap. Signals from the
compact decoder to the gate-switch band are explicit nets for routing.
No decoder-specific fill masters are synthesized or stretched to hide gaps.
Different widths within a decoder slot are rejected; the library must provide
compatible native cells or a different placement algorithm.

## Dimensions and placement units

Generated `cell.size` values are in microns. Backend placement metadata and the
profile's margins, gaps and area limits use placement units. The current 350nm
profile declares 1000 placement units per micron. This must agree with the
selected process backend; the adapter does not infer units from a process name.

The profile places Volatile centered below A and Out below its output switch.
Out's drain channels extend the AB bank continuously; there is no local Out
drain strip or extra Out spacer gap. Anchors use master plus logical location,
not whichever matching cell happens to appear first in backend item order.

## Algorithm structure versus hardcoded policy: remaining limits

This flow is not an automatic arbitrary-topology generator. The following
structure remains intentional algorithm code and should not be mistaken for
universally configurable profile data:

1. `bridged_radix4` is a two-input/four-output decoder-tree algorithm. Its radix,
   parent/child math and A/B/C/D bridge topology are part of that algorithm.
   A different topology requires a different builder, not a renamed master.
2. `sectioned` implements exactly three functional sections and a diagonal
   connector staircase. Cell names, pin names, capacities and fillers are profile
   data; changing to a different number/arrangement of sections requires another
   compatible body algorithm. Unsupported section counts fail explicitly.
3. `abut_native` implements the named A/B/Out/CEW/CNS CAB recipe, two fabric input
   halves and one activation group. Topology roles and public frame interface
   names remain in that recipe. It is not a profile interpreter for any circuit.
4. The shared sizing API retains a default of six S-block channels for old
   callers. The 350nm path supplies the value derived from its section/interface
   profile. This compatibility default preserves the original 16nm behavior;
   it is not used to size the new native path implicitly.
5. The existing 16nm recipe, folded decoder and switch-matrix S-block retain
   inherited 16nm assumptions. They were not fully generalized in this work;
   their graph remains identical to the original design. The core compiler's
   existing process parameter table is also outside this CAB-profile refactor.
6. Decoder stage pitch uses native dimensions, including the maximum height
   within a stage. Cells are never stretched. A nominal difference between
   native helper heights is a library/continuity question, not permission to
   resize their geometry in software.
7. Test fixtures contain numeric dimensions and alternate names. Those values
   are test data, not production layout constants.

These limits are deliberately disclosed. Moving native names into profiles
does not, by itself, generalize an algorithm's circuit topology.

## Electrical assumptions recorded for 350nm

- Activation WTA/complement and ambiguous VG_N continuity follows the owner's
  native Bot abutment instruction. No inferred shorts or Vg_m rename are added.
- Bot `IOUT_e` is the WTA_bot_bias role, excluded from functional CAB outputs.
- Known Vc/Vg_pFET/Vg_p rails and support supplies are connected explicitly.
- Volatile clock/reset/data/COM pass-throughs are profile declarations. Serial
  input and output remain separate. Internal CP/DFF1Q have no independent driver;
  volatile FG peripherals and its programming-drain terminal remain deferred.
- Decoder auxiliary/internal label interpretation is provisional owner input.
  Model checks do not verify the physical continuity of those labels.
- Gate-switch analog paths are not automatically shorted to VDD by pin spelling.
  Shared power and RUN/PROG contacts are listed explicitly in the profile.

## Checks after editing a profile

From the project's `CAB_NN_global` folder, in the ASHES environment:

```bash
bash parameters.sh
bash check.sh
bash draft.sh
```

These inspect generated Python definitions and circuit metadata, not project
GDS/technology LEF. `bash run.sh` invokes the physical backend and accesses those
resources. Physical synthesis has not been rerun as part of these changes.
Model net/placement checks are not DRC/LVS or verification of abutting pin shapes.

If a check fails after regeneration, correct the profile's cell/pin contract.
Do not edit generated classes, increase area limits to conceal overlaps, or
add guessed aliases to silence an unresolved electrical interface.


## Connected physical pin checks

External-PD builds write pd/pin_extraction_diagnostics.json and fail when a connected port is missing from the extracted macro pin set. No technology-specific substitutions were added. Matching is unchanged; bus-width validation remains separate. Details: /home/praveen/Tools/ashes/docs/physical-pin-preflight.md


## Cell-library geometry validation

Cell build/generate now omit unmatched physical pin labels from definitions and log each omission. Add --strict-pin-geometry to reject unusable labels before committing the batch. Pinless cells remain allowed. See /home/praveen/Tools/ashes/docs/cell-pin-geometry.md for explicit layer selection, defaults and inherited geometry limitations.


### Pin geometry modes

Default warning mode omits unmatched labels from cells.py and cells.json and logs each omission in cell_generation.log. With --strict-pin-geometry, the same issue stops generation before committing any batch outputs. Genuinely pinless cells remain supported. This supersedes any earlier statement that unmatched pins are retained. No cell-specific exceptions were added.


## Optional native internal terminals

The component interface accepts optional_native_internal_ports for annotation-only terminals with no CAB wiring. Missing entries log a warning without creating a port or net. The 350nm volatile profile explicitly places CP_w and DFF1Q_s in this category. Required native_internal_ports, public interfaces, pass-throughs and deferred_fg_ports still validate their declared ports. Supply pins are not made optional by this policy. CAB NN generator logic is unchanged; the technology choice lives in the profile.


## Optional decoder auxiliary annotations

Decoder contracts support optional_internal_ports. Absent entries warn; present entries remain classified internal without new connections. The 350nm drain profile uses this for IN1_n, IN2_n, IN1_Bar_w and IN2_Bar_s, previously accepted as internal/pass-through labels. Required internal_ports and leaf_ports still fail if absent; functional address, enable, output and analog-input mappings remain required. No cell-name tests were added to the decoder algorithm.

Activation metadata also supports optional_native_abutment_ports. The 350nm profile uses this only for the previously owner-approved WTA/complement and VG_N native Bot continuity annotations. Missing labels warn, with no created pins or alias shorts. Physical continuity remains an owner assumption, not verified by the model draft. Functional rail, bias and exposed terminals remain required. All 80 unit tests and the regenerated-library 126-instance draft passed; physical synthesis was not run.


Physical synthesis writes detailed unmatched-pin warnings to design/pd/pin_extraction.log, with only the log path printed to the terminal. The JSON diagnostic report is retained, and fatal preflight errors still stop the build. This supersedes earlier references to unmatched-pin console warnings. Logging is per build, without modifying root/global logging handlers.


## Requested 350nm design area

The wafer5 profile now requests design_limits [450000, 650000] (450um width by 650um height at 1000 DBU/um). CEW is 15000 DBU above A_GorS, providing the CSC-to-AB bank gap; Sblock and CNS follow CEW. Other gaps remain unchanged. This is a profile-only configuration. The current generated-definition placement requires at least 611270 by 455000 DBU including margins and therefore does not fit the requested width. No automatic rotation, scaling, capacity reduction or fit-check bypass was introduced; physical synthesis was not run.


Area correction: the requested orientation is 650um wide by 450um high, design_limits [650000, 450000]. The 15um CSC-to-AB gap remains. The prior model extent is 611.27um by 455um including margins, so height remains 5um over the corrected boundary. No margin reduction or fit-check bypass was applied.


## Design area belongs to the run

Current area is set in the design run synthesis_settings.json as "design_limits": [650000, 450000] (650um wide by 450um high at 1000 DBU/um). The 350nm cell profile no longer defines it. A design file may override it with tile = build(design_limits=[650000, 450000]) before publishing vars(tile); the explicit argument takes precedence over run settings. Older profiles remain supported as a fallback. Generic build/native/legacy adapters only forward the area; no wiring or placement topology changed. The ASHES CLI removes the resolved setting from forwarded kwargs to avoid duplicate arguments. Fit checks and the existing 455um model height remain unchanged. This section supersedes older profile-area instructions.


## Current CSC spacing and side clearance

The run synthesis_settings.json now sets design_limits [750000, 495000]: 750um width (+50um on each side of the former 650um area), 495um height (the current 460um height plus 35um for the increased inter-bank gap). Profile CEW placement above A_GorS uses gap 50000 DBU. Profile layout_margin is a per-side mapping: left/right 50000, bottom/top 10000. Scalar margins remain backward compatible. This adds generic margin plumbing only; no CAB wiring, scaling or rotation changes. The generated-definition model fits, with a 50um gap and at least 50um horizontal margins; minimum model extent including margins is 691.27 by 490um. All 80 existing tests and synthetic margin/fit checks passed. Physical synthesis was not run. These settings supersede previous area/gap values in this document.


Latest spacing update: CSC-to-AB gap and left/right minimum margins are now 75um each. Top/bottom margins remain 10um. Run design_limits is [800000, 520000] (800 by 520um), adding 25um to each side and 25um height for the larger gap. Profile settings only; no algorithm or wiring changes.


## Latest exposed-supply routing and reference floorplan

The wafer5 run now opts into placement-aware exposed supply terminal export in pd_settings.json. Run core area is 920x610um with 10um PD core margins; model padding is 10um and CSC-to-AB GorS gap is 34.48um, taken from cab_rerun. This supersedes earlier 75um gap and 800x520um area values. Full logical supply connectivity remains in the model and inputs/TILE_NN.full.v; the router gets a filtered inputs/TILE_NN.v, conditional on an explicit within-cell continuity declaration and measured abutment contacts. Uncertain or inaccessible components are preserved, not silently disconnected. NDR dimensions match the reference; power-grid generation remains enabled. Details, assumptions, configurable defaults and validation: /home/praveen/Tools/ashes/docs/supply-access.md


## Native-abutment-only A/B boundary rows

The 350nm A and B matrix_rows recipes now explicitly set boundary_routing to native_abutment. The shared matrix-row assembler tags only the before/after boundary members; body cells stay explicit. The shared physical exporter resolves the tagged model members to exact instance names, verifies their master and placement, and writes those instances with empty port lists in the router Verilog. No cell names are embedded in that exporter.

This suppresses all external terminal connections on TSMC350nm_4x2_Indirect_top_AorB_matrx and TSMC350nm_4x2_Indirect_bot_B_matrx in those recipes, following the owner declaration that these rows connect entirely by native abutment. Logical pin/net relationships, capacity/reserved-lane accounting and placement remain unchanged. inputs/TILE_NN.full.v preserves the full logical export; inputs/TILE_NN.v is the routing export. pd/supply_access.json includes a separate native_abutment_export section, and the text log reports its omission count. This works even with no supply_access policy configured.

Verification on the current 126-instance model selects exactly 21 physical boundary instances and omits 294 terminal connections (189 signal/control/FG plus 105 supply connections). Every nonselected instance connection and every model pin-to-net identity remains unchanged. Physical continuity is an owner assumption, not an electrical extraction result. Defaults remain explicit for other recipes, including 16nm. Restore explicit boundary routing by setting boundary_routing to explicit in the matrix recipe. No synthesis/routing was executed; rebuild to regenerate the routing inputs.


## Current routing access representation (supersedes face pruning)

Directional copies such as X_n/X_s are internal aliases with alternate access shapes, not separate pins requiring an external tie. The 350nm profile enables routing_access, and the shared exporter emits one logical terminal and one LEF PIN/PORT containing all declared equivalent shapes. Both native names remain in the Python interface. The old pd_settings supply_access face-pruning policy is removed; do not enable both policies. A/B boundary rows still export no external connections. Full logical Verilog and pd/routing_access reports are retained. Bus export now preserves unused positions. Tests: 103 pass; both project model launchers pass. Details, declarations, references and limitations: /home/praveen/Tools/ashes/docs/multi-access-pins.md


## Frame access and remote matrix drains

Matrix row recipes may declare routing_ports as exact native names. Those ports are eligible for routed access; all others remain native-only. The default remains a fully native matrix. read_port and program_port choose the assembly's ordered drain interfaces. Missing declared ports fail validation.

Folded decoder filler profiles may declare frame_access with name, port and band. The value outer selects the final placed connector band. Returned gap_connections provide the algorithm interface; no arbitrary body/filler route is synthesized. Library metadata owns native pin conventions.

Tile frame roles now use algorithms/cab/tile_frame.py with ordinary side spreading. The former paired_ports explicit-coordinate feature was removed. Local analog/bias interfaces stay on their previous sides. See cab-frame-and-output-drains.md for current roles, count exceptions and verification.


350nm confirmed run/activation contract: gate_analog_input_net selects the named common rail for decoder run inputs; omit it to retain independent inputs. Activation native_rails and device native_abutment_ports annotate native-only contacts, while expose_rails/expose_bias_roles decide public frame access. The current owner-selected 350nm profile uses common VGRUN and omits WTA/bottom-control frame access. No arbitrary lane shorts are inferred from labels.
