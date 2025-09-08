module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1));
	EPOT I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1));
	EPOT I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1));
	AnalogBuffer I__3 (.island_num(0), .row(7), .col(0), .matrix_row(1), .matrix_col(1));
	TSMC350nm_Amplifier9T_FGBias I__4 (.island_num(0), .row(4), .col(0), .matrix_row(1), .matrix_col(1));
	TSMC350nm_Amplifier9T_FGBias I__5 (.island_num(0), .row(5), .col(0), .matrix_row(1), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(6), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 2 */
	Capacitor_80ff I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1));

 	/*Programming Mux */ 

 endmodule