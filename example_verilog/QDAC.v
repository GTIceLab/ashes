module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net135), .VINJrow_0(net146[0]), .GNDrow_0(net147[0]), .VTUNrow_0(net98[0]), .Progrow_0(net129[0]), .Vg_0_row_0(net132[0]), .Vg_1_row_0(net133[0]), .Vsel_0_row_0(net130[0]), .Vsel_1_row_0(net131[0]), .VD_P_0_col_0(net84[0:5]), .VD_P_1_col_0(net85[0:5]), .VIN_PLUScol_0(net135), .Voutcol_0(net99[0:5]));
	EPOT I__1 (.island_num(0), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net120), .VINJ_brow_0(net138), .GND_brow_0(net137[0]), .VTUN_brow_0(net123), .Prog_brow_0(net122), .Vg_b_0_row_0(net124), .Vsel_b_0_row_0(net125), .VD_P_0_row_0(net94[0]), .VD_P_1_row_0(net95[0]), .VIN_PLUSrow_0(net135), .Voutrow_0(net128));
	TSMC350nm_Amplifier9T_FGBias I__2 (.island_num(0), .row(7), .col(0), .VPWR(net121), .VPWR_b(net120), .VINJ(net138), .GND(net137[0]), .VTUN(net123), .Vg(net124), .VD_P(net96[0]), .VD_R(net97[0]), .Vsel(net125), .PROG(net122), .VIN_PLUS(net128), .VIN_MINUS(net126), .Vout(net127));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net148), .decode_n0_VINJ_b_0_(net146[0]), .decode_n0_GNDV(net147[0]), .decode_n0_n0_IN_1_(net150), .decode_n0_n0_IN_0_(net149));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net135), .switch_n0_RUN_IN_1_(net135), .switch_n0_GND_T(net147[0]), .switch_n0_VINJ_T(net146[0]), .switch_n0_CTRL_B_0_(net130[0]), .switch_n0_CTRL_B_1_(net131[0]), .switch_n0_Vg_0_(net132[0]), .switch_n0_Vg_1_(net133[0]), .switch_n0_VINJ(net146[0]), .switch_n0_PROG(net129[0]), .switch_n0_RUN(net136), .switch_n0_Vgsel(net134));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net144), .decode_n0_IN_0_(net143), .decode_n2_IN_1_(net142), .decode_n2_IN_0_(net141), .decode_n0_ENABLE(net145));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net139), .switch_n0_run_drainrail(net140), .switch_n0_VINJ(net146[0]), .switch_n0_GND(net147[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net84[0]), .switch_n0_PR_1_(net85[0]), .switch_n0_PR_2_(net84[1]), .switch_n0_PR_3_(net85[1]), .switch_n1_PR_0_(net84[2]), .switch_n1_PR_1_(net85[2]), .switch_n1_PR_2_(net84[3]), .switch_n1_PR_3_(net85[3]), .switch_n2_PR_0_(net84[4]), .switch_n2_PR_1_(net85[4]), .switch_n2_PR_2_(net94[0]), .switch_n2_PR_3_(net95[0]), .switch_n3_PR_0_(net96[0]), .switch_n3_In_0_(net97[0]), .switch_n0_VDD(net138), .switch_n0_GND(net137[0]), .switch_n0_RUN(net136));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net135), .GNDrow_0(net147[0]), .GND_brow_4(net137[0]), .SELAcol_0(net109[0:5]), .Ccol_0(net104[0:5]), .Acol_0(net99[0:5]), .Bcol_0(net128));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net135), .GNDrow_0(net147[0]), .SELAcol_0(net119), .Ccol_0(net114[0:5]), .Acol_0(net128), .Bcol_0(net104[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net114[0:5]), .Botcol_0(net126));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD(net135), .GND(net147[0]), .SELA(net119), .C(net127), .A(net126));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net126), .Bot(net127));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net129[0]), .N_n_Run(net136), .N_n_VGPROG(net134), .N_n_VTUN(net98[0]), .N_n_avdd(net135), .S_s_avdd(net121), .N_n_gnd(net147[0]), .S_s_gnd(net137[0]), .N_n_vinj(net146[0]), .S_s_vinj(net138), .W_w_GateB_0_(net149), .W_w_GateB_1_(net150), .N_n_GateEnable(net148), .W_w_DrainB_0_(net141), .W_w_DrainB_1_(net142), .W_w_DrainB_2_(net143), .W_w_DrainB_3_(net144), .W_w_DrainEnable(net145), .S_s_Run_Drainline(net140), .S_s_Prog_Drainline(net139), .S_s_Vout(net127), .N_n_RST(net119), .N_n_Code_0_(net109[0]), .N_n_Code_1_(net109[1]), .N_n_Code_2_(net109[2]), .N_n_Code_3_(net109[3]), .N_n_Code_4_(net109[4]));
 endmodule