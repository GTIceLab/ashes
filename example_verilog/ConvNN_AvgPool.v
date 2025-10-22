module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__1 (.island_num(0), .row(0), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__2 (.island_num(0), .row(1), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__3 (.island_num(0), .row(0), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__4 (.island_num(0), .row(1), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__5 (.island_num(0), .row(0), .col(8), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4195), .CLKrow_0(net4194), .RST_Brow_0(net4196), .Vimg_CLKrow_0(net4197), .nxt_rw_0_row_0(net4198), .nxt_rw_1_row_0(net4198), .GNDrow_0(net4217), .AVDD_by_2_0_row_0(net4199), .AVDD_by_2_1_row_0(net4199), .prog_0_row_0(net4200), .prog_1_row_0(net4200), .run_0_row_0(net4201), .run_1_row_0(net4201), .Vg_0_row_0(net4078[0]), .Vg_1_row_0(net4080[0]), .Vsel_b_0_row_0(net4079[0]), .Vsel_b_1_row_0(net4081[0]), .AVDD_0_row_0(net4207[0]), .AVDD_1_row_0(net4207[0]), .VINJ_0_row_0(net4202), .VINJ_1_row_0(net4202), .VTUNrow_0(net4203), .DVDDrow_0(net4218), .Qrow_0(net479), .Dinrow_0(net4193));
	Integration_fr_AvgPool_core I__6 (.island_num(0), .row(0), .col(9), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4195), .CLKrow_0(net4194), .RST_Brow_0(net4196), .Vimg_CLKrow_0(net4197), .nxt_rw_0_row_0(net4198), .nxt_rw_1_row_0(net4198), .GNDrow_0(net4217), .AVDD_by_2_0_row_0(net4199), .AVDD_by_2_1_row_0(net4199), .prog_0_row_0(net4200), .prog_1_row_0(net4200), .run_0_row_0(net4201), .run_1_row_0(net4201), .Vg_0_row_0(net4082[0]), .Vg_1_row_0(net4084[0]), .Vsel_b_0_row_0(net4083[0]), .Vsel_b_1_row_0(net4085[0]), .AVDD_0_row_0(net4207[0]), .AVDD_1_row_0(net4207[0]), .VINJ_0_row_0(net4202), .VINJ_1_row_0(net4202), .VTUNrow_0(net4203), .DVDDrow_0(net4218), .Qrow_0(net480), .Dinrow_0(net481));
	Integration_fr_AvgPool_core I__7 (.island_num(0), .row(0), .col(10), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4195), .CLKrow_0(net4194), .RST_Brow_0(net4196), .Vimg_CLKrow_0(net4197), .nxt_rw_0_row_0(net4198), .nxt_rw_1_row_0(net4198), .GNDrow_0(net4217), .AVDD_by_2_0_row_0(net4199), .AVDD_by_2_1_row_0(net4199), .prog_0_row_0(net4200), .prog_1_row_0(net4200), .run_0_row_0(net4201), .run_1_row_0(net4201), .Vg_0_row_0(net4086[0]), .Vg_1_row_0(net4088[0]), .Vsel_b_0_row_0(net4087[0]), .Vsel_b_1_row_0(net4089[0]), .AVDD_0_row_0(net4207[0]), .AVDD_1_row_0(net4207[0]), .VINJ_0_row_0(net4202), .VINJ_1_row_0(net4202), .VTUNrow_0(net4203), .DVDDrow_0(net4218), .Qrow_0(net482), .Dinrow_0(net483));
	Integration_fr_AvgPool_core I__8 (.island_num(0), .row(0), .col(11), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4195), .CLKrow_0(net4194), .RST_Brow_0(net4196), .Vimg_CLKrow_0(net4197), .nxt_rw_0_row_0(net4198), .nxt_rw_1_row_0(net4198), .GNDrow_0(net4217), .AVDD_by_2_0_row_0(net4199), .AVDD_by_2_1_row_0(net4199), .prog_0_row_0(net4200), .prog_1_row_0(net4200), .run_0_row_0(net4201), .run_1_row_0(net4201), .Vg_0_row_0(net4090[0]), .Vg_1_row_0(net4092[0]), .Vsel_b_0_row_0(net4091[0]), .Vsel_b_1_row_0(net4093[0]), .AVDD_0_row_0(net4207[0]), .AVDD_1_row_0(net4207[0]), .VINJ_0_row_0(net4202), .VINJ_1_row_0(net4202), .VTUNrow_0(net4203), .DVDDrow_0(net4218), .Qrow_0(net492), .Dinrow_0(net484));
	Integration_fr_AvgPool_core I__9 (.island_num(0), .row(1), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net485), .Dinrow_0(net492));
	Integration_fr_AvgPool_core I__10 (.island_num(0), .row(1), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net486), .Dinrow_0(net487));
	Integration_fr_AvgPool_core I__11 (.island_num(0), .row(1), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net488), .Dinrow_0(net489));
	Integration_fr_AvgPool_core I__12 (.island_num(0), .row(1), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net490), .Dinrow_0(net491));
	AvgPool_n_Relu I__13 (.island_num(0), .row(0), .col(12), .matrix_row(2), .matrix_col(1), .prog_lvrow_0(net4204[0]), .run_lvrow_0(net4205[0]), .Vbrow_0(net4206[0]), .AVDDrow_0(net4207[0]), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4208), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__14 (.island_num(0), .row(2), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__15 (.island_num(0), .row(2), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__16 (.island_num(0), .row(3), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__17 (.island_num(0), .row(2), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__18 (.island_num(0), .row(3), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__19 (.island_num(0), .row(2), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net940), .Dinrow_0(net941));
	Integration_fr_AvgPool_core I__20 (.island_num(0), .row(2), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net942), .Dinrow_0(net943));
	Integration_fr_AvgPool_core I__21 (.island_num(0), .row(2), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net944), .Dinrow_0(net945));
	Integration_fr_AvgPool_core I__22 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net954), .Dinrow_0(net946));
	Integration_fr_AvgPool_core I__23 (.island_num(0), .row(3), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net947), .Dinrow_0(net954));
	Integration_fr_AvgPool_core I__24 (.island_num(0), .row(3), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net948), .Dinrow_0(net949));
	Integration_fr_AvgPool_core I__25 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net950), .Dinrow_0(net951));
	Integration_fr_AvgPool_core I__26 (.island_num(0), .row(3), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net952), .Dinrow_0(net953));
	AvgPool_n_Relu I__27 (.island_num(0), .row(2), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4209), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__28 (.island_num(0), .row(4), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__29 (.island_num(0), .row(4), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__30 (.island_num(0), .row(5), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__31 (.island_num(0), .row(4), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__32 (.island_num(0), .row(5), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__33 (.island_num(0), .row(4), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1402), .Dinrow_0(net1403));
	Integration_fr_AvgPool_core I__34 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1404), .Dinrow_0(net1405));
	Integration_fr_AvgPool_core I__35 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1406), .Dinrow_0(net1407));
	Integration_fr_AvgPool_core I__36 (.island_num(0), .row(4), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1416), .Dinrow_0(net1408));
	Integration_fr_AvgPool_core I__37 (.island_num(0), .row(5), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1409), .Dinrow_0(net1416));
	Integration_fr_AvgPool_core I__38 (.island_num(0), .row(5), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1410), .Dinrow_0(net1411));
	Integration_fr_AvgPool_core I__39 (.island_num(0), .row(5), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1412), .Dinrow_0(net1413));
	Integration_fr_AvgPool_core I__40 (.island_num(0), .row(5), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1414), .Dinrow_0(net1415));
	AvgPool_n_Relu I__41 (.island_num(0), .row(4), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4210), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__42 (.island_num(0), .row(6), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__43 (.island_num(0), .row(6), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__44 (.island_num(0), .row(7), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__45 (.island_num(0), .row(6), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__46 (.island_num(0), .row(7), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__47 (.island_num(0), .row(6), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1864), .Dinrow_0(net1865));
	Integration_fr_AvgPool_core I__48 (.island_num(0), .row(6), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1866), .Dinrow_0(net1867));
	Integration_fr_AvgPool_core I__49 (.island_num(0), .row(6), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1868), .Dinrow_0(net1869));
	Integration_fr_AvgPool_core I__50 (.island_num(0), .row(6), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1878), .Dinrow_0(net1870));
	Integration_fr_AvgPool_core I__51 (.island_num(0), .row(7), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1871), .Dinrow_0(net1878));
	Integration_fr_AvgPool_core I__52 (.island_num(0), .row(7), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1872), .Dinrow_0(net1873));
	Integration_fr_AvgPool_core I__53 (.island_num(0), .row(7), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1874), .Dinrow_0(net1875));
	Integration_fr_AvgPool_core I__54 (.island_num(0), .row(7), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1876), .Dinrow_0(net1877));
	AvgPool_n_Relu I__55 (.island_num(0), .row(6), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4211), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__56 (.island_num(0), .row(8), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__57 (.island_num(0), .row(8), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__58 (.island_num(0), .row(9), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__59 (.island_num(0), .row(8), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__60 (.island_num(0), .row(9), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__61 (.island_num(0), .row(8), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2326), .Dinrow_0(net2327));
	Integration_fr_AvgPool_core I__62 (.island_num(0), .row(8), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2328), .Dinrow_0(net2329));
	Integration_fr_AvgPool_core I__63 (.island_num(0), .row(8), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2330), .Dinrow_0(net2331));
	Integration_fr_AvgPool_core I__64 (.island_num(0), .row(8), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2340), .Dinrow_0(net2332));
	Integration_fr_AvgPool_core I__65 (.island_num(0), .row(9), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2333), .Dinrow_0(net2340));
	Integration_fr_AvgPool_core I__66 (.island_num(0), .row(9), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2334), .Dinrow_0(net2335));
	Integration_fr_AvgPool_core I__67 (.island_num(0), .row(9), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2336), .Dinrow_0(net2337));
	Integration_fr_AvgPool_core I__68 (.island_num(0), .row(9), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2338), .Dinrow_0(net2339));
	AvgPool_n_Relu I__69 (.island_num(0), .row(8), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4212), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__70 (.island_num(0), .row(10), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__71 (.island_num(0), .row(10), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__72 (.island_num(0), .row(11), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__73 (.island_num(0), .row(10), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__74 (.island_num(0), .row(11), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__75 (.island_num(0), .row(10), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2788), .Dinrow_0(net2789));
	Integration_fr_AvgPool_core I__76 (.island_num(0), .row(10), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2790), .Dinrow_0(net2791));
	Integration_fr_AvgPool_core I__77 (.island_num(0), .row(10), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2792), .Dinrow_0(net2793));
	Integration_fr_AvgPool_core I__78 (.island_num(0), .row(10), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2802), .Dinrow_0(net2794));
	Integration_fr_AvgPool_core I__79 (.island_num(0), .row(11), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2795), .Dinrow_0(net2802));
	Integration_fr_AvgPool_core I__80 (.island_num(0), .row(11), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2796), .Dinrow_0(net2797));
	Integration_fr_AvgPool_core I__81 (.island_num(0), .row(11), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2798), .Dinrow_0(net2799));
	Integration_fr_AvgPool_core I__82 (.island_num(0), .row(11), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2800), .Dinrow_0(net2801));
	AvgPool_n_Relu I__83 (.island_num(0), .row(10), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4213), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__84 (.island_num(0), .row(12), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__85 (.island_num(0), .row(12), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__86 (.island_num(0), .row(13), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__87 (.island_num(0), .row(12), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__88 (.island_num(0), .row(13), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__89 (.island_num(0), .row(12), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3250), .Dinrow_0(net3251));
	Integration_fr_AvgPool_core I__90 (.island_num(0), .row(12), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3252), .Dinrow_0(net3253));
	Integration_fr_AvgPool_core I__91 (.island_num(0), .row(12), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3254), .Dinrow_0(net3255));
	Integration_fr_AvgPool_core I__92 (.island_num(0), .row(12), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3264), .Dinrow_0(net3256));
	Integration_fr_AvgPool_core I__93 (.island_num(0), .row(13), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3257), .Dinrow_0(net3264));
	Integration_fr_AvgPool_core I__94 (.island_num(0), .row(13), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3258), .Dinrow_0(net3259));
	Integration_fr_AvgPool_core I__95 (.island_num(0), .row(13), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3260), .Dinrow_0(net3261));
	Integration_fr_AvgPool_core I__96 (.island_num(0), .row(13), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3262), .Dinrow_0(net3263));
	AvgPool_n_Relu I__97 (.island_num(0), .row(12), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4214), .Out_En_bcol_0(net4215[0:2]));
	TSMC350nm_4x2_Indirect I__98 (.island_num(0), .row(14), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__99 (.island_num(0), .row(14), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__100 (.island_num(0), .row(15), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__101 (.island_num(0), .row(14), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__102 (.island_num(0), .row(15), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__103 (.island_num(0), .row(14), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3712), .Dinrow_0(net3713));
	Integration_fr_AvgPool_core I__104 (.island_num(0), .row(14), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3714), .Dinrow_0(net3715));
	Integration_fr_AvgPool_core I__105 (.island_num(0), .row(14), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3716), .Dinrow_0(net3717));
	Integration_fr_AvgPool_core I__106 (.island_num(0), .row(14), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3726), .Dinrow_0(net3718));
	Integration_fr_AvgPool_core I__107 (.island_num(0), .row(15), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3719), .Dinrow_0(net3726));
	Integration_fr_AvgPool_core I__108 (.island_num(0), .row(15), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3720), .Dinrow_0(net3721));
	Integration_fr_AvgPool_core I__109 (.island_num(0), .row(15), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3722), .Dinrow_0(net3723));
	Integration_fr_AvgPool_core I__110 (.island_num(0), .row(15), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3724), .Dinrow_0(net3725));
	AvgPool_n_Relu I__111 (.island_num(0), .row(14), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4217), .DVDDcol_0(net4218), .Sub_img_outcol_0(net4216), .Out_En_bcol_0(net4215[0:2]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4), .decode_n0_VGRUN_0_(net4173[0]), .decode_n0_VGRUN_1_(net4174[0]), .decode_n0_VGRUN_2_(net4175[0]), .decode_n0_VGRUN_3_(net4176[0]), .decode_n1_VGRUN_0_(net4177[0]), .decode_n1_VGRUN_1_(net4178[0]), .decode_n1_VGRUN_2_(net4179[0]), .decode_n1_VGRUN_3_(net4180[0]), .decode_n2_VGRUN_0_(net4181[0]), .decode_n2_VGRUN_1_(net4182[0]), .decode_n2_VGRUN_2_(net4183[0]), .decode_n2_VGRUN_3_(net4184[0]), .decode_n2_n0_RUN_OUT_0_(net3984), .decode_n2_n0_RUN_OUT_1_(net3988), .decode_n2_n0_RUN_OUT_2_(net3992), .decode_n2_n0_RUN_OUT_3_(net3996), .decode_n2_n1_RUN_OUT_0_(net4000), .decode_n2_n1_RUN_OUT_1_(net4004), .decode_n2_n0_OUT_0_(net3985), .decode_n2_n0_OUT_1_(net3989), .decode_n2_n0_OUT_2_(net3993), .decode_n2_n0_OUT_3_(net3997), .decode_n2_n1_OUT_0_(net4001), .decode_n2_n1_OUT_1_(net4005), .decode_n0_ENABLE(net3980), .decode_n2_n0_VINJ_b_0_(net3982), .decode_n2_n0_VINJ_b_1_(net3986), .decode_n2_n1_VINJ_b_0_(net3990), .decode_n2_n1_VINJ_b_1_(net3994), .decode_n2_n2_VINJ_b_0_(net3998), .decode_n2_n2_VINJ_b_1_(net4002), .decode_n2_n0_GND_b_0_(net3983), .decode_n2_n0_GND_b_1_(net3987), .decode_n2_n1_GND_b_0_(net3991), .decode_n2_n1_GND_b_1_(net3995), .decode_n2_n2_GND_b_0_(net3999), .decode_n2_n2_GND_b_1_(net4003), .decode_n0_VINJV(net4202), .decode_n0_GNDV(net4217), .decode_n0_n0_IN_1_(net3981), .decode_n0_n0_IN_0_(net4098), .decode_n2_n0_IN_1_(net4097), .decode_n2_n0_IN_0_(net4096));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(6), .switch_n0_RUN_IN_0_(net3984), .switch_n0_RUN_IN_1_(net3988), .switch_n1_RUN_IN_0_(net3992), .switch_n1_RUN_IN_1_(net3996), .switch_n2_RUN_IN_0_(net4000), .switch_n2_RUN_IN_1_(net4004), .switch_n0_GND_T(net3983), .switch_n1_GND_T(net3987), .switch_n2_GND_T(net3991), .switch_n3_GND_T(net3995), .switch_n4_GND_T(net3999), .switch_n5_GND_T(net4003), .switch_n0_decode_0_(net3985), .switch_n0_decode_1_(net3989), .switch_n1_decode_0_(net3993), .switch_n1_decode_1_(net3997), .switch_n2_decode_0_(net4001), .switch_n2_decode_1_(net4005), .switch_n0_VINJ_T(net3982), .switch_n1_VINJ_T(net3986), .switch_n2_VINJ_T(net3990), .switch_n3_VINJ_T(net3994), .switch_n4_VINJ_T(net3998), .switch_n5_VINJ_T(net4002), .switch_n0_PROG(net4200), .switch_n0_RUN(net4201), .switch_n0_Vgsel(net4094), .switch_n0_vtun_l(net4203));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6), .decode_n0_VINJ(net4202), .decode_n0_GND(net4217), .decode_n0_IN_1_(net4014), .decode_n0_IN_0_(net4013), .decode_n2_IN_1_(net4012), .decode_n2_IN_0_(net4011), .decode_n4_IN_1_(net4010), .decode_n4_IN_0_(net4009), .decode_n0_ENABLE(net4008));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(16), .type(drain_select), .switch_n0_prog_drainrail(net4006), .switch_n0_run_drainrail(net4007), .switch_n0_VINJ(net4202), .switch_n0_GND(net4217));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(16), .type(prog_switch), .switch_n0_RUN(net4201), .switch_n0_VDD_b(net4202), .switch_n0_GND_b(net4217));


	/* Island 1 */
	FakeCellGateDecoder I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(4));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(3), .decode_n2_n0_RUN_OUT_0_(net4101), .decode_n2_n0_RUN_OUT_1_(net4105), .decode_n2_n0_RUN_OUT_2_(net4109), .decode_n2_n0_RUN_OUT_3_(net4113), .decode_n2_n0_OUT_0_(net4102), .decode_n2_n0_OUT_1_(net4106), .decode_n2_n0_OUT_2_(net4110), .decode_n2_n0_OUT_3_(net4114), .decode_n0_ENABLE(net4095), .decode_n2_n0_VINJ_b_0_(net4099), .decode_n2_n0_VINJ_b_1_(net4103), .decode_n2_n1_VINJ_b_0_(net4107), .decode_n2_n1_VINJ_b_1_(net4111), .decode_n2_n0_GND_b_0_(net4100), .decode_n2_n0_GND_b_1_(net4104), .decode_n2_n1_GND_b_0_(net4108), .decode_n2_n1_GND_b_1_(net4112), .decode_n0_VINJV(net4202), .decode_n0_GNDV(net4217), .decode_n0_n0_IN_0_(net4098), .decode_n2_n0_IN_1_(net4097), .decode_n2_n0_IN_0_(net4096));
	TSMC350nm_IndirectSwitches switch(.island_num(1), .direction(horizontal), .num(4), .switch_n0_RUN_IN_0_(net4101), .switch_n0_RUN_IN_1_(net4105), .switch_n1_RUN_IN_0_(net4109), .switch_n1_RUN_IN_1_(net4113), .switch_n0_GND_T(net4100), .switch_n1_GND_T(net4104), .switch_n2_GND_T(net4108), .switch_n3_GND_T(net4112), .switch_n0_decode_0_(net4102), .switch_n0_decode_1_(net4106), .switch_n1_decode_0_(net4110), .switch_n1_decode_1_(net4114), .switch_n0_VINJ_T(net4099), .switch_n1_VINJ_T(net4103), .switch_n2_VINJ_T(net4107), .switch_n3_VINJ_T(net4111), .switch_n0_CTRL_B_0_(net4079[0]), .switch_n0_CTRL_B_1_(net4081[0]), .switch_n1_CTRL_B_0_(net4083[0]), .switch_n1_CTRL_B_1_(net4085[0]), .switch_n2_CTRL_B_0_(net4087[0]), .switch_n2_CTRL_B_1_(net4089[0]), .switch_n3_CTRL_B_0_(net4091[0]), .switch_n3_CTRL_B_1_(net4093[0]), .switch_n0_Vg_0_(net4078[0]), .switch_n0_Vg_1_(net4080[0]), .switch_n1_Vg_0_(net4082[0]), .switch_n1_Vg_1_(net4084[0]), .switch_n2_Vg_0_(net4086[0]), .switch_n2_Vg_1_(net4088[0]), .switch_n3_Vg_0_(net4090[0]), .switch_n3_Vg_1_(net4092[0]), .switch_n0_PROG(net4200), .switch_n0_RUN(net4201), .switch_n0_Vgsel(net4094), .switch_n0_vtun_l(net4203));


	/* Island 2 */
	DynamicShiftReg_Rst_Lo I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(4), .Dincol_0(net4189[0]), .RST_Bcol_0(net4192[0]), .CLKcol_0(net4190[0]), .CLKBcol_0(net4191[0]));
	Tgate_swc_fr_Kernel_Vert I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .GNDrow_0(net4217), .Vg_Rrow_0(net4173[0]), .Vimgrow_0(net4185), .DVDDrow_0(net4218), .AVDDrow_0(net4207[0]));
	Tgate_swc_fr_Kernel_Vert I__2 (.island_num(2), .row(1), .col(1), .matrix_row(1), .matrix_col(1), .Vg_Rrow_0(net4174[0]));
	Tgate_swc_fr_Kernel_Vert I__3 (.island_num(2), .row(1), .col(2), .matrix_row(1), .matrix_col(1), .Vg_Rrow_0(net4175[0]));
	Tgate_swc_fr_Kernel_Vert I__4 (.island_num(2), .row(1), .col(3), .matrix_row(1), .matrix_col(1), .Vg_Rrow_0(net4176[0]));
	Tgate_swc_fr_Kernel_Vert I__5 (.island_num(2), .row(1), .col(5), .GND(net4217), .Q(net4188), .Vg_R(net4177[0]), .Q_bot(net4188), .Vimg(net4186), .DVDD(net4218), .AVDD(net4207[0]));
	Tgate_swc_fr_Kernel_Vert I__6 (.island_num(2), .row(1), .col(6), .matrix_row(1), .matrix_col(1), .Qrow_0(net4188), .Vg_Rrow_0(net4178[0]));
	Tgate_swc_fr_Kernel_Vert I__7 (.island_num(2), .row(1), .col(7), .matrix_row(1), .matrix_col(1), .Qrow_0(net4188), .Vg_Rrow_0(net4179[0]));
	Tgate_swc_fr_Kernel_Vert I__8 (.island_num(2), .row(1), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net4188), .Vg_Rrow_0(net4180[0]));
	Tgate_swc_fr_Kernel_Vert I__9 (.island_num(2), .row(1), .col(10), .GND(net4217), .Q(net4188), .Vg_R(net4181[0]), .Vimg(net4187), .DVDD(net4218), .AVDD(net4207[0]));
	Tgate_swc_fr_Kernel_Vert I__10 (.island_num(2), .row(1), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net4188), .Vg_Rrow_0(net4182[0]));
	Tgate_swc_fr_Kernel_Vert I__11 (.island_num(2), .row(1), .col(12), .matrix_row(1), .matrix_col(1), .Qrow_0(net4188), .Vg_Rrow_0(net4183[0]));
	Tgate_swc_fr_Kernel_Vert I__12 (.island_num(2), .row(1), .col(13), .matrix_row(1), .matrix_col(1), .Qrow_0(net4188), .Vg_Rrow_0(net4184[0]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Kvmm_G_En(net3980), .N_n_AvgPool_FGs_G_En(net4095), .N_n_Kvmm_G_bit_0_(net4096), .N_n_Kvmm_G_bit_1_(net4097), .N_n_Kvmm_G_bit_2_(net4098), .N_n_Kvmm_G_bit_3_(net3981), .N_n_Kvmm_AvgP_Dr_En(net4008), .N_n_Kvmm_AvgP_Dr_bit_0_(net4009), .N_n_Kvmm_AvgP_Dr_bit_1_(net4010), .N_n_Kvmm_AvgP_Dr_bit_2_(net4011), .N_n_Kvmm_AvgP_Dr_bit_3_(net4012), .N_n_Kvmm_AvgP_Dr_bit_4_(net4013), .N_n_Kvmm_AvgP_Dr_bit_5_(net4014), .N_n_Kvmm_AvgP_Prog_Drln(net4006), .N_n_Kvmm_AvgP_Run_Drln(net4007), .N_n_K_col_Din(net4189[0]), .N_n_K_col_CLKB(net4191[0]), .N_n_K_col_RST_B(net4192[0]), .N_n_K_col_CLK(net4190[0]), .E_e_Vin_inp_Ch_0_(net4185), .E_e_Vin_inp_Ch_1_(net4186), .E_e_Vin_inp_Ch_2_(net4187), .N_n_AVDD_by_2(net4199), .N_n_SR_Intg_RST_B(net4196), .N_n_SR_Intg_Din(net4193), .N_n_SR_Intg_CLK(net4194), .N_n_SR_Intg_CLKB(net4195), .N_n_SR_Intg_nxt_rw(net4198), .N_n_Vimg_CLK(net4197), .N_n_AvgPool_Relu_Vb(net4206[0]), .E_e_Sub_img_out_0_(net4208), .E_e_Sub_img_out_1_(net4209), .E_e_Sub_img_out_2_(net4210), .E_e_Sub_img_out_3_(net4211), .E_e_Sub_img_out_4_(net4212), .E_e_Sub_img_out_5_(net4213), .E_e_Sub_img_out_6_(net4214), .E_e_Sub_img_out_7_(net4216), .N_n_VTUN(net4203), .N_n_DVDD(net4218), .N_n_AVDD(net4207[0]), .N_n_GND(net4217), .N_n_VINJ(net4202), .N_n_VGPROG(net4094), .N_n_prog_hv(net4200), .N_n_run_hv(net4201), .N_n_prog_lv(net4204[0]), .N_n_run_lv(net4205[0]));
 endmodule