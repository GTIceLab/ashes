module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(7), .matrix_col(1), .VDDrow_0(net120[0]), .VINJrow_0(net143[0]), .VINJ_brow_6(net136[0]), .GNDrow_0(net144[0]), .GND_brow_6(net137[0]), .Progrow_0(net116[0]), .Vg_0_row_0(net117[0]), .Vg_1_row_0(net118[0]), .VD_P_0_col_0(net121[0:7]), .VD_P_1_col_0(net122[0:7]), .Voutcol_0(net17[0:7]));
	AnalogBuffer I__1 (.island_num(0), .row(8), .col(0), .matrix_row(1), .matrix_col(1), .VDDrow_0(net120[0]), .GNDrow_0(net137[0]), .Vd_Prow_0(net135[0]), .Voutrow_0(net115));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net145), .decode_n0_VINJV(net143[0]), .decode_n0_GNDV(net144[0]), .decode_n0_n0_IN_1_(net147), .decode_n0_n0_IN_0_(net146));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_GND_T(net144[0]), .switch_n0_VINJ_T(net143[0]), .switch_n0_GND_B_0_(net137[0]), .switch_n0_GND_B_1_(net137[0]), .switch_n0_CTRL_B_0_(net117[0]), .switch_n0_CTRL_B_1_(net118[0]), .switch_n0_VINJ(net143[0]), .switch_n0_PROG(net116[0]));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_VINJ(net136[0]), .decode_n0_GND(net137[0]), .decode_n0_IN_1_(net141), .decode_n0_IN_0_(net140), .decode_n2_IN_1_(net139), .decode_n2_IN_0_(net138), .decode_n0_ENABLE(net142));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net121[0]), .switch_n0_PR_1_(net122[0]), .switch_n0_PR_2_(net121[1]), .switch_n0_PR_3_(net122[1]), .switch_n1_PR_0_(net121[2]), .switch_n1_PR_1_(net122[2]), .switch_n1_PR_2_(net121[3]), .switch_n1_PR_3_(net122[3]), .switch_n2_PR_0_(net121[4]), .switch_n2_PR_1_(net122[4]), .switch_n2_PR_2_(net121[5]), .switch_n2_PR_3_(net122[5]), .switch_n3_PR_0_(net121[6]), .switch_n3_PR_1_(net122[6]), .switch_n3_PR_2_(net135[0]), .switch_n0_VDD(net120[0]), .switch_n0_GND(net144[0]), .switch_n0_RUN(net119));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(1), .matrix_row(5), .matrix_col(1), .Acol_0(net17), .Bcol_0(net17));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net116[0]), .N_n_Run(net119), .N_n_AVDD(net120[0]), .N_n_gnd(net144[0]), .S_s_gnd(net137[0]), .N_n_vinj(net143[0]), .S_s_vinj(net136[0]), .W_w_DrainB_0_(net138), .W_w_DrainB_1_(net139), .W_w_DrainB_2_(net140), .W_w_DrainB_3_(net141), .W_w_DrainEnable(net142), .W_w_GateB_0_(net146), .W_w_GateB_1_(net147), .W_w_GateEnable(net145), .S_s_Vout(net115));
 endmodule