module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGInputs_Bias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net136[0]), .VINJrow_0(net150[0]), .GNDrow_0(net151[0]), .VTUNrow_0(net137[0]), .Vg_0_row_0(net114[0]), .Vg_1_row_0(net115[0]), .Vg_b_0_row_4(net116[0]), .Vd_P_0_col_0(net92[0:5]), .Vd_P_1_col_0(net93[0:5]), .Vd_Rcol_0(net94[0:5]), .Vsel_0_row_0(net112[0]), .Vsel_1_row_0(net113[0]), .Progrow_0(net138[0]), .VIN_PLUScol_0(net118[0:5]), .VIN_MINUScol_0(net117), .Voutcol_0(net117));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net152), .decode_n0_VINJ_b_0_(net150[0]), .decode_n0_GNDV(net151[0]), .decode_n0_n0_IN_1_(net154), .decode_n0_n0_IN_0_(net153));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net139), .switch_n0_RUN_IN_1_(net139), .switch_n0_GND_T(net151[0]), .switch_n0_VINJ_T(net150[0]), .switch_n0_CTRL_B_0_(net112[0]), .switch_n0_CTRL_B_1_(net113[0]), .switch_n0_Vg_0_(net114[0]), .switch_n0_Vg_1_(net115[0]), .switch_n0_VINJ(net150[0]), .switch_n0_PROG(net138[0]), .switch_n0_RUN(net141), .switch_n0_Vgsel(net140));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net148), .decode_n0_IN_0_(net147), .decode_n2_IN_1_(net146), .decode_n2_IN_0_(net145), .decode_n0_ENABLE(net149));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net143), .switch_n0_run_drainrail(net144), .switch_n0_VINJ(net150[0]), .switch_n0_GND(net151[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net92[0]), .switch_n0_PR_1_(net93[0]), .switch_n0_PR_2_(net92[1]), .switch_n0_PR_3_(net93[1]), .switch_n1_PR_0_(net92[2]), .switch_n1_PR_1_(net93[2]), .switch_n1_PR_2_(net92[3]), .switch_n1_PR_3_(net93[3]), .switch_n2_PR_0_(net92[4]), .switch_n2_PR_1_(net93[4]), .switch_n2_PR_2_(net107[0]), .switch_n2_PR_3_(net108[0]), .switch_n3_PR_0_(net109[0]), .switch_n3_PR_1_(net110[0]), .switch_n3_PR_2_(net111[0]), .switch_n0_In_0_(net94[0]), .switch_n0_In_1_(net94[1]), .switch_n0_In_2_(net94[2]), .switch_n0_In_3_(net94[3]), .switch_n1_In_0_(net94[4]), .switch_n0_VDD(net142), .switch_n0_GND(net151[0]), .switch_n0_RUN(net141));


	/* Island 1 */
	EPOT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .Vg_0_row_0(net116[0]), .VD_P_0_row_0(net107[0]), .VD_P_1_row_0(net108[0]), .VIN_PLUSrow_0(net136[0]), .Voutrow_0(net123));
	EPOT I__1 (.island_num(1), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net132), .VINJ_brow_0(net142), .GND_brow_0(net131), .VTUN_brow_0(net133), .Vg_b_0_row_0(net135), .Vsel_b_0_row_0(net134), .VD_P_0_row_0(net109[0]), .VD_P_1_row_0(net110[0]), .VIN_PLUSrow_0(net136[0]), .Voutrow_0(net124));

 	/*Programming Mux */ 


	/* Island 2 */
	AnalogBuffer I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VTUNrow_0(net133), .VDDrow_0(net132), .GNDrow_0(net131), .VINJrow_0(net142), .Vgrow_0(net135), .Vd_Prow_0(net111[0]), .Vselrow_0(net134), .Vinrow_0(net117), .Voutrow_0(net130));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net136[0]), .GNDrow_0(net151[0]), .SELAcol_0(net125[0:5]), .Ccol_0(net118[0:5]), .Acol_0(net123), .Bcol_0(net124));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net138[0]), .N_n_Run(net141), .N_n_VGRUN(net139), .N_n_VGPROG(net140), .N_n_VTUN(net137[0]), .N_n_avdd(net136[0]), .S_s_avdd(net132), .N_n_gnd(net151[0]), .S_s_gnd(net131), .N_n_vinj(net150[0]), .S_s_vinj(net142), .W_w_DrainB_0_(net145), .W_w_DrainB_1_(net146), .W_w_DrainB_2_(net147), .W_w_DrainB_3_(net148), .W_w_DrainEnable(net149), .W_w_GateB_0_(net153), .W_w_GateB_1_(net154), .N_n_GateEnable(net152), .S_s_Run_Drainline(net144), .S_s_Prog_Drainline(net143), .S_s_Vout(net130), .E_e_Code_0_(net125[0]), .E_e_Code_1_(net125[1]), .E_e_Code_2_(net125[2]), .E_e_Code_3_(net125[3]), .E_e_Code_4_(net125[4]), .S_s_DEBUG_0_(net123), .S_s_DEBUG_1_(net124));
 endmodule