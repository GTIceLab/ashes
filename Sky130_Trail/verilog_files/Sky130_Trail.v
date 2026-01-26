module TOP(port1);


	/* Island 0 */
	IndirectVMM_4x2 I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(4), .Vd_P_e_0_col_3(net132[0:4]), .Vd_P_e_1_col_3(net133[0:4]), .Vd_P_e_2_col_3(net134[0:4]), .Vd_P_e_3_col_3(net135[0:4]), .Vd_R_e_0_col_3(net153[0:4]), .Vd_R_e_1_col_3(net161[0:4]), .Vd_R_e_2_col_3(net154[0:4]), .Vd_R_e_3_col_3(net162[0:4]), .Vs_n_0_row_0(net142), .Vs_n_1_row_0(net142), .VINJ_n_0_row_0(net140), .VINJ_n_1_row_0(net140), .Vsel_n_0_row_0(net116[0:4]), .Vsel_n_1_row_0(net118[0:4]), .Vg_n_0_row_0(net115[0:4]), .Vg_n_1_row_0(net117[0:4]), .GND_n_0_row_0(net67[0:4]), .GND_n_1_row_0(net67[0:4]), .GND_n_2_row_0(net67[0:4]), .GND_n_3_row_0(net67[0:4]), .VTUN_n_0_row_0(net93[0:4]), .VTUN_n_1_row_0(net93[0:4]));

 	/*Programming Mux */ 


	/* Island 1 */
	TA_FGbias_1x2 I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .Vd_P_w_0_col_0(net132[0:4]), .Vd_P_w_1_col_0(net133[0:4]), .Vin_P_w_0_col_0(net153[0:4]), .Vin_P_w_1_col_0(net154[0:4]), .Vin_M_w_0_col_0(net161[0:4]), .Vin_M_w_1_col_0(net162[0:4]), .OUTPUT_e_0_col_0(net169[0:4]), .OUTPUT_e_1_col_0(net170[0:4]), .Vg_nrow_0(net143[0]), .Vsel_nrow_0(net144[0]), .VINJ_nrow_0(net140), .GND_n_0_row_0(net67[0]), .AVDD_n_0_row_0(net142));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Vg_0_(net115[0]), .N_n_Vg_1_(net117[0]), .N_n_Vg_2_(net115[1]), .N_n_Vg_3_(net117[1]), .N_n_Vg_4_(net115[2]), .N_n_Vg_5_(net117[2]), .N_n_Vg_6_(net115[3]), .N_n_Vg_7_(net117[3]), .N_n_Vg_8_(net143[0]), .N_n_Vsel_0_(net116[0]), .N_n_Vsel_1_(net118[0]), .N_n_Vsel_2_(net116[1]), .N_n_Vsel_3_(net118[1]), .N_n_Vsel_4_(net116[2]), .N_n_Vsel_5_(net118[2]), .N_n_Vsel_6_(net116[3]), .N_n_Vsel_7_(net118[3]), .N_n_Vsel_8_(net144[0]), .W_w_Vd_P_0_(net132[0]), .W_w_Vd_P_1_(net133[0]), .W_w_Vd_P_2_(net134[0]), .W_w_Vd_P_3_(net135[0]), .W_w_Vd_P_4_(net132[1]), .W_w_Vd_P_5_(net133[1]), .W_w_Vd_P_6_(net134[1]), .W_w_Vd_P_7_(net135[1]), .W_w_Vd_P_8_(net132[2]), .W_w_Vd_P_9_(net133[2]), .W_w_Vd_P_10_(net134[2]), .W_w_Vd_P_11_(net135[2]), .W_w_Vd_P_12_(net132[3]), .W_w_Vd_P_13_(net133[3]), .W_w_Vd_P_14_(net134[3]), .W_w_Vd_P_15_(net135[3]), .N_n_Output_0_(net169[0]), .N_n_Output_1_(net170[0]), .N_n_Output_2_(net169[1]), .N_n_Output_3_(net170[1]), .N_n_Output_4_(net169[2]), .N_n_Output_5_(net170[2]), .N_n_Output_6_(net169[3]), .N_n_Output_7_(net170[3]));
 endmodule