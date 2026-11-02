# Supply routing access after placement

The wafer5 global CAB run enables `supply_access.mode: exposed_boundary` in `pd_settings.json`. The algorithm is shared ASHES code; supply net/family names belong to the run configuration. The original logical circuit and `inputs/TILE_NN.full.v` retain all electrical connections.

## Selection rule

After final DEF placement, examine each declared supply pin against every neighboring macro, regardless of island. A fully covered north/south/east/west contact is not exported as a routing target when its native supply assembly retains exposed access. An isolated cell retains both faces. The top row retains north access, the bottom row south access, and an interior row does not require those covered contacts. West/east use the same rule. A volatile-bank macro can therefore cover an A-matrix contact even though they belong to different islands.

Coverage is checked over the individual pin rectangle's boundary span, not by grid index or by hiding an entire side because one neighbor exists. Multiple neighbors can jointly cover that span. The declared physical side is used even for a recessed label/rectangle. Boundary mode is a placement-access rule, independent of the neighbor's highest-metal layer; it is not a via-clearance or DRC checker. The configured tolerance is zero DBU.

## Abstract and netlist stay consistent

Supply faces remain separate native pins in the generated macro LEF. A blocked face is disconnected in the routing netlist, so its shape is not an alternate shape of a connected supply pin. Physical macro geometry and master names are preserved; no per-instance GDS masters are invented. This avoids the previous multi-access supply pin offering an inaccessible south shape through its north pin name. Buried native pin geometry can still appear in the shared macro abstract as an unconnected pin; it is not a supply routing target for that instance.

Signal aliases are unaffected: for example, gate-decoder analog entry/exit shapes remain a single logical lane with both physical accesses. A bus with only some hidden lanes keeps its original width using declared unconnected placeholder wires.

## Native continuity and missing access

The mode requires explicit declarations that same-net supplies connect within each cell and across native abutments. Only the same actual net is considered continuous; GND and GND_b, or VINJ and VINJ_b, are never merged. Physically touching macro boxes establish assembly continuity under that owner declaration. For array interiors whose terminals were not emitted, a master/family can carry continuity only if all observed bindings for it identify one unambiguous net. Those carrier records create no routing terminal and cannot count as an external supply anchor.

Algorithm-declared native-only contacts also cannot count as exposed external anchors. At least one genuinely exposed routing contact must remain in each proven supply-connected assembly before buried contacts are removed.

The enabled setting `on_no_exposed_access: preserve` keeps contacts in an assembly for which no exposed supply access can be proven, and writes a warning in the design report. `error` instead stops routing-netlist export after writing the report. In either mode this case is not silently disconnected.

## Reports and limits

`pd/routing_access.json` records every candidate, its net, exposure decision, blocking neighbor instance names, removed contacts, native continuity carriers, partial/uncertain cases and assemblies without a proven exposed anchor. `pd/routing_access.log` summarizes counts and names the groups whose contacts were preserved. Detailed warnings stay in files rather than flooding the terminal.

Partially covered rectangles are preserved and flagged; this implementation does not manufacture per-instance clipped macro shapes. Unknown orientation, nonzero macro origin, missing geometry or ambiguous buses are preserved and reported. Exposure selection does not guarantee DRC-clean vias or routing; PD must still check spacing and access.

## Validation

The model/saved-abstract preview removed 172 additional buried supply contacts, while preserving and reporting seven decoder supply groups without proven exposed access. The filtered Verilog passed connected-pin checks against the matching generated macro abstract. Preview artifacts are in `cab-350nm/exposed-supply-preview/`; they are not a physical synthesis run. No user GDS or technology LEF was inspected.

Regressions cover cross-island row coverage, isolated/gapped cells, retained signal aliases, prevention of buried supply aliases, partial coverage, native-only contacts not counting as anchors, and report-before-failure behavior.

## All-signal mode and explicit exceptions

The wafer5 run now enables `scope: all_signals`. Boundary selection covers controls and ordinary signals as well as supplies. S-block E/W fabric access is explicitly retained. Every per-pin exception and preserve-on-error decision is logged as `OVERRIDE`. In this mode native pin faces stay separate and one exposed endpoint represents each same-net internal cell connection. See the all-signal-access guide for the current rules and limitations; earlier supply-only scope statements are superseded.

## Correction: direct-host drain contacts and pinless continuity

The native drain bank now suppresses read/program contacts for its directly abutting host, determined from the existing island reference and zero gap. The remote Out extension still exports its read/program contacts because it crosses a gap. This avoids a fixed A/CEW cell-name list.

Boundary continuity now traverses the entire physically abutting macro component, including pinless helpers. Under the enabled declaration of native same-net continuity, terminals with the same actual logical net in that component share an access path. No new net is assigned to a helper, and different nets are not merged. A real placement gap breaks that component. This supersedes the earlier master/family inference for array-interior carriers and removes that extra inference code.

In the refreshed saved-placement preview, A's four drain-switch instances have no Vd_R/Vd_P routing targets; its three interior instances have no routing terminals at all. Supplies/controls remain only at the outer ends of the A/Out strip. Out's three remote read/program groups remain explicit. There are no supply/control groups using the no-exposed-access preserve override in that preview. Other functional-signal warnings remain logged. The netlist matches its generated macro LEF. These checks are not a new physical routing run.
