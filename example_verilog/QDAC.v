module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(6), .matrix_col(1), .VDDrow_0(net122), .VDD_brow_5(net108[0]), .VINJrow_0(net133[0]), .VINJ_brow_5(net125[0]), .GNDrow_0(net134[0]), .GND_brow_5(net124[0]), .VTUNrow_0(net91[0]), .VTUN_brow_5(net110[0]), .Progrow_0(net116[0]), .Prog_brow_5(net109[0]), .Vg_0_row_0(net119[0]), .Vg_1_row_0(net120[0]), .Vg_b_0_row_5(net111[0]), .Vsel_0_row_0(net117[0]), .Vsel_1_row_0(net118[0]), .Vsel_b_0_row_5(net112[0]), .VD_P_0_col_0(net77[0:6]), .VD_P_1_col_0(net78[0:6]), .VIN_PLUScol_0(net122), .Voutcol_0(net2[0:6]));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(7), .col(0), .VDD(net108[0]), .VINJ(net125[0]), .GND(net124[0]), .VTUN(net110[0]), .Vg(net111[0]), .VD_P(net89[0]), .VD_R(net90[0]), .Vsel(net112[0]), .PROG(net109[0]), .VIN_PLUS(net2[5]), .VIN_MINUS(net113), .Vout(net114));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net135), .decode_n0_VINJ_b_0_(net133[0]), .decode_n0_GNDV(net134[0]), .decode_n0_n0_IN_1_(net137), .decode_n0_n0_IN_0_(net136));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net122), .switch_n0_RUN_IN_1_(net122), .switch_n0_GND_T(net134[0]), .switch_n0_VINJ_T(net133[0]), .switch_n0_CTRL_B_0_(net117[0]), .switch_n0_CTRL_B_1_(net118[0]), .switch_n0_Vg_0_(net119[0]), .switch_n0_Vg_1_(net120[0]), .switch_n0_VINJ(net133[0]), .switch_n0_PROG(net116[0]), .switch_n0_RUN(net123), .switch_n0_Vgsel(net121));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net131), .decode_n0_IN_0_(net130), .decode_n2_IN_1_(net129), .decode_n2_IN_0_(net128), .decode_n0_ENABLE(net132));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net126), .switch_n0_run_drainrail(net127), .switch_n0_VINJ(net133[0]), .switch_n0_GND(net134[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net77[0]), .switch_n0_PR_1_(net78[0]), .switch_n0_PR_2_(net77[1]), .switch_n0_PR_3_(net78[1]), .switch_n1_PR_0_(net77[2]), .switch_n1_PR_1_(net78[2]), .switch_n1_PR_2_(net77[3]), .switch_n1_PR_3_(net78[3]), .switch_n2_PR_0_(net77[4]), .switch_n2_PR_1_(net78[4]), .switch_n2_PR_2_(net77[5]), .switch_n2_PR_3_(net78[5]), .switch_n3_PR_0_(net89[0]), .switch_n3_In_0_(net90[0]), .switch_n0_VDD(net125[0]), .switch_n0_GND(net124[0]), .switch_n0_RUN(net123));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net122), .GNDrow_0(net134[0]), .GND_brow_4(net124[0]), .SELAcol_0(net97[0:5]), .Ccol_0(net92[0:5]), .Bcol_0(net2));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net122), .GNDrow_0(net134[0]), .SELAcol_0(net107), .Ccol_0(net102[0:5]), .Acol_0(net2), .Bcol_0(net92[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net102[0:5]), .Botcol_0(net113));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD(net122), .GND(net134[0]), .SELA(net107), .C(net114), .A(net113));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net113), .Bot(net114));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net116[0]), .N_n_Run(net123), .N_n_VGPROG(net121), .N_n_VTUN(net91[0]), .N_n_avdd(net122), .S_s_avdd(net108[0]), .N_n_gnd(net134[0]), .S_s_gnd(net124[0]), .N_n_vinj(net133[0]), .S_s_vinj(net125[0]), .W_w_GateB_0_(net136), .W_w_GateB_1_(net137), .N_n_GateEnable(net135), .W_w_DrainB_0_(net128), .W_w_DrainB_1_(net129), .W_w_DrainB_2_(net130), .W_w_DrainB_3_(net131), .W_w_DrainEnable(net132), .S_s_Run_Drainline(net127), .S_s_Prog_Drainline(net126), .S_s_Vout(net114), .N_n_RST(net107), .N_n_Code_0_(net97[0]), .N_n_Code_1_(net97[1]), .N_n_Code_2_(net97[2]), .N_n_Code_3_(net97[3]), .N_n_Code_4_(net97[4]));
 endmodule