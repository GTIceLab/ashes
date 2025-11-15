module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VDDrow_0(net195), .VINJrow_0(net135), .GNDrow_0(net196), .VTUNrow_0(net154), .Progrow_0(net153), .Vg_0_row_0(net149), .Vg_1_row_0(net150), .Vsel_0_row_0(net151), .Vsel_1_row_0(net152), .VD_P_0_row_0(net168[0]), .VD_P_1_row_0(net169[0]), .VIN_PLUSrow_0(net161), .Voutrow_0(net188));
	EPOT I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net170[0]), .VD_P_1_row_0(net171[0]), .VIN_PLUSrow_0(net161), .Voutrow_0(net186));
	EPOT I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net161), .VINJ_brow_0(net160), .GND_brow_0(net159), .VTUN_brow_0(net156), .Prog_brow_0(net155), .Vg_b_0_row_0(net158), .Vsel_b_0_row_0(net157), .VD_P_0_row_0(net172[0]), .VD_P_1_row_0(net173[0]), .VIN_PLUSrow_0(net161), .Voutrow_0(net191));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net145), .decode_n0_VINJ_b_0_(net136), .decode_n0_VINJV(net148), .decode_n0_GNDV(net196), .decode_n0_n0_IN_1_(net147), .decode_n0_n0_IN_0_(net146));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net138), .switch_n0_RUN_IN_1_(net138), .switch_n0_GND_T(net196), .switch_n0_VINJ_T(net136), .switch_n0_CTRL_B_0_(net151), .switch_n0_CTRL_B_1_(net152), .switch_n0_Vg_0_(net149), .switch_n0_Vg_1_(net150), .switch_n0_VINJ(net135), .switch_n0_PROG(net153), .switch_n0_RUN(net139), .switch_n0_Vgsel(net137));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net143), .decode_n0_IN_0_(net142), .decode_n2_IN_1_(net141), .decode_n2_IN_0_(net140), .decode_n0_ENABLE(net144));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(3), .type(drain_select), .switch_n0_prog_drainrail(net133), .switch_n0_run_drainrail(net134), .switch_n0_VINJ(net179), .switch_n0_GND(net187));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(3), .type(prog_switch), .switch_n0_PR_0_(net168[0]), .switch_n0_PR_1_(net169[0]), .switch_n0_PR_2_(net170[0]), .switch_n0_PR_3_(net171[0]), .switch_n1_PR_0_(net172[0]), .switch_n1_PR_1_(net173[0]), .switch_n1_PR_2_(net174[0]), .switch_n1_PR_3_(net176[0]), .switch_n2_PR_0_(net178[0]), .switch_n1_In_2_(net175[0]), .switch_n1_In_3_(net177[0]), .switch_n0_VDD(net179), .switch_n0_GND(net187), .switch_n0_RUN(net139));


	/* Island 1 */
	TSMC350nm_AnalogBuffer I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VTUNrow_0(net162), .VDDrow_0(net166), .GNDrow_0(net167), .VINJrow_0(net165), .VINJ_brow_0(net179), .Vgrow_0(net163), .Vd_Prow_0(net178[0]), .Vselrow_0(net164), .Vinrow_0(net193), .Voutrow_0(net182));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VPWRrow_0(net161), .VINJrow_0(net160), .GNDrow_0(net159), .VTUNrow_0(net156), .Vgrow_0(net158), .VD_Prow_0(net174[0]), .VD_Rrow_0(net175[0]), .Vselrow_0(net157), .PROGrow_0(net155), .VIN_PLUSrow_0(net184), .VIN_MINUSrow_0(net188), .Voutrow_0(net197));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VPWR_brow_0(net166), .VINJ_brow_0(net165), .GND_brow_0(net167), .VTUN_brow_0(net162), .Vg_brow_0(net163), .VD_Prow_0(net176[0]), .VD_Rrow_0(net177[0]), .Vsel_brow_0(net164), .VIN_PLUSrow_0(net191), .VIN_MINUSrow_0(net189), .Voutrow_0(net192));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VDDrow_0(net195), .GNDrow_0(net196), .SELArow_0(net181), .Crow_0(net180), .Arow_0(net193));
	TGate_DT I__1 (.island_num(3), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net183), .Crow_0(net182), .Arow_0(net184));
	TGate_DT I__2 (.island_num(3), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net190), .Crow_0(net184), .Arow_0(net189));
	TGate_DT I__3 (.island_num(3), .row(3), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net190), .Crow_0(net189), .Arow_0(net192));
	TGate_DT I__4 (.island_num(3), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net197), .Crow_0(net185), .Arow_0(net187), .Brow_0(net186));
	TGate_DT I__5 (.island_num(3), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net194), .Crow_0(net193), .Arow_0(net192));

 	/*Programming Mux */ 


	/* Island 4 */
	Capacitor_80ff I__0 (.island_num(4), .row(0), .col(0), .matrix_row(2), .matrix_col(1), .Topcol_0(net184), .Botcol_0(net189));
	Capacitor_80ff I__1 (.island_num(4), .row(2), .col(0), .matrix_row(2), .matrix_col(1), .Topcol_0(net189), .Botcol_0(net185));
	Capacitor_80ff I__2 (.island_num(4), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .Toprow_0(net189), .Botrow_0(net192));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_PROG(net153), .N_n_RUN(net139), .N_n_VGRUN(net138), .N_n_VGPROG(net137), .N_n_VTUN(net154), .N_n_gnd(net196), .S_s_gnd(net187), .N_n_vinj(net148), .S_s_vinj(net179), .N_n_avdd(net195), .S_s_avdd(net161), .W_w_DrainB_0_(net140), .W_w_DrainB_1_(net141), .W_w_DrainB_2_(net142), .W_w_DrainB_3_(net143), .W_w_DrainEnable(net144), .W_w_GateB_0_(net146), .W_w_GateB_1_(net147), .N_n_GateEnable(net145), .S_s_Drainline_Prog(net133), .S_s_Drainline_Run(net134), .W_w_VIN(net180), .E_e_CLK_Sample(net181), .E_e_CLK_Amp(net183), .S_s_CLK_RST(net190), .E_e_CLK_Load(net194), .S_s_VRES(net192), .S_s_Code(net197), .E_e_DEBUG_0_(net188), .E_e_DEBUG_1_(net186), .E_e_DEBUG_2_(net191));
 endmodule