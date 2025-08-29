module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(3));
	dotproduct_L I__1 (.island_num(0), .row(0), .col(3), .matrix_row(4), .matrix_col(1));
	dotproduct_mid I__2 (.island_num(0), .row(0), .col(4), .matrix_row(4), .matrix_col(5));
	dotproduct_R I__3 (.island_num(0), .row(0), .col(9), .matrix_row(4), .matrix_col(1));
	K_layer_output I__4 (.island_num(0), .row(0), .col(10), .matrix_row(4), .matrix_col(1));
	TSMC350nm_4x2_Indirect I__5 (.island_num(0), .row(0), .col(11), .matrix_row(4), .matrix_col(3));

 	/*Programming Mux */ 

 endmodule