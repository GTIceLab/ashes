module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net120), .VINJrow_0(net148[0]), .GNDrow_0(net149[0]), .VTUNrow_0(net99[0]), .Progrow_0(net131[0]), .Vg_0_row_0(net134[0]), .Vg_1_row_0(net135[0]), .Vsel_0_row_0(net132[0]), .Vsel_1_row_0(net133[0]), .VD_P_0_col_0(net85[0:5]), .VD_P_1_col_0(net86[0:5]), .VIN_PLUScol_0(net120), .Voutcol_0(net100[0:5]));
	EPOT I__1 (.island_num(0), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net122), .VINJ_brow_0(net140), .GND_brow_0(net139[0]), .VTUN_brow_0(net125), .Prog_brow_0(net124), .Vg_b_0_row_0(net126), .Vsel_b_0_row_0(net127), .VD_P_0_row_0(net95[0]), .VD_P_1_row_0(net96[0]), .VIN_PLUSrow_0(net120), .Voutrow_0(net130));
	TSMC350nm_Amplifier9T_FGBias I__2 (.island_num(0), .row(7), .col(0), .VPWR(net123), .VPWR_b(net122), .VINJ(net140), .GND(net139[0]), .VTUN(net125), .Vg(net126), .VD_P(net97[0]), .VD_R(net98[0]), .Vsel(net127), .PROG(net124), .VIN_PLUS(net130), .VIN_MINUS(net128), .Vout(net129));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net150), .decode_n0_VINJ_b_0_(net148[0]), .decode_n0_GNDV(net149[0]), .decode_n0_n0_IN_1_(net152), .decode_n0_n0_IN_0_(net151));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net137), .switch_n0_RUN_IN_1_(net137), .switch_n0_GND_T(net149[0]), .switch_n0_VINJ_T(net148[0]), .switch_n0_CTRL_B_0_(net132[0]), .switch_n0_CTRL_B_1_(net133[0]), .switch_n0_Vg_0_(net134[0]), .switch_n0_Vg_1_(net135[0]), .switch_n0_VINJ(net148[0]), .switch_n0_PROG(net131[0]), .switch_n0_RUN(net138), .switch_n0_Vgsel(net136));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net146), .decode_n0_IN_0_(net145), .decode_n2_IN_1_(net144), .decode_n2_IN_0_(net143), .decode_n0_ENABLE(net147));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net141), .switch_n0_run_drainrail(net142), .switch_n0_VINJ(net148[0]), .switch_n0_GND(net149[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net85[0]), .switch_n0_PR_1_(net86[0]), .switch_n0_PR_2_(net85[1]), .switch_n0_PR_3_(net86[1]), .switch_n1_PR_0_(net85[2]), .switch_n1_PR_1_(net86[2]), .switch_n1_PR_2_(net85[3]), .switch_n1_PR_3_(net86[3]), .switch_n2_PR_0_(net85[4]), .switch_n2_PR_1_(net86[4]), .switch_n2_PR_2_(net95[0]), .switch_n2_PR_3_(net96[0]), .switch_n3_PR_0_(net97[0]), .switch_n3_In_0_(net98[0]), .switch_n0_VDD(net140), .switch_n0_GND(net139[0]), .switch_n0_RUN(net138));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net120), .GNDrow_0(net149[0]), .GND_brow_4(net139[0]), .SELAcol_0(net110[0:5]), .Ccol_0(net105[0:5]), .Acol_0(net100[0:5]), .Bcol_0(net130));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net120), .GNDrow_0(net149[0]), .SELAcol_0(net121), .Ccol_0(net115[0:5]), .Acol_0(net130), .Bcol_0(net105[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net115[0:5]), .Botcol_0(net128));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD(net120), .GND(net149[0]), .SELA(net121), .C(net129), .A(net128));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net128), .Bot(net129));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net131[0]), .N_n_Run(net138), .N_n_VGPROG(net136), .N_n_VGRUN(net137), .N_n_VTUN(net99[0]), .N_n_avdd(net120), .S_s_avdd(net123), .N_n_gnd(net149[0]), .S_s_gnd(net139[0]), .N_n_vinj(net148[0]), .S_s_vinj(net140), .W_w_GateB_0_(net151), .W_w_GateB_1_(net152), .N_n_GateEnable(net150), .W_w_DrainB_0_(net143), .W_w_DrainB_1_(net144), .W_w_DrainB_2_(net145), .W_w_DrainB_3_(net146), .W_w_DrainEnable(net147), .S_s_Run_Drainline(net142), .S_s_Prog_Drainline(net141), .S_s_Vout(net129), .N_n_RST(net121), .N_n_Code_0_(net110[0]), .N_n_Code_1_(net110[1]), .N_n_Code_2_(net110[2]), .N_n_Code_3_(net110[3]), .N_n_Code_4_(net110[4]));
 endmodule