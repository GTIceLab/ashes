module TOP(port1);


	/* Island 0 */
	TSMC350nm_4WTA_IndirectProg I__0 (.island_num(0), .row(0), .col(5), .matrix_row(6), .matrix_col(1), .matrix_row(6), .matrix_col(1), .Vbiasrow_0(net298[0:6]));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(0), .matrix_row(6), .matrix_col(5));

 	/*Programming Mux */ 

 endmodule