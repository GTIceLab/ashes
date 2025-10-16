module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(5));
	FNN_DiodeConn I__1 (.island_num(0), .row(0), .col(5), .matrix_row(5), .matrix_col(1));
	FNN_Relu_and_Sig I__2 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(5));
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(3));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

 endmodule