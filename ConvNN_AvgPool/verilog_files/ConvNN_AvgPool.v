module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(3), .matrix_row(1), .matrix_col(3));
	Tgate_swc_fr_Kernel_Horiz_bot_only I__1 (.island_num(0), .row(0), .col(3), .matrix_row(1), .matrix_col(1));
	I_Subtractor_AvgPool_top I__2 (.island_num(0), .row(0), .col(4), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_start I__3 (.island_num(0), .row(0), .col(5), .matrix_row(1), .matrix_col(1));
	Integration_fr_AvgPool_core I__4 (.island_num(0), .row(0), .col(6), .matrix_row(1), .matrix_col(1));
	AvgPool_n_Relu I__5 (.island_num(0), .row(0), .col(7), .matrix_row(1), .matrix_col(1));

 	/*Programming Mux */ 

 endmodule