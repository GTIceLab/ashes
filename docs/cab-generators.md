# Decoder continuity and profile-policy audit

The circled internal decoder gap was caused by host-column spacing leaking into
the decoder's own stage pitch. The native decoder bands now abut consecutively,
independently of S-block routing gaps. Channel count remains 30, with five address
bits. Cells are not stretched and no fabricated decoder fillers are added.

Native decoder/helper class names and pin/supply contracts, drain/cutoff pins,
matrix pass-throughs, switch/volatile capacities, shared-programming groups,
power-input order, S-block capacity/ports and placement policy are explicit
profile data. The 350nm sizing path derives S-block capacity from its profile;
the old six-channel default remains only for compatibility with existing callers.

The dedicated `README_CAB_PROFILES.md` beside both cell libraries and ASHES
`docs/cab-profiles.md` document every contract plus the remaining fixed topology,
legacy 16nm and native-abutment assumptions. The implementation is not claimed
to infer arbitrary circuit topology automatically.

All 65 unit tests, both model runners, original 16nm graph equivalence and
350nm model connection/placement checks pass. Every decoder stage is checked
for horizontal continuity using generated-definition dimensions. No physical
synthesis, GDS or technology LEF inspection was performed.

The following sections are implementation history. See the profile guide and
runner READMEs for current behavior.

# Component integration and active-only CSC decoding

The current 350nm model has 126 instances; all 59 unit tests and both project
runners pass. The existing 16nm graph remains unchanged at 184 instances.

The three supplied gate-side filler families are registered and placed over
the corresponding passive S-block columns. Their four-track signal ports are
connected explicitly. Passive columns consume no decoder outputs: CSC uses
30 channels and five address bits for the current parameters. Physical spacing
is separate from compact electrical channel numbering.

Volatile COM/data aliases now match the regenerated cell. Clock/reset and
scanner-compatible data interfaces are exposed; serial input/output remain
distinct. No separate scanner/FG peripheral cells are generated. The Bot is
still excluded from functional CAB signal counts; IOUT_e is its WTA_bot_bias
role. Known activation rails are mapped, while ambiguous WTA/VG_N continuity
follows the owner's native-abutment instruction without guessed alias shorts.

Changes are in the 350nm profile, sectioned S-block algorithm and native shared
adapter/component helpers. The common CAB entry point and project launcher do
not acquire process-specific branches. No physical synthesis, GDS or technology
LEF inspection was performed. Model connectivity/placement checks are not LVS/DRC.

The following sections are implementation history; the runner READMEs describe
current behavior and supersede earlier six-bit decoder and placement-only notes.

# Current shared AB/Out extension

Out's drain channels now extend the AB drain bank continuously, as requested.
The Out-local switch offset and volatile-driven extra Out clearance are removed.
Out abuts its output switch; the volatile bank remains centered below A.
There is one shared AB/Out decoder, with separate channel ranges, and no local
drain strip beside Out. The 350nm model has 131 instances; all 53 unit tests,
both project runners, model placement/net checks and the 16nm graph comparison pass.
No physical synthesis or GDS/technology-LEF inspection was performed.

The earlier placement/clearance descriptions below are implementation history,
superseded by this shared extension. The runner READMEs describe current behavior.

# CAB implementation and current validation

## Latest placement corrections

The 350nm model now has 151 instances. Gate switches align only with the three
functional S-block sections; passive routing columns are excluded. Decoder
addresses retain those physical holes (six gate address bits in this setup).
The gate decoder is anchored above CEW, spanning the CSC bands. Shared A/Out
drain programming includes passive gap rows and a horizontally offset Out
switch strip. Both AB and CSC drain banks abut the left side of their hosts.
The volatile bank is now centered below A; see the correction below.

Explicit checks now verify switch-to-section X alignment, drain-to-matrix XY
abutment, and that the volatile bank clears the drain side, in addition to
macro overlap checks. These use generated-definition dimensions, not GDS.

