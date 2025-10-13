module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(2), .matrix_col(1), .VDDrow_0(net91[0:1]), .GND_brow_1(net89[0:1]), .VTUNrow_0(net90[0:1]), .VTUN_brow_1(net92[0:1]));

 	/*Programming Mux */ 


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .GND_brow_4(net89[0:1]));

 	/*Programming Mux */ 


	/* Island 2 */
	EPOT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net91[0:1]), .GNDrow_0(net88[0:1]), .VTUN_brow_4(net92[0:1]));

 	/*Programming Mux */ 


	/* Island 3 */
	AnalogBuffer I__0 (.island_num(3), .row(0), .col(0), .Vout(net93));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_VTUN(net90[0]), .N_n_AVDD(net91[0]), .N_n_gnd(net88[0]), .S_s_gnd(net89[0]), .E_e_Vout(net93));
 endmodule