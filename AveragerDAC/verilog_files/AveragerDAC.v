module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(3), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(3));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(2), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(2), .type(prog_switch));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(1));

 	/*Programming Mux */ 

 endmodule