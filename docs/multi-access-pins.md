## Internally connected access pins

The owner contract is that directional copies such as X_n and X_s are internally
connected. They support native array pass-through and access from either side;
they require no external tie. Different signals and bus lanes stay separate.

The shared physical exporter now emits one routing terminal and one LEF PIN
containing one PORT with all the equivalent access shapes, at their original
coordinates and layers. It does not select away a face or emit MUSTJOIN.
Shapes in one PORT are strongly connected; separate PORTs have different
semantics. References: [Cadence-authored LEF/DEF 5.8](https://coriolis.lip6.fr/doc/lefdef/lefdefref/LEFSyntax.html),
[Cadence routing discussion](https://community.cadence.com/cadence_technology_forums/f/digital-implementation/57013/innovus-routing-quires-general-advice).

Python definitions retain both native names. A design may connect X_n or X_s;
either resolves to the same routing terminal with both access shapes. The
canonical native name is only an identifier, not a physical-face restriction.
The full logical export remains in inputs/TILE_NN.full.v; the router uses
inputs/TILE_NN.v. Conflicting net assignments on declared aliases stop generation
instead of silently shorting signals.

### Library declarations and generic implementation

The 350nm profile owns routing_access; the CAB adapter attaches this metadata to
the circuit. The shared ASIC exporter applies it across all eligible masters,
without cell names or process-specific branches in multi_access.py.

- same_family_faces_connected explicitly declares the library's convention that
  matching signal families with lowercase directional suffixes are internal
  aliases. It is not assumed for arbitrary libraries by default.
- family_aliases and groups_by_master are explicit profile declarations. Groups
  reuse matrix continuity, volatile pass-through, activation rail and decoder/
  gate-switch rail/control declarations.
- Ordinary buses group matching indices only. Broadcast merging of different
  indices requires an explicit broadcast group. Static-family membership alone
  does not authorize collapsing a bus.
- Missing shapes do not create invented geometry. Incompatible lane sets remain
  separate. Suffixes such as _b are not guessed to mean another signal; that
  requires a profile declaration. Equal voltage alone is not proof of aliasing.

The separately requested A/B top and B-bottom boundary cells remain placed with
empty routing port lists, relying on owner-declared native abutment. Their
logical model remains unchanged, as do the other cells' functional connections.

The old pd_settings supply_access/exposed_abutment face-pruning policy is disabled
for this run: it discarded alternate access faces. Both policies cannot be
enabled simultaneously. Power-grid and floorplan settings remain unchanged.
Libraries without routing_access, including the current 16nm run, keep their
original access-pin representation.

### Bus export correction and reports

The shared conventional Verilog writer now preserves unused bus positions.
Previously it skipped unused lanes, shortening buses and potentially shifting
indices. Unused positions now use distinct, declared isolated wires, never a
supply tie or a wire shared with another terminal. Entirely unused ports are
omitted. This correction also applies to other conventional-Verilog exports.

pd/routing_access.json records native/canonical mapping, access shapes, duplicate
reference counts and separate native-abutment boundary omissions. The text log
is beside it. Rebuild to regenerate the LEF and Verilog together; do not mix
canonical and old ungrouped files.

### Validation and limits

All 103 unit tests pass, including multi-layer geometry, one-PIN/one-PORT output,
either face resolving to the same terminal, distinct signals/lanes, conflict
rejection, explicit broadcast and unused bus positions. Both project model
launchers pass: 184 model instances for 16nm and 126 for 350nm. The CAB adapter
change only attaches policy metadata; no CAB NN signal topology was changed.

Using the current model and saved generated abstracts, the preview consolidates
pins in 12 masters and removes 171 duplicate terminal references, separately
from 294 boundary terminal omissions. All access geometry is retained, with
exact duplicate rectangles deduplicated. Files: cab-350nm/multi-access-preview.

Terminal references are not wire counts. Different physical cell instances can
remain terminals of one signal even where a native array carries the path.
This consolidates within-cell aliases; it does not delete inter-cell connectivity
or infer every array's internal metal path. Internal continuity follows the
explicit library/owner contract, not electrical extraction.

No user GDS or technology LEF was inspected and no physical synthesis, routing,
DRC or LVS was run. Preview LEF and Verilog were checked against each other.

## Algorithm-owned native connection export

Native matrix assemblies now export every body and boundary macro without routed terminals, including Vs, Vg, drain/control nets and supplies such as VTUN. This also applies to edge macros. Logical model nets remain intact. The main native CAB adapter excludes matrix-facing GorS and output-switch source/gate/selection ports, and activation output ports / B GorS input ports where those rows abut. External device bias and control ports remain routable.

The bridged decoder algorithm excludes higher-stage output ports and non-root enables: native bridges provide those connections. Root enable, address pins, leaf outputs and analog interfaces remain explicit. Other decoder algorithms retain their existing behavior.

These rules live in the algorithms, not new profile settings. The shared routing exporter supports both whole-instance and selected-native-port omission, records removed ports/counts in the routing-access report, and preserves the full logical Verilog. Existing boundary-only profile flags are redundant for native matrix assemblies. No process names, cell-master names or fixed placement coordinates were added to the exporter. Legacy matrix builders are unaffected.

This records owner-confirmed native electrical continuity; it is not a geometric overlap detector. If these assemblies are deliberately separated in a future design, their native-abutment algorithm must be changed accordingly. Matrix-only external nets still need a physically accessible peripheral contact for delivery; omission does not fabricate such a contact.

Validation: 104 unit tests pass, including selective-port omission retaining address connections. Saved Desktop macro abstracts currently lack several connected native port names, so the saved-abstract preview fails preflight; no GDS or technology LEF was inspected and physical synthesis was not run.

Drain-decoder leaf OUT and adjoining drain-switch SELECT contacts are also native abutments. The native CAB adapter now omits both endpoints from routing, while preserving logical nets. Address inputs, root enables and non-abutting CSC gate-decoder links remain explicit.

CAB-device functional input ports (for example I1_P_w, I1_N_w, I3_P_w and I3_N_w), as well as functional outputs, are native abutment contacts. The main native adapter marks ports from the declared device interface, without hardcoded pin names. Bias/control ports are not covered by this omission. Logical input/output connections remain intact.

### Native-contact cleanup

Native matrix routing behavior belongs to the assembly algorithm. The obsolete boundary_routing profile knob and its unused validation have been removed. Device interfaces are marked once while resolving declared inputs/outputs; a second scan of device output pins was removed. Routing export contains no cell-master or process-specific tests. It accepts whole-instance or selected-port declarations and validates their matching placement.

Topology remains explicit in the algorithms (matrix banks, decoder stages, and which component interfaces abut). Physical master and port spellings remain library metadata; these are necessary interface definitions, not routing exceptions. External bias/control connections and non-abutting links are not suppressed by a name-based heuristic.

The sectioned S-block programming-drain interface is supplied by native abutment to the adjoining C-block. Its declared drain port is omitted from routing without hardcoded Vd_P/Vd_w spelling; the logical programming net remains intact.

S-block north gate-side fillers retain their outer signal contact as the routing access. The matching inner routing-body port and intermediate connector/pass-through contacts are native abutments and are omitted from routing. Logical nets remain shared. South access stays on the outer bottom routing cell, west on SEC1, east on SEC3. The legacy 16nm implementation instead obtains its lateral routing-band interfaces through companion termination/TAP OUT ports. These are different physical cell organizations, not an implied common side-name mapping.

S-block gate-return and selection-return ports (currently Vg_b_s and Vsel_b_s) are native continuations. The sectioned algorithm retains their logical lane correspondence and suppresses their routing terminals. North-side decoder/switch access remains explicit. This uses interface roles, not a blanket rule shorting every _b pin to a similarly named signal.

The B-cutoff functional interface (B-read, A-read and programming paths) is native continuation through the abutting A/B assembly. Both matrix terminals and cutoff functional contacts are excluded from routing. Supply/control access outside those declared functional roles is unchanged. Extended drain-to-Out paths across a gap remain explicit.

The north faces of the banks directly below A and B (volatile and output-switch banks) are native matrix-abutment faces. All contacts on those faces, including selection and tunneling supplies, are omitted from routing. This uses native port orientation rather than a Vsel/VTUN name exception. Side-facing controls/scanner access remains explicit; no global supply net is deleted.

### Decoder analog pass-through access

Owner-confirmed analog entry/exit ports on each gate-decoder cell are now joined lane by lane in the logical model and declared as physical multi-access aliases. The decoder algorithm obtains their names from its existing analog-input and run-output interfaces. The shared helper validates equal widths and preserves independent lanes. External Gate_analog_in is attached to the decoder entry. Its entry and exit shapes form one physical pin with one PORT; no separate internal tie is routed. The run-output to gate-switch VPWR bridge remains explicit across the existing 4 um gap. No abutment is assumed for that bridge. The scalar global VGRUN-to-RUN_IN path is distinct and has not been shorted to the analog lane bus.

## Supply exposure after placement

Directional supply accesses now remain separate and use final-placement, cross-island coverage checks. Signal multi-access aliases remain enabled. See the exposed-supply-access guide for continuity assumptions, retained uncertain contacts and design logs. This supersedes the older statement that supply filtering and signal multi-access cannot be combined.

## All-signal mode and explicit exceptions

The wafer5 run now enables `scope: all_signals`. Boundary selection covers controls and ordinary signals as well as supplies. S-block E/W fabric access is explicitly retained. Every per-pin exception and preserve-on-error decision is logged as `OVERRIDE`. In this mode native pin faces stay separate and one exposed endpoint represents each same-net internal cell connection. See the all-signal-access guide for the current rules and limitations; earlier supply-only scope statements are superseded.

## Topmost decoder analog access

Analog lanes now continue natively through every cell in their physical decoder column. External Gate_analog_in lanes are taken from the topmost row (including spacing/pass-through masters), not the leaf row near the switches. Intermediate analog-entry and run-output contacts are native-only routing omissions. Leaf RUN_OUT contacts remain available for the explicit bottom bridge to gate switches across the existing gap. The 30 active lanes remain independent. The refreshed preview contains no middle-row VGRUN_n routing targets and matches its LEF; 119 tests pass. This supersedes the earlier leaf-only analog access description.