This is an implementation checkpoint, not a completed 350nm synthesis result.
The 350nm circuit model now passes preflight under a provisional owner-agreed
decoder contract. Physical synthesis has not been run, and electrical/physical
signoff is not established by this model check.

## Installed locations

- `/home/praveen/Tools/ashes/ashes_fg/algorithms/`: installed shared algorithms.
- `/home/praveen/Tools/ashes/ashes_fg/generators/cab_nn/`: shared CAB entry point.
- `/home/praveen/Projects/wafer5/6_Tools/lib/cell_def/cells_profiles.py`: native
  350nm port roles, boundary rows, memory and bias mappings, algorithm selection.
- `/home/praveen/Projects/NNopt_FPAA_16nm/5_Tools/run_syn/CAB_NN_global/`: 16nm runner.
- `/home/praveen/Projects/wafer5/6_Tools/run_syn/CAB_NN_global/`: 350nm runner.

Each global runner includes `TILE_NN.py`, `cab_settings.json`,
`synthesis_settings.json`, `parameters.sh`, `check.sh`, `draft.sh`, `run.sh`,
and a README. The existing NNopt `CAB_NN_abs` source/settings remain unchanged.
An earlier 350nm `CAB_NN_abs` launcher was also created during this implementation;
use `CAB_NN_global` as the documented run directory in both projects.

## Exact CAB changes

1. Copied the original 16nm construction function into
   `ashes_fg.generators.cab_nn.legacy`; its circuit wiring and layout recipe are
   unchanged. Its project directory is now an explicit argument, and imports
   refer to `ashes_fg.algorithms`. It accepts the common `strict` argument for
   runner compatibility; that flag does not change the legacy circuit.
2. Added `ashes_fg.generators.cab_nn.build(project, ...)`, which reads project
   settings, loads cell profiles and selects `cab_profile.builder`. The existing
   16nm recipe is the default. It has no 350nm cell names or process tests.
3. Added thin project launchers calling that entry point and exposing the
   returned design variables to the existing ASHES CLI.
4. Added the native abutting adapter and reusable boundary-row/S-block/decoder
   algorithms. Native 350nm topology code is separate from the legacy recipe.
5. Added optional profile-defined A-bias target aliases to the shared binder.
   Its existing behavior is unchanged when aliases are omitted. The 350nm
   profile maps former Scanner and COM references to the integrated volatile
   cell's native D/Q/com terminals.
6. Changed the shared peripheral generator's default decoder import from the
   project-local `algorithms.decoders.folded_radix4` to the installed
   `ashes_fg.algorithms.decoders.folded_radix4`. Explicit callback overrides work.

## Boundary rows

The profile chooses A/B top and B-bottom masters. They replace nominal VMM row
units, rather than increasing the requested row count. The top definition's
read indices are [1:3]; the bottom definition's are [0:2]. The model explicitly
records missing slots, preserving four programming lanes per nominal row.

With 16 nominal rows:

| Matrix | Physical row units | Usable read lanes | Reserved nominal lanes |
| --- | --- | --- | --- |
| A | 4 | 15 | 0 |
| B | 4 | 14 | 0, 15 |

Device requirements exceeding usable capacity fail. Top-cap memory outputs are
connected to corresponding GorS `fg_pu_s` pins; B-bottom outputs connect to
output-switch `fg_pu_n`. These follow the owner's stated abutment contract.
No layout geometry was used to establish or verify these connections.

## Model contents and limitations

The 350nm draft contains 127 model instances. It uses two GorS banks, no separate
A/B gate switches, no level shifters, no separate VMM_DigMem banks, no edge/TAP
insertion, and one volatile bank without FG peripherals. The activation bottom
is placed only, as requested. The adapter includes CSC gate switches, shared
AB/CSC drain groups, B-cutoff draft wiring, A-input/device connections and
profile-resolved A-bias wiring.

