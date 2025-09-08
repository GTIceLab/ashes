module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(60), .matrix_col(40));
	TSMC350nm_4TGate_ST_BMatrix I__1 (.island_num(0), .row(0), .col(41), .matrix_row(60), .matrix_col(1), .A_0_col_0(net2320[0:60]), .A_1_col_0(net2321[0:60]), .A_2_col_0(net2322[0:60]), .A_3_col_0(net2323[0:60]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(7));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(40));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(8));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(60), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(60), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_NeuralNetworkProgActFunc I__0 (.island_num(1), .row(60), .col(43), .matrix_row(60), .matrix_col(1), .I1_Pcol_0(net2320[0:60]), .I1_Ncol_0(net2321[0:60]), .I3_Pcol_0(net2322[0:60]), .I3_Ncol_0(net2323[0:60]), .VCrow_0(net4566[0:1]));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_Termination_bot I__0 (.island_num(2), .row(0), .col(44), .GATE(net4566[0]));

 	/*Programming Mux */ 

 endmodule