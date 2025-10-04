module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0_abstract I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net223), .fast_clk(net224), .cpu_en(net175), .dbg_en(net176), .dbg_uart_rxd(net177), .nmi(net178), .reset_n(net179), .scan_enable(net180), .dbg_uart_txd(net181), .scan_mode(net182), .wkup(net183), .scan_in1(net184), .scan_in2(net185), .dco_clk(net225), .AVDD(net227), .Cal_IO(net205), .VINJ(net228), .ADC_Trim(net219), .Bias_Trim(net220), .Cal_Vin(net206), .Debug_IO(net207), .I_IO(net208), .VD_IO(net209), .VGPROG(net393), .VGPROG_IO(net210), .VGRUN(net392), .VG_IO(net211), .VTUN_AM(net341), .V_IO(net212), .SystemDrainline_0_(net411), .SystemDrainline_1_(net412), .pulse_fr_drain(net213), .GND(net226), .VTUN_fgmem(net221), .DVDD(net229), .mmio_reg_5_vinj_0_(net394), .mmio_reg_5_vinj_1_(net395), .mmio_reg_5_vinj_2_(net397), .mmio_reg_5_vinj_3_(net398), .mmio_reg_5_vinj_4_(net399), .mmio_reg_5_vinj_5_(net400), .mmio_reg_5_vinj_6_(net342), .mmio_reg_5_vinj_7_(net396), .mmio_reg_5_vinj_9_(net374), .mmio_reg_9_bout_0_(net358), .mmio_reg_9_bout_1_(net375), .mmio_reg_9_bout_2_(net376), .mmio_reg_9_bout_3_(net377), .mmio_reg_9_bout_4_(net378), .mmio_reg_9_bout_5_(net328), .mmio_reg_9_bout_6_(net329), .mmio_reg_9_bout_7_(net330), .mmio_reg_9_bout_8_(net331), .mmio_reg_9_bout_9_(net332), .mmio_reg_9_bout_10_(net333), .mmio_reg_9_bout_11_(net334), .mmio_reg_9_bout_13_(net239[0]), .mmio_reg_9_bout_14_(net240[0]), .mmio_reg_9_bout_15_(net241[0]), .mmio_reg_10_bout_0_(net403), .mmio_reg_10_bout_1_(net404), .mmio_reg_10_bout_2_(net405), .mmio_reg_10_bout_3_(net406), .mmio_reg_10_bout_4_(net407), .mmio_reg_10_bout_5_(net360), .mmio_reg_10_bout_6_(net361), .mmio_reg_10_bout_7_(net362), .mmio_reg_10_bout_8_(net363), .mmio_reg_10_bout_9_(net364), .mmio_reg_10_bout_10_(net365), .mmio_reg_10_bout_11_(net366), .mmio_reg_10_bout_12_(net367), .mmio_reg_10_bout_13_(net380), .mmio_reg_10_bout_14_(net343), .mmio_reg_10_bout_15_(net359), .puc_rst_bout(net214), .irq_0_(net215), .irq_1_(net215), .irq_2_(net216), .irq_3_(net217), .irq_4_(net218), .PROG_HV(net401), .RUN_HV(net402), .sram_CS_VBIAS(net204), .peri_use_uP(net203), .peri_spi_slave_clk(net202), .peri_spi_mstr_miso(net198), .peri_spi_slave_mosi(net200), .peri_spi_slave_cs_n(net199), .peri_spi_mstr_spiclk(net222), .peri_spi_slave_miso(net201), .peri_spi_mstr_mosi(net197), .peri_spi_mstr_cs_n_0(net196), .peri_spi_mstr_cs_n_1(net195), .peri_spi_mstr_cs_n_2(net194), .peri_spi_mstr_cs_n_3(net193), .mmio_reg_7_bout_0_(net192), .mmio_reg_7_bout_1_(net191), .Macro_dbg_Scan_Vout(net190), .Macro_dbg_Scan_CLK(net189), .Macro_dbg_Scan_Din(net188), .Macro_dbg_Scan_RST(net187), .dbg_freeze_bout(net186), .dco_enable_bout(net166), .dco_wkup_bout(net167), .lfxt_enable_bout(net168), .lfxt_wkup_bout(net169), .scan_out2_bout(net170), .scan_out1_bout(net171), .fgmem_CS_VBIAS(net172), .mmio_reg_in_5_0_(net174), .mmio_reg_in_5_1_(net173));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_2_(net215), .gnd_N_8_(net226), .avdd_N_2_(net227), .VINJ_N_2_(net228), .DVDD_N_2_(net229), .IO_N_CLK_0_(net222), .IO_N_CLK_1_(net223), .IO_N_CLK_2_(net224), .IO_N_CLK_3_(net225), .IO_N_0_(net166), .IO_N_1_(net167), .IO_N_2_(net168), .IO_N_3_(net169), .IO_N_4_(net170), .IO_N_5_(net171), .IO_N_6_(net172), .IO_N_7_(net173), .IO_N_8_(net174), .IO_N_9_(net175), .IO_N_10_(net176), .IO_N_11_(net177), .IO_N_12_(net178), .IO_N_13_(net179), .IO_N_14_(net180), .IO_N_15_(net181), .IO_N_16_(net182), .IO_N_17_(net183), .IO_N_18_(net184), .IO_N_19_(net185), .gnd_S_0_(net389), .gnd_S_2_(net356[0]), .avdd_S_0_(net388), .avdd_S_2_(net355[0]), .VINJ_S_0_(net390), .VINJ_S_2_(net357[0]), .DVDD_S_2_(net327[0]), .IO_S_0_(net193), .IO_S_1_(net194), .IO_S_2_(net195), .IO_S_3_(net196), .IO_S_4_(net197), .IO_S_5_(net198), .IO_S_6_(net199), .IO_S_7_(net200), .IO_S_8_(net201), .IO_S_9_(net202), .IO_S_10_(net203), .IO_S_11_(net204), .IO_S_12_(net368), .IO_S_13_(net379), .IO_S_14_(net300[0]), .IO_S_15_(net300[1]), .IO_S_16_(net300[2]), .IO_S_17_(net300[3]), .IO_S_26_(net218), .IO_S_27_(net217), .IO_S_44_(net216), .IO_S_45_(net214), .IO_Bare_E_0_(net219), .IO_Bare_E_1_(net220), .IO_E_RES_0_(net341), .IO_E_RES_1_(net221), .IO_E_0_(net205), .IO_E_1_(net206), .IO_E_2_(net207), .IO_E_3_(net208), .IO_E_4_(net209), .IO_E_5_(net210), .IO_E_6_(net211), .IO_E_7_(net212), .IO_E_8_(net213), .IO_W_RES_0_(net391), .IO_W_0_(net186), .IO_W_1_(net187), .IO_W_2_(net188), .IO_W_3_(net189), .IO_W_4_(net190), .IO_W_5_(net191), .IO_W_6_(net192));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_VerticalScanner_STD I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .In_0_col_0(net344[0:4]), .In_1_col_0(net230[0:4]), .In_2_col_0(net231[0:4]), .In_3_col_0(net232[0:4]), .Outrow_0(net247[0]), .Dinrow_0(net241[0]), .VDDrow_0(net327[0]), .GNDrow_0(net356[0]), .CLKrow_0(net239[0]), .RSTBarrow_0(net240[0]));

 	/*Programming Mux */ 


	/* Island 3 */
	TSMC350nm_AnalogBuffer I__0 (.island_num(3), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VDD_brow_3(net355[0]), .GNDrow_0(net356[0]), .GND_brow_3(net356[0]), .VINJrow_0(net357[0]), .VINJ_brow_3(net357[0]), .Vgrow_0(net298[0]), .Vd_Pcol_0(net294[0:4]), .Vselrow_0(net299[0]), .Vincol_0(net247[0:4]), .Voutcol_0(net300[0:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(3), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net336), .decode_n0_n0_IN_1_(net395), .decode_n0_n0_IN_0_(net394));
	TSMC350nm_IndirectSwitches switch(.island_num(3), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net392), .switch_n0_RUN_IN_1_(net392), .switch_n0_GND_B_0_(net356[0]), .switch_n0_GND_B_1_(net356[0]), .switch_n0_CTRL_B_0_(net299[0]), .switch_n0_Vg_0_(net298[0]), .switch_n0_VINJ(net357[0]), .switch_n0_PROG(net401), .switch_n0_RUN(net402), .switch_n0_Vgsel(net393));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(3), .direction(vertical), .bits(2), .decode_n0_IN_1_(net398), .decode_n0_IN_0_(net397), .decode_n0_ENABLE(net337));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(3), .direction(vertical), .num(1), .type(drain_select), .switch_n0_prog_drainrail(net411), .switch_n0_run_drainrail(net412));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(3), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net294[0]), .switch_n0_PR_1_(net294[1]), .switch_n0_PR_2_(net294[2]), .switch_n0_PR_3_(net294[3]), .switch_n0_VDD(net357[0]), .switch_n0_GND(net356[0]), .switch_n0_RUN(net402));


	/* Island 4 */
	TSMC350nm_LVLShift_x16 I__0 (.island_num(4), .row(0), .col(0), .Vin_0_(net328), .Vin_1_(net329), .Vin_2_(net330), .Vin_3_(net331), .Vin_4_(net332), .Vin_5_(net333), .Vin_6_(net334), .DVDD(net327[0]), .GND(net356[0]), .VINJ(net357[0]), .OUT_0_(net337), .OUT_1_(net336));

 	/*Programming Mux */ 


	/* Island 5 */
	QDAC_synth I__0 (.island_num(5), .row(0), .col(0), .s_avdd(net388), .s_vinj(net390), .s_gnd(net389), .n_VTUN(net341), .w_DrainB_0_(net397), .w_DrainB_1_(net398), .w_DrainB_2_(net399), .w_DrainB_3_(net400), .w_DrainEnable(net342), .n_GateEnable(net342), .w_GateB_0_(net394), .w_GateB_1_(net395), .n_Prog(net401), .n_Run(net402), .n_RST(net343), .n_Code_0_(net403), .n_Code_1_(net404), .n_Code_2_(net405), .n_Code_3_(net406), .n_Code_4_(net407), .e_DEBUG_0_(net344[0]), .e_DEBUG_1_(net230[0]), .e_DEBUG_2_(net231[0]), .e_DEBUG_3_(net232[0]), .e_DEBUG_4_(net344[1]), .s_Vout(net247[1]), .s_Prog_Drainline(net411), .s_Prog_Drainline(net412), .n_VGRUN(net392), .n_VGPROG(net393));

 	/*Programming Mux */ 


	/* Island 6 */
	RampADC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net355[0]), .s_vinj(net357[0]), .s_gnd(net356[0]), .n_VTUN(net391), .w_DrainB_0_(net397), .w_DrainB_1_(net398), .w_DrainEnable(net396), .n_GateEnable(net396), .w_GateB_0_(net394), .w_GateB_1_(net395), .n_Prog(net401), .w_RST(net359), .w_CLK(net358), .w_Vin(net368), .s_Code_0_(net360), .s_Code_1_(net361), .s_Code_2_(net362), .s_Code_3_(net363), .s_Code_4_(net364), .s_Code_5_(net365), .s_Code_6_(net366), .s_Code_7_(net367), .e_DEBUG_0_(net230[1]), .e_DEBUG_1_(net231[1]), .s_Prog_Drainline(net411), .s_Prog_Drainline(net412), .n_VGRUN(net392), .n_VGPROG(net393));

 	/*Programming Mux */ 


	/* Island 7 */
	AlgorithmicADC_synth I__0 (.island_num(7), .row(0), .col(0), .s_avdd(net388), .s_vinj(net390), .s_gnd(net389), .n_VTUN(net391), .w_DrainB_0_(net397), .w_DrainB_1_(net398), .w_DrainB_2_(net399), .w_DrainB_3_(net400), .w_DrainEnable(net374), .n_GateEnable(net374), .w_GateB_0_(net394), .w_GateB_1_(net395), .n_PROG(net401), .n_RUN(net402), .w_Vin(net379), .s_Code(net380), .e_CLK_Sample(net375), .e_CLK_Amp(net378), .e_CLK_Load(net377), .s_CLK_RST(net376), .s_VRES(net344[3]), .e_DEBUG_0_(net232[1]), .e_DEBUG_1_(net344[2]), .e_DEBUG_2_(net230[2]), .s_Prog_Drainline(net411), .s_Prog_Drainline(net412), .n_VGRUN(net392), .n_VGPROG(net393));

 	/*Programming Mux */ 


	/* Island 8 */
	AveragerDAC_synth I__0 (.island_num(8), .row(0), .col(0), .s_avdd(net388), .s_vinj(net390), .s_gnd(net389), .n_VTUN(net391), .w_DrainB_0_(net397), .w_DrainB_1_(net398), .w_DrainB_2_(net399), .w_DrainB_3_(net400), .w_DrainEnable(net396), .n_GateEnable(net396), .w_GateB_0_(net394), .w_GateB_1_(net395), .n_Prog(net401), .n_Run(net402), .n_Code_0_(net403), .n_Code_1_(net404), .n_Code_2_(net405), .n_Code_3_(net406), .n_Code_4_(net407), .e_DEBUG_0_(net231[2]), .e_DEBUG_1_(net232[2]), .s_Vout(net247[2]), .s_Prog_Drainline(net411), .s_Prog_Drainline(net412), .n_VGRUN(net392), .n_VGPROG(net393));

 	/*Programming Mux */ 

 endmodule