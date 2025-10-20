module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__1 (.island_num(0), .row(0), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__2 (.island_num(0), .row(1), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__3 (.island_num(0), .row(0), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__4 (.island_num(0), .row(1), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__5 (.island_num(0), .row(0), .col(8), .matrix_row(1), .matrix_col(1), .Vg_0_row_0(net4275[0]), .Vg_1_row_0(net4276[0]), .Vsel_b_0_row_0(net4279[0]), .Vsel_b_1_row_0(net4280[0]), .Qrow_0(net575), .Dinrow_0(net576));
	Integration_fr_AvgPool_core I__6 (.island_num(0), .row(0), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net577), .Dinrow_0(net578));
	Integration_fr_AvgPool_core I__7 (.island_num(0), .row(0), .col(10), .matrix_row(1), .matrix_col(1), .Vg_0_row_0(net4277[0]), .Vg_1_row_0(net4278[0]), .Vsel_b_0_row_0(net4281[0]), .Vsel_b_1_row_0(net4282[0]), .Qrow_0(net579), .Dinrow_0(net580));
	Integration_fr_AvgPool_core I__8 (.island_num(0), .row(0), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net589), .Dinrow_0(net581));
	Integration_fr_AvgPool_core I__9 (.island_num(0), .row(1), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net582), .Dinrow_0(net589));
	Integration_fr_AvgPool_core I__10 (.island_num(0), .row(1), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net583), .Dinrow_0(net584));
	Integration_fr_AvgPool_core I__11 (.island_num(0), .row(1), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net585), .Dinrow_0(net586));
	Integration_fr_AvgPool_core I__12 (.island_num(0), .row(1), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net587), .Dinrow_0(net588));
	AvgPool_n_Relu I__13 (.island_num(0), .row(0), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__14 (.island_num(0), .row(2), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__15 (.island_num(0), .row(2), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__16 (.island_num(0), .row(3), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__17 (.island_num(0), .row(2), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__18 (.island_num(0), .row(3), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__19 (.island_num(0), .row(2), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1045), .Dinrow_0(net1046));
	Integration_fr_AvgPool_core I__20 (.island_num(0), .row(2), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1047), .Dinrow_0(net1048));
	Integration_fr_AvgPool_core I__21 (.island_num(0), .row(2), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1049), .Dinrow_0(net1050));
	Integration_fr_AvgPool_core I__22 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1059), .Dinrow_0(net1051));
	Integration_fr_AvgPool_core I__23 (.island_num(0), .row(3), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1052), .Dinrow_0(net1059));
	Integration_fr_AvgPool_core I__24 (.island_num(0), .row(3), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1053), .Dinrow_0(net1054));
	Integration_fr_AvgPool_core I__25 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1055), .Dinrow_0(net1056));
	Integration_fr_AvgPool_core I__26 (.island_num(0), .row(3), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1057), .Dinrow_0(net1058));
	AvgPool_n_Relu I__27 (.island_num(0), .row(2), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__28 (.island_num(0), .row(4), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__29 (.island_num(0), .row(4), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__30 (.island_num(0), .row(5), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__31 (.island_num(0), .row(4), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__32 (.island_num(0), .row(5), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__33 (.island_num(0), .row(4), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1515), .Dinrow_0(net1516));
	Integration_fr_AvgPool_core I__34 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1517), .Dinrow_0(net1518));
	Integration_fr_AvgPool_core I__35 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1519), .Dinrow_0(net1520));
	Integration_fr_AvgPool_core I__36 (.island_num(0), .row(4), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1529), .Dinrow_0(net1521));
	Integration_fr_AvgPool_core I__37 (.island_num(0), .row(5), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1522), .Dinrow_0(net1529));
	Integration_fr_AvgPool_core I__38 (.island_num(0), .row(5), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1523), .Dinrow_0(net1524));
	Integration_fr_AvgPool_core I__39 (.island_num(0), .row(5), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1525), .Dinrow_0(net1526));
	Integration_fr_AvgPool_core I__40 (.island_num(0), .row(5), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1527), .Dinrow_0(net1528));
	AvgPool_n_Relu I__41 (.island_num(0), .row(4), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__42 (.island_num(0), .row(6), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__43 (.island_num(0), .row(6), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__44 (.island_num(0), .row(7), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__45 (.island_num(0), .row(6), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__46 (.island_num(0), .row(7), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__47 (.island_num(0), .row(6), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1985), .Dinrow_0(net1986));
	Integration_fr_AvgPool_core I__48 (.island_num(0), .row(6), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1987), .Dinrow_0(net1988));
	Integration_fr_AvgPool_core I__49 (.island_num(0), .row(6), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1989), .Dinrow_0(net1990));
	Integration_fr_AvgPool_core I__50 (.island_num(0), .row(6), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1999), .Dinrow_0(net1991));
	Integration_fr_AvgPool_core I__51 (.island_num(0), .row(7), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1992), .Dinrow_0(net1999));
	Integration_fr_AvgPool_core I__52 (.island_num(0), .row(7), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1993), .Dinrow_0(net1994));
	Integration_fr_AvgPool_core I__53 (.island_num(0), .row(7), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1995), .Dinrow_0(net1996));
	Integration_fr_AvgPool_core I__54 (.island_num(0), .row(7), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1997), .Dinrow_0(net1998));
	AvgPool_n_Relu I__55 (.island_num(0), .row(6), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__56 (.island_num(0), .row(8), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__57 (.island_num(0), .row(8), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__58 (.island_num(0), .row(9), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__59 (.island_num(0), .row(8), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__60 (.island_num(0), .row(9), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__61 (.island_num(0), .row(8), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2455), .Dinrow_0(net2456));
	Integration_fr_AvgPool_core I__62 (.island_num(0), .row(8), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2457), .Dinrow_0(net2458));
	Integration_fr_AvgPool_core I__63 (.island_num(0), .row(8), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2459), .Dinrow_0(net2460));
	Integration_fr_AvgPool_core I__64 (.island_num(0), .row(8), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2469), .Dinrow_0(net2461));
	Integration_fr_AvgPool_core I__65 (.island_num(0), .row(9), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2462), .Dinrow_0(net2469));
	Integration_fr_AvgPool_core I__66 (.island_num(0), .row(9), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2463), .Dinrow_0(net2464));
	Integration_fr_AvgPool_core I__67 (.island_num(0), .row(9), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2465), .Dinrow_0(net2466));
	Integration_fr_AvgPool_core I__68 (.island_num(0), .row(9), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2467), .Dinrow_0(net2468));
	AvgPool_n_Relu I__69 (.island_num(0), .row(8), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__70 (.island_num(0), .row(10), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__71 (.island_num(0), .row(10), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__72 (.island_num(0), .row(11), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__73 (.island_num(0), .row(10), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__74 (.island_num(0), .row(11), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__75 (.island_num(0), .row(10), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2925), .Dinrow_0(net2926));
	Integration_fr_AvgPool_core I__76 (.island_num(0), .row(10), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2927), .Dinrow_0(net2928));
	Integration_fr_AvgPool_core I__77 (.island_num(0), .row(10), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2929), .Dinrow_0(net2930));
	Integration_fr_AvgPool_core I__78 (.island_num(0), .row(10), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2939), .Dinrow_0(net2931));
	Integration_fr_AvgPool_core I__79 (.island_num(0), .row(11), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2932), .Dinrow_0(net2939));
	Integration_fr_AvgPool_core I__80 (.island_num(0), .row(11), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2933), .Dinrow_0(net2934));
	Integration_fr_AvgPool_core I__81 (.island_num(0), .row(11), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2935), .Dinrow_0(net2936));
	Integration_fr_AvgPool_core I__82 (.island_num(0), .row(11), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2937), .Dinrow_0(net2938));
	AvgPool_n_Relu I__83 (.island_num(0), .row(10), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__84 (.island_num(0), .row(12), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__85 (.island_num(0), .row(12), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__86 (.island_num(0), .row(13), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__87 (.island_num(0), .row(12), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__88 (.island_num(0), .row(13), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__89 (.island_num(0), .row(12), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3395), .Dinrow_0(net3396));
	Integration_fr_AvgPool_core I__90 (.island_num(0), .row(12), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3397), .Dinrow_0(net3398));
	Integration_fr_AvgPool_core I__91 (.island_num(0), .row(12), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3399), .Dinrow_0(net3400));
	Integration_fr_AvgPool_core I__92 (.island_num(0), .row(12), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3409), .Dinrow_0(net3401));
	Integration_fr_AvgPool_core I__93 (.island_num(0), .row(13), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3402), .Dinrow_0(net3409));
	Integration_fr_AvgPool_core I__94 (.island_num(0), .row(13), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3403), .Dinrow_0(net3404));
	Integration_fr_AvgPool_core I__95 (.island_num(0), .row(13), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3405), .Dinrow_0(net3406));
	Integration_fr_AvgPool_core I__96 (.island_num(0), .row(13), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3407), .Dinrow_0(net3408));
	AvgPool_n_Relu I__97 (.island_num(0), .row(12), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__98 (.island_num(0), .row(14), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__99 (.island_num(0), .row(14), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__100 (.island_num(0), .row(15), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__101 (.island_num(0), .row(14), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__102 (.island_num(0), .row(15), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__103 (.island_num(0), .row(14), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3865), .Dinrow_0(net3866));
	Integration_fr_AvgPool_core I__104 (.island_num(0), .row(14), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3867), .Dinrow_0(net3868));
	Integration_fr_AvgPool_core I__105 (.island_num(0), .row(14), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3869), .Dinrow_0(net3870));
	Integration_fr_AvgPool_core I__106 (.island_num(0), .row(14), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3879), .Dinrow_0(net3871));
	Integration_fr_AvgPool_core I__107 (.island_num(0), .row(15), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3872), .Dinrow_0(net3879));
	Integration_fr_AvgPool_core I__108 (.island_num(0), .row(15), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3873), .Dinrow_0(net3874));
	Integration_fr_AvgPool_core I__109 (.island_num(0), .row(15), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3875), .Dinrow_0(net3876));
	Integration_fr_AvgPool_core I__110 (.island_num(0), .row(15), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3877), .Dinrow_0(net3878));
	AvgPool_n_Relu I__111 (.island_num(0), .row(14), .col(12), .matrix_row(2), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(6));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(8), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(8), .type(prog_switch));


	/* Island 1 */
	FakeCellGateDecoder I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(4), .matrix_row(1), .matrix_col(4));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(3));
	TSMC350nm_IndirectSwitches switch(.island_num(1), .direction(horizontal), .num(4), .switch_n0_CTRL_B_0_(net4279[0]), .switch_n0_CTRL_B_1_(net4280[0]), .switch_n1_CTRL_B_0_(net4281[0]), .switch_n1_CTRL_B_1_(net4282[0]), .switch_n0_Vg_0_(net4275[0]), .switch_n0_Vg_1_(net4276[0]), .switch_n1_Vg_0_(net4277[0]), .switch_n1_Vg_1_(net4278[0]));


	/* Island 2 */
	DynamicShiftReg_Rst_Lo I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(4), .Dincol_0(net4374[0]), .RST_Bcol_0(net4377[0]), .CLKcol_0(net4375[0]), .CLKBcol_0(net4376[0]));
	Tgate_swc_fr_Kernel_Vert I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__2 (.island_num(2), .row(1), .col(1), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__3 (.island_num(2), .row(1), .col(2), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__4 (.island_num(2), .row(1), .col(3), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__5 (.island_num(2), .row(1), .col(5));
	Tgate_swc_fr_Kernel_Vert I__6 (.island_num(2), .row(1), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__7 (.island_num(2), .row(1), .col(7), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__8 (.island_num(2), .row(1), .col(8), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__9 (.island_num(2), .row(1), .col(10));
	Tgate_swc_fr_Kernel_Vert I__10 (.island_num(2), .row(1), .col(11), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__11 (.island_num(2), .row(1), .col(12), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Vert I__12 (.island_num(2), .row(1), .col(13), .matrix_row(1), .matrix_col(1));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_K_col_Din(net4374[0]), .N_n_K_col_CLK(net4375[0]), .N_n_K_col_CLKB(net4376[0]), .N_n_K_col_RST_B(net4377[0]));
 endmodule