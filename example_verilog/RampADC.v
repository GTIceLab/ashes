module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VPWRrow_0(net108), .VINJrow_0(net105), .GNDrow_0(net113[0]), .VTUNrow_0(net103), .Vgrow_0(net101), .VD_Prow_0(net88), .VD_Rrow_0(net86), .Vselrow_0(net102), .PROGrow_0(net104), .VIN_PLUSrow_0(net108), .VIN_MINUSrow_0(net107[0]), .Voutrow_0(net106));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VPWR_brow_0(net114[0]), .VINJ_brow_0(net115), .GND_brow_0(net113[0]), .VD_Prow_0(net89), .VD_Rrow_0(net87), .VIN_PLUSrow_0(net106), .VIN_MINUSrow_0(net112), .Voutrow_0(net109));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net95), .decode_n0_VINJ_b_0_(net105), .decode_n0_GNDV(net113[0]), .decode_n0_n0_IN_1_(net97), .decode_n0_n0_IN_0_(net96));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net98), .switch_n0_RUN_IN_1_(net98), .switch_n0_VINJ_T(net105), .switch_n0_GND_B_0_(net113[0]), .switch_n0_CTRL_B_0_(net102), .switch_n0_Vg_0_(net101), .switch_n0_PROG(net104), .switch_n0_RUN(net100), .switch_n0_Vgsel(net99));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(2), .decode_n0_IN_1_(net93), .decode_n0_IN_0_(net92), .decode_n0_ENABLE(net94));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(1), .type(drain_select), .switch_n0_prog_drainrail(net90), .switch_n0_run_drainrail(net91), .switch_n0_VINJ(net105), .switch_n0_GND(net113[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net88), .switch_n0_PR_1_(net89), .switch_n0_In_0_(net86), .switch_n0_In_1_(net87), .switch_n0_VDD(net115), .switch_n0_GND(net113[0]), .switch_n0_RUN(net100));


	/* Island 1 */
	Capacitor_80ff I__0 (.island_num(1), .row(0), .col(0), .Top(net106), .Bot(net113[0]));
	Capacitor_80ff I__1 (.island_num(1), .row(1), .col(0), .Top(net106), .Bot(net113[0]));
	Capacitor_80ff I__2 (.island_num(1), .row(0), .col(1), .Top(net106), .Bot(net113[0]));
	Capacitor_80ff I__3 (.island_num(1), .row(1), .col(1), .Top(net106), .Bot(net113[0]));
	Capacitor_80ff I__4 (.island_num(1), .row(0), .col(2), .Top(net106), .Bot(net113[0]));
	Capacitor_80ff I__5 (.island_num(1), .row(1), .col(2), .Top(net106), .Bot(net113[0]));
	TGate_DT I__6 (.island_num(1), .row(0), .col(4), .VDD(net108), .GND(net113[0]), .SELA(net107[0]), .C(net113[0]), .A(net106));
	TGate_DT I__7 (.island_num(1), .row(1), .col(4), .SELA(net109), .C(net111[0]), .A(net113[0]), .B(net110));

 	/*Programming Mux */ 


	/* Island 2 */
	RippleCounter I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(8), .Countrow_0(net78[0:8]), .RST_Lcol_0(net107[0]), .CLKcol_0(net111[0]), .GNDcol_7(net113[0]), .VDDcol_7(net114[0]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net104), .N_n_Run(net100), .N_n_VGRUN(net98), .N_n_VGPROG(net99), .N_n_VTUN(net103), .N_n_gnd(net113[0]), .S_s_gnd(net113[0]), .N_n_vinj(net105), .S_s_vinj(net115), .N_n_avdd(net108), .S_s_avdd(net114[0]), .W_w_DrainB_0_(net92), .W_w_DrainB_1_(net93), .W_w_DrainEnable(net94), .W_w_GateB_0_(net96), .W_w_GateB_1_(net97), .N_n_GateEnable(net95), .S_s_Run_Drainline(net91), .S_s_Prog_Drainline(net90), .S_s_Code_0_(net78[0]), .S_s_Code_1_(net78[1]), .S_s_Code_2_(net78[2]), .S_s_Code_3_(net78[3]), .S_s_Code_4_(net78[4]), .S_s_Code_5_(net78[5]), .S_s_Code_6_(net78[6]), .S_s_Code_7_(net78[7]), .W_w_CLK(net110), .W_w_RST(net107[0]), .W_w_Vin(net112));
 endmodule