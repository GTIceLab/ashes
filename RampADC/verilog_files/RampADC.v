module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VINJrow_0(net126), .GNDrow_0(net134), .VTUNrow_0(net129), .Vgrow_0(net127), .VD_Prow_0(net116), .VD_Rrow_0(net114), .Vselrow_0(net128), .PROGrow_0(net130), .VIN_PLUSrow_0(net133[0]), .VIN_MINUSrow_0(net132[0]), .Voutrow_0(net131));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_Prow_0(net117), .VD_Rrow_0(net115), .VIN_PLUSrow_0(net131), .VIN_MINUSrow_0(net135));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net122), .decode_n0_GND_b_1_(net134), .decode_n0_VINJV(net125), .decode_n0_n0_IN_1_(net124), .decode_n0_n0_IN_0_(net123));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_GND(net134), .switch_n0_CTRL_B_0_(net128), .switch_n0_Vg_0_(net127), .switch_n0_VINJ(net126));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(2), .decode_n0_VINJ(net121), .decode_n0_GND(net120[0]), .decode_n0_IN_1_(net119), .decode_n0_IN_0_(net118));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(1), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net116), .switch_n0_PR_1_(net117), .switch_n0_In_0_(net114), .switch_n0_In_1_(net115));


	/* Island 1 */
	Capacitor_80ff I__0 (.island_num(1), .row(0), .col(0), .Top(net131), .Bot(net134));
	Capacitor_80ff I__1 (.island_num(1), .row(1), .col(0), .Top(net131), .Bot(net134));
	Capacitor_80ff I__2 (.island_num(1), .row(0), .col(1), .Top(net131), .Bot(net134));
	Capacitor_80ff I__3 (.island_num(1), .row(1), .col(1), .Top(net131), .Bot(net134));
	Capacitor_80ff I__4 (.island_num(1), .row(0), .col(2), .Top(net131), .Bot(net134));
	Capacitor_80ff I__5 (.island_num(1), .row(1), .col(2), .Top(net131), .Bot(net134));
	TGate_DT I__6 (.island_num(1), .row(1), .col(4), .VDD(net133[0]), .GND(net134), .SELA(net132[0]), .C(net134), .A(net131));

 	/*Programming Mux */ 


	/* Island 2 */
	RippleCounter I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(14), .Countrow_0(net99[0:14]), .RST_Lcol_0(net132[0:1]), .CLKcol_0(net113[0:1]), .GNDcol_13(net120[0:1]), .VDDcol_13(net133[0:1]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net130), .N_n_VTUN(net129), .N_n_AVDD(net133[0]), .N_n_gnd(net134), .S_s_gnd(net120[0]), .N_n_vinj(net125), .S_s_vinj(net121), .W_w_DrainB_0_(net118), .W_w_DrainB_1_(net119), .W_w_GateB_0_(net123), .W_w_GateB_1_(net124), .N_n_GateEnable(net122), .S_s_Code_0_(net99[0]), .S_s_Code_1_(net99[1]), .S_s_Code_2_(net99[2]), .S_s_Code_3_(net99[3]), .S_s_Code_4_(net99[4]), .S_s_Code_5_(net99[5]), .S_s_Code_6_(net99[6]), .S_s_Code_7_(net99[7]), .S_s_Code_8_(net99[8]), .S_s_Code_9_(net99[9]), .S_s_Code_10_(net99[10]), .S_s_Code_11_(net99[11]), .S_s_Code_12_(net99[12]), .S_s_Code_13_(net99[13]), .W_w_CLK(net113[0]), .W_w_RST(net132[0]), .W_w_Vin(net135));
 endmodule