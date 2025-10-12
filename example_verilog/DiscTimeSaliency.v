module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(25), .matrix_col(50));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(7));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(50));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(7));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(25), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(25), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(0), .matrix_row(150), .matrix_col(50));
	Q_layer_output I__1 (.island_num(1), .row(0), .col(50), .matrix_row(150), .matrix_col(1), .VPWR_0_row_0(net21933[0:1]), .VPWR_1_row_0(net21933[0:1]), .Vdbias_0_row_0(net21778[0:1]), .Vdbias_1_row_0(net21778[0:1]), .Vbias_0_row_0(net21777[0:1]), .Vbias_1_row_0(net21777[0:1]), .Vgbiasrow_0(net21779[0:1]), .Q_out_0_col_0(net21236[0:150]), .Q_out_1_col_0(net21237[0:150]), .Q_out_2_col_0(net21238[0:150]), .Q_out_3_col_0(net21239[0:150]), .GND_0_row_0(net21938[0:1]), .GND_1_row_0(net21938[0:1]));
	dotproduct_L I__7 (.island_num(1), .row(0), .col(101), .matrix_row(150), .matrix_col(1), .phi1_Brow_149(net21784[0:1]), .phi2_Brow_149(net21834[0:1]), .GND_Brow_149(net21884[0:1]));
	dotproduct_mid I__8 (.island_num(1), .row(0), .col(102), .matrix_row(150), .matrix_col(48), .phi1_Brow_149(net21786[0:48]), .phi2_Brow_149(net21836[0:48]), .GND_Brow_149(net21885[0:48]));
	dotproduct_R I__9 (.island_num(1), .row(0), .col(150), .matrix_row(150), .matrix_col(1), .phi1_Brow_149(net21785[0:1]), .phi2_Brow_149(net21835[0:1]), .GND_Brow_149(net21938[0:1]));
	K_layer_output I__10 (.island_num(1), .row(0), .col(151), .matrix_row(150), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(7), .decode_n0_ENABLE(net21775), .decode_n0_VINJV(net21776));
	TSMC350nm_IndirectSwitches switch(.island_num(1), .direction(horizontal), .num(50), .switch_n0_PROG(net21773), .switch_n0_RUN(net21772), .switch_n0_Vgsel(net21774));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(10));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(150), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(1), .direction(vertical), .num(150), .type(prog_switch));


	/* Island 2 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(2), .row(0), .col(0), .matrix_row(150), .matrix_col(50));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(2), .direction(horizontal), .bits(7));
	TSMC350nm_IndirectSwitches switch(.island_num(2), .direction(horizontal), .num(50));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(2), .direction(vertical), .bits(10));
	TSMC350nm_drainSelect01d3 switch(.island_num(2), .direction(vertical), .num(150), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(2), .direction(vertical), .num(150), .type(prog_switch));


	/* Island 3 */
	SampleControl I__0 (.island_num(3), .row(0), .col(0), .phi1(net21784[0]), .phi2(net21834[0]), .GND(net21884[0]), .Sample(net21935), .D(net21936), .CLK(net21934), .Q(net21937));
	SampleControl I__1 (.island_num(3), .row(0), .col(1), .matrix_row(1), .matrix_col(48), .phi1row_0(net21786[0:48]), .phi2row_0(net21836[0:48]), .GNDrow_0(net21885[0:48]));
	SampleControl I__2 (.island_num(3), .row(0), .col(49), .phi1(net21785[0]), .phi2(net21835[0]), .GND(net21938[0]));

 	/*Programming Mux */ 


	/* Island 4 */
	TSMC350nm_HorizontalScanner I__0 (.island_num(4), .row(0), .col(0), .matrix_row(1), .matrix_col(50), .In_0_row_0(net21236[0:50]), .In_1_row_0(net21237[0:50]), .In_2_row_0(net21238[0:50]), .In_3_row_0(net21239[0:50]));

 	/*Programming Mux */ 


	/* Island 5 */
	TSMC350nm_HorizontalScanner I__0 (.island_num(5), .row(0), .col(0), .matrix_row(1), .matrix_col(50));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net21773), .N_n_RUN(net21772), .N_n_VGPROG(net21774), .N_n_avdd(net21933[0]), .S_s_avdd(net21933[0]), .N_n_gnd(net21938[0]), .S_s_gnd(net21938[0]), .N_n_vinj(net21776), .S_s_vinj(net21776), .N_n_Q_enable(net21775), .E_e_vbias(net21777[0]), .E_e_vdbias(net21778[0]), .E_e_vgbias(net21779[0]), .S_s_CLK(net21934), .S_s_Sample(net21935), .S_s_Q(net21937), .S_s_D(net21936));
 endmodule