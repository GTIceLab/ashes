module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VINJrow_0(net171), .GNDrow_0(net183), .VTUNrow_0(net164), .Progrow_0(net159), .Vg_0_row_0(net154), .Vg_1_row_0(net155), .Vsel_0_row_0(net156), .Vsel_1_row_0(net157), .VD_P_0_row_0(net184[0]), .VD_P_1_row_0(net185[0]), .Voutrow_0(net205));
	EPOT I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net186[0]), .VD_P_1_row_0(net187[0]), .Voutrow_0(net203));
	EPOT I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .VINJ_brow_0(net163), .GND_brow_0(net162), .VTUN_brow_0(net160), .Prog_brow_0(net158), .Vsel_b_0_row_0(net161), .VD_P_0_row_0(net188[0]), .VD_P_1_row_0(net189[0]), .Voutrow_0(net207));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net179), .decode_n0_VINJ_b_0_(net172), .decode_n0_VINJV(net182), .decode_n0_GNDV(net183), .decode_n0_n0_IN_1_(net181), .decode_n0_n0_IN_0_(net180));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_GND_T(net183), .switch_n0_VINJ_T(net172), .switch_n0_CTRL_B_0_(net156), .switch_n0_CTRL_B_1_(net157), .switch_n0_Vg_0_(net154), .switch_n0_Vg_1_(net155), .switch_n0_VINJ(net171), .switch_n0_PROG(net159), .switch_n0_RUN(net153));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_GND(net178), .decode_n0_IN_1_(net176), .decode_n0_IN_0_(net175), .decode_n2_IN_1_(net174), .decode_n2_IN_0_(net173), .decode_n0_ENABLE(net177));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(3), .type(drain_select), .switch_n0_prog_drainrail(net151), .switch_n0_run_drainrail(net152), .switch_n0_VINJ(net195), .switch_n0_GND(net178));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(3), .type(prog_switch), .switch_n0_PR_0_(net184[0]), .switch_n0_PR_1_(net185[0]), .switch_n0_PR_2_(net186[0]), .switch_n0_PR_3_(net187[0]), .switch_n1_PR_0_(net188[0]), .switch_n1_PR_1_(net189[0]), .switch_n1_PR_2_(net190[0]), .switch_n1_PR_3_(net192[0]), .switch_n2_PR_0_(net194[0]), .switch_n1_In_2_(net191[0]), .switch_n1_In_3_(net193[0]), .switch_n0_RUN(net153));


	/* Island 1 */
	AnalogBuffer I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VTUNrow_0(net165), .VDDrow_0(net169), .GNDrow_0(net170), .VINJrow_0(net168), .VINJ_brow_0(net195), .Vgrow_0(net166), .Vd_Prow_0(net194[0]), .Vselrow_0(net167), .Vinrow_0(net209), .Voutrow_0(net198));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VINJrow_0(net163), .GNDrow_0(net162), .VTUNrow_0(net160), .VD_Prow_0(net190[0]), .VD_Rrow_0(net191[0]), .Vselrow_0(net161), .PROGrow_0(net158), .VIN_PLUSrow_0(net206[1]), .VIN_MINUSrow_0(net205), .Voutrow_0(net204));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VDD_brow_0(net169), .VINJ_brow_0(net168), .GND_brow_0(net170), .VTUN_brow_0(net165), .Vg_brow_0(net166), .VD_Prow_0(net192[0]), .VD_Rrow_0(net193[0]), .Vsel_brow_0(net167), .VIN_PLUSrow_0(net207), .VIN_MINUSrow_0(net206[1]), .Voutrow_0(net208));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net197), .Crow_0(net209), .Arow_0(net196));
	TGate_DT I__1 (.island_num(3), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net199), .Crow_0(net200[1]), .Arow_0(net198));
	TGate_DT I__2 (.island_num(3), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net201), .Crow_0(net206[1]), .Arow_0(net200[1]));
	TGate_DT I__3 (.island_num(3), .row(3), .col(0), .matrix_row(1), .matrix_col(1), .Crow_0(net206[1]));
	TGate_DT I__4 (.island_num(3), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net204), .Crow_0(net202[1]), .Brow_0(net203));
	TGate_DT I__5 (.island_num(3), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .SELArow_0(net210), .Crow_0(net209), .Arow_0(net208));

 	/*Programming Mux */ 


	/* Island 4 */
	Capacitor_80ff I__0 (.island_num(4), .row(0), .col(0), .matrix_row(2), .matrix_col(1), .Topcol_0(net200[0:2]), .Botcol_0(net206[0:2]));
	Capacitor_80ff I__1 (.island_num(4), .row(2), .col(0), .matrix_row(2), .matrix_col(1), .Topcol_0(net206[0:2]), .Botcol_0(net202[0:2]));
	Capacitor_80ff I__2 (.island_num(4), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .Toprow_0(net206[1]), .Botrow_0(net208));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_PROG(net159), .N_n_RUN(net153), .N_n_VTUN(net164), .N_n_gnd(net183), .S_s_gnd(net178), .N_n_vinj(net182), .S_s_vinj(net195), .W_w_DrainB_0_(net173), .W_w_DrainB_1_(net174), .W_w_DrainB_2_(net175), .W_w_DrainB_3_(net176), .W_w_DrainEnable(net177), .W_w_GateB_0_(net180), .W_w_GateB_1_(net181), .N_n_GateEnable(net179), .S_s_Drainline_Prog(net151), .S_s_Drainline_Run(net152), .W_w_VIN(net196), .E_e_CLK_Sample(net197), .E_e_CLK_Amp(net199), .S_s_CLK_RST(net201), .E_e_CLK_Load(net210), .S_s_VOUT(net208));
 endmodule