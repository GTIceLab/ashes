module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(6), .matrix_col(1), .VDDrow_0(net129[0:1]), .VDD_brow_5(net151[0:1]), .VINJrow_0(net168[0:1]), .VINJ_brow_5(net161[0:1]), .GNDrow_0(net169[0:1]), .GND_brow_5(net162[0:1]), .Progrow_0(net157[0:1]), .Prog_brow_5(net152[0:1]), .Vg_0_row_0(net158[0:1]), .Vg_1_row_0(net159[0:1]), .Vg_b_0_row_5(net153[0:1]), .Vsel_b_0_row_5(net154[0:1]), .VD_P_0_col_0(net112[0:6]), .VD_P_1_col_0(net113[0:6]), .Voutcol_0(net12[0:6]));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(7), .col(0), .VDD(net151[0]), .VINJ(net161[0]), .Vg(net153[0]), .VD_P(net124[0]), .VD_R(net125[0]), .Vsel(net154[0]), .PROG(net152[0]), .VIN_PLUS(net149[4]), .VIN_MINUS(net12[4]), .Vout(net156));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net170), .decode_n0_VINJV(net168[0]), .decode_n0_GNDV(net169[0]), .decode_n0_n0_IN_1_(net172), .decode_n0_n0_IN_0_(net171));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(0), .GND_T(net169[0]), .VINJ_T(net168[0]), .GND(net162[0]), .CTRL_B_0_(net158[0]), .CTRL_B_1_(net159[0]), .VINJ(net168[0]), .PROG(net157[0]));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_VINJ(net161[0]), .decode_n0_GND(net162[0]), .decode_n0_IN_1_(net166), .decode_n0_IN_0_(net165), .decode_n2_IN_1_(net164), .decode_n2_IN_0_(net163), .decode_n0_ENABLE(net167));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net112[0]), .switch_n0_PR_1_(net113[0]), .switch_n0_PR_2_(net112[1]), .switch_n0_PR_3_(net113[1]), .switch_n1_PR_0_(net112[2]), .switch_n1_PR_1_(net113[2]), .switch_n1_PR_2_(net112[3]), .switch_n1_PR_3_(net113[3]), .switch_n2_PR_0_(net112[4]), .switch_n2_PR_1_(net113[4]), .switch_n2_PR_2_(net112[5]), .switch_n2_PR_3_(net113[5]), .switch_n3_PR_0_(net124[0]), .switch_n3_In_0_(net125[0]), .switch_n0_RUN(net160));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net168[0:1]), .VDD_brow_4(net161[0:1]), .GNDrow_0(net169[0:1]), .GND_brow_4(net162[0:1]), .SELAcol_0(net135[0:5]), .Ccol_0(net130[0:5]), .Acol_0(net12[0:5]), .Bcol_0(net12[0:5]));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDD_brow_4(net161[0:1]), .GNDrow_0(net169[0:1]), .SELAcol_0(net150[0:5]), .Ccol_0(net144[0:5]), .Acol_0(net12[0:5]), .Bcol_0(net130[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net144[0:5]), .Botcol_0(net149[0:5]));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD_b(net161[0]), .GND_b(net162[0]), .SELA(net150[4]), .C(net156), .A(net12[4]));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net12[4]), .Bot(net156));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net157[0]), .N_n_Run(net160), .N_n_AVDD(net129[0]), .N_n_gnd(net169[0]), .S_s_gnd(net162[0]), .N_n_vinj(net168[0]), .S_s_vinj(net161[0]), .W_w_DrainB_0_(net163), .W_w_DrainB_1_(net164), .W_w_DrainB_2_(net165), .W_w_DrainB_3_(net166), .W_w_DrainEnable(net167), .W_w_GateB_0_(net171), .W_w_GateB_1_(net172), .W_w_GateEnable(net170), .S_s_Vout(net156), .N_n_RST(net150[4]), .N_n_Code_0_(net135[0]), .N_n_Code_1_(net135[1]), .N_n_Code_2_(net135[2]), .N_n_Code_3_(net135[3]), .N_n_Code_4_(net135[4]));
 endmodule