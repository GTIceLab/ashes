module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGInputs_Bias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net137[0]), .VINJrow_0(net151[0]), .GNDrow_0(net152[0]), .VTUNrow_0(net138[0]), .Vg_0_row_0(net115[0]), .Vg_1_row_0(net116[0]), .Vg_b_0_row_4(net117[0]), .Vd_P_0_col_0(net93[0:5]), .Vd_P_1_col_0(net94[0:5]), .Vd_Rcol_0(net95[0:5]), .Vsel_0_row_0(net113[0]), .Vsel_1_row_0(net114[0]), .Progrow_0(net139[0]), .VIN_PLUScol_0(net119[0:5]), .VIN_MINUScol_0(net118), .Voutcol_0(net118));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net153), .decode_n0_VINJ_b_0_(net151[0]), .decode_n0_GNDV(net152[0]), .decode_n0_n0_IN_1_(net155), .decode_n0_n0_IN_0_(net154));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net140), .switch_n0_RUN_IN_1_(net140), .switch_n0_GND_T(net152[0]), .switch_n0_VINJ_T(net151[0]), .switch_n0_CTRL_B_0_(net113[0]), .switch_n0_CTRL_B_1_(net114[0]), .switch_n0_Vg_0_(net115[0]), .switch_n0_Vg_1_(net116[0]), .switch_n0_VINJ(net151[0]), .switch_n0_PROG(net139[0]), .switch_n0_RUN(net142), .switch_n0_Vgsel(net141));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net149), .decode_n0_IN_0_(net148), .decode_n2_IN_1_(net147), .decode_n2_IN_0_(net146), .decode_n0_ENABLE(net150));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net144), .switch_n0_run_drainrail(net145), .switch_n0_VINJ(net151[0]), .switch_n0_GND(net152[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net93[0]), .switch_n0_PR_1_(net94[0]), .switch_n0_PR_2_(net93[1]), .switch_n0_PR_3_(net94[1]), .switch_n1_PR_0_(net93[2]), .switch_n1_PR_1_(net94[2]), .switch_n1_PR_2_(net93[3]), .switch_n1_PR_3_(net94[3]), .switch_n2_PR_0_(net93[4]), .switch_n2_PR_1_(net94[4]), .switch_n2_PR_2_(net108[0]), .switch_n2_PR_3_(net109[0]), .switch_n3_PR_0_(net110[0]), .switch_n3_PR_1_(net111[0]), .switch_n3_PR_2_(net112[0]), .switch_n0_In_0_(net95[0]), .switch_n0_In_1_(net95[1]), .switch_n0_In_2_(net95[2]), .switch_n0_In_3_(net95[3]), .switch_n1_In_0_(net95[4]), .switch_n0_VDD(net143), .switch_n0_GND(net152[0]), .switch_n0_RUN(net142));


	/* Island 1 */
	EPOT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .Vg_0_row_0(net117[0]), .VD_P_0_row_0(net108[0]), .VD_P_1_row_0(net109[0]), .VIN_PLUSrow_0(net137[0]), .Voutrow_0(net124));
	EPOT I__1 (.island_num(1), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net133), .VINJ_brow_0(net143), .GND_brow_0(net132), .VTUN_brow_0(net134), .Vg_b_0_row_0(net136), .Vsel_b_0_row_0(net135), .VD_P_0_row_0(net110[0]), .VD_P_1_row_0(net111[0]), .VIN_PLUSrow_0(net137[0]), .Voutrow_0(net125));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_AnalogBuffer I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VTUNrow_0(net134), .VDDrow_0(net133), .GNDrow_0(net132), .VINJrow_0(net143), .Vgrow_0(net136), .Vd_Prow_0(net112[0]), .Vselrow_0(net135), .Vinrow_0(net118), .Voutrow_0(net131));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net137[0]), .GNDrow_0(net152[0]), .SELAcol_0(net126[0:5]), .Ccol_0(net119[0:5]), .Acol_0(net124), .Bcol_0(net125));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net139[0]), .N_n_Run(net142), .N_n_VGRUN(net140), .N_n_VGPROG(net141), .N_n_VTUN(net138[0]), .N_n_avdd(net137[0]), .S_s_avdd(net133), .N_n_gnd(net152[0]), .S_s_gnd(net132), .N_n_vinj(net151[0]), .S_s_vinj(net143), .W_w_DrainB_0_(net146), .W_w_DrainB_1_(net147), .W_w_DrainB_2_(net148), .W_w_DrainB_3_(net149), .W_w_DrainEnable(net150), .W_w_GateB_0_(net154), .W_w_GateB_1_(net155), .N_n_GateEnable(net153), .S_s_Run_Drainline(net145), .S_s_Prog_Drainline(net144), .S_s_Vout(net131), .E_e_Code_0_(net126[0]), .E_e_Code_1_(net126[1]), .E_e_Code_2_(net126[2]), .E_e_Code_3_(net126[3]), .E_e_Code_4_(net126[4]), .S_s_DEBUG_0_(net124), .S_s_DEBUG_1_(net125));
 endmodule