The following still require implementation review before synthesis:

- Gate decoder analog VGRUN/RUN_OUT and helper pass-through connectivity. The
  old example's analog rail use differs from a conventional digital decoder;
  the draft must not silently short all analog lanes together.
- Drain decoder auxiliary IN1/IN2 and complemented-pin aliases. The generated
  definitions expose multiple labels whose intended electrical equivalence
  is not established by the class signatures alone.
- B-cutoff draft read/program mappings against the intended CAB circuit.
- The profile-driven global placement callback is now implemented and passes
  generated-definition checks for island coverage, array pitches and overlaps.
  Physical pin alignment against GDS remains unverified.

`draft.sh` and `check.sh` now report these assumptions as review notes rather
than fixed failure reminders. Explicit profile classifications distinguish
internal decoder labels from required external terminals; unknown disconnected
terminals still fail. The 350nm synthesis settings deliberately do not guess
a technology/backend configuration.

## Verification performed

- ASHES unittest discovery: 43 tests passed, including new reserved-lane and
  decoder-topology tests and the existing cell-generation/coordinate tests.
- Original versus packaged 16nm circuit graph: same 184 instances, pin widths,
  and pin/net connectivity.
- Actual generated 350nm Python library: draft builds, A/B capacities are 15/14,
  integrated memory nets match their target switch lanes, one volatile bank,
  no shifters/edges, and strict synthesis protection holds.
- Both runner folders: shell syntax, parameter inspection and draft commands
  pass. Both 16nm and 350nm model checks now pass.
- No physical synthesis or `run.sh` execution was performed. No GDS or technology
  LEF contents were inspected. Existing tests generate synthetic fixtures only.

## Preflight correction

Fixed review reminders no longer masquerade as detected electrical errors.
They are retained as `review_notes`. Auxiliary decoder pins are rechecked after
CAB wiring, removing stale reports for connected RUN_OUT lanes and identifying
the exact remaining disconnected lanes. Strict mode still blocks unresolved
decoder terminals; it does not bypass them to make synthesis appear successful.

## Provisional decoder contract

Following the owner's tentative confirmation, IN_n[0:1] remains the external
drain address bus. IN1_n, IN2_n, IN1_Bar_w and IN2_Bar_s are explicitly classified
as internal/pass-through; no independent driver or guessed short is added.
The gate decoder exposes active leaf VGRUN_n terminals as `Gate_analog_in`.
Helper/higher-stage copies and unused rounded-up run lanes are internal under
the profile contract. Tests verify analog lane independence, undriven internal
complement labels, and failure when the profile interpretation is removed.
This is an explicit working assumption, not a verified schematic extraction.

## Volatile and AB/Out drain correction

The volatile bank is centered immediately below A, matching A's active [2:-2]
lane slice. Its 66.55 um height requires clearance from Out's left-side drain
strip. Out moves down by an additional 44 um (whole 22 um native row units);
the shared drain decoder gets matching passive spacer rows. The B-bottom/output
switch abutment is retained, while the output-switch-to-Out connection spans
the explicit clearance. This is an intentional placement gap, not an assumed
abutment across empty space.

Drain anchors now identify the host and its logical row/column, rather than
the first occurrence of SWC_Drain. This fixes the physical backend reordering
that previously anchored Out's switch strip to A. Tests exercise reordered
backend item dictionaries as well as the model's construction ordering.

Electrical checks verify decoder selections and all programming drain lanes,
reserved read slots, A/B read separation through the cutoff, shared programming
drains, frame-exposed direct/indirect drain rails, cutoff PROG pass-through,
and A/B/Out Vsel continuity. The current 350nm model has 151 instances.
The original 16nm graph is unchanged, and all 52 unit tests pass.

These checks use generated Python definitions and circuit nets. No GDS or
technology LEF contents were read, and physical synthesis was not rerun.
