module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1));
	TSMC350nm_4TGate_ST_BMatrix I__1 (.island_num(0), .row(0), .col(2), .matrix_row(5), .matrix_col(1), .A_0_col_0(net142[0:5]), .A_1_col_0(net143[0:5]), .A_2_col_0(net144[0:5]), .A_3_col_0(net145[0:5]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(1));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_NeuralNetworkProgActFunc I__0 (.island_num(1), .row(5), .col(4), .matrix_row(5), .matrix_col(1), .I1_Pcol_0(net142[0:5]), .I1_Ncol_0(net143[0:5]), .I3_Pcol_0(net144[0:5]), .I3_Ncol_0(net145[0:5]), .VCrow_0(net293[0:1]));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Termination_bot I__0 (.island_num(2), .row(0), .col(5), .GATE(net293[0]));

 	/*Programming Mux */ 

 endmodule