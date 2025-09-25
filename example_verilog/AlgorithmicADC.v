module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VDDrow_0(net194), .VINJrow_0(net134), .GNDrow_0(net195), .VTUNrow_0(net153), .Progrow_0(net152), .Vg_0_row_0(net148), .Vg_1_row_0(net149), .Vsel_0_row_0(net150), .Vsel_1_row_0(net151), .VD_P_0_row_0(net167[0]), .VD_P_1_row_0(net168[0]), .VIN_PLUSrow_0(net160), .Voutrow_0(net187));
	EPOT I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net169[0]), .VD_P_1_row_0(net170[0]), .VIN_PLUSrow_0(net160), .Voutrow_0(net185));
	EPOT I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net160), .VINJ_brow_0(net159), .GND_brow_0(net158), .VTUN_brow_0(net155), .Prog_brow_0(net154), .Vg_b_0_row_0(net157), .Vsel_b_0_row_0(net156), .VD_P_0_row_0(net171[0]), .VD_P_1_row_0(net172[0]), .VIN_PLUSrow_0(net160), .Voutrow_0(net190));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net144), .decode_n0_VINJ_b_0_(net135), .decode_n0_VINJV(net147), .decode_n0_GNDV(net195), .decode_n0_n0_IN_1_(net146), .decode_n0_n0_IN_0_(net145));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net137), .switch_n0_RUN_IN_1_(net137), .switch_n0_GND_T(net195), .switch_n0_VINJ_T(net135), .switch_n0_CTRL_B_0_(net150), .switch_n0_CTRL_B_1_(net151), .switch_n0_Vg_0_(net148), .switch_n0_Vg_1_(net149), .switch_n0_VINJ(net134), .switch_n0_PROG(net152), .switch_n0_RUN(net138), .switch_n0_Vgsel(net136));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net142), .decode_n0_IN_0_(net141), .decode_n2_IN_1_(net140), .decode_n2_IN_0_(net139), .decode_n0_ENABLE(net143));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(3), .type(drain_select), .switch_n0_prog_drainrail(net132), .switch_n0_run_drainrail(net133), .switch_n0_VINJ(net178), .switch_n0_GND(net186));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(3), .type(prog_switch), .switch_n0_PR_0_(net167[0]), .switch_n0_PR_1_(net168[0]), .switch_n0_PR_2_(net169[0]), .switch_n0_PR_3_(net170[0]), .switch_n1_PR_0_(net171[0]), .switch_n1_PR_1_(net172[0]), .switch_n1_PR_2_(net173[0]), .switch_n1_PR_3_(net175[0]), .switch_n2_PR_0_(net177[0]), .switch_n1_In_2_(net174[0]), .switch_n1_In_3_(net176[0]), .switch_n0_VDD(net178), .switch_n0_GND(net186), .switch_n0_RUN(net138));


	/* Island 1 */
	AnalogBuffer I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VTUNrow_0(net161), .VDDrow_0(net165), .GNDrow_0(net166), .VINJrow_0(net164), .VINJ_brow_0(net178), .Vgrow_0(net162), .Vd_Prow_0(net177[0]), .Vselrow_0(net163), .Vinrow_0(net192), .Voutrow_0(net181));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VPWRrow_0(net160), .VINJrow_0(net159), .GNDrow_0(net158), .VTUNrow_0(net155), .Vgrow_0(net157), .VD_Prow_0(net173[0]), .VD_Rrow_0(net174[0]), .Vselrow_0(net156), .PROGrow_0(net154), .VIN_PLUSrow_0(net183), .VIN_MINUSrow_0(net187), .Voutrow_0(net196));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VPWR_brow_0(net165), .VINJ_brow_0(net164), .GND_brow_0(net166), .VTUN_brow_0(net161), .Vg_brow_0(net162), .VD_Prow_0(net175[0]), .VD_Rrow_0(net176[0]), .Vsel_brow_0(net163), .VIN_PLUSrow_0(net190), .VIN_MINUSrow_0(net188), .Voutrow_0(net191));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VDDrow_0(net194), .GNDrow_0(net195), .SELArow_0(net180), .Crow_0(net179), .Arow_0(net192));
	TGate_DT I__1 (.island_num(3), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net182), .Crow_0(net181), .Arow_0(net183));
	TGate_DT I__2 (.island_num(3), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net189), .Crow_0(net183), .Arow_0(net188));
	TGate_DT I__3 (.island_num(3), .row(3), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net189), .Crow_0(net188), .Arow_0(net191));
	TGate_DT I__4 (.island_num(3), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net196), .Crow_0(net184), .Arow_0(net186), .Brow_0(net185));
	TGate_DT I__5 (.island_num(3), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net193), .Crow_0(net192), .Arow_0(net191));

 	/*Programming Mux */ 


	/* Island 4 */
	Capacitor_80ff I__0 (.island_num(4), .row(0), .col(0), .matrix_row(2), .matrix_col(1), .Topcol_0(net183), .Botcol_0(net188));
	Capacitor_80ff I__1 (.island_num(4), .row(2), .col(0), .matrix_row(2), .matrix_col(1), .Topcol_0(net188), .Botcol_0(net184));
	Capacitor_80ff I__2 (.island_num(4), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .Toprow_0(net188), .Botrow_0(net191));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_PROG(net152), .N_n_RUN(net138), .N_n_VGRUN(net137), .N_n_VGPROG(net136), .N_n_VTUN(net153), .N_n_gnd(net195), .S_s_gnd(net186), .N_n_vinj(net147), .S_s_vinj(net178), .N_n_avdd(net194), .S_s_avdd(net160), .W_w_DrainB_0_(net139), .W_w_DrainB_1_(net140), .W_w_DrainB_2_(net141), .W_w_DrainB_3_(net142), .W_w_DrainEnable(net143), .W_w_GateB_0_(net145), .W_w_GateB_1_(net146), .N_n_GateEnable(net144), .S_s_Drainline_Prog(net132), .S_s_Drainline_Run(net133), .W_w_VIN(net179), .E_e_CLK_Sample(net180), .E_e_CLK_Amp(net182), .S_s_CLK_RST(net189), .E_e_CLK_Load(net193), .S_s_VRES(net191), .S_s_Code(net196), .E_e_DEBUG_0_(net187), .E_e_DEBUG_1_(net185), .E_e_DEBUG_2_(net190));
 endmodule