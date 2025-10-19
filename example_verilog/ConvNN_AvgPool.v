module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__1 (.island_num(0), .row(0), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__2 (.island_num(0), .row(1), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__3 (.island_num(0), .row(0), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__4 (.island_num(0), .row(1), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__5 (.island_num(0), .row(0), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net711), .Dinrow_0(net712));
	Integration_fr_AvgPool_core I__6 (.island_num(0), .row(0), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net713), .Dinrow_0(net714));
	Integration_fr_AvgPool_core I__7 (.island_num(0), .row(0), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net715), .Dinrow_0(net716));
	Integration_fr_AvgPool_core I__8 (.island_num(0), .row(0), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net725), .Dinrow_0(net717));
	Integration_fr_AvgPool_core I__9 (.island_num(0), .row(1), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net718), .Dinrow_0(net725));
	Integration_fr_AvgPool_core I__10 (.island_num(0), .row(1), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net719), .Dinrow_0(net720));
	Integration_fr_AvgPool_core I__11 (.island_num(0), .row(1), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net721), .Dinrow_0(net722));
	Integration_fr_AvgPool_core I__12 (.island_num(0), .row(1), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net723), .Dinrow_0(net724));
	AvgPool_n_Relu I__13 (.island_num(0), .row(0), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__14 (.island_num(0), .row(2), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__15 (.island_num(0), .row(2), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__16 (.island_num(0), .row(3), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__17 (.island_num(0), .row(2), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__18 (.island_num(0), .row(3), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__19 (.island_num(0), .row(2), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1181), .Dinrow_0(net1182));
	Integration_fr_AvgPool_core I__20 (.island_num(0), .row(2), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1183), .Dinrow_0(net1184));
	Integration_fr_AvgPool_core I__21 (.island_num(0), .row(2), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1185), .Dinrow_0(net1186));
	Integration_fr_AvgPool_core I__22 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1195), .Dinrow_0(net1187));
	Integration_fr_AvgPool_core I__23 (.island_num(0), .row(3), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1188), .Dinrow_0(net1195));
	Integration_fr_AvgPool_core I__24 (.island_num(0), .row(3), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1189), .Dinrow_0(net1190));
	Integration_fr_AvgPool_core I__25 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1191), .Dinrow_0(net1192));
	Integration_fr_AvgPool_core I__26 (.island_num(0), .row(3), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1193), .Dinrow_0(net1194));
	AvgPool_n_Relu I__27 (.island_num(0), .row(2), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__28 (.island_num(0), .row(4), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__29 (.island_num(0), .row(4), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__30 (.island_num(0), .row(5), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__31 (.island_num(0), .row(4), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__32 (.island_num(0), .row(5), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__33 (.island_num(0), .row(4), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1651), .Dinrow_0(net1652));
	Integration_fr_AvgPool_core I__34 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1653), .Dinrow_0(net1654));
	Integration_fr_AvgPool_core I__35 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1655), .Dinrow_0(net1656));
	Integration_fr_AvgPool_core I__36 (.island_num(0), .row(4), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1665), .Dinrow_0(net1657));
	Integration_fr_AvgPool_core I__37 (.island_num(0), .row(5), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1658), .Dinrow_0(net1665));
	Integration_fr_AvgPool_core I__38 (.island_num(0), .row(5), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1659), .Dinrow_0(net1660));
	Integration_fr_AvgPool_core I__39 (.island_num(0), .row(5), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1661), .Dinrow_0(net1662));
	Integration_fr_AvgPool_core I__40 (.island_num(0), .row(5), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1663), .Dinrow_0(net1664));
	AvgPool_n_Relu I__41 (.island_num(0), .row(4), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__42 (.island_num(0), .row(6), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__43 (.island_num(0), .row(6), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__44 (.island_num(0), .row(7), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__45 (.island_num(0), .row(6), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__46 (.island_num(0), .row(7), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__47 (.island_num(0), .row(6), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2121), .Dinrow_0(net2122));
	Integration_fr_AvgPool_core I__48 (.island_num(0), .row(6), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2123), .Dinrow_0(net2124));
	Integration_fr_AvgPool_core I__49 (.island_num(0), .row(6), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2125), .Dinrow_0(net2126));
	Integration_fr_AvgPool_core I__50 (.island_num(0), .row(6), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2135), .Dinrow_0(net2127));
	Integration_fr_AvgPool_core I__51 (.island_num(0), .row(7), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2128), .Dinrow_0(net2135));
	Integration_fr_AvgPool_core I__52 (.island_num(0), .row(7), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2129), .Dinrow_0(net2130));
	Integration_fr_AvgPool_core I__53 (.island_num(0), .row(7), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2131), .Dinrow_0(net2132));
	Integration_fr_AvgPool_core I__54 (.island_num(0), .row(7), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2133), .Dinrow_0(net2134));
	AvgPool_n_Relu I__55 (.island_num(0), .row(6), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__56 (.island_num(0), .row(8), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__57 (.island_num(0), .row(8), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__58 (.island_num(0), .row(9), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__59 (.island_num(0), .row(8), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__60 (.island_num(0), .row(9), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__61 (.island_num(0), .row(8), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2591), .Dinrow_0(net2592));
	Integration_fr_AvgPool_core I__62 (.island_num(0), .row(8), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2593), .Dinrow_0(net2594));
	Integration_fr_AvgPool_core I__63 (.island_num(0), .row(8), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2595), .Dinrow_0(net2596));
	Integration_fr_AvgPool_core I__64 (.island_num(0), .row(8), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2605), .Dinrow_0(net2597));
	Integration_fr_AvgPool_core I__65 (.island_num(0), .row(9), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2598), .Dinrow_0(net2605));
	Integration_fr_AvgPool_core I__66 (.island_num(0), .row(9), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2599), .Dinrow_0(net2600));
	Integration_fr_AvgPool_core I__67 (.island_num(0), .row(9), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2601), .Dinrow_0(net2602));
	Integration_fr_AvgPool_core I__68 (.island_num(0), .row(9), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2603), .Dinrow_0(net2604));
	AvgPool_n_Relu I__69 (.island_num(0), .row(8), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__70 (.island_num(0), .row(10), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__71 (.island_num(0), .row(10), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__72 (.island_num(0), .row(11), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__73 (.island_num(0), .row(10), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__74 (.island_num(0), .row(11), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__75 (.island_num(0), .row(10), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3061), .Dinrow_0(net3062));
	Integration_fr_AvgPool_core I__76 (.island_num(0), .row(10), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3063), .Dinrow_0(net3064));
	Integration_fr_AvgPool_core I__77 (.island_num(0), .row(10), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3065), .Dinrow_0(net3066));
	Integration_fr_AvgPool_core I__78 (.island_num(0), .row(10), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3075), .Dinrow_0(net3067));
	Integration_fr_AvgPool_core I__79 (.island_num(0), .row(11), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3068), .Dinrow_0(net3075));
	Integration_fr_AvgPool_core I__80 (.island_num(0), .row(11), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3069), .Dinrow_0(net3070));
	Integration_fr_AvgPool_core I__81 (.island_num(0), .row(11), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3071), .Dinrow_0(net3072));
	Integration_fr_AvgPool_core I__82 (.island_num(0), .row(11), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3073), .Dinrow_0(net3074));
	AvgPool_n_Relu I__83 (.island_num(0), .row(10), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__84 (.island_num(0), .row(12), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__85 (.island_num(0), .row(12), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__86 (.island_num(0), .row(13), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__87 (.island_num(0), .row(12), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__88 (.island_num(0), .row(13), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__89 (.island_num(0), .row(12), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3531), .Dinrow_0(net3532));
	Integration_fr_AvgPool_core I__90 (.island_num(0), .row(12), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3533), .Dinrow_0(net3534));
	Integration_fr_AvgPool_core I__91 (.island_num(0), .row(12), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3535), .Dinrow_0(net3536));
	Integration_fr_AvgPool_core I__92 (.island_num(0), .row(12), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3545), .Dinrow_0(net3537));
	Integration_fr_AvgPool_core I__93 (.island_num(0), .row(13), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3538), .Dinrow_0(net3545));
	Integration_fr_AvgPool_core I__94 (.island_num(0), .row(13), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3539), .Dinrow_0(net3540));
	Integration_fr_AvgPool_core I__95 (.island_num(0), .row(13), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3541), .Dinrow_0(net3542));
	Integration_fr_AvgPool_core I__96 (.island_num(0), .row(13), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3543), .Dinrow_0(net3544));
	AvgPool_n_Relu I__97 (.island_num(0), .row(12), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__98 (.island_num(0), .row(14), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__99 (.island_num(0), .row(14), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__100 (.island_num(0), .row(15), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__101 (.island_num(0), .row(14), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__102 (.island_num(0), .row(15), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__103 (.island_num(0), .row(14), .col(8), .matrix_row(1), .matrix_col(1), .Vg_0_row_0(net4445[0]), .Vg_1_row_0(net4446[0]), .Qrow_0(net3997), .Dinrow_0(net3998));
	Integration_fr_AvgPool_core I__104 (.island_num(0), .row(14), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3999), .Dinrow_0(net4000));
	Integration_fr_AvgPool_core I__105 (.island_num(0), .row(14), .col(10), .matrix_row(1), .matrix_col(1), .Vg_0_row_0(net4447[0]), .Vg_1_row_0(net4448[0]), .Qrow_0(net4515), .Dinrow_0(net4001));
	Integration_fr_AvgPool_core I__106 (.island_num(0), .row(14), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net4008), .Dinrow_0(net4002));
	Integration_fr_AvgPool_core I__107 (.island_num(0), .row(15), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net4516), .Dinrow_0(net4008));
	Integration_fr_AvgPool_core I__108 (.island_num(0), .row(15), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net4003), .Dinrow_0(net4004));
	Integration_fr_AvgPool_core I__109 (.island_num(0), .row(15), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net4005), .Dinrow_0(net4006));
	Integration_fr_AvgPool_core I__110 (.island_num(0), .row(15), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net4517), .Dinrow_0(net4007));
	AvgPool_n_Relu I__111 (.island_num(0), .row(14), .col(12), .matrix_row(2), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4), .decode_n0_VGRUN_0_(net4503[0]), .decode_n0_VGRUN_1_(net4503[1]), .decode_n0_VGRUN_2_(net4503[2]), .decode_n0_VGRUN_3_(net4503[3]), .decode_n1_VGRUN_0_(net4503[4]), .decode_n1_VGRUN_1_(net4503[5]), .decode_n1_VGRUN_2_(net4503[6]), .decode_n1_VGRUN_3_(net4503[7]), .decode_n2_VGRUN_0_(net4503[8]), .decode_n2_VGRUN_1_(net4503[9]), .decode_n2_VGRUN_2_(net4503[10]), .decode_n2_VGRUN_3_(net4503[11]));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(6));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(16), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(16), .type(prog_switch));


	/* Island 1 */
	FakeCellGateDecoder I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(4), .matrix_row(1), .matrix_col(4));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(3));
	TSMC350nm_IndirectSwitches switch(.island_num(1), .direction(horizontal), .num(4), .switch_n0_Vg_0_(net4445[0]), .switch_n0_Vg_1_(net4446[0]), .switch_n1_Vg_0_(net4447[0]), .switch_n1_Vg_1_(net4448[0]));


	/* Island 2 */
	DynamicShiftReg_Rst_Lo I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(12), .Dincol_0(net4518[0]), .RST_Bcol_0(net4521[0]), .CLKcol_0(net4519[0]), .CLKBcol_0(net4520[0]));
	Tgate_swc_fr_Kernel_Vert I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(12), .Vg_Rrow_0(net4503[0:12]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Q_0(net4515), .N_n_Q_1(net4516), .N_n_Q_2(net4517), .N_n_K_col_Din(net4518[0]), .N_n_K_col_CLK(net4519[0]), .N_n_K_col_CLKB(net4520[0]), .N_n_K_col_RST_B(net4521[0]));
 endmodule