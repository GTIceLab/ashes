module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(12));
	TSMC350nm_4TGate_ST_BMatrix I__1 (.island_num(0), .row(0), .col(13), .matrix_row(5), .matrix_col(1), .A_0_col_0(net811[0:5]), .A_1_col_0(net812[0:5]), .A_2_col_0(net813[0:5]), .A_3_col_0(net814[0:5]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(5), .decode_n0_ENABLE(net835), .decode_n0_VINJV(net841), .decode_n0_GNDV(net842));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(12), .switch_n0_RUN_IN_0_(net831[0]), .switch_n0_RUN_IN_1_(net831[0]), .switch_n1_RUN_IN_0_(net831[0]), .switch_n1_RUN_IN_1_(net831[0]), .switch_n2_RUN_IN_0_(net831[0]), .switch_n2_RUN_IN_1_(net831[0]), .switch_n3_RUN_IN_0_(net831[0]), .switch_n3_RUN_IN_1_(net831[0]), .switch_n4_RUN_IN_0_(net831[0]), .switch_n4_RUN_IN_1_(net831[0]), .switch_n5_RUN_IN_0_(net831[0]), .switch_n5_RUN_IN_1_(net831[0]), .switch_n6_RUN_IN_0_(net831[0]), .switch_n6_RUN_IN_1_(net831[0]), .switch_n7_RUN_IN_0_(net831[0]), .switch_n7_RUN_IN_1_(net831[0]), .switch_n8_RUN_IN_0_(net831[0]), .switch_n8_RUN_IN_1_(net831[0]), .switch_n9_RUN_IN_0_(net831[0]), .switch_n9_RUN_IN_1_(net831[0]), .switch_n10_RUN_IN_0_(net831[0]), .switch_n10_RUN_IN_1_(net831[0]), .switch_n11_RUN_IN_0_(net831[0]), .switch_n0_PROG(net833), .switch_n0_RUN(net838), .switch_n0_Vgsel(net832), .switch_n0_vtun_l(net834));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5), .decode_n0_VINJ(net841), .decode_n0_GND(net842), .decode_n0_ENABLE(net843));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select), .switch_n0_prog_drainrail(net839), .switch_n0_run_drainrail(net840), .switch_n0_VINJ(net841), .switch_n0_GND(net842));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch), .switch_n0_VDD(net836), .switch_n0_GND(net837), .switch_n0_RUN(net838));


	/* Island 1 */
	Routes_GateDecodeSwc I__0 (.island_num(1), .row(7), .col(0), .matrix_row(1), .matrix_col(6));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Modulation I__0 (.island_num(2), .row(0), .col(15), .matrix_row(5), .matrix_col(1), .I1_Pcol_0(net811[0:5]), .I1_Ncol_0(net812[0:5]), .I3_Pcol_0(net813[0:5]), .I3_Ncol_0(net814[0:5]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net833), .N_n_Run(net838), .N_n_VGRUN(net831[0]), .N_n_VGPROG(net832), .N_n_VTUN(net834), .N_n_gnd(net842), .S_s_gnd(net837), .N_n_vinj(net841), .S_s_vinj(net836), .W_w_Drainline_Prog(net839), .W_w_Drainline_Run(net840), .N_n_GateEnable(net835), .W_w_DrainEnable(net843));
 endmodule