module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(8), .matrix_col(1), .VDDrow_0(net137[0:1]), .VINJrow_0(net162[0:1]), .VINJ_brow_7(net154[0:1]), .GNDrow_0(net163[0:1]), .GND_brow_7(net155[0:1]), .Progrow_0(net133[0:1]), .Vg_0_row_0(net134[0:1]), .Vg_1_row_0(net135[0:1]), .VD_P_0_col_0(net138[0:8]), .VD_P_1_col_0(net139[0:8]), .Voutcol_0(net18[0:8]));
	AnalogBuffer I__1 (.island_num(0), .row(9), .col(0), .VDD(net137[0]), .GND(net155[0]), .Vout(net132));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net164), .decode_n0_VINJV(net162[0]), .decode_n0_GNDV(net163[0]), .decode_n0_n0_IN_1_(net166), .decode_n0_n0_IN_0_(net165));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_GND_T(net163[0]), .switch_n0_VINJ_T(net162[0]), .switch_n0_GND(net155[0]), .switch_n0_CTRL_B_0_(net134[0]), .switch_n0_CTRL_B_1_(net135[0]), .switch_n0_VINJ(net162[0]), .switch_n0_PROG(net133[0]));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5), .decode_n0_VINJ(net154[0]), .decode_n0_GND(net155[0]), .decode_n0_IN_0_(net160), .decode_n2_IN_1_(net159), .decode_n2_IN_0_(net158), .decode_n4_IN_1_(net157), .decode_n4_IN_0_(net156), .decode_n0_ENABLE(net161));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch), .switch_n0_PR_0_(net138[0]), .switch_n0_PR_1_(net139[0]), .switch_n0_PR_2_(net138[1]), .switch_n0_PR_3_(net139[1]), .switch_n1_PR_0_(net138[2]), .switch_n1_PR_1_(net139[2]), .switch_n1_PR_2_(net138[3]), .switch_n1_PR_3_(net139[3]), .switch_n2_PR_0_(net138[4]), .switch_n2_PR_1_(net139[4]), .switch_n2_PR_2_(net138[5]), .switch_n2_PR_3_(net139[5]), .switch_n3_PR_0_(net138[6]), .switch_n3_PR_1_(net139[6]), .switch_n3_PR_2_(net138[7]), .switch_n3_PR_3_(net139[7]), .switch_n0_VDD(net137[0]), .switch_n0_GND(net163[0]), .switch_n0_RUN(net136));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(1), .matrix_row(8), .matrix_col(1), .Acol_0(net18[0:8]), .Bcol_0(net18[0:8]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net133[0]), .N_n_Run(net136), .N_n_AVDD(net137[0]), .N_n_gnd(net163[0]), .S_s_gnd(net155[0]), .N_n_vinj(net162[0]), .S_s_vinj(net154[0]), .W_w_DrainB_0_(net156), .W_w_DrainB_1_(net157), .W_w_DrainB_2_(net158), .W_w_DrainB_3_(net159), .W_w_DrainB_4_(net160), .W_w_DrainEnable(net161), .W_w_GateB_0_(net165), .W_w_GateB_1_(net166), .W_w_GateEnable(net164), .S_s_Vout(net132));
 endmodule