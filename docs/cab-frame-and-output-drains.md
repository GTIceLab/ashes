# CAB tile frame and side spreading

ASHES now generates ordinary `edit_pin -spread_type side` commands for Cadence. The explicit `-assign` coordinate feature and `paired_ports` settings were removed. Opposite sides retain the original clockwise/counterclockwise spreading directions. No pin positions, placeholder slots, or dummy frame pins are calculated to compensate for unequal counts.

The CAB frame algorithm owns the signal roles. Fabric N/S and E/W buses, and CAB_IN_N/CAB_OUT_S and CAB_IN_E/CAB_OUT_W, are separate electrical nets with matching lane counts and ordering. Control and power directions below are native physical sides, following the original TILE_NN; the coordinate adapter handles the 16nm fabric orientation.

| Interface | Direction | Connection |
|---|---|---|
| GateBits, GateEnable | N input / S output | Existing 16nm buffer input/output; unbuffered pass-through in 350nm |
| DrainBits, DrainEnables, PROG | W input / E output | Existing 16nm buffer input/output; unbuffered pass-through in 350nm |
| Scanner_CLK, Scanner_RSTN | N input / S output | Existing buffered 16nm path; native 350nm pass-through |
| Supplies, VGPROG, VGRUN | N / S | Same-net opposite frame access; independent analog lanes are not merged |
| Drainline_Indirect, Drainline_Direct | W / E | Same-net pass-through |
| 350nm RUN | W input / E output | Native control pass-through |

Extra Sblock_S/Sblock_W exports and spare/diagnostic AB_extra and C-block spare exports are removed from tile IO. The physical cells and internal circuitry are preserved. In 16nm the N frame source remains the outer decoder-filler E_w contact; its superseded inner north copy is native-only. In 350nm S/W use only final-column CNS/CEW Vd_R_e contacts. The requested CEW W access keeps its explicit, per-lane logged boundary override.

The original 16nm TILE_NN is the reference for deciding which interfaces belong on the frame. Signals supplied internally or by declared native abutment are not exported simply because a cell has a label. In particular, Activation_0_Vg_pFET/Vg_p/Vg_m and Scanner_D_In_s/D_Out_n/COM are removed. Scanner COM/Din/Dout retain the three design-owned A-matrix input bindings; activation bias contacts are native-only. Scanner clock/reset retain their external directional control pairs. WTA's existing configuration-memory wiring is unchanged.

| Process | North | South | East | West | Remaining process-specific local ports |
|---|---:|---:|---:|---:|---|
| 16nm | 32 | 32 | 28 | 28 | None |
| 350nm | 36 | 36 | 29 | 29 | None |

For 350nm the owner confirmed that decoder analog run inputs use the common VGRUN rail, like 16nm. The profile declares gate_analog_input_net: VGRUN, so the CAB adapter binds all existing decoder run inputs to that rail instead of exposing Gate_analog_in. Profiles without this declaration retain independent-input behavior; the shared decoder algorithm itself is not globally changed. Access still enters through the decoder's outer pass-through terminals; the existing 4 um decoder-to-switch bridge remains.

The owner also confirmed that WTA, WTA_B, WTA_bot_bias, Bot_GATE, Bot_IREF and Bot_Vg are native-only. The 350nm activation profile removes their exports and marks the corresponding rail/port roles native. This does not tie those six signals together, rename them, fabricate physical pins, or invent a configuration-memory driver. Their connectivity relies on the owner's native-abutment contract. Generic component metadata now allows expose_bias_roles to select public bias roles independently of native-abutment annotations.

Both processes now have no unmatched local frame ports. Opposite paired lists have equal counts and normal side spreading. The remaining process count differences are explicit 350nm power/control roles, not added dummy pins.

The new global `algorithms/cab/tile_frame.py` composes frame roles from builder interfaces, not fixed instance IDs or lane counts. The CAB generators provide their actual control endpoints. Existing 16nm buffers retain separate input/output nets; 350nm gains no invented buffers or level shifters. Shared frame Verilog alias serialization now works per lane and retains canonical supply names, avoiding the previous scalar patch-wire bus collapse.

The 350nm remote Out-matrix routing fix remains: all 12 read and all 12 program lanes connect to the corresponding extended AB SWC_Drain lanes using west-facing Out contacts. Other matrix contacts retain native-only behavior. C-block source access uses south-facing Vs_s copies. Floorplans, placement, NDR and stripe settings were not changed in this correction.

Validation: 136 unit tests pass. Both actual model frame audits, generated macro-LEF/netlist checks, 350nm output/final-column drain checks, the owner-selected common VGRUN mapping, and 16nm 30 true plus 30 complementary cross-gap selections pass. Two existing unexposed 16nm power accesses remain explicitly logged. No GDS or technology LEF contents were inspected, and no physical routing/DRC run was performed.

Both runs' generated pins.tcl and conventional routing Verilog were synchronized using saved placement-only DEFs and generated macro abstracts. Previous Verilog inputs are retained with `.before_tile_frame_spread` suffixes. Frame audits are in each run's `pd/frame_audit.json`; reloading PD is required. Normal synthesis regeneration will reproduce the corrected frame.
