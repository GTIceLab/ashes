module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(2));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(1), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(1), .type(prog_switch));


	/* Island 1 */
	Capacitor_80ff I__0 (.island_num(1), .row(0), .col(0));
	Capacitor_80ff I__1 (.island_num(1), .row(1), .col(0));
	Capacitor_80ff I__2 (.island_num(1), .row(0), .col(1));
	Capacitor_80ff I__3 (.island_num(1), .row(1), .col(1));
	Capacitor_80ff I__4 (.island_num(1), .row(0), .col(2));
	Capacitor_80ff I__5 (.island_num(1), .row(1), .col(2));
	TGate_DT I__6 (.island_num(1), .row(1), .col(4));

 	/*Programming Mux */ 


	/* Island 2 */
	RippleCounter I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(8), .Countrow_0(net158[0:8]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .S_s_Code_0_(net158[0]), .S_s_Code_1_(net158[1]), .S_s_Code_2_(net158[2]), .S_s_Code_3_(net158[3]), .S_s_Code_4_(net158[4]), .S_s_Code_5_(net158[5]), .S_s_Code_6_(net158[6]), .S_s_Code_7_(net158[7]));
 endmodule