# 16nm native-abutment routing

The global 16nm runner now carries the 350nm concept of recording logical continuity without requesting router wires for native contacts. It retains 16nm level shifters, memory strips, switch banks, edge cells and TAPs; it does not use the 350nm physical topology.

## A/B drain paths

A/B matrix read/program interfaces and the matching cutoff interfaces are marked native in the legacy builder. Logical nets are unchanged. The A-serving part of the shared drain extension is also native. Its Out-serving part remains explicit because it is remote. This requires per-pin marks to be resolved to individual physical array units: the first four extension switch units are omitted for native A paths, and the remaining three units retain the Out interface. No master-name selection list was added to shared export code.

## Native assembly routing

The run opts into `native_assembly_routing: boundary_only` within its all-signal access policy. Only declared native nets (supply nets declared continuous in the policy, or nets attached to algorithm-marked native contacts) qualify for contraction. Being somewhere in a contiguous macro cluster alone does not declare an arbitrary functional signal connected internally.

A qualified internal net wholly within one physically abutting assembly is omitted as a routing request. External qualified nets, or qualified nets spanning physical gaps, retain one access point per assembly. Logical circuit nets and the full Verilog remain unchanged. For other functional nets, ordinary exposed-contact selection continues without assuming a new internal physical wire.

For a native assembly with no proven exposed access, the explicit preserve override keeps one fallback contact rather than all its buried copies. The selected instance/pin and reason are logged. Strict `error` mode remains available; exact per-contact exceptions also require a reason and are logged.

## Verified preview

- Full logical graph remains identical to the previous global logical export: same macro/master mapping and complete net membership.
- 224 native A/B drain/cutoff terminal references are omitted.
- Power routing targets reduce from 135 to 9.
- Two of those nine are unexposed fallback accesses retained by the explicit override: `I_0_0_7.VTUN_w` and `I_0_0_8.VINJ_n`. Their DRC accessibility has not been established. Removing these last fallbacks safely requires an exposed native access or a deliberate user-selected access override, not silently dropping supply delivery.
- Updated preview has 1903 cell-pin references; the older filtered export had 2253 and the full logical export has 3606.
- Netlist pin preflight against the matching generated 16nm cell macro LEF passes.
- 122 regression tests pass, including per-array-unit A/Out selection and rejection of undeclared internal-net contraction.

Artifacts: `access-preview/TILE_NN.v`, `access-preview/TILE_NN.full.v`, `access-preview/routing_access.json` and `.log`. These are previews made from generated cell metadata, model materialization and saved placement/abstracts. No user GDS or technology LEF was read; physical synthesis was not run. Regenerate synthesis inputs and reload the PD design to apply the new routing export.

The requested 80 um top / 24 um side area trim remains pending the earlier placement-fit choice; it is not silently combined with this routing change.

## A/B end companions, GorS and both decoder chains

The 16nm A/B matrix bodies are declared native-only, and this status now propagates to their end/edge/TAP companions during physical model materialization. Matrix-facing GorS VG_e, VS_e and SEL_e are also native-only. Required external fabric, bias and control access on other structures stays available. This fixes the missing propagation that allowed A/B TAP copies of Vg/Vs/Vsel to become routed ties after the core contacts had been hidden.

Both folded gate and drain decoder selection-output copies, non-root branch enables and passive branch-helper contacts are native-only. Decoder core address buses are accessed through their outer connector/termination interfaces. Local switch selector contacts are native when a local level shifter drives them. A/B local switches with no local shifter retain their routed CSC selection delivery. Every one of the 30 true and 30 complemented A/B selection nets retains destination access in the checked preview.

The drain extension still imported the old local folded decoder package; it now imports the global ASHES folded decoder. Its logical connection graph is unchanged. No new cell-master name cases were added to shared export code. Interface spellings belong to the existing folded-decoder/legacy interfaces.

### S-block reference access

| Interface | Older original CAB_NN/TILE_NN | CAB_NN_abs and current global |
|---|---|---|
| N | SBlock_FILL_GateDecodeCONN.E_w (decoder pass-through) | Sblock_N.N_n |
| E | Sblock_Routing_TAP.OUT_e | Sblock_Routing_TAP.OUT_e |
| S | C_NS VMM read interface | C_NS VMM read interface |
| W | C_EW VMM read interface | C_EW VMM read interface |
| Sblock_S | no separately named port | Sblock_S_1.S_s |
| Sblock_W | no separately named port | Sblock_Routing_TAP.OUT_w |

The older original has 36 fabric lanes; the current device configuration has 12. All 12 current E, Sblock_W and Sblock_S bits remain exported at the outer S-block interfaces. N has a pre-existing mapping difference between the original and CAB_NN_abs; this routing cleanup preserves the current logical design and does not silently reassign it.

### Verification and remaining exceptions

The current saved-placement preview has 846 cell-pin references and passes matching macro-LEF pin validation. Complete logical instance/master and net-membership comparison against the prior full global export is identical, after ignoring arbitrary internal wire names. Both decoder selection-output families and the A/B native matrix/GorS interfaces are absent from routing targets.

All 124 tests pass. Synthetic tests cover whole native bodies propagating to terminations, native interfaces propagating without hiding unrelated signals, and per-array-unit A versus remote Out selection. The 350nm builder is unchanged. Its 605 x 455 um model, 20 um CSC gap, all 30 independent top-access analog lanes, and netlist-to-LEF export checks pass. The new boundary-only native-assembly mode is enabled for 16nm; 350nm retains its prior mode.

Nine power targets remain in the 16nm preview. Two are still unexposed VINJ/VTUN fallbacks under the explicit preserve override and are individually logged. No DRC-clean access is asserted for them. Other geometry/access warnings remain in the report. No user GDS or technology LEF was read, and no physical synthesis was run. Reload regenerated routing inputs to see the changes.
