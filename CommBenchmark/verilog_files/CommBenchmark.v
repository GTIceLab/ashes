module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(64), .matrix_col(140));
	TSMC350nm_4WTA_IndirectProg_noncab I__1 (.island_num(0), .row(141), .col(0), .matrix_row(64), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(9), .decode_n0_ENABLE(net11263), .decode_n0_VINJV(net11278), .decode_n0_GNDV(net11293), .decode_n0_n0_IN_0_(net11272), .decode_n2_n0_IN_1_(net11271), .decode_n2_n0_IN_0_(net11270), .decode_n4_n0_IN_1_(net11269), .decode_n4_n0_IN_0_(net11268), .decode_n6_n0_IN_1_(net11267), .decode_n6_n0_IN_0_(net11266), .decode_n8_n0_IN_1_(net11265), .decode_n8_n0_IN_0_(net11264));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(140), .switch_n0_PROG(net11261), .switch_n0_RUN(net11275), .switch_n0_Vgsel(net11260), .switch_n0_vtun_l(net11262));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(8), .decode_n0_VINJ(net11278), .decode_n0_GND(net11293), .decode_n0_IN_1_(net11286), .decode_n0_IN_0_(net11285), .decode_n2_IN_1_(net11284), .decode_n2_IN_0_(net11283), .decode_n4_IN_1_(net11282), .decode_n4_IN_0_(net11281), .decode_n6_IN_1_(net11280), .decode_n6_IN_0_(net11279), .decode_n0_ENABLE(net11287));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(64), .type(drain_select), .switch_n0_prog_drainrail(net11276), .switch_n0_run_drainrail(net11277), .switch_n0_VINJ(net11278), .switch_n0_GND(net11293));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(64), .type(prog_switch), .switch_n0_VDD(net11273), .switch_n0_GND(net11274), .switch_n0_RUN(net11275));


	/* Island 1 */
	TSMC350nm_VerticalScanner_STD I__0 (.island_num(1), .row(0), .col(0), .Out(net11288), .Din(net11289), .VDD(net11292[0]), .GND(net11293), .CLK(net11290), .RSTBar(net11291));
	TSMC350nm_VerticalScanner_STD I__1 (.island_num(1), .row(1), .col(0));
	TSMC350nm_VerticalScanner_STD I__2 (.island_num(1), .row(2), .col(0));
	TSMC350nm_VerticalScanner_STD I__3 (.island_num(1), .row(3), .col(0));
	TSMC350nm_VerticalScanner_STD I__4 (.island_num(1), .row(4), .col(0));
	TSMC350nm_VerticalScanner_STD I__5 (.island_num(1), .row(5), .col(0));
	TSMC350nm_VerticalScanner_STD I__6 (.island_num(1), .row(6), .col(0));
	TSMC350nm_VerticalScanner_STD I__7 (.island_num(1), .row(7), .col(0));
	TSMC350nm_VerticalScanner_STD I__8 (.island_num(1), .row(8), .col(0));
	TSMC350nm_VerticalScanner_STD I__9 (.island_num(1), .row(9), .col(0));
	TSMC350nm_VerticalScanner_STD I__10 (.island_num(1), .row(10), .col(0));
	TSMC350nm_VerticalScanner_STD I__11 (.island_num(1), .row(11), .col(0));
	TSMC350nm_VerticalScanner_STD I__12 (.island_num(1), .row(12), .col(0));
	TSMC350nm_VerticalScanner_STD I__13 (.island_num(1), .row(13), .col(0));
	TSMC350nm_VerticalScanner_STD I__14 (.island_num(1), .row(14), .col(0));
	TSMC350nm_VerticalScanner_STD I__15 (.island_num(1), .row(15), .col(0));
	TSMC350nm_VerticalScanner_STD I__16 (.island_num(1), .row(16), .col(0));
	TSMC350nm_VerticalScanner_STD I__17 (.island_num(1), .row(17), .col(0));
	TSMC350nm_VerticalScanner_STD I__18 (.island_num(1), .row(18), .col(0));
	TSMC350nm_VerticalScanner_STD I__19 (.island_num(1), .row(19), .col(0));
	TSMC350nm_VerticalScanner_STD I__20 (.island_num(1), .row(20), .col(0));
	TSMC350nm_VerticalScanner_STD I__21 (.island_num(1), .row(21), .col(0));
	TSMC350nm_VerticalScanner_STD I__22 (.island_num(1), .row(22), .col(0));
	TSMC350nm_VerticalScanner_STD I__23 (.island_num(1), .row(23), .col(0));
	TSMC350nm_VerticalScanner_STD I__24 (.island_num(1), .row(24), .col(0));
	TSMC350nm_VerticalScanner_STD I__25 (.island_num(1), .row(25), .col(0));
	TSMC350nm_VerticalScanner_STD I__26 (.island_num(1), .row(26), .col(0));
	TSMC350nm_VerticalScanner_STD I__27 (.island_num(1), .row(27), .col(0));
	TSMC350nm_VerticalScanner_STD I__28 (.island_num(1), .row(28), .col(0));
	TSMC350nm_VerticalScanner_STD I__29 (.island_num(1), .row(29), .col(0));
	TSMC350nm_VerticalScanner_STD I__30 (.island_num(1), .row(30), .col(0));
	TSMC350nm_VerticalScanner_STD I__31 (.island_num(1), .row(31), .col(0));
	TSMC350nm_VerticalScanner_STD I__32 (.island_num(1), .row(32), .col(0));
	TSMC350nm_VerticalScanner_STD I__33 (.island_num(1), .row(33), .col(0));
	TSMC350nm_VerticalScanner_STD I__34 (.island_num(1), .row(34), .col(0));
	TSMC350nm_VerticalScanner_STD I__35 (.island_num(1), .row(35), .col(0));
	TSMC350nm_VerticalScanner_STD I__36 (.island_num(1), .row(36), .col(0));
	TSMC350nm_VerticalScanner_STD I__37 (.island_num(1), .row(37), .col(0));
	TSMC350nm_VerticalScanner_STD I__38 (.island_num(1), .row(38), .col(0));
	TSMC350nm_VerticalScanner_STD I__39 (.island_num(1), .row(39), .col(0));
	TSMC350nm_VerticalScanner_STD I__40 (.island_num(1), .row(40), .col(0));
	TSMC350nm_VerticalScanner_STD I__41 (.island_num(1), .row(41), .col(0));
	TSMC350nm_VerticalScanner_STD I__42 (.island_num(1), .row(42), .col(0));
	TSMC350nm_VerticalScanner_STD I__43 (.island_num(1), .row(43), .col(0));
	TSMC350nm_VerticalScanner_STD I__44 (.island_num(1), .row(44), .col(0));
	TSMC350nm_VerticalScanner_STD I__45 (.island_num(1), .row(45), .col(0));
	TSMC350nm_VerticalScanner_STD I__46 (.island_num(1), .row(46), .col(0));
	TSMC350nm_VerticalScanner_STD I__47 (.island_num(1), .row(47), .col(0));
	TSMC350nm_VerticalScanner_STD I__48 (.island_num(1), .row(48), .col(0));
	TSMC350nm_VerticalScanner_STD I__49 (.island_num(1), .row(49), .col(0));
	TSMC350nm_VerticalScanner_STD I__50 (.island_num(1), .row(50), .col(0));
	TSMC350nm_VerticalScanner_STD I__51 (.island_num(1), .row(51), .col(0));
	TSMC350nm_VerticalScanner_STD I__52 (.island_num(1), .row(52), .col(0));
	TSMC350nm_VerticalScanner_STD I__53 (.island_num(1), .row(53), .col(0));
	TSMC350nm_VerticalScanner_STD I__54 (.island_num(1), .row(54), .col(0));
	TSMC350nm_VerticalScanner_STD I__55 (.island_num(1), .row(55), .col(0));
	TSMC350nm_VerticalScanner_STD I__56 (.island_num(1), .row(56), .col(0));
	TSMC350nm_VerticalScanner_STD I__57 (.island_num(1), .row(57), .col(0));
	TSMC350nm_VerticalScanner_STD I__58 (.island_num(1), .row(58), .col(0));
	TSMC350nm_VerticalScanner_STD I__59 (.island_num(1), .row(59), .col(0));
	TSMC350nm_VerticalScanner_STD I__60 (.island_num(1), .row(60), .col(0));
	TSMC350nm_VerticalScanner_STD I__61 (.island_num(1), .row(61), .col(0));
	TSMC350nm_VerticalScanner_STD I__62 (.island_num(1), .row(62), .col(0));
	TSMC350nm_VerticalScanner_STD I__63 (.island_num(1), .row(63), .col(0));

 	/*Programming Mux */ 


	/* Island 2 */
	Routes_GateDecodeSwc I__0 (.island_num(2), .row(66), .col(0), .matrix_row(1), .matrix_col(70), .AVDDcol_0(net11292[0]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net11261), .N_n_Run(net11275), .N_n_VGPROG(net11260), .N_n_VTUN(net11262), .N_n_AVDD(net11292[0]), .N_n_gnd(net11293), .S_s_gnd(net11274), .N_n_vinj(net11278), .S_s_vinj(net11273), .N_n_GateB_0_(net11264), .N_n_GateB_1_(net11265), .N_n_GateB_2_(net11266), .N_n_GateB_3_(net11267), .N_n_GateB_4_(net11268), .N_n_GateB_5_(net11269), .N_n_GateB_6_(net11270), .N_n_GateB_7_(net11271), .N_n_GateB_8_(net11272), .W_w_DrainB_0_(net11279), .W_w_DrainB_1_(net11280), .W_w_DrainB_2_(net11281), .W_w_DrainB_3_(net11282), .W_w_DrainB_4_(net11283), .W_w_DrainB_5_(net11284), .W_w_DrainB_6_(net11285), .W_w_DrainB_7_(net11286), .W_w_Drainline_Prog(net11276), .W_w_Drainline_Run(net11277), .N_n_GateEnable_WTA(net11263), .W_w_DrainEnable_WTA(net11287), .E_e_WTA_out(net11288), .E_e_Din(net11289), .E_e_CLK(net11290), .E_e_RSTBar(net11291));
 endmodule