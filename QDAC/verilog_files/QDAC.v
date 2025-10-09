module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net121), .VINJrow_0(net149[0]), .GNDrow_0(net150[0]), .VTUNrow_0(net100[0]), .Progrow_0(net132[0]), .Vg_0_row_0(net135[0]), .Vg_1_row_0(net136[0]), .Vsel_0_row_0(net133[0]), .Vsel_1_row_0(net134[0]), .VD_P_0_col_0(net86[0:5]), .VD_P_1_col_0(net87[0:5]), .VIN_PLUScol_0(net121), .Voutcol_0(net101[0:5]));
	EPOT I__1 (.island_num(0), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net123), .VINJ_brow_0(net141), .GND_brow_0(net140[0]), .VTUN_brow_0(net126), .Prog_brow_0(net125), .Vg_b_0_row_0(net127), .Vsel_b_0_row_0(net128), .VD_P_0_row_0(net96[0]), .VD_P_1_row_0(net97[0]), .VIN_PLUSrow_0(net121), .Voutrow_0(net131));
	TSMC350nm_Amplifier9T_FGBias I__2 (.island_num(0), .row(7), .col(0), .VPWR(net124), .VPWR_b(net123), .VINJ(net141), .GND(net140[0]), .VTUN(net126), .Vg(net127), .VD_P(net98[0]), .VD_R(net99[0]), .Vsel(net128), .PROG(net125), .VIN_PLUS(net131), .VIN_MINUS(net129), .Vout(net130));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net151), .decode_n0_VINJ_b_0_(net149[0]), .decode_n0_GNDV(net150[0]), .decode_n0_n0_IN_1_(net153), .decode_n0_n0_IN_0_(net152));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net138), .switch_n0_RUN_IN_1_(net138), .switch_n0_GND_T(net150[0]), .switch_n0_VINJ_T(net149[0]), .switch_n0_CTRL_B_0_(net133[0]), .switch_n0_CTRL_B_1_(net134[0]), .switch_n0_Vg_0_(net135[0]), .switch_n0_Vg_1_(net136[0]), .switch_n0_VINJ(net149[0]), .switch_n0_PROG(net132[0]), .switch_n0_RUN(net139), .switch_n0_Vgsel(net137));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net147), .decode_n0_IN_0_(net146), .decode_n2_IN_1_(net145), .decode_n2_IN_0_(net144), .decode_n0_ENABLE(net148));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net142), .switch_n0_run_drainrail(net143), .switch_n0_VINJ(net149[0]), .switch_n0_GND(net150[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net86[0]), .switch_n0_PR_1_(net87[0]), .switch_n0_PR_2_(net86[1]), .switch_n0_PR_3_(net87[1]), .switch_n1_PR_0_(net86[2]), .switch_n1_PR_1_(net87[2]), .switch_n1_PR_2_(net86[3]), .switch_n1_PR_3_(net87[3]), .switch_n2_PR_0_(net86[4]), .switch_n2_PR_1_(net87[4]), .switch_n2_PR_2_(net96[0]), .switch_n2_PR_3_(net97[0]), .switch_n3_PR_0_(net98[0]), .switch_n3_In_0_(net99[0]), .switch_n0_VDD(net141), .switch_n0_GND(net140[0]), .switch_n0_RUN(net139));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net121), .GNDrow_0(net150[0]), .GND_brow_4(net140[0]), .SELAcol_0(net111[0:5]), .Ccol_0(net106[0:5]), .Acol_0(net101[0:5]), .Bcol_0(net131));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net121), .GNDrow_0(net150[0]), .SELAcol_0(net122), .Ccol_0(net116[0:5]), .Acol_0(net131), .Bcol_0(net106[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net116[0:5]), .Botcol_0(net129));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD(net121), .GND(net150[0]), .SELA(net122), .C(net130), .A(net129));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net129), .Bot(net130));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net132[0]), .N_n_Run(net139), .N_n_VGPROG(net137), .N_n_VGRUN(net138), .N_n_VTUN(net100[0]), .N_n_avdd(net121), .S_s_avdd(net124), .N_n_gnd(net150[0]), .S_s_gnd(net140[0]), .N_n_vinj(net149[0]), .S_s_vinj(net141), .W_w_GateB_0_(net152), .W_w_GateB_1_(net153), .N_n_GateEnable(net151), .W_w_DrainB_0_(net144), .W_w_DrainB_1_(net145), .W_w_DrainB_2_(net146), .W_w_DrainB_3_(net147), .W_w_DrainEnable(net148), .S_s_Run_Drainline(net143), .S_s_Prog_Drainline(net142), .S_s_Vout(net130), .N_n_RST(net122), .N_n_Code_0_(net111[0]), .N_n_Code_1_(net111[1]), .N_n_Code_2_(net111[2]), .N_n_Code_3_(net111[3]), .N_n_Code_4_(net111[4]), .E_e_DEBUG_0_(net101[0]), .E_e_DEBUG_1_(net101[1]), .E_e_DEBUG_2_(net101[2]), .E_e_DEBUG_3_(net101[3]), .E_e_DEBUG_4_(net101[4]));
 endmodule