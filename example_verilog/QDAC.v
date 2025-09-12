module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(6), .matrix_col(1), .VDDrow_0(net117[5:6]), .VDD_brow_5(net104[0:1]), .VINJrow_0(net128[0:1]), .VINJ_brow_5(net120[0:1]), .GNDrow_0(net129[0:1]), .GND_brow_5(net119[0:1]), .VTUNrow_0(net82[0:1]), .VTUN_brow_5(net106[0:1]), .Progrow_0(net111[0:1]), .Prog_brow_5(net105[0:1]), .Vg_0_row_0(net114[0:1]), .Vg_1_row_0(net115[0:1]), .Vg_b_0_row_5(net107[0:1]), .Vsel_0_row_0(net112[0:1]), .Vsel_1_row_0(net113[0:1]), .Vsel_b_0_row_5(net108[0:1]), .VD_P_0_col_0(net68[0:6]), .VD_P_1_col_0(net69[0:6]), .VIN_PLUScol_0(net117[0:6]), .Voutcol_0(net2[0:6]));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(7), .col(0), .VDD(net104[0]), .VINJ(net120[0]), .GND(net119[0]), .VTUN(net106[0]), .Vg(net107[0]), .VD_P(net80[0]), .VD_R(net81[0]), .Vsel(net108[0]), .PROG(net105[0]), .VIN_PLUS(net109[4]), .VIN_MINUS(net109[4]), .Vout(net110));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net130), .decode_n0_VINJ_b_0_(net128[0]), .decode_n0_GNDV(net129[0]), .decode_n0_n0_IN_1_(net132), .decode_n0_n0_IN_0_(net131));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net117[5]), .switch_n0_RUN_IN_1_(net117[5]), .switch_n0_GND_T(net129[0]), .switch_n0_VINJ_T(net128[0]), .switch_n0_CTRL_B_0_(net112[0]), .switch_n0_CTRL_B_1_(net113[0]), .switch_n0_Vg_0_(net114[0]), .switch_n0_Vg_1_(net115[0]), .switch_n0_VINJ(net128[0]), .switch_n0_PROG(net111[0]), .switch_n0_RUN(net118), .switch_n0_Vgsel(net116));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net126), .decode_n0_IN_0_(net125), .decode_n2_IN_1_(net124), .decode_n2_IN_0_(net123), .decode_n0_ENABLE(net127));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net121), .switch_n0_run_drainrail(net122), .switch_n0_VINJ(net128[0]), .switch_n0_GND(net129[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net68[0]), .switch_n0_PR_1_(net69[0]), .switch_n0_PR_2_(net68[1]), .switch_n0_PR_3_(net69[1]), .switch_n1_PR_0_(net68[2]), .switch_n1_PR_1_(net69[2]), .switch_n1_PR_2_(net68[3]), .switch_n1_PR_3_(net69[3]), .switch_n2_PR_0_(net68[4]), .switch_n2_PR_1_(net69[4]), .switch_n2_PR_2_(net68[5]), .switch_n2_PR_3_(net69[5]), .switch_n3_PR_0_(net80[0]), .switch_n3_In_0_(net81[0]), .switch_n0_VDD(net120[0]), .switch_n0_GND(net119[0]), .switch_n0_RUN(net118));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net117[5:6]), .GNDrow_0(net129[0:1]), .GND_brow_4(net119[0:1]), .SELAcol_0(net88[0:5]), .Ccol_0(net83[0:5]), .Acol_0(net2[0:5]), .Bcol_0(net2[0:5]));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net117[5:6]), .GNDrow_0(net129[0:1]), .SELAcol_0(net103[0:5]), .Ccol_0(net97[0:5]), .Acol_0(net2[0:5]), .Bcol_0(net83[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net97[0:5]), .Botcol_0(net109[0:5]));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD(net117[5]), .GND(net129[0]), .SELA(net103[4]), .C(net110), .A(net109[4]));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net109[4]), .Bot(net110));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net111[0]), .N_n_Run(net118), .N_n_VGPROG(net116), .N_n_VTUN(net82[0]), .N_n_avdd(net117[5]), .S_s_avdd(net104[0]), .N_n_gnd(net129[0]), .S_s_gnd(net119[0]), .N_n_vinj(net128[0]), .S_s_vinj(net120[0]), .W_w_GateB_0_(net131), .W_w_GateB_1_(net132), .N_n_GateEnable(net130), .W_w_DrainB_0_(net123), .W_w_DrainB_1_(net124), .W_w_DrainB_2_(net125), .W_w_DrainB_3_(net126), .W_w_DrainEnable(net127), .S_s_Run_Drainline(net122), .S_s_Prog_Drainline(net121), .S_s_Vout(net110), .N_n_RST(net103[4]), .N_n_Code_0_(net88[0]), .N_n_Code_1_(net88[1]), .N_n_Code_2_(net88[2]), .N_n_Code_3_(net88[3]), .N_n_Code_4_(net88[4]));
 endmodule