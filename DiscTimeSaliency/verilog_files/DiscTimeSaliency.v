module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(4));
	Q_layer_output I__1 (.island_num(0), .row(0), .col(4), .matrix_row(4), .matrix_col(1));
	dotproduct_L I__7 (.island_num(0), .row(0), .col(9), .matrix_row(16), .matrix_col(1));
	dotproduct_mid I__8 (.island_num(0), .row(0), .col(10), .matrix_row(16), .matrix_col(2));
	dotproduct_R I__9 (.island_num(0), .row(0), .col(12), .matrix_row(16), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(3));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(4));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch));

 endmodule