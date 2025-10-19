module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__1 (.island_num(0), .row(0), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__2 (.island_num(0), .row(1), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__3 (.island_num(0), .row(0), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__4 (.island_num(0), .row(1), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__5 (.island_num(0), .row(0), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net720), .Dinrow_0(net721));
	Integration_fr_AvgPool_core I__6 (.island_num(0), .row(0), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net722), .Dinrow_0(net723));
	Integration_fr_AvgPool_core I__7 (.island_num(0), .row(0), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net724), .Dinrow_0(net725));
	Integration_fr_AvgPool_core I__8 (.island_num(0), .row(0), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net734), .Dinrow_0(net726));
	Integration_fr_AvgPool_core I__9 (.island_num(0), .row(1), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net727), .Dinrow_0(net734));
	Integration_fr_AvgPool_core I__10 (.island_num(0), .row(1), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net728), .Dinrow_0(net729));
	Integration_fr_AvgPool_core I__11 (.island_num(0), .row(1), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net730), .Dinrow_0(net731));
	Integration_fr_AvgPool_core I__12 (.island_num(0), .row(1), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net732), .Dinrow_0(net733));
	AvgPool_n_Relu I__13 (.island_num(0), .row(0), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__14 (.island_num(0), .row(2), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__15 (.island_num(0), .row(2), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__16 (.island_num(0), .row(3), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__17 (.island_num(0), .row(2), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__18 (.island_num(0), .row(3), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__19 (.island_num(0), .row(2), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1199), .Dinrow_0(net1200));
	Integration_fr_AvgPool_core I__20 (.island_num(0), .row(2), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1201), .Dinrow_0(net1202));
	Integration_fr_AvgPool_core I__21 (.island_num(0), .row(2), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1203), .Dinrow_0(net1204));
	Integration_fr_AvgPool_core I__22 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1213), .Dinrow_0(net1205));
	Integration_fr_AvgPool_core I__23 (.island_num(0), .row(3), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1206), .Dinrow_0(net1213));
	Integration_fr_AvgPool_core I__24 (.island_num(0), .row(3), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1207), .Dinrow_0(net1208));
	Integration_fr_AvgPool_core I__25 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1209), .Dinrow_0(net1210));
	Integration_fr_AvgPool_core I__26 (.island_num(0), .row(3), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1211), .Dinrow_0(net1212));
	AvgPool_n_Relu I__27 (.island_num(0), .row(2), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__28 (.island_num(0), .row(4), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__29 (.island_num(0), .row(4), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__30 (.island_num(0), .row(5), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__31 (.island_num(0), .row(4), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__32 (.island_num(0), .row(5), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__33 (.island_num(0), .row(4), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1678), .Dinrow_0(net1679));
	Integration_fr_AvgPool_core I__34 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1680), .Dinrow_0(net1681));
	Integration_fr_AvgPool_core I__35 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1682), .Dinrow_0(net1683));
	Integration_fr_AvgPool_core I__36 (.island_num(0), .row(4), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1692), .Dinrow_0(net1684));
	Integration_fr_AvgPool_core I__37 (.island_num(0), .row(5), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1685), .Dinrow_0(net1692));
	Integration_fr_AvgPool_core I__38 (.island_num(0), .row(5), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1686), .Dinrow_0(net1687));
	Integration_fr_AvgPool_core I__39 (.island_num(0), .row(5), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1688), .Dinrow_0(net1689));
	Integration_fr_AvgPool_core I__40 (.island_num(0), .row(5), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1690), .Dinrow_0(net1691));
	AvgPool_n_Relu I__41 (.island_num(0), .row(4), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__42 (.island_num(0), .row(6), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__43 (.island_num(0), .row(6), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__44 (.island_num(0), .row(7), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__45 (.island_num(0), .row(6), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__46 (.island_num(0), .row(7), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__47 (.island_num(0), .row(6), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2157), .Dinrow_0(net2158));
	Integration_fr_AvgPool_core I__48 (.island_num(0), .row(6), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2159), .Dinrow_0(net2160));
	Integration_fr_AvgPool_core I__49 (.island_num(0), .row(6), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2161), .Dinrow_0(net2162));
	Integration_fr_AvgPool_core I__50 (.island_num(0), .row(6), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2171), .Dinrow_0(net2163));
	Integration_fr_AvgPool_core I__51 (.island_num(0), .row(7), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2164), .Dinrow_0(net2171));
	Integration_fr_AvgPool_core I__52 (.island_num(0), .row(7), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2165), .Dinrow_0(net2166));
	Integration_fr_AvgPool_core I__53 (.island_num(0), .row(7), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2167), .Dinrow_0(net2168));
	Integration_fr_AvgPool_core I__54 (.island_num(0), .row(7), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2169), .Dinrow_0(net2170));
	AvgPool_n_Relu I__55 (.island_num(0), .row(6), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__56 (.island_num(0), .row(8), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__57 (.island_num(0), .row(8), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__58 (.island_num(0), .row(9), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__59 (.island_num(0), .row(8), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__60 (.island_num(0), .row(9), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__61 (.island_num(0), .row(8), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2636), .Dinrow_0(net2637));
	Integration_fr_AvgPool_core I__62 (.island_num(0), .row(8), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2638), .Dinrow_0(net2639));
	Integration_fr_AvgPool_core I__63 (.island_num(0), .row(8), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2640), .Dinrow_0(net2641));
	Integration_fr_AvgPool_core I__64 (.island_num(0), .row(8), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2650), .Dinrow_0(net2642));
	Integration_fr_AvgPool_core I__65 (.island_num(0), .row(9), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2643), .Dinrow_0(net2650));
	Integration_fr_AvgPool_core I__66 (.island_num(0), .row(9), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2644), .Dinrow_0(net2645));
	Integration_fr_AvgPool_core I__67 (.island_num(0), .row(9), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2646), .Dinrow_0(net2647));
	Integration_fr_AvgPool_core I__68 (.island_num(0), .row(9), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2648), .Dinrow_0(net2649));
	AvgPool_n_Relu I__69 (.island_num(0), .row(8), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__70 (.island_num(0), .row(10), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__71 (.island_num(0), .row(10), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__72 (.island_num(0), .row(11), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__73 (.island_num(0), .row(10), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__74 (.island_num(0), .row(11), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__75 (.island_num(0), .row(10), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3115), .Dinrow_0(net3116));
	Integration_fr_AvgPool_core I__76 (.island_num(0), .row(10), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3117), .Dinrow_0(net3118));
	Integration_fr_AvgPool_core I__77 (.island_num(0), .row(10), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3119), .Dinrow_0(net3120));
	Integration_fr_AvgPool_core I__78 (.island_num(0), .row(10), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3129), .Dinrow_0(net3121));
	Integration_fr_AvgPool_core I__79 (.island_num(0), .row(11), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3122), .Dinrow_0(net3129));
	Integration_fr_AvgPool_core I__80 (.island_num(0), .row(11), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3123), .Dinrow_0(net3124));
	Integration_fr_AvgPool_core I__81 (.island_num(0), .row(11), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3125), .Dinrow_0(net3126));
	Integration_fr_AvgPool_core I__82 (.island_num(0), .row(11), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3127), .Dinrow_0(net3128));
	AvgPool_n_Relu I__83 (.island_num(0), .row(10), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__84 (.island_num(0), .row(12), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__85 (.island_num(0), .row(12), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__86 (.island_num(0), .row(13), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__87 (.island_num(0), .row(12), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__88 (.island_num(0), .row(13), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__89 (.island_num(0), .row(12), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3594), .Dinrow_0(net3595));
	Integration_fr_AvgPool_core I__90 (.island_num(0), .row(12), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3596), .Dinrow_0(net3597));
	Integration_fr_AvgPool_core I__91 (.island_num(0), .row(12), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3598), .Dinrow_0(net3599));
	Integration_fr_AvgPool_core I__92 (.island_num(0), .row(12), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3608), .Dinrow_0(net3600));
	Integration_fr_AvgPool_core I__93 (.island_num(0), .row(13), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3601), .Dinrow_0(net3608));
	Integration_fr_AvgPool_core I__94 (.island_num(0), .row(13), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3602), .Dinrow_0(net3603));
	Integration_fr_AvgPool_core I__95 (.island_num(0), .row(13), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3604), .Dinrow_0(net3605));
	Integration_fr_AvgPool_core I__96 (.island_num(0), .row(13), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3606), .Dinrow_0(net3607));
	AvgPool_n_Relu I__97 (.island_num(0), .row(12), .col(12), .matrix_row(2), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__98 (.island_num(0), .row(14), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__99 (.island_num(0), .row(14), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__100 (.island_num(0), .row(15), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__101 (.island_num(0), .row(14), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__102 (.island_num(0), .row(15), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__103 (.island_num(0), .row(14), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net4073), .Dinrow_0(net4074));
	Integration_fr_AvgPool_core I__104 (.island_num(0), .row(14), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net4075), .Dinrow_0(net4076));
	Integration_fr_AvgPool_core I__105 (.island_num(0), .row(14), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net4537), .Dinrow_0(net4077));
	Integration_fr_AvgPool_core I__106 (.island_num(0), .row(14), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net4084), .Dinrow_0(net4078));
	Integration_fr_AvgPool_core I__107 (.island_num(0), .row(15), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net4538), .Dinrow_0(net4084));
	Integration_fr_AvgPool_core I__108 (.island_num(0), .row(15), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net4079), .Dinrow_0(net4080));
	Integration_fr_AvgPool_core I__109 (.island_num(0), .row(15), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net4081), .Dinrow_0(net4082));
	Integration_fr_AvgPool_core I__110 (.island_num(0), .row(15), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net4539), .Dinrow_0(net4083));
	AvgPool_n_Relu I__111 (.island_num(0), .row(14), .col(12), .matrix_row(2), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(6));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(16), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(16), .type(prog_switch));


	/* Island 1 */
	FakeCellGateDecoder I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(4), .matrix_row(1), .matrix_col(4));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(3));
	TSMC350nm_IndirectSwitches switch(.island_num(1), .direction(horizontal), .num(4));


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Q_0(net4537), .N_n_Q_1(net4538), .N_n_Q_2(net4539));
 endmodule