module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(64), .matrix_col(140));
	TSMC350nm_4WTA_IndirectProg_noncab I__1 (.island_num(0), .row(0), .col(141), .matrix_row(64), .matrix_col(1), .Vout_0_col_0(net10747[0:64]), .Vout_1_col_0(net10748[0:64]), .Vout_2_col_0(net10749[0:64]), .Vout_3_col_0(net10750[0:64]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(9), .decode_n0_ENABLE(net11007), .decode_n0_VINJV(net11022), .decode_n0_GNDV(net11037), .decode_n0_n0_IN_0_(net11016), .decode_n2_n0_IN_1_(net11015), .decode_n2_n0_IN_0_(net11014), .decode_n4_n0_IN_1_(net11013), .decode_n4_n0_IN_0_(net11012), .decode_n6_n0_IN_1_(net11011), .decode_n6_n0_IN_0_(net11010), .decode_n8_n0_IN_1_(net11009), .decode_n8_n0_IN_0_(net11008));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(140), .switch_n0_PROG(net11005), .switch_n0_RUN(net11019), .switch_n0_Vgsel(net11004), .switch_n0_vtun_l(net11006));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(8), .decode_n0_VINJ(net11022), .decode_n0_GND(net11037), .decode_n0_IN_1_(net11030), .decode_n0_IN_0_(net11029), .decode_n2_IN_1_(net11028), .decode_n2_IN_0_(net11027), .decode_n4_IN_1_(net11026), .decode_n4_IN_0_(net11025), .decode_n6_IN_1_(net11024), .decode_n6_IN_0_(net11023), .decode_n0_ENABLE(net11031));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(64), .type(drain_select), .switch_n0_prog_drainrail(net11020), .switch_n0_run_drainrail(net11021), .switch_n0_VINJ(net11022), .switch_n0_GND(net11037));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(64), .type(prog_switch), .switch_n0_VDD(net11017), .switch_n0_GND(net11018), .switch_n0_RUN(net11019));


	/* Island 1 */
	TSMC350nm_VerticalScanner_STD I__0 (.island_num(1), .row(0), .col(0), .In_0_(net10747[0]), .In_1_(net10748[0]), .In_2_(net10749[0]), .In_3_(net10750[0]), .Out(net11032), .Din(net11033), .VDD(net11036[0]), .GND(net11037), .CLK(net11034), .RSTBar(net11035));
	TSMC350nm_VerticalScanner_STD I__1 (.island_num(1), .row(1), .col(0), .In_0_(net10747[1]), .In_1_(net10748[1]), .In_2_(net10749[1]), .In_3_(net10750[1]));
	TSMC350nm_VerticalScanner_STD I__2 (.island_num(1), .row(2), .col(0), .In_0_(net10747[2]), .In_1_(net10748[2]), .In_2_(net10749[2]), .In_3_(net10750[2]));
	TSMC350nm_VerticalScanner_STD I__3 (.island_num(1), .row(3), .col(0), .In_0_(net10747[3]), .In_1_(net10748[3]), .In_2_(net10749[3]), .In_3_(net10750[3]));
	TSMC350nm_VerticalScanner_STD I__4 (.island_num(1), .row(4), .col(0), .In_0_(net10747[4]), .In_1_(net10748[4]), .In_2_(net10749[4]), .In_3_(net10750[4]));
	TSMC350nm_VerticalScanner_STD I__5 (.island_num(1), .row(5), .col(0), .In_0_(net10747[5]), .In_1_(net10748[5]), .In_2_(net10749[5]), .In_3_(net10750[5]));
	TSMC350nm_VerticalScanner_STD I__6 (.island_num(1), .row(6), .col(0), .In_0_(net10747[6]), .In_1_(net10748[6]), .In_2_(net10749[6]), .In_3_(net10750[6]));
	TSMC350nm_VerticalScanner_STD I__7 (.island_num(1), .row(7), .col(0), .In_0_(net10747[7]), .In_1_(net10748[7]), .In_2_(net10749[7]), .In_3_(net10750[7]));
	TSMC350nm_VerticalScanner_STD I__8 (.island_num(1), .row(8), .col(0), .In_0_(net10747[8]), .In_1_(net10748[8]), .In_2_(net10749[8]), .In_3_(net10750[8]));
	TSMC350nm_VerticalScanner_STD I__9 (.island_num(1), .row(9), .col(0), .In_0_(net10747[9]), .In_1_(net10748[9]), .In_2_(net10749[9]), .In_3_(net10750[9]));
	TSMC350nm_VerticalScanner_STD I__10 (.island_num(1), .row(10), .col(0), .In_0_(net10747[10]), .In_1_(net10748[10]), .In_2_(net10749[10]), .In_3_(net10750[10]));
	TSMC350nm_VerticalScanner_STD I__11 (.island_num(1), .row(11), .col(0), .In_0_(net10747[11]), .In_1_(net10748[11]), .In_2_(net10749[11]), .In_3_(net10750[11]));
	TSMC350nm_VerticalScanner_STD I__12 (.island_num(1), .row(12), .col(0), .In_0_(net10747[12]), .In_1_(net10748[12]), .In_2_(net10749[12]), .In_3_(net10750[12]));
	TSMC350nm_VerticalScanner_STD I__13 (.island_num(1), .row(13), .col(0), .In_0_(net10747[13]), .In_1_(net10748[13]), .In_2_(net10749[13]), .In_3_(net10750[13]));
	TSMC350nm_VerticalScanner_STD I__14 (.island_num(1), .row(14), .col(0), .In_0_(net10747[14]), .In_1_(net10748[14]), .In_2_(net10749[14]), .In_3_(net10750[14]));
	TSMC350nm_VerticalScanner_STD I__15 (.island_num(1), .row(15), .col(0), .In_0_(net10747[15]), .In_1_(net10748[15]), .In_2_(net10749[15]), .In_3_(net10750[15]));
	TSMC350nm_VerticalScanner_STD I__16 (.island_num(1), .row(16), .col(0), .In_0_(net10747[16]), .In_1_(net10748[16]), .In_2_(net10749[16]), .In_3_(net10750[16]));
	TSMC350nm_VerticalScanner_STD I__17 (.island_num(1), .row(17), .col(0), .In_0_(net10747[17]), .In_1_(net10748[17]), .In_2_(net10749[17]), .In_3_(net10750[17]));
	TSMC350nm_VerticalScanner_STD I__18 (.island_num(1), .row(18), .col(0), .In_0_(net10747[18]), .In_1_(net10748[18]), .In_2_(net10749[18]), .In_3_(net10750[18]));
	TSMC350nm_VerticalScanner_STD I__19 (.island_num(1), .row(19), .col(0), .In_0_(net10747[19]), .In_1_(net10748[19]), .In_2_(net10749[19]), .In_3_(net10750[19]));
	TSMC350nm_VerticalScanner_STD I__20 (.island_num(1), .row(20), .col(0), .In_0_(net10747[20]), .In_1_(net10748[20]), .In_2_(net10749[20]), .In_3_(net10750[20]));
	TSMC350nm_VerticalScanner_STD I__21 (.island_num(1), .row(21), .col(0), .In_0_(net10747[21]), .In_1_(net10748[21]), .In_2_(net10749[21]), .In_3_(net10750[21]));
	TSMC350nm_VerticalScanner_STD I__22 (.island_num(1), .row(22), .col(0), .In_0_(net10747[22]), .In_1_(net10748[22]), .In_2_(net10749[22]), .In_3_(net10750[22]));
	TSMC350nm_VerticalScanner_STD I__23 (.island_num(1), .row(23), .col(0), .In_0_(net10747[23]), .In_1_(net10748[23]), .In_2_(net10749[23]), .In_3_(net10750[23]));
	TSMC350nm_VerticalScanner_STD I__24 (.island_num(1), .row(24), .col(0), .In_0_(net10747[24]), .In_1_(net10748[24]), .In_2_(net10749[24]), .In_3_(net10750[24]));
	TSMC350nm_VerticalScanner_STD I__25 (.island_num(1), .row(25), .col(0), .In_0_(net10747[25]), .In_1_(net10748[25]), .In_2_(net10749[25]), .In_3_(net10750[25]));
	TSMC350nm_VerticalScanner_STD I__26 (.island_num(1), .row(26), .col(0), .In_0_(net10747[26]), .In_1_(net10748[26]), .In_2_(net10749[26]), .In_3_(net10750[26]));
	TSMC350nm_VerticalScanner_STD I__27 (.island_num(1), .row(27), .col(0), .In_0_(net10747[27]), .In_1_(net10748[27]), .In_2_(net10749[27]), .In_3_(net10750[27]));
	TSMC350nm_VerticalScanner_STD I__28 (.island_num(1), .row(28), .col(0), .In_0_(net10747[28]), .In_1_(net10748[28]), .In_2_(net10749[28]), .In_3_(net10750[28]));
	TSMC350nm_VerticalScanner_STD I__29 (.island_num(1), .row(29), .col(0), .In_0_(net10747[29]), .In_1_(net10748[29]), .In_2_(net10749[29]), .In_3_(net10750[29]));
	TSMC350nm_VerticalScanner_STD I__30 (.island_num(1), .row(30), .col(0), .In_0_(net10747[30]), .In_1_(net10748[30]), .In_2_(net10749[30]), .In_3_(net10750[30]));
	TSMC350nm_VerticalScanner_STD I__31 (.island_num(1), .row(31), .col(0), .In_0_(net10747[31]), .In_1_(net10748[31]), .In_2_(net10749[31]), .In_3_(net10750[31]));
	TSMC350nm_VerticalScanner_STD I__32 (.island_num(1), .row(32), .col(0), .In_0_(net10747[32]), .In_1_(net10748[32]), .In_2_(net10749[32]), .In_3_(net10750[32]));
	TSMC350nm_VerticalScanner_STD I__33 (.island_num(1), .row(33), .col(0), .In_0_(net10747[33]), .In_1_(net10748[33]), .In_2_(net10749[33]), .In_3_(net10750[33]));
	TSMC350nm_VerticalScanner_STD I__34 (.island_num(1), .row(34), .col(0), .In_0_(net10747[34]), .In_1_(net10748[34]), .In_2_(net10749[34]), .In_3_(net10750[34]));
	TSMC350nm_VerticalScanner_STD I__35 (.island_num(1), .row(35), .col(0), .In_0_(net10747[35]), .In_1_(net10748[35]), .In_2_(net10749[35]), .In_3_(net10750[35]));
	TSMC350nm_VerticalScanner_STD I__36 (.island_num(1), .row(36), .col(0), .In_0_(net10747[36]), .In_1_(net10748[36]), .In_2_(net10749[36]), .In_3_(net10750[36]));
	TSMC350nm_VerticalScanner_STD I__37 (.island_num(1), .row(37), .col(0), .In_0_(net10747[37]), .In_1_(net10748[37]), .In_2_(net10749[37]), .In_3_(net10750[37]));
	TSMC350nm_VerticalScanner_STD I__38 (.island_num(1), .row(38), .col(0), .In_0_(net10747[38]), .In_1_(net10748[38]), .In_2_(net10749[38]), .In_3_(net10750[38]));
	TSMC350nm_VerticalScanner_STD I__39 (.island_num(1), .row(39), .col(0), .In_0_(net10747[39]), .In_1_(net10748[39]), .In_2_(net10749[39]), .In_3_(net10750[39]));
	TSMC350nm_VerticalScanner_STD I__40 (.island_num(1), .row(40), .col(0), .In_0_(net10747[40]), .In_1_(net10748[40]), .In_2_(net10749[40]), .In_3_(net10750[40]));
	TSMC350nm_VerticalScanner_STD I__41 (.island_num(1), .row(41), .col(0), .In_0_(net10747[41]), .In_1_(net10748[41]), .In_2_(net10749[41]), .In_3_(net10750[41]));
	TSMC350nm_VerticalScanner_STD I__42 (.island_num(1), .row(42), .col(0), .In_0_(net10747[42]), .In_1_(net10748[42]), .In_2_(net10749[42]), .In_3_(net10750[42]));
	TSMC350nm_VerticalScanner_STD I__43 (.island_num(1), .row(43), .col(0), .In_0_(net10747[43]), .In_1_(net10748[43]), .In_2_(net10749[43]), .In_3_(net10750[43]));
	TSMC350nm_VerticalScanner_STD I__44 (.island_num(1), .row(44), .col(0), .In_0_(net10747[44]), .In_1_(net10748[44]), .In_2_(net10749[44]), .In_3_(net10750[44]));
	TSMC350nm_VerticalScanner_STD I__45 (.island_num(1), .row(45), .col(0), .In_0_(net10747[45]), .In_1_(net10748[45]), .In_2_(net10749[45]), .In_3_(net10750[45]));
	TSMC350nm_VerticalScanner_STD I__46 (.island_num(1), .row(46), .col(0), .In_0_(net10747[46]), .In_1_(net10748[46]), .In_2_(net10749[46]), .In_3_(net10750[46]));
	TSMC350nm_VerticalScanner_STD I__47 (.island_num(1), .row(47), .col(0), .In_0_(net10747[47]), .In_1_(net10748[47]), .In_2_(net10749[47]), .In_3_(net10750[47]));
	TSMC350nm_VerticalScanner_STD I__48 (.island_num(1), .row(48), .col(0), .In_0_(net10747[48]), .In_1_(net10748[48]), .In_2_(net10749[48]), .In_3_(net10750[48]));
	TSMC350nm_VerticalScanner_STD I__49 (.island_num(1), .row(49), .col(0), .In_0_(net10747[49]), .In_1_(net10748[49]), .In_2_(net10749[49]), .In_3_(net10750[49]));
	TSMC350nm_VerticalScanner_STD I__50 (.island_num(1), .row(50), .col(0), .In_0_(net10747[50]), .In_1_(net10748[50]), .In_2_(net10749[50]), .In_3_(net10750[50]));
	TSMC350nm_VerticalScanner_STD I__51 (.island_num(1), .row(51), .col(0), .In_0_(net10747[51]), .In_1_(net10748[51]), .In_2_(net10749[51]), .In_3_(net10750[51]));
	TSMC350nm_VerticalScanner_STD I__52 (.island_num(1), .row(52), .col(0), .In_0_(net10747[52]), .In_1_(net10748[52]), .In_2_(net10749[52]), .In_3_(net10750[52]));
	TSMC350nm_VerticalScanner_STD I__53 (.island_num(1), .row(53), .col(0), .In_0_(net10747[53]), .In_1_(net10748[53]), .In_2_(net10749[53]), .In_3_(net10750[53]));
	TSMC350nm_VerticalScanner_STD I__54 (.island_num(1), .row(54), .col(0), .In_0_(net10747[54]), .In_1_(net10748[54]), .In_2_(net10749[54]), .In_3_(net10750[54]));
	TSMC350nm_VerticalScanner_STD I__55 (.island_num(1), .row(55), .col(0), .In_0_(net10747[55]), .In_1_(net10748[55]), .In_2_(net10749[55]), .In_3_(net10750[55]));
	TSMC350nm_VerticalScanner_STD I__56 (.island_num(1), .row(56), .col(0), .In_0_(net10747[56]), .In_1_(net10748[56]), .In_2_(net10749[56]), .In_3_(net10750[56]));
	TSMC350nm_VerticalScanner_STD I__57 (.island_num(1), .row(57), .col(0), .In_0_(net10747[57]), .In_1_(net10748[57]), .In_2_(net10749[57]), .In_3_(net10750[57]));
	TSMC350nm_VerticalScanner_STD I__58 (.island_num(1), .row(58), .col(0), .In_0_(net10747[58]), .In_1_(net10748[58]), .In_2_(net10749[58]), .In_3_(net10750[58]));
	TSMC350nm_VerticalScanner_STD I__59 (.island_num(1), .row(59), .col(0), .In_0_(net10747[59]), .In_1_(net10748[59]), .In_2_(net10749[59]), .In_3_(net10750[59]));
	TSMC350nm_VerticalScanner_STD I__60 (.island_num(1), .row(60), .col(0), .In_0_(net10747[60]), .In_1_(net10748[60]), .In_2_(net10749[60]), .In_3_(net10750[60]));
	TSMC350nm_VerticalScanner_STD I__61 (.island_num(1), .row(61), .col(0), .In_0_(net10747[61]), .In_1_(net10748[61]), .In_2_(net10749[61]), .In_3_(net10750[61]));
	TSMC350nm_VerticalScanner_STD I__62 (.island_num(1), .row(62), .col(0), .In_0_(net10747[62]), .In_1_(net10748[62]), .In_2_(net10749[62]), .In_3_(net10750[62]));
	TSMC350nm_VerticalScanner_STD I__63 (.island_num(1), .row(63), .col(0), .In_0_(net10747[63]), .In_1_(net10748[63]), .In_2_(net10749[63]), .In_3_(net10750[63]));

 	/*Programming Mux */ 


	/* Island 2 */
	Routes_GateDecodeSwc I__0 (.island_num(2), .row(66), .col(0), .matrix_row(1), .matrix_col(70), .AVDDcol_0(net11036[0]));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net11005), .N_n_Run(net11019), .N_n_VGPROG(net11004), .N_n_VTUN(net11006), .N_n_AVDD(net11036[0]), .N_n_gnd(net11037), .S_s_gnd(net11018), .N_n_vinj(net11022), .S_s_vinj(net11017), .N_n_GateB_0_(net11008), .N_n_GateB_1_(net11009), .N_n_GateB_2_(net11010), .N_n_GateB_3_(net11011), .N_n_GateB_4_(net11012), .N_n_GateB_5_(net11013), .N_n_GateB_6_(net11014), .N_n_GateB_7_(net11015), .N_n_GateB_8_(net11016), .W_w_DrainB_0_(net11023), .W_w_DrainB_1_(net11024), .W_w_DrainB_2_(net11025), .W_w_DrainB_3_(net11026), .W_w_DrainB_4_(net11027), .W_w_DrainB_5_(net11028), .W_w_DrainB_6_(net11029), .W_w_DrainB_7_(net11030), .W_w_Drainline_Prog(net11020), .W_w_Drainline_Run(net11021), .N_n_GateEnable_WTA(net11007), .W_w_DrainEnable_WTA(net11031), .E_e_WTA_out(net11032), .E_e_Din(net11033), .E_e_CLK(net11034), .E_e_RSTBar(net11035));
 endmodule