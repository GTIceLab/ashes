module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .Progrow_0(net191), .VD_P_0_row_0(net200[0]), .VD_P_1_row_0(net201[0]));
	EPOT I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net202[0]), .VD_P_1_row_0(net203[0]));
	EPOT I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net204[0]), .VD_P_1_row_0(net205[0]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net197), .decode_n0_n0_IN_1_(net199), .decode_n0_n0_IN_0_(net198));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_PROG(net191), .switch_n0_RUN(net190));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_IN_1_(net195), .decode_n0_IN_0_(net194), .decode_n2_IN_1_(net193), .decode_n2_IN_0_(net192), .decode_n0_ENABLE(net196));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(3), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(3), .type(prog_switch), .switch_n0_PR_0_(net200[0]), .switch_n0_PR_1_(net201[0]), .switch_n0_PR_2_(net202[0]), .switch_n0_PR_3_(net203[0]), .switch_n1_PR_0_(net204[0]), .switch_n1_PR_1_(net205[0]), .switch_n1_PR_2_(net206[0]), .switch_n1_PR_3_(net208[0]), .switch_n2_PR_0_(net210[0]), .switch_n1_In_2_(net207[0]), .switch_n1_In_3_(net209[0]), .switch_n0_RUN(net190));


	/* Island 1 */
	AnalogBuffer I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .Vd_Prow_0(net210[0]), .Vinrow_0(net111[0]), .Voutrow_0(net114[1]));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VD_Prow_0(net206[0]), .VD_Rrow_0(net207[0]), .PROGrow_0(net191));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(2), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_Prow_0(net208[0]), .VD_Rrow_0(net209[0]));

 	/*Programming Mux */ 


	/* Island 3 */
	TGate_DT I__0 (.island_num(3), .row(0), .col(0), .matrix_row(6), .matrix_col(1), .SELAcol_0(net108[0:6]), .Ccol_0(net111[0:6]), .Acol_0(net114[0:6]));

 	/*Programming Mux */ 


	/* Island 4 */
	Capacitor_80ff I__0 (.island_num(4), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net123[0:5]), .Botcol_0(net124[0:5]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_PROG(net191), .N_n_RUN(net190), .W_w_DrainB_0_(net192), .W_w_DrainB_1_(net193), .W_w_DrainB_2_(net194), .W_w_DrainB_3_(net195), .W_w_DrainEnable(net196), .W_w_GateB_0_(net198), .W_w_GateB_1_(net199), .W_w_GateEnable(net197), .W_w_VIN(net114[0]), .E_e_CLK_Sample(net108[0]), .E_e_CLK_Amp(net108[1]), .E_e_CLK_RST(net108[2]));
 endmodule