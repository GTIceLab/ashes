## Exposed supply routing access

The wafer5 run now opts into post-placement supply access selection through
`pd_settings.json` -> `supply_access`. This is a shared physical-export feature,
not CAB-specific netlist wiring. It is disabled unless explicitly configured.
The 16nm run has not opted in.

The circuit model and original conventional netlist retain every logical supply
connection. After physical placement and DEF export, the router's input Verilog
can omit buried supply terminals. The original input is saved beside it as
`inputs/TILE_NN.full.v`. Routing uses `inputs/TILE_NN.v`.

Reports are written under the design's `pd` folder:

- `supply_access.json`: per-terminal decisions, geometry, net, preserved cases,
  and removal counts.
- `supply_access.log`: short summary and continuity assumption reminder.

Only the report path is printed to the terminal.

### Configurable electrical and geometric contract

`nets` explicitly selects eligible supply net names. `port_families` explicitly
selects supply port families, obtained by removing the final physical side
suffix. This prevents constant-ground connections on decoder address ports from
being treated as supply access pins. No cell/master names are embedded in the
algorithm. Aliases are not inferred; GND and GND_b, for example, remain separate.

The required flag `same_net_terminals_connected_within_cell: true` declares that
eligible terminals on the same instance and same logical supply net are already
internally connected in the cell. This is an electrical assumption, not a result
of parsing geometry. It follows the existing shared-supply model and the owner's
requested native-abutment policy; it must be checked against the library before
physical signoff. Set no policy to retain the original full routing netlist.

The physical selection then:

1. Uses actual placed macro boxes and extracted physical pin rectangles.
2. Uses native `_n`, `_s`, `_e`, `_w` suffixes as physical access-side declarations.
3. Treats an access face as buried only if abutting neighbors fully cover its
   projected interval and block routing through the pin's metal layer.
4. Links supply components between cells only when same-net, same-layer pin
   rectangles actually touch/overlap with positive edge length or area. A
   point-only contact is insufficient.
5. Omits a buried terminal only if its supply component has a known exposed
   access point, using the declared within-cell continuity and measured
   between-cell contacts. An enclosed component without such access is retained.

Only normal (`N`) orientation and zero-origin macro abstracts are currently
eligible. Unknown placement, unsupported orientation/origin, missing/invalid
rectangles, unknown side/layer, non-contiguous indices, and partial bus-width
mismatches are preserved or excluded from pruning. Uncertain access cannot
justify deleting other terminals. Preserved cases are reported.

The feature does not perform general routing-access, DRC, resistance, current
capacity, EM/IR, or LVS verification. It uses the current macro-blockage model
(layers through each macro's detected top metal), not detailed internal routing
obstructions. Native side declarations and single-rectangle abstract extraction
are inherited limitations. It does not fix the separate partial-bus exporter
issue; mismatched buses are preserved. Where pruning affects only some lanes of
a correctly sized supply bus, isolated, explicitly declared wires preserve bit
positions. No replacement supply/ground ties are invented.

### Current PD and floorplan settings

The owner selected the `cab_rerun` floorplan. The wafer5 run now uses:

- Run-owned `synthesis_settings.json`: `design_limits: [920000, 610000]`,
  corresponding to the reference Tcl's 920 by 610 micron core.
- `pd_settings.json` -> `pins` -> `core_margins`: 10 microns on every side,
  matching the reference Tcl arguments. These are tool core-to-die margins,
  separate from the model's island padding.
- Profile `island_layout.CEW.gap`: 34480 DBU, or 34.48 microns. This is measured
  from the reference generated placement: CSC bottom 373.50 minus AB GorS top
  (294.00 + 45.02) microns. The topology/cell set differs, so this copies the
  separation, not every reference placement coordinate.
- Profile `layout_margin`: 10000 DBU (10 microns).

The reference input DEF says 910 by 510 microns while its Tcl recreates the
floorplan as 920 by 610 with margins. The Tcl dimensions were chosen deliberately;
the inconsistent input DEF was not copied. Model placement fits the new area.
Earlier 800 by 520 area and 75 micron spacing instructions are superseded.

NDR widths and spacing were already equal to the reference and remain unchanged:
M1/M2 widths 1 micron, M3/M4 widths 2 microns; spacing 0.6/0.6/0.8/0.8 microns.
CLOCK_ROUTE's VIA12 minimum is now 1, matching the reference. ANALOG_THICK is
defined with the reference's values, but no automatic assignment is added.
The run explicitly sets `route.default_ndr: ANALOG`; the shared emitter retains
its old fallback for existing projects, and supports null to omit default NDR
assignments. Explicit net NDR tags still take precedence.

The run's route settings now explicitly use 10 iterations and omit forced
antenna-diode insertion and the placeholder antenna cell, matching the reference
Tcl. Iteration count and diode insertion are now configurable emitter settings.
Power-grid generation remains enabled because the newer design declares GND,
VDD and VINJ power nets: the reference's skipped power step was not copied
without checking power delivery. `power_enabled` is configurable, defaulting to
true. Pin layers/dimensions and supply domains have not been changed to the old
design's interface.

### Validation and preview

All 90 tests pass, including synthetic abutment paths, absent exposed access,
partial buses, separate supply names, gaps/layers/orientations, and PD settings.
The model-only check confirms the 920 by 610 core and exact 34.48 micron gap.

On the saved desktop TILE_NN generated DEF, macro abstract and Verilog snapshot,
the preview examined 827 eligible supply terminals and omitted 184: 93 GND,
61 VINJ and 30 VTUN. It retained the remaining terminals. This is a snapshot
preview, not a measured result for the next regenerated layout and not a routing
runtime prediction. Preview files are in `cab-350nm/supply-access-preview` in
the workspace. Source desktop files were not modified.

No user GDS or technology LEF contents were inspected, no physical synthesis or
Innovus routing was executed, and no physical continuity/signoff is claimed.
Run the project's usual synthesis command to generate the new routing inputs
and review `pd/supply_access.json` before comparing routing results. Restore
full terminal export by removing `supply_access` from the run PD settings.


## Native-abutment-only A/B boundary rows

The 350nm A and B matrix_rows recipes now explicitly set boundary_routing to native_abutment. The shared matrix-row assembler tags only the before/after boundary members; body cells stay explicit. The shared physical exporter resolves the tagged model members to exact instance names, verifies their master and placement, and writes those instances with empty port lists in the router Verilog. No cell names are embedded in that exporter.

This suppresses all external terminal connections on TSMC350nm_4x2_Indirect_top_AorB_matrx and TSMC350nm_4x2_Indirect_bot_B_matrx in those recipes, following the owner declaration that these rows connect entirely by native abutment. Logical pin/net relationships, capacity/reserved-lane accounting and placement remain unchanged. inputs/TILE_NN.full.v preserves the full logical export; inputs/TILE_NN.v is the routing export. pd/supply_access.json includes a separate native_abutment_export section, and the text log reports its omission count. This works even with no supply_access policy configured.

Verification on the current 126-instance model selects exactly 21 physical boundary instances and omits 294 terminal connections (189 signal/control/FG plus 105 supply connections). Every nonselected instance connection and every model pin-to-net identity remains unchanged. Physical continuity is an owner assumption, not an electrical extraction result. Defaults remain explicit for other recipes, including 16nm. Restore explicit boundary routing by setting boundary_routing to explicit in the matrix recipe. No synthesis/routing was executed; rebuild to regenerate the routing inputs.


## Current routing access representation (supersedes face pruning)

Directional copies such as X_n/X_s are internal aliases with alternate access shapes, not separate pins requiring an external tie. The 350nm profile enables routing_access, and the shared exporter emits one logical terminal and one LEF PIN/PORT containing all declared equivalent shapes. Both native names remain in the Python interface. The old pd_settings supply_access face-pruning policy is removed; do not enable both policies. A/B boundary rows still export no external connections. Full logical Verilog and pd/routing_access reports are retained. Bus export now preserves unused positions. Tests: 103 pass; both project model launchers pass. Details, declarations, references and limitations: /home/praveen/Tools/ashes/docs/multi-access-pins.md
