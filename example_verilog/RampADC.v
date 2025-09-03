module TOP(port1);


	/* Island 0 */
	TSMC350nm_Amplifier9T_FGBias I__0 (.island_num(0), .row(0), .col(0));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(1), .col(0));

 	/*Programming Mux */ 


	/* Island 1 */
	Capacitor_80ff I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(1));
	TGate_DT I__1 (.island_num(1), .row(4), .col(0));

 	/*Programming Mux */ 


	/* Island 2 */
	RippleCounter I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(5));

 	/*Programming Mux */ 

 endmodule