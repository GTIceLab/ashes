module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(4), .Vd_P_0_col_3(net110[0:4]), .Vd_P_1_col_3(net111[0:4]), .Vd_P_2_col_3(net112[0:4]), .Vd_P_3_col_3(net113[0:4]), .Vd_R_0_col_3(net80[0:4]), .Vd_R_1_col_3(net80[0:4]), .Vd_R_2_col_3(net80[0:4]), .Vd_R_3_col_3(net118[0:4]), .Vs_0_row_0(net125), .Vs_1_row_0(net125), .VINJ_0_row_0(net122), .VINJ_1_row_0(net122), .Vsel_0_row_0(net95[0:4]), .Vsel_1_row_0(net97[0:4]), .Vg_0_row_0(net94[0:4]), .Vg_1_row_0(net96[0:4]), .GND_0_row_0(net1[0:4]), .GND_1_row_0(net1[0:4]), .VTUNrow_0(net124));

 	/*Programming Mux */ 


	/* Island 1 */
	TSMC350nm_TA2Cell_NoFG I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VD_P_0_col_0(net110[0:4]), .VD_P_1_col_0(net111[0:4]), .VIN1_PLUScol_0(net80[0:4]), .VIN1_MINUScol_0(net82[0:4]), .VIN2_PLUScol_0(net84[0:4]), .VIN2_MINUScol_0(net86[0:4]), .OUTPUT_0_col_0(net144[0:4]), .OUTPUT_1_col_0(net145[0:4]), .VTUNrow_0(net124), .Vgrow_0(net126[0]), .Vselrow_0(net127[0]), .VINJrow_0(net122), .GNDrow_0(net1[1]), .VPWRrow_0(net125));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Vg_0_(net94[0]), .N_n_Vg_1_(net96[0]), .N_n_Vg_2_(net94[1]), .N_n_Vg_3_(net96[1]), .N_n_Vg_4_(net94[2]), .N_n_Vg_5_(net96[2]), .N_n_Vg_6_(net94[3]), .N_n_Vg_7_(net96[3]), .N_n_Vg_8_(net126[0]), .N_n_Vsel_0_(net95[0]), .N_n_Vsel_1_(net97[0]), .N_n_Vsel_2_(net95[1]), .N_n_Vsel_3_(net97[1]), .N_n_Vsel_4_(net95[2]), .N_n_Vsel_5_(net97[2]), .N_n_Vsel_6_(net95[3]), .N_n_Vsel_7_(net97[3]), .N_n_Vsel_8_(net127[0]), .W_w_Vd_P_0_(net110[0]), .W_w_Vd_P_1_(net111[0]), .W_w_Vd_P_2_(net112[0]), .W_w_Vd_P_3_(net113[0]), .W_w_Vd_P_4_(net110[1]), .W_w_Vd_P_5_(net111[1]), .W_w_Vd_P_6_(net112[1]), .W_w_Vd_P_7_(net113[1]), .W_w_Vd_P_8_(net110[2]), .W_w_Vd_P_9_(net111[2]), .W_w_Vd_P_10_(net112[2]), .W_w_Vd_P_11_(net113[2]), .W_w_Vd_P_12_(net110[3]), .W_w_Vd_P_13_(net111[3]), .W_w_Vd_P_14_(net112[3]), .W_w_Vd_P_15_(net113[3]), .E_e_Output_0_(net144[0]), .E_e_Output_1_(net145[0]), .E_e_Output_2_(net144[1]), .E_e_Output_3_(net145[1]), .E_e_Output_4_(net144[2]), .E_e_Output_5_(net145[2]), .E_e_Output_6_(net144[3]), .E_e_Output_7_(net145[3]));
 endmodule