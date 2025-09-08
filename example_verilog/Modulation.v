module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(60), .matrix_col(48));
	TSMC350nm_4TGate_ST_BMatrix I__1 (.island_num(0), .row(0), .col(49), .matrix_row(60), .matrix_col(1), .A_0_col_0(net2496[0:60]), .A_1_col_0(net2497[0:60]), .A_2_col_0(net2498[0:60]), .A_3_col_0(net2499[0:60]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(7));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(48));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(8));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(60), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(60), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_Modulation I__0 (.island_num(1), .row(60), .col(51), .matrix_row(60), .matrix_col(1), .I1_Pcol_0(net2496[0:60]), .I1_Ncol_0(net2497[0:60]), .I3_Pcol_0(net2498[0:60]), .I3_Ncol_0(net2499[0:60]));

 	/*Programming Mux */ 

 endmodule