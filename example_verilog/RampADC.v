module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VPWRrow_0(net108), .VINJrow_0(net106), .GNDrow_0(net112[0]), .VTUNrow_0(net104), .Vgrow_0(net102), .VD_Prow_0(net89), .VD_Rrow_0(net87), .Vselrow_0(net103), .PROGrow_0(net105), .VIN_PLUSrow_0(net108), .VIN_MINUSrow_0(net107[0]), .Voutrow_0(net116));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VPWR_brow_0(net113[0]), .VINJ_brow_0(net114), .GND_brow_0(net112[0]), .VD_Prow_0(net90), .VD_Rrow_0(net88), .VIN_PLUSrow_0(net116), .VIN_MINUSrow_0(net111), .Voutrow_0(net115));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net96), .decode_n0_VINJ_b_0_(net106), .decode_n0_GNDV(net112[0]), .decode_n0_n0_IN_1_(net98), .decode_n0_n0_IN_0_(net97));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net99), .switch_n0_RUN_IN_1_(net99), .switch_n0_VINJ_T(net106), .switch_n0_GND_B_0_(net112[0]), .switch_n0_CTRL_B_0_(net103), .switch_n0_Vg_0_(net102), .switch_n0_PROG(net105), .switch_n0_RUN(net101), .switch_n0_Vgsel(net100));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(2), .decode_n0_IN_1_(net94), .decode_n0_IN_0_(net93), .decode_n0_ENABLE(net95));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(1), .type(drain_select), .switch_n0_prog_drainrail(net91), .switch_n0_run_drainrail(net92), .switch_n0_VINJ(net106), .switch_n0_GND(net112[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net89), .switch_n0_PR_1_(net90), .switch_n0_In_0_(net87), .switch_n0_In_1_(net88), .switch_n0_VDD(net114), .switch_n0_GND(net112[0]), .switch_n0_RUN(net101));


	/* Island 1 */
	Capacitor_80ff I__0 (.island_num(1), .row(0), .col(0), .Top(net116), .Bot(net112[0]));
	Capacitor_80ff I__1 (.island_num(1), .row(1), .col(0), .Top(net116), .Bot(net112[0]));
	Capacitor_80ff I__2 (.island_num(1), .row(0), .col(1), .Top(net116), .Bot(net112[0]));
	Capacitor_80ff I__3 (.island_num(1), .row(1), .col(1), .Top(net116), .Bot(net112[0]));
	Capacitor_80ff I__4 (.island_num(1), .row(0), .col(2), .Top(net116), .Bot(net112[0]));
	Capacitor_80ff I__5 (.island_num(1), .row(1), .col(2), .Top(net116), .Bot(net112[0]));
	TGate_DT I__6 (.island_num(1), .row(0), .col(4), .VDD(net108), .GND(net112[0]), .SELA(net107[0]), .C(net112[0]), .A(net116));
	TGate_DT I__7 (.island_num(1), .row(1), .col(4), .SELA(net115), .C(net110[0]), .A(net112[0]), .B(net109));

 	/*Programming Mux */ 


	/* Island 2 */
	RippleCounter I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(8), .Countrow_0(net79[0:8]), .RST_Lcol_0(net107[0]), .CLKcol_0(net110[0]), .GNDcol_7(net112[0]), .VDDcol_7(net113[0]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net105), .N_n_Run(net101), .N_n_VGRUN(net99), .N_n_VGPROG(net100), .N_n_VTUN(net104), .N_n_gnd(net112[0]), .S_s_gnd(net112[0]), .N_n_vinj(net106), .S_s_vinj(net114), .N_n_avdd(net108), .S_s_avdd(net113[0]), .W_w_DrainB_0_(net93), .W_w_DrainB_1_(net94), .W_w_DrainEnable(net95), .W_w_GateB_0_(net97), .W_w_GateB_1_(net98), .N_n_GateEnable(net96), .S_s_Run_Drainline(net92), .S_s_Prog_Drainline(net91), .S_s_Code_0_(net79[0]), .S_s_Code_1_(net79[1]), .S_s_Code_2_(net79[2]), .S_s_Code_3_(net79[3]), .S_s_Code_4_(net79[4]), .S_s_Code_5_(net79[5]), .S_s_Code_6_(net79[6]), .S_s_Code_7_(net79[7]), .W_w_CLK(net109), .W_w_RST(net107[0]), .W_w_Vin(net111), .E_e_DEBUG_0_(net115), .E_e_DEBUG_1_(net116));
 endmodule