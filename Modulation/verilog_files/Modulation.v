module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(3), .matrix_col(6));
	TSMC350nm_4TGate_ST_BMatrix I__1 (.island_num(0), .row(0), .col(7), .matrix_row(3), .matrix_col(1), .A_0_col_0(net204[0:3]), .A_1_col_0(net205[0:3]), .A_2_col_0(net206[0:3]), .A_3_col_0(net207[0:3]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(6));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(3), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(3), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_Modulation I__0 (.island_num(1), .row(3), .col(9), .matrix_row(3), .matrix_col(1), .I1_Pcol_0(net204[0:3]), .I1_Ncol_0(net205[0:3]), .I3_Pcol_0(net206[0:3]), .I3_Ncol_0(net207[0:3]));

 	/*Programming Mux */ 

 endmodule