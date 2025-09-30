module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0 I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net223), .fast_clk(net224), .cpu_en(net175), .dbg_en(net176), .dbg_uart_rxd(net177), .nmi(net178), .reset_n(net179), .scan_enable(net180), .dbg_uart_txd(net181), .scan_mode(net182), .wkup(net183), .scan_in1(net184), .scan_in2(net185), .dco_clk(net225), .AVDD(net227), .Cal_IO(net207), .VINJ(net228), .ADC_Trim(net219), .Bias_Trim(net220), .Cal_Vin(net208), .Debug_IO(net209), .I_IO(net210), .VD_IO(net211), .VGPROG(net402), .VGPROG_IO(net212), .VGRUN(net401), .VG_IO(net213), .VTUN_AM(net347), .SystemDrainline_0_(net342), .SystemDrainline_1_(net343), .pulse_fr_drain(net214), .GND(net226), .VTUN_fgmem(net221), .DVDD(net229), .mmio_reg_5_vinj_0_(net403), .mmio_reg_5_vinj_1_(net404), .mmio_reg_5_vinj_2_(net406), .mmio_reg_5_vinj_3_(net407), .mmio_reg_5_vinj_4_(net408), .mmio_reg_5_vinj_5_(net409), .mmio_reg_5_vinj_6_(net348), .mmio_reg_5_vinj_7_(net405), .mmio_reg_5_vinj_9_(net381), .mmio_reg_9_bout_0_(net363), .mmio_reg_9_bout_1_(net382), .mmio_reg_9_bout_2_(net383), .mmio_reg_9_bout_3_(net384), .mmio_reg_9_bout_4_(net385), .mmio_reg_9_bout_5_(net331), .mmio_reg_9_bout_6_(net332), .mmio_reg_9_bout_7_(net333), .mmio_reg_9_bout_8_(net334), .mmio_reg_9_bout_9_(net335), .mmio_reg_9_bout_10_(net336), .mmio_reg_9_bout_11_(net337), .mmio_reg_9_bout_13_(net239[0]), .mmio_reg_9_bout_14_(net240[0]), .mmio_reg_9_bout_15_(net241[0]), .mmio_reg_10_bout_0_(net412), .mmio_reg_10_bout_1_(net413), .mmio_reg_10_bout_2_(net414), .mmio_reg_10_bout_3_(net415), .mmio_reg_10_bout_4_(net416), .mmio_reg_10_bout_5_(net365), .mmio_reg_10_bout_6_(net366), .mmio_reg_10_bout_7_(net367), .mmio_reg_10_bout_8_(net368), .mmio_reg_10_bout_9_(net369), .mmio_reg_10_bout_10_(net370), .mmio_reg_10_bout_11_(net371), .mmio_reg_10_bout_12_(net372), .mmio_reg_10_bout_13_(net387), .mmio_reg_10_bout_14_(net349), .mmio_reg_10_bout_15_(net364), .puc_rst_bout(net215), .irq_0_(net173), .irq_1_(net174), .irq_2_(net216), .irq_3_(net217), .irq_4_(net218), .PROG_HV(net410), .RUN_HV(net411), .sram_CS_VBIAS(net206), .peri_use_uP(net205), .peri_spi_slave_clk(net204), .peri_spi_mstr_miso(net200), .peri_spi_slave_mosi(net202), .peri_spi_slave_cs_n(net201), .peri_spi_mstr_spiclk(net222), .peri_spi_slave_miso(net203), .peri_spi_mstr_mosi(net199), .peri_spi_mstr_cs_n_0(net198), .peri_spi_mstr_cs_n_1(net197), .peri_spi_mstr_cs_n_2(net196), .peri_spi_mstr_cs_n_3(net195), .mmio_reg_7_bout_0_(net194), .mmio_reg_7_bout_1_(net193), .Macro_dbg_Scan_Vout(net192), .Macro_dbg_Scan_CLK(net191), .Macro_dbg_Scan_Din(net190), .Macro_dbg_Scan_RST(net189), .dbg_freeze_bout(net188), .dco_enable_bout(net187), .dco_wkup_bout(net186), .lfxt_enable_bout(net167), .lfxt_wkup_bout(net168), .scan_out2_bout(net169), .fgmem_CS_VBIAS(net170), .mmio_reg_in_5_0_(net172), .mmio_reg_in_5_1_(net171));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net226), .avdd_N_2_(net227), .VINJ_N_2_(net228), .DVDD_N_2_(net229), .IO_N_CLK_0_(net222), .IO_N_CLK_1_(net223), .IO_N_CLK_2_(net224), .IO_N_CLK_3_(net225), .IO_N_0_(net167), .IO_N_1_(net168), .IO_N_2_(net169), .IO_N_3_(net169), .IO_N_4_(net170), .IO_N_5_(net171), .IO_N_6_(net172), .IO_N_7_(net173), .IO_N_8_(net174), .IO_N_9_(net175), .IO_N_10_(net176), .IO_N_11_(net177), .IO_N_12_(net178), .IO_N_13_(net179), .IO_N_14_(net180), .IO_N_15_(net181), .IO_N_16_(net182), .IO_N_17_(net183), .IO_N_18_(net184), .IO_N_19_(net185), .gnd_S_0_(net398), .gnd_S_2_(net330[0]), .avdd_S_0_(net397), .avdd_S_2_(net294[0]), .VINJ_S_0_(net399), .VINJ_S_2_(net329[0]), .DVDD_S_2_(net328[0]), .IO_S_0_(net195), .IO_S_1_(net196), .IO_S_2_(net197), .IO_S_3_(net198), .IO_S_4_(net199), .IO_S_5_(net200), .IO_S_6_(net201), .IO_S_7_(net202), .IO_S_8_(net203), .IO_S_9_(net204), .IO_S_10_(net205), .IO_S_11_(net206), .IO_S_12_(net373), .IO_S_13_(net386), .IO_S_14_(net302[0]), .IO_S_15_(net302[1]), .IO_S_16_(net302[2]), .IO_S_17_(net302[3]), .IO_S_26_(net218), .IO_S_27_(net217), .IO_S_44_(net216), .IO_S_45_(net215), .IO_Bare_E_0_(net219), .IO_Bare_E_1_(net220), .IO_E_RES_0_(net347), .IO_E_RES_1_(net221), .IO_E_0_(net207), .IO_E_1_(net208), .IO_E_2_(net209), .IO_E_3_(net210), .IO_E_4_(net211), .IO_E_5_(net212), .IO_E_6_(net402), .IO_E_7_(net213), .IO_E_8_(net214), .IO_W_RES_0_(net400), .IO_W_0_(net186), .IO_W_1_(net187), .IO_W_2_(net188), .IO_W_3_(net189), .IO_W_4_(net190), .IO_W_5_(net191), .IO_W_6_(net192), .IO_W_7_(net193), .IO_W_8_(net194));

 	/*Programming Mux */ 


	/* Island 2 */
<<<<<<< HEAD
	TSMC350nm_VerticalScanner_STD I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .In_0_col_0(net350[0:4]), .In_1_col_0(net230[0:4]), .In_2_col_0(net231[0:4]), .In_3_col_0(net232[0:4]), .Outrow_0(net262[0]), .Dinrow_0(net241[0]), .VDDrow_0(net328[0]), .GNDrow_0(net330[0]), .CLKrow_0(net239[0]), .RSTBarrow_0(net240[0]));
=======
	TSMC350nm_VerticalScanner I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .In_0_col_0(net350[0:4]), .In_1_col_0(net230[0:4]), .In_2_col_0(net231[0:4]), .In_3_col_0(net232[0:4]), .Outrow_0(net262[0]), .Dinrow_0(net241[0]), .VDDrow_0(net328[0]), .GNDrow_0(net330[0]), .CLKrow_0(net239[0]), .RSTBarrow_0(net240[0]));
>>>>>>> main

 	/*Programming Mux */ 


	/* Island 3 */
	FakeCellGateDecoder I__3 (.island_num(3), .row(0), .col(0));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(3), .direction(vertical), .bits(3), .decode_n0_IN_0_(net341), .decode_n2_IN_1_(net340), .decode_n2_IN_0_(net339));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(3), .direction(vertical), .num(2), .type(drain_select), .switch_n0_prog_drainrail(net342), .switch_n0_run_drainrail(net343));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(3), .direction(vertical), .num(2), .type(prog_switch), .switch_n0_PR_0_(net355[0]), .switch_n0_PR_1_(net376[0]), .switch_n0_PR_2_(net392[0]), .switch_n0_PR_3_(net420[0]), .switch_n1_PR_0_(net298[0]), .switch_n1_PR_1_(net298[1]), .switch_n1_PR_2_(net298[2]), .switch_n1_PR_3_(net298[3]), .switch_n0_In_0_(net356[0]), .switch_n0_In_1_(net377[0]), .switch_n0_In_2_(net393[0]), .switch_n0_In_3_(net421[0]), .switch_n0_VDD(net329[0]), .switch_n0_GND(net330[0]));


	/* Island 4 */
<<<<<<< HEAD
	TSMC350nm_AnalogBuffer I__0 (.island_num(4), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VDD_brow_3(net294[0]), .GND_brow_3(net330[0]), .VINJrow_0(net295[0]), .VINJ_brow_3(net329[0]), .Vgrow_0(net296[0]), .Vd_Pcol_0(net298[0:4]), .Vselrow_0(net297[0]), .Vincol_0(net262[0:4]), .Voutcol_0(net302[0:4]));
=======
	AnalogBuffer I__0 (.island_num(4), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VDD_brow_3(net294[0]), .GND_brow_3(net330[0]), .VINJrow_0(net295[0]), .VINJ_brow_3(net329[0]), .Vgrow_0(net296[0]), .Vd_Pcol_0(net298[0:4]), .Vselrow_0(net297[0]), .Vincol_0(net262[0:4]), .Voutcol_0(net302[0:4]));
>>>>>>> main

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(4), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net406), .decode_n0_n0_IN_1_(net404), .decode_n0_n0_IN_0_(net403));
	TSMC350nm_IndirectSwitches switch(.island_num(4), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net401), .switch_n0_RUN_IN_1_(net401), .switch_n0_GND_B_0_(net330[0]), .switch_n0_GND_B_1_(net330[0]), .switch_n0_CTRL_B_0_(net297[0]), .switch_n0_Vg_0_(net296[0]), .switch_n0_VINJ(net295[0]), .switch_n0_VDD_0_(net329[0]), .switch_n0_VDD_1_(net329[0]), .switch_n0_PROG(net410), .switch_n0_RUN(net411), .switch_n0_Vgsel(net402));


	/* Island 5 */
	TSMC350nm_LVLShift_x16 I__0 (.island_num(5), .row(0), .col(0), .Vin_0_(net331), .Vin_1_(net332), .Vin_2_(net333), .Vin_3_(net334), .Vin_4_(net335), .Vin_5_(net336), .Vin_6_(net337), .DVDD(net328[0]), .GND(net330[0]), .VINJ(net329[0]), .OUT_0_(net339), .OUT_1_(net340), .OUT_2_(net341));

 	/*Programming Mux */ 


	/* Island 6 */
	QDAC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net397), .s_vinj(net399), .s_gnd(net398), .n_VTUN(net347), .w_DrainB_0_(net406), .w_DrainB_1_(net407), .w_DrainB_2_(net408), .w_DrainB_3_(net409), .w_DrainEnable(net348), .n_GateEnable(net348), .w_GateB_0_(net403), .w_GateB_1_(net404), .n_Prog(net410), .n_Run(net411), .n_RST(net349), .n_Code_0_(net412), .n_Code_1_(net413), .n_Code_2_(net414), .n_Code_3_(net415), .n_Code_4_(net416), .e_DEBUG_0_(net350[0]), .e_DEBUG_1_(net230[0]), .e_DEBUG_2_(net231[0]), .e_DEBUG_3_(net232[0]), .e_DEBUG_4_(net350[1]), .s_Vout(net262[1]), .s_Prog_Drainline(net355[0]), .s_Prog_Drainline(net356[0]), .n_VGRUN(net401), .n_VGPROG(net402));

 	/*Programming Mux */ 


	/* Island 7 */
	RampADC_synth I__0 (.island_num(7), .row(0), .col(0), .s_avdd(net397), .s_vinj(net399), .s_gnd(net398), .n_VTUN(net400), .w_DrainB_0_(net406), .w_DrainB_1_(net407), .w_DrainEnable(net405), .n_GateEnable(net405), .w_GateB_0_(net403), .w_GateB_1_(net404), .n_Prog(net410), .w_RST(net364), .w_CLK(net363), .w_Vin(net373), .s_Code_0_(net365), .s_Code_1_(net366), .s_Code_2_(net367), .s_Code_3_(net368), .s_Code_4_(net369), .s_Code_5_(net370), .s_Code_6_(net371), .s_Code_7_(net372), .e_DEBUG_0_(net230[1]), .e_DEBUG_1_(net231[1]), .s_Prog_Drainline(net376[0]), .s_Prog_Drainline(net377[0]), .n_VGRUN(net401), .n_VGPROG(net402));

 	/*Programming Mux */ 


	/* Island 8 */
	AlgorithmicADC_synth I__0 (.island_num(8), .row(0), .col(0), .s_avdd(net397), .s_vinj(net399), .s_gnd(net398), .n_VTUN(net400), .w_DrainB_0_(net406), .w_DrainB_1_(net407), .w_DrainB_2_(net408), .w_DrainB_3_(net409), .w_DrainEnable(net381), .n_GateEnable(net381), .w_GateB_0_(net403), .w_GateB_1_(net404), .n_PROG(net410), .n_RUN(net411), .w_Vin(net386), .s_Code(net387), .e_CLK_Sample(net382), .e_CLK_Amp(net385), .e_CLK_Load(net384), .s_CLK_RST(net383), .s_VRES(net350[3]), .e_DEBUG_0_(net232[1]), .e_DEBUG_1_(net350[2]), .e_DEBUG_2_(net230[2]), .s_Prog_Drainline(net392[0]), .s_Prog_Drainline(net393[0]), .n_VGRUN(net401), .n_VGPROG(net402));

 	/*Programming Mux */ 


	/* Island 9 */
	AveragerDAC_synth I__0 (.island_num(9), .row(0), .col(0), .s_avdd(net397), .s_vinj(net399), .s_gnd(net398), .n_VTUN(net400), .w_DrainB_0_(net406), .w_DrainB_1_(net407), .w_DrainB_2_(net408), .w_DrainB_3_(net409), .w_DrainEnable(net405), .n_GateEnable(net405), .w_GateB_0_(net403), .w_GateB_1_(net404), .n_Prog(net410), .n_Run(net411), .n_Code_0_(net412), .n_Code_1_(net413), .n_Code_2_(net414), .n_Code_3_(net415), .n_Code_4_(net416), .e_DEBUG_0_(net231[2]), .e_DEBUG_1_(net232[2]), .s_Vout(net262[2]), .s_Prog_Drainline(net420[0]), .s_Prog_Drainline(net421[0]), .n_VGRUN(net401), .n_VGPROG(net402));

 	/*Programming Mux */ 

 endmodule