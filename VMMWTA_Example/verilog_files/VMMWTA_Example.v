module TOP(port1);


	/* Island 0 */
<<<<<<< HEAD
	TSMC350nm_VMMWTA I__0 (.island_num(0), .row(0), .col(119), .matrix_row(180), .matrix_col(1), .matrix_row(180), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(0), .matrix_row(180), .matrix_col(119));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(8));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(120));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(10));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(180), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(180), .type(prog_switch));
=======
	TSMC350nm_VMMWTA I__0 (.island_num(0), .row(0), .col(3), .matrix_row(6), .matrix_col(1), .matrix_row(6), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(0), .matrix_row(6), .matrix_col(3));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(3));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(4));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(6), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(6), .type(prog_switch));
>>>>>>> 918d362 (Adding current VMMWTA and LLM algorithm progress)

 endmodule