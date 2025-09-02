module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(16), .matrix_col(1), .VDDrow_0(net193[0:1]), .VINJrow_0(net235[0:1]), .VINJ_brow_15(net226[0:1]), .GNDrow_0(net236[0:1]), .GND_brow_15(net227[0:1]), .Progrow_0(net189[0:1]), .Vg_0_row_0(net190[0:1]), .Vg_1_row_0(net191[0:1]), .VD_P_0_col_0(net194[0:16]), .VD_P_1_col_0(net195[0:16]), .Voutcol_0(net26[0:16]));
	AnalogBuffer I__1 (.island_num(0), .row(17), .col(0), .VDD(net193[0]), .GND(net227[0]), .Vout(net188));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net237), .decode_n0_VINJV(net235[0]), .decode_n0_GNDV(net236[0]), .decode_n0_n0_IN_1_(net239), .decode_n0_n0_IN_0_(net238));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_GND_T(net236[0]), .switch_n0_VINJ_T(net235[0]), .switch_n0_GND(net227[0]), .switch_n0_CTRL_B_0_(net190[0]), .switch_n0_CTRL_B_1_(net191[0]), .switch_n0_VINJ(net235[0]), .switch_n0_PROG(net189[0]));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6), .decode_n0_VINJ(net226[0]), .decode_n0_GND(net227[0]), .decode_n0_IN_1_(net233), .decode_n0_IN_0_(net232), .decode_n2_IN_1_(net231), .decode_n2_IN_0_(net230), .decode_n4_IN_1_(net229), .decode_n4_IN_0_(net228), .decode_n0_ENABLE(net234));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(9), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(9), .type(prog_switch), .switch_n0_PR_0_(net194[0]), .switch_n0_PR_1_(net195[0]), .switch_n0_PR_2_(net194[1]), .switch_n0_PR_3_(net195[1]), .switch_n1_PR_0_(net194[2]), .switch_n1_PR_1_(net195[2]), .switch_n1_PR_2_(net194[3]), .switch_n1_PR_3_(net195[3]), .switch_n2_PR_0_(net194[4]), .switch_n2_PR_1_(net195[4]), .switch_n2_PR_2_(net194[5]), .switch_n2_PR_3_(net195[5]), .switch_n3_PR_0_(net194[6]), .switch_n3_PR_1_(net195[6]), .switch_n3_PR_2_(net194[7]), .switch_n3_PR_3_(net195[7]), .switch_n4_PR_0_(net194[8]), .switch_n4_PR_1_(net195[8]), .switch_n4_PR_2_(net194[9]), .switch_n4_PR_3_(net195[9]), .switch_n5_PR_0_(net194[10]), .switch_n5_PR_1_(net195[10]), .switch_n5_PR_2_(net194[11]), .switch_n5_PR_3_(net195[11]), .switch_n6_PR_0_(net194[12]), .switch_n6_PR_1_(net195[12]), .switch_n6_PR_2_(net194[13]), .switch_n6_PR_3_(net195[13]), .switch_n7_PR_0_(net194[14]), .switch_n7_PR_1_(net195[14]), .switch_n7_PR_2_(net194[15]), .switch_n7_PR_3_(net195[15]), .switch_n0_VDD(net193[0]), .switch_n0_GND(net236[0]), .switch_n0_RUN(net192));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(1), .matrix_row(16), .matrix_col(1), .Acol_0(net26[0:16]), .Bcol_0(net26[0:16]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net189[0]), .N_n_Run(net192), .N_n_AVDD(net193[0]), .N_n_gnd(net236[0]), .S_s_gnd(net227[0]), .N_n_vinj(net235[0]), .S_s_vinj(net226[0]), .W_w_DrainB_0_(net228), .W_w_DrainB_1_(net229), .W_w_DrainB_2_(net230), .W_w_DrainB_3_(net231), .W_w_DrainB_4_(net232), .W_w_DrainB_5_(net233), .W_w_DrainEnable(net234), .W_w_GateB_0_(net238), .W_w_GateB_1_(net239), .W_w_GateEnable(net237), .S_s_Vout(net188));
 endmodule