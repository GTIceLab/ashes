module TOP(port1);


	/* Island 0 */
	dotproduct_L I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 1 */
	dotproduct_mid I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(5));

 	/*Programming Mux */ 


	/* Island 2 */
	dotproduct_R I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 3 */
	K_layer_output I__0 (.island_num(3), .row(0), .col(0), .matrix_row(4), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 4 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(4), .row(0), .col(0), .matrix_row(4), .matrix_col(3));

 	/*Programming Mux */ 

 endmodule