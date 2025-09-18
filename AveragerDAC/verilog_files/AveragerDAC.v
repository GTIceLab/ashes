module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGInputs_Bias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net138[0]), .VINJrow_0(net153[0]), .GNDrow_0(net154[0]), .VTUNrow_0(net139[0]), .Vg_0_row_0(net117[0]), .Vg_1_row_0(net118[0]), .Vd_P_0_col_0(net95[0:5]), .Vd_P_1_col_0(net96[0:5]), .Vd_Rcol_0(net97[0:5]), .Vsel_0_row_0(net115[0]), .Vsel_1_row_0(net116[0]), .Progrow_0(net140[0]), .VIN_PLUScol_0(net121[0:5]), .VIN_MINUScol_0(net120), .Voutcol_0(net120));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net155), .decode_n0_VINJV(net153[0]), .decode_n0_GNDV(net154[0]), .decode_n0_n0_IN_1_(net157), .decode_n0_n0_IN_0_(net156));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net141), .switch_n0_RUN_IN_1_(net141), .switch_n0_GND_T(net154[0]), .switch_n0_VINJ_T(net153[0]), .switch_n0_CTRL_B_0_(net115[0]), .switch_n0_CTRL_B_1_(net116[0]), .switch_n0_Vg_0_(net117[0]), .switch_n0_Vg_1_(net118[0]), .switch_n0_VINJ(net153[0]), .switch_n0_PROG(net140[0]), .switch_n0_RUN(net142));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_VINJ(net146), .decode_n0_GND(net147), .decode_n0_IN_1_(net151), .decode_n0_IN_0_(net150), .decode_n2_IN_1_(net149), .decode_n2_IN_0_(net148), .decode_n0_ENABLE(net152));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select), .switch_n0_prog_drainrail(net144), .switch_n0_run_drainrail(net145), .switch_n0_VINJ(net153[0]), .switch_n0_GND(net154[0]));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net95[0]), .switch_n0_PR_1_(net96[0]), .switch_n0_PR_2_(net95[1]), .switch_n0_PR_3_(net96[1]), .switch_n1_PR_0_(net95[2]), .switch_n1_PR_1_(net96[2]), .switch_n1_PR_2_(net95[3]), .switch_n1_PR_3_(net96[3]), .switch_n2_PR_0_(net95[4]), .switch_n2_PR_1_(net96[4]), .switch_n2_PR_2_(net110[0]), .switch_n2_PR_3_(net111[0]), .switch_n3_PR_0_(net112[0]), .switch_n3_PR_1_(net113[0]), .switch_n3_PR_2_(net114[0]), .switch_n0_In_0_(net97[0]), .switch_n0_In_1_(net97[1]), .switch_n0_In_2_(net97[2]), .switch_n0_In_3_(net97[3]), .switch_n1_In_0_(net97[4]), .switch_n0_VDD(net143), .switch_n0_GND(net154[0]), .switch_n0_RUN(net142));


	/* Island 1 */
	EPOT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net110[0]), .VD_P_1_row_0(net111[0]), .Voutrow_0(net126));
	EPOT I__1 (.island_num(1), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net143), .VINJ_brow_0(net135), .GND_brow_0(net147), .VTUN_brow_0(net134), .Vg_0_row_0(net137), .Vsel_0_row_0(net136), .VD_P_0_row_0(net112[0]), .VD_P_1_row_0(net113[0]), .Voutrow_0(net127));

 	/*Programming Mux */ 


	/* Island 2 */
	AnalogBuffer I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VTUNrow_0(net134), .VDDrow_0(net143), .GNDrow_0(net147), .VINJrow_0(net135), .Vgrow_0(net137), .Vd_Prow_0(net114[0]), .Vselrow_0(net136), .Vinrow_0(net120), .Voutrow_0(net133));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net138[0]), .GNDrow_0(net154[0]), .SELAcol_0(net128[0:5]), .Ccol_0(net121[0:5]), .Acol_0(net126), .Bcol_0(net127));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net140[0]), .N_n_Run(net142), .N_n_VGRUN(net141), .N_n_VTUN(net139[0]), .N_n_avdd(net138[0]), .S_s_avdd(net143), .N_n_gnd(net154[0]), .S_s_gnd(net147), .N_n_vinj(net153[0]), .S_s_vinj(net146), .W_w_DrainB_0_(net148), .W_w_DrainB_1_(net149), .W_w_DrainB_2_(net150), .W_w_DrainB_3_(net151), .W_w_DrainEnable(net152), .W_w_GateB_0_(net156), .W_w_GateB_1_(net157), .W_w_GateEnable(net155), .S_s_Run_Drainline(net145), .S_s_Prog_Drainline(net144), .S_s_Vout(net133), .E_e_Code_0_(net128[0]), .E_e_Code_1_(net128[1]), .E_e_Code_2_(net128[2]), .E_e_Code_3_(net128[3]), .E_e_Code_4_(net128[4]));
 endmodule