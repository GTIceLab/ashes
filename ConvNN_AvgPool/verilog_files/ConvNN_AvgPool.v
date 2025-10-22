module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__1 (.island_num(0), .row(0), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__2 (.island_num(0), .row(1), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__3 (.island_num(0), .row(0), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__4 (.island_num(0), .row(1), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__5 (.island_num(0), .row(0), .col(8), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4288), .CLKrow_0(net4287), .RST_Brow_0(net4289), .Vimg_CLKrow_0(net4290[0]), .GNDrow_0(net4308), .AVDD_by_2_0_row_0(net4291), .AVDD_by_2_1_row_0(net4291), .prog_0_row_0(net4292), .prog_1_row_0(net4292), .run_0_row_0(net4293), .run_1_row_0(net4293), .Vg_0_row_0(net4176[0]), .Vg_1_row_0(net4178[0]), .Vsel_b_0_row_0(net4177[0]), .Vsel_b_1_row_0(net4179[0]), .AVDD_0_row_0(net4299[0]), .AVDD_1_row_0(net4299[0]), .VINJ_0_row_0(net4294), .VINJ_1_row_0(net4294), .VTUNrow_0(net4295), .Qrow_0(net491), .Dinrow_0(net4286));
	Integration_fr_AvgPool_core I__6 (.island_num(0), .row(0), .col(9), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4288), .CLKrow_0(net4287), .RST_Brow_0(net4289), .Vimg_CLKrow_0(net4290[0]), .GNDrow_0(net4308), .AVDD_by_2_0_row_0(net4291), .AVDD_by_2_1_row_0(net4291), .prog_0_row_0(net4292), .prog_1_row_0(net4292), .run_0_row_0(net4293), .run_1_row_0(net4293), .Vg_0_row_0(net4180[0]), .Vg_1_row_0(net4182[0]), .Vsel_b_0_row_0(net4181[0]), .Vsel_b_1_row_0(net4183[0]), .AVDD_0_row_0(net4299[0]), .AVDD_1_row_0(net4299[0]), .VINJ_0_row_0(net4294), .VINJ_1_row_0(net4294), .VTUNrow_0(net4295), .Qrow_0(net492), .Dinrow_0(net493));
	Integration_fr_AvgPool_core I__7 (.island_num(0), .row(0), .col(10), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4288), .CLKrow_0(net4287), .RST_Brow_0(net4289), .Vimg_CLKrow_0(net4290[0]), .GNDrow_0(net4308), .AVDD_by_2_0_row_0(net4291), .AVDD_by_2_1_row_0(net4291), .prog_0_row_0(net4292), .prog_1_row_0(net4292), .run_0_row_0(net4293), .run_1_row_0(net4293), .Vg_0_row_0(net4184[0]), .Vg_1_row_0(net4186[0]), .Vsel_b_0_row_0(net4185[0]), .Vsel_b_1_row_0(net4187[0]), .AVDD_0_row_0(net4299[0]), .AVDD_1_row_0(net4299[0]), .VINJ_0_row_0(net4294), .VINJ_1_row_0(net4294), .VTUNrow_0(net4295), .Qrow_0(net494), .Dinrow_0(net495));
	Integration_fr_AvgPool_core I__8 (.island_num(0), .row(0), .col(11), .matrix_row(1), .matrix_col(1), .CLKBrow_0(net4288), .CLKrow_0(net4287), .RST_Brow_0(net4289), .Vimg_CLKrow_0(net4290[0]), .GNDrow_0(net4308), .AVDD_by_2_0_row_0(net4291), .AVDD_by_2_1_row_0(net4291), .prog_0_row_0(net4292), .prog_1_row_0(net4292), .run_0_row_0(net4293), .run_1_row_0(net4293), .Vg_0_row_0(net4188[0]), .Vg_1_row_0(net4190[0]), .Vsel_b_0_row_0(net4189[0]), .Vsel_b_1_row_0(net4191[0]), .AVDD_0_row_0(net4299[0]), .AVDD_1_row_0(net4299[0]), .VINJ_0_row_0(net4294), .VINJ_1_row_0(net4294), .VTUNrow_0(net4295), .Qrow_0(net504), .Dinrow_0(net496));
	Integration_fr_AvgPool_core I__9 (.island_num(0), .row(1), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net497), .Dinrow_0(net504));
	Integration_fr_AvgPool_core I__10 (.island_num(0), .row(1), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net498), .Dinrow_0(net499));
	Integration_fr_AvgPool_core I__11 (.island_num(0), .row(1), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net500), .Dinrow_0(net501));
	Integration_fr_AvgPool_core I__12 (.island_num(0), .row(1), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net502), .Dinrow_0(net503));
	AvgPool_n_Relu I__13 (.island_num(0), .row(0), .col(12), .matrix_row(2), .matrix_col(1), .prog_lvrow_0(net4296[0]), .run_lvrow_0(net4297[0]), .Vbrow_0(net4298[0]), .AVDDrow_0(net4299[0]), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4300), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__14 (.island_num(0), .row(2), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__15 (.island_num(0), .row(2), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__16 (.island_num(0), .row(3), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__17 (.island_num(0), .row(2), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__18 (.island_num(0), .row(3), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__19 (.island_num(0), .row(2), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net952), .Dinrow_0(net953));
	Integration_fr_AvgPool_core I__20 (.island_num(0), .row(2), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net954), .Dinrow_0(net955));
	Integration_fr_AvgPool_core I__21 (.island_num(0), .row(2), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net956), .Dinrow_0(net957));
	Integration_fr_AvgPool_core I__22 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net966), .Dinrow_0(net958));
	Integration_fr_AvgPool_core I__23 (.island_num(0), .row(3), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net959), .Dinrow_0(net966));
	Integration_fr_AvgPool_core I__24 (.island_num(0), .row(3), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net960), .Dinrow_0(net961));
	Integration_fr_AvgPool_core I__25 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net962), .Dinrow_0(net963));
	Integration_fr_AvgPool_core I__26 (.island_num(0), .row(3), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net964), .Dinrow_0(net965));
	AvgPool_n_Relu I__27 (.island_num(0), .row(2), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4301), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__28 (.island_num(0), .row(4), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__29 (.island_num(0), .row(4), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__30 (.island_num(0), .row(5), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__31 (.island_num(0), .row(4), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__32 (.island_num(0), .row(5), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__33 (.island_num(0), .row(4), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1414), .Dinrow_0(net1415));
	Integration_fr_AvgPool_core I__34 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1416), .Dinrow_0(net1417));
	Integration_fr_AvgPool_core I__35 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1418), .Dinrow_0(net1419));
	Integration_fr_AvgPool_core I__36 (.island_num(0), .row(4), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1428), .Dinrow_0(net1420));
	Integration_fr_AvgPool_core I__37 (.island_num(0), .row(5), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1421), .Dinrow_0(net1428));
	Integration_fr_AvgPool_core I__38 (.island_num(0), .row(5), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1422), .Dinrow_0(net1423));
	Integration_fr_AvgPool_core I__39 (.island_num(0), .row(5), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1424), .Dinrow_0(net1425));
	Integration_fr_AvgPool_core I__40 (.island_num(0), .row(5), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1426), .Dinrow_0(net1427));
	AvgPool_n_Relu I__41 (.island_num(0), .row(4), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4302), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__42 (.island_num(0), .row(6), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__43 (.island_num(0), .row(6), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__44 (.island_num(0), .row(7), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__45 (.island_num(0), .row(6), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__46 (.island_num(0), .row(7), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__47 (.island_num(0), .row(6), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1876), .Dinrow_0(net1877));
	Integration_fr_AvgPool_core I__48 (.island_num(0), .row(6), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1878), .Dinrow_0(net1879));
	Integration_fr_AvgPool_core I__49 (.island_num(0), .row(6), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1880), .Dinrow_0(net1881));
	Integration_fr_AvgPool_core I__50 (.island_num(0), .row(6), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1890), .Dinrow_0(net1882));
	Integration_fr_AvgPool_core I__51 (.island_num(0), .row(7), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net1883), .Dinrow_0(net1890));
	Integration_fr_AvgPool_core I__52 (.island_num(0), .row(7), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net1884), .Dinrow_0(net1885));
	Integration_fr_AvgPool_core I__53 (.island_num(0), .row(7), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net1886), .Dinrow_0(net1887));
	Integration_fr_AvgPool_core I__54 (.island_num(0), .row(7), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net1888), .Dinrow_0(net1889));
	AvgPool_n_Relu I__55 (.island_num(0), .row(6), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4303), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__56 (.island_num(0), .row(8), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__57 (.island_num(0), .row(8), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__58 (.island_num(0), .row(9), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__59 (.island_num(0), .row(8), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__60 (.island_num(0), .row(9), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__61 (.island_num(0), .row(8), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2338), .Dinrow_0(net2339));
	Integration_fr_AvgPool_core I__62 (.island_num(0), .row(8), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2340), .Dinrow_0(net2341));
	Integration_fr_AvgPool_core I__63 (.island_num(0), .row(8), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2342), .Dinrow_0(net2343));
	Integration_fr_AvgPool_core I__64 (.island_num(0), .row(8), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2352), .Dinrow_0(net2344));
	Integration_fr_AvgPool_core I__65 (.island_num(0), .row(9), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2345), .Dinrow_0(net2352));
	Integration_fr_AvgPool_core I__66 (.island_num(0), .row(9), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2346), .Dinrow_0(net2347));
	Integration_fr_AvgPool_core I__67 (.island_num(0), .row(9), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2348), .Dinrow_0(net2349));
	Integration_fr_AvgPool_core I__68 (.island_num(0), .row(9), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2350), .Dinrow_0(net2351));
	AvgPool_n_Relu I__69 (.island_num(0), .row(8), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4304), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__70 (.island_num(0), .row(10), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__71 (.island_num(0), .row(10), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__72 (.island_num(0), .row(11), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__73 (.island_num(0), .row(10), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__74 (.island_num(0), .row(11), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__75 (.island_num(0), .row(10), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2800), .Dinrow_0(net2801));
	Integration_fr_AvgPool_core I__76 (.island_num(0), .row(10), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2802), .Dinrow_0(net2803));
	Integration_fr_AvgPool_core I__77 (.island_num(0), .row(10), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2804), .Dinrow_0(net2805));
	Integration_fr_AvgPool_core I__78 (.island_num(0), .row(10), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2814), .Dinrow_0(net2806));
	Integration_fr_AvgPool_core I__79 (.island_num(0), .row(11), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net2807), .Dinrow_0(net2814));
	Integration_fr_AvgPool_core I__80 (.island_num(0), .row(11), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net2808), .Dinrow_0(net2809));
	Integration_fr_AvgPool_core I__81 (.island_num(0), .row(11), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net2810), .Dinrow_0(net2811));
	Integration_fr_AvgPool_core I__82 (.island_num(0), .row(11), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net2812), .Dinrow_0(net2813));
	AvgPool_n_Relu I__83 (.island_num(0), .row(10), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4305), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__84 (.island_num(0), .row(12), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__85 (.island_num(0), .row(12), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__86 (.island_num(0), .row(13), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__87 (.island_num(0), .row(12), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__88 (.island_num(0), .row(13), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__89 (.island_num(0), .row(12), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3262), .Dinrow_0(net3263));
	Integration_fr_AvgPool_core I__90 (.island_num(0), .row(12), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3264), .Dinrow_0(net3265));
	Integration_fr_AvgPool_core I__91 (.island_num(0), .row(12), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3266), .Dinrow_0(net3267));
	Integration_fr_AvgPool_core I__92 (.island_num(0), .row(12), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3276), .Dinrow_0(net3268));
	Integration_fr_AvgPool_core I__93 (.island_num(0), .row(13), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3269), .Dinrow_0(net3276));
	Integration_fr_AvgPool_core I__94 (.island_num(0), .row(13), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3270), .Dinrow_0(net3271));
	Integration_fr_AvgPool_core I__95 (.island_num(0), .row(13), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3272), .Dinrow_0(net3273));
	Integration_fr_AvgPool_core I__96 (.island_num(0), .row(13), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3274), .Dinrow_0(net3275));
	AvgPool_n_Relu I__97 (.island_num(0), .row(12), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4306), .Out_En_bcol_0(net4307[0:2]));
	TSMC350nm_4x2_Indirect I__98 (.island_num(0), .row(14), .col(0), .matrix_row(2), .matrix_col(6));
	Tgate_swc_fr_Kernel_Horiz_top_edge I__99 (.island_num(0), .row(14), .col(6), .matrix_row(1), .matrix_col(1));
	Tgate_swc_fr_Kernel_Horiz_bot_edge I__100 (.island_num(0), .row(15), .col(6), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__101 (.island_num(0), .row(14), .col(7), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_core I__102 (.island_num(0), .row(15), .col(7), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__103 (.island_num(0), .row(14), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3724), .Dinrow_0(net3725));
	Integration_fr_AvgPool_core I__104 (.island_num(0), .row(14), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3726), .Dinrow_0(net3727));
	Integration_fr_AvgPool_core I__105 (.island_num(0), .row(14), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3728), .Dinrow_0(net3729));
	Integration_fr_AvgPool_core I__106 (.island_num(0), .row(14), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3738), .Dinrow_0(net3730));
	Integration_fr_AvgPool_core I__107 (.island_num(0), .row(15), .col(8), .matrix_row(1), .matrix_col(1), .Qrow_0(net3731), .Dinrow_0(net3738));
	Integration_fr_AvgPool_core I__108 (.island_num(0), .row(15), .col(9), .matrix_row(1), .matrix_col(1), .Qrow_0(net3732), .Dinrow_0(net3733));
	Integration_fr_AvgPool_core I__109 (.island_num(0), .row(15), .col(10), .matrix_row(1), .matrix_col(1), .Qrow_0(net3734), .Dinrow_0(net3735));
	Integration_fr_AvgPool_core I__110 (.island_num(0), .row(15), .col(11), .matrix_row(1), .matrix_col(1), .Qrow_0(net3736), .Dinrow_0(net3737));
	AvgPool_n_Relu I__111 (.island_num(0), .row(14), .col(12), .matrix_row(2), .matrix_col(1), .GNDcol_0(net4308), .DVDDcol_0(net4309), .Sub_img_outcol_0(net4311), .Out_En_bcol_0(net4307[0:2]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(6));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(16), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(16), .type(prog_switch));


	/* Island 1 */
	FakeCellGateDecoder I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(4));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(3));
	TSMC350nm_IndirectSwitches switch(.island_num(1), .direction(horizontal), .num(4), .switch_n0_CTRL_B_0_(net4177[0]), .switch_n0_CTRL_B_1_(net4179[0]), .switch_n1_CTRL_B_0_(net4181[0]), .switch_n1_CTRL_B_1_(net4183[0]), .switch_n2_CTRL_B_0_(net4185[0]), .switch_n2_CTRL_B_1_(net4187[0]), .switch_n3_CTRL_B_0_(net4189[0]), .switch_n3_CTRL_B_1_(net4191[0]), .switch_n0_Vg_0_(net4176[0]), .switch_n0_Vg_1_(net4178[0]), .switch_n1_Vg_0_(net4180[0]), .switch_n1_Vg_1_(net4182[0]), .switch_n2_Vg_0_(net4184[0]), .switch_n2_Vg_1_(net4186[0]), .switch_n3_Vg_0_(net4188[0]), .switch_n3_Vg_1_(net4190[0]));


	/* Island 2 */
	DynamicShiftReg_Rst_Lo I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(4), .Dincol_0(net4283[0]), .RST_Bcol_0(net4285[0]), .CLKcol_0(net4290[0]), .CLKBcol_0(net4284[0]));
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
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_K_col_Din(net4283[0]), .N_n_K_col_CLK(net4290[0]), .N_n_K_col_CLKB(net4284[0]), .N_n_K_col_RST_B(net4285[0]), .N_n_AVDD_by_2(net4291), .N_n_SR_Intg_Din(net4286), .N_n_SR_Intg_CLK(net4287), .N_n_SR_Intg_CLKB(net4288), .N_n_SR_Intg_RST_B(net4289), .N_n_AvgPool_Relu_Vb(net4298[0]), .E_e_Sub_img_out_0(net4300), .E_e_Sub_img_out_1(net4301), .E_e_Sub_img_out_2(net4302), .E_e_Sub_img_out_3(net4303), .E_e_Sub_img_out_4(net4304), .E_e_Sub_img_out_5(net4305), .E_e_Sub_img_out_6(net4306), .E_e_Sub_img_out_7(net4311), .N_n_VTUN(net4295), .N_n_DVDD(net4309), .N_n_AVDD(net4299[0]), .N_n_GND(net4308), .N_n_VINJ(net4294), .N_n_prog_hv(net4292), .N_n_run_hv(net4293), .N_n_prog_lv(net4296[0]), .N_n_run_lv(net4297[0]));
 endmodule