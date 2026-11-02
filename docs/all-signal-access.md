# Routing access for all signals

The wafer5 run now sets `supply_access.scope: all_signals`. The historical configuration section name is retained for compatibility; selection is no longer restricted to power supplies. RUN, PROG, drain-line controls and ordinary buses use the same final-placement boundary checks. Different logical nets and bus lanes remain independent.

Each physical contact is checked against all placed macros, across island boundaries. Fully covered contacts can be omitted when the same native net has exposed access in its assembly. Gaps remain routing gaps. Whole-instance and per-port native-abutment declarations continue to apply. Native-only internal nets do not require a router anchor merely because they exist in the logical model.

## Physical faces and repeated contacts

In all-signal mode, directional shapes are exported as separate native LEF pins rather than merging hidden shapes into a connected alias. Within a physical instance, one exposed contact is selected for each actual same-net internal connection; equivalent exposed copies are omitted as routing endpoints. This selection changes only the routing representation, not the logical circuit or physical macro geometry. Decoder analog pass-through lane connectivity remains in the logical model. Its external entry can represent the decoder net, and the connection across a physical gap to a switch still needs routing.

Unambiguous shared-control nets can carry native continuity through array interiors even when no terminal was emitted for those instances. A master/family with multiple observed net bindings is not used to invent an interior connection. Unknown geometry and partially covered pins remain reported rather than fabricated or clipped.

## Explicit exceptions

The S-block west/east fabric interfaces need routing even where adjacent C-blocks cover their declared faces. They are retained through explicit run-level `keep_access_overrides`, using master/port names resolved from the library interface. The shared exporter contains no S-block cell-name exception.

An override requires an exact instance or master selector, a native port, and a nonempty reason. A net selector is optional. For example:

```json
{
  "master": "my_cell",
  "port": "signal_e",
  "reason": "External fabric connection explicitly required here"
}
```

Use `instance` instead of `master` to restrict the exception to a single placed cell, or supply both. There is no wildcard matching. Every applied pin/lane exception is written as `OVERRIDE` in `pd/routing_access.log` and in `access_overrides` in the JSON report. These exceptions override boundary selection, not algorithm-declared native-only wiring.

The existing run setting `on_no_exposed_access: preserve` is also an explicit override of an access-check error. Each affected net/assembly is recorded in `error_overrides` and receives an `OVERRIDE` log entry. Change that setting to `error` for strict failure after the diagnostic report is written. Without exposed access or an explicit preservation setting, the routing netlist is not committed.

## Current verification

The saved-placement/current-model preview removes 319 contacts (276 buried contacts and 43 redundant exposed copies). RUN contacts reduce from 19 to 12; Drainline_Direct and Drainline_Indirect each reduce from 3 to 2. S-block lateral fabric pins are preserved and individually logged. There remain 168 groups without a proven exposed path, retained by the explicit preserve setting, plus two uncertain geometry cases. These exceptions mean the remaining targets are not all proven DRC-accessible.

The preview netlist passes connected-pin validation against its matching native-pin LEF. All 117 unit tests pass. No physical synthesis was run. Regenerate synthesis inputs to apply the all-signal abstract/netlist representation; old routing sessions retain old pin definitions.

See `EXPOSED_SUPPLY_README.md` for the boundary geometry and continuity assumptions; this guide supersedes its earlier supply-only scope and signal-alias behavior for runs enabling `scope: all_signals`.

## Correction: direct-host drain contacts and pinless continuity

The native drain bank now suppresses read/program contacts for its directly abutting host, determined from the existing island reference and zero gap. The remote Out extension still exports its read/program contacts because it crosses a gap. This avoids a fixed A/CEW cell-name list.

Boundary continuity now traverses the entire physically abutting macro component, including pinless helpers. Under the enabled declaration of native same-net continuity, terminals with the same actual logical net in that component share an access path. No new net is assigned to a helper, and different nets are not merged. A real placement gap breaks that component. This supersedes the earlier master/family inference for array-interior carriers and removes that extra inference code.

In the refreshed saved-placement preview, A's four drain-switch instances have no Vd_R/Vd_P routing targets; its three interior instances have no routing terminals at all. Supplies/controls remain only at the outer ends of the A/Out strip. Out's three remote read/program groups remain explicit. There are no supply/control groups using the no-exposed-access preserve override in that preview. Other functional-signal warnings remain logged. The netlist matches its generated macro LEF. These checks are not a new physical routing run.

## Topmost decoder analog access

Analog lanes now continue natively through every cell in their physical decoder column. External Gate_analog_in lanes are taken from the topmost row (including spacing/pass-through masters), not the leaf row near the switches. Intermediate analog-entry and run-output contacts are native-only routing omissions. Leaf RUN_OUT contacts remain available for the explicit bottom bridge to gate switches across the existing gap. The 30 active lanes remain independent. The refreshed preview contains no middle-row VGRUN_n routing targets and matches its LEF; 119 tests pass. This supersedes the earlier leaf-only analog access description.
