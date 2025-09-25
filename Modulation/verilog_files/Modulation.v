module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(75), .matrix_col(160));
	TSMC350nm_4TGate_ST_BMatrix I__1 (.island_num(0), .row(0), .col(161), .matrix_row(75), .matrix_col(1), .A_0_col_0(net11365[0:75]), .A_1_col_0(net11366[0:75]), .A_2_col_0(net11367[0:75]), .A_3_col_0(net11368[0:75]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(9));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(160));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(9));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(75), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(75), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_Modulation I__0 (.island_num(1), .row(75), .col(163), .matrix_row(75), .matrix_col(1), .I1_Pcol_0(net11365[0:75]), .I1_Ncol_0(net11366[0:75]), .I3_Pcol_0(net11367[0:75]), .I3_Ncol_0(net11368[0:75]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3));
 endmodule