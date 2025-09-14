module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VINJrow_0(net114), .GNDrow_0(net122), .VTUNrow_0(net117), .Vgrow_0(net115), .VD_Prow_0(net104), .VD_Rrow_0(net102), .Vselrow_0(net116), .PROGrow_0(net118), .VIN_PLUSrow_0(net121[0]), .VIN_MINUSrow_0(net120[0]), .Voutrow_0(net119));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_Prow_0(net105), .VD_Rrow_0(net103), .VIN_PLUSrow_0(net119), .VIN_MINUSrow_0(net123));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net110), .decode_n0_GND_b_1_(net122), .decode_n0_VINJV(net113), .decode_n0_n0_IN_1_(net112), .decode_n0_n0_IN_0_(net111));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_GND(net122), .switch_n0_CTRL_B_0_(net116), .switch_n0_Vg_0_(net115), .switch_n0_VINJ(net114));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(2), .decode_n0_VINJ(net109), .decode_n0_GND(net108[0]), .decode_n0_IN_1_(net107), .decode_n0_IN_0_(net106));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(1), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net104), .switch_n0_PR_1_(net105), .switch_n0_In_0_(net102), .switch_n0_In_1_(net103));


	/* Island 1 */
	Capacitor_80ff I__0 (.island_num(1), .row(0), .col(0), .Top(net119), .Bot(net122));
	Capacitor_80ff I__1 (.island_num(1), .row(1), .col(0), .Top(net119), .Bot(net122));
	Capacitor_80ff I__2 (.island_num(1), .row(0), .col(1), .Top(net119), .Bot(net122));
	Capacitor_80ff I__3 (.island_num(1), .row(1), .col(1), .Top(net119), .Bot(net122));
	Capacitor_80ff I__4 (.island_num(1), .row(0), .col(2), .Top(net119), .Bot(net122));
	Capacitor_80ff I__5 (.island_num(1), .row(1), .col(2), .Top(net119), .Bot(net122));
	TGate_DT I__6 (.island_num(1), .row(1), .col(4), .VDD(net121[0]), .GND(net122), .SELA(net120[0]), .C(net122), .A(net119));

 	/*Programming Mux */ 


	/* Island 2 */
	RippleCounter I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(8), .Countrow_0(net93[0:8]), .RST_Lcol_0(net120[0:1]), .CLKcol_0(net101[0:1]), .GNDcol_7(net108[0:1]), .VDDcol_7(net121[0:1]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net118), .N_n_VTUN(net117), .N_n_AVDD(net121[0]), .N_n_gnd(net122), .S_s_gnd(net108[0]), .N_n_vinj(net113), .S_s_vinj(net109), .W_w_DrainB_0_(net106), .W_w_DrainB_1_(net107), .W_w_GateB_0_(net111), .W_w_GateB_1_(net112), .N_n_GateEnable(net110), .S_s_Code_0_(net93[0]), .S_s_Code_1_(net93[1]), .S_s_Code_2_(net93[2]), .S_s_Code_3_(net93[3]), .S_s_Code_4_(net93[4]), .S_s_Code_5_(net93[5]), .S_s_Code_6_(net93[6]), .S_s_Code_7_(net93[7]), .W_w_CLK(net101[0]), .W_w_RST(net120[0]), .W_w_Vin(net123));
 endmodule