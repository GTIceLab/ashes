module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0_abstract I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net222), .fast_clk(net223), .cpu_en(net174), .dbg_en(net175), .dbg_uart_rxd(net176), .nmi(net177), .reset_n(net178), .scan_enable(net179), .dbg_uart_txd(net180), .scan_mode(net181), .wkup(net182), .scan_in1(net183), .scan_in2(net184), .dco_clk(net224), .AVDD(net226), .Cal_IO(net204), .VINJ(net227), .ADC_Trim(net218), .Bias_Trim(net219), .Cal_Vin(net205), .Debug_IO(net206), .I_IO(net207), .VD_IO(net208), .VGPROG(net388), .VGPROG_IO(net209), .VGRUN(net387), .VG_IO(net210), .VTUN_AM(net339), .V_IO(net211), .SystemDrainline_0_(net406), .SystemDrainline_1_(net407), .pulse_fr_drain(net212), .GND(net225), .VTUN_fgmem(net220), .DVDD(net228), .mmio_reg_5_vinj_0_(net299), .mmio_reg_5_vinj_1_(net300), .mmio_reg_5_vinj_2_(net301), .mmio_reg_5_vinj_3_(net302), .mmio_reg_9_bout_0_(net323), .mmio_reg_9_bout_1_(net324), .mmio_reg_9_bout_2_(net325), .mmio_reg_9_bout_3_(net326), .mmio_reg_9_bout_4_(net327), .mmio_reg_9_bout_5_(net328), .mmio_reg_9_bout_6_(net329), .mmio_reg_9_bout_7_(net330), .mmio_reg_9_bout_8_(net331), .mmio_reg_9_bout_9_(net332), .mmio_reg_9_bout_10_(net333), .mmio_reg_9_bout_13_(net238[0]), .mmio_reg_9_bout_14_(net239[0]), .mmio_reg_9_bout_15_(net240[0]), .mmio_reg_10_bout_0_(net341), .mmio_reg_10_bout_1_(net398), .mmio_reg_10_bout_2_(net399), .mmio_reg_10_bout_3_(net400), .mmio_reg_10_bout_4_(net401), .mmio_reg_10_bout_5_(net402), .mmio_reg_10_bout_6_(net370), .mmio_reg_10_bout_7_(net371), .mmio_reg_10_bout_8_(net372), .mmio_reg_10_bout_9_(net373), .mmio_reg_10_bout_10_(net353), .mmio_reg_10_bout_11_(net354), .puc_rst_bout(net213), .irq_0_(net214), .irq_1_(net214), .irq_2_(net215), .irq_3_(net216), .irq_4_(net217), .PROG_HV(net396), .RUN_HV(net397), .sram_CS_VBIAS(net203), .peri_use_uP(net202), .peri_spi_slave_clk(net201), .peri_spi_mstr_miso(net197), .peri_spi_slave_mosi(net199), .peri_spi_slave_cs_n(net198), .peri_spi_mstr_spiclk(net221), .peri_spi_slave_miso(net200), .peri_spi_mstr_mosi(net196), .peri_spi_mstr_cs_n_0(net195), .peri_spi_mstr_cs_n_1(net194), .peri_spi_mstr_cs_n_2(net193), .peri_spi_mstr_cs_n_3(net192), .mmio_reg_7_bout_0_(net191), .mmio_reg_7_bout_1_(net190), .Macro_dbg_Scan_Vout(net189), .Macro_dbg_Scan_CLK(net188), .Macro_dbg_Scan_Din(net187), .Macro_dbg_Scan_RST(net186), .dbg_freeze_bout(net185), .dco_enable_bout(net165), .dco_wkup_bout(net166), .lfxt_enable_bout(net167), .lfxt_wkup_bout(net168), .scan_out2_bout(net169), .scan_out1_bout(net170), .fgmem_CS_VBIAS(net171), .mmio_reg_in_5_0_(net173), .mmio_reg_in_5_1_(net172), .mmio_reg_in_5_2_(net355), .mmio_reg_in_5_3_(net356), .mmio_reg_in_5_4_(net357), .mmio_reg_in_5_5_(net358), .mmio_reg_in_5_6_(net359), .mmio_reg_in_5_7_(net360), .mmio_reg_in_5_8_(net361), .mmio_reg_in_5_9_(net362), .mmio_reg_in_5_10_(net375));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_2_(net214), .gnd_N_8_(net225), .avdd_N_2_(net226), .VINJ_N_2_(net227), .DVDD_N_2_(net228), .IO_N_CLK_0_(net221), .IO_N_CLK_1_(net222), .IO_N_CLK_2_(net223), .IO_N_CLK_3_(net224), .IO_N_0_(net165), .IO_N_1_(net166), .IO_N_2_(net167), .IO_N_3_(net168), .IO_N_4_(net169), .IO_N_5_(net170), .IO_N_6_(net171), .IO_N_7_(net172), .IO_N_8_(net173), .IO_N_9_(net174), .IO_N_10_(net175), .IO_N_11_(net176), .IO_N_12_(net177), .IO_N_13_(net178), .IO_N_14_(net179), .IO_N_15_(net180), .IO_N_16_(net181), .IO_N_17_(net182), .IO_N_18_(net183), .IO_N_19_(net184), .gnd_S_0_(net384), .gnd_S_1_(net304[0]), .gnd_S_2_(net322[0]), .avdd_S_0_(net383), .avdd_S_1_(net303[0]), .VINJ_S_0_(net385), .VINJ_S_1_(net305[0]), .VINJ_S_2_(net321[0]), .DVDD_S_2_(net320[0]), .IO_S_0_(net192), .IO_S_1_(net193), .IO_S_2_(net194), .IO_S_3_(net195), .IO_S_4_(net196), .IO_S_5_(net197), .IO_S_6_(net198), .IO_S_7_(net199), .IO_S_8_(net200), .IO_S_9_(net201), .IO_S_10_(net202), .IO_S_11_(net203), .IO_S_12_(net363), .IO_S_13_(net374), .IO_S_14_(net306[0]), .IO_S_15_(net306[1]), .IO_S_16_(net306[2]), .IO_S_17_(net306[3]), .IO_S_26_(net217), .IO_S_27_(net216), .IO_S_44_(net215), .IO_S_45_(net213), .IO_Bare_E_0_(net218), .IO_Bare_E_1_(net219), .IO_E_RES_0_(net339), .IO_E_RES_1_(net220), .IO_E_0_(net204), .IO_E_1_(net205), .IO_E_2_(net206), .IO_E_3_(net207), .IO_E_4_(net208), .IO_E_5_(net209), .IO_E_6_(net210), .IO_E_7_(net211), .IO_E_8_(net212), .IO_W_RES_0_(net386), .IO_W_0_(net185), .IO_W_1_(net186), .IO_W_2_(net187), .IO_W_3_(net188), .IO_W_4_(net189), .IO_W_5_(net190), .IO_W_6_(net191));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_VerticalScanner_STD I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .In_0_col_0(net342[0:4]), .In_1_col_0(net229[0:4]), .In_2_col_0(net230[0:4]), .In_3_col_0(net231[0:4]), .Outrow_0(net246[0]), .Dinrow_0(net240[0]), .VDDrow_0(net320[0]), .GNDrow_0(net322[0]), .CLKrow_0(net238[0]), .RSTBarrow_0(net239[0]));

 	/*Programming Mux */ 


	/* Island 3 */
	TSMC350nm_AnalogBuffer I__0 (.island_num(3), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VDD_brow_3(net303[0]), .GNDrow_0(net322[0]), .GND_brow_3(net304[0]), .VINJrow_0(net321[0]), .VINJ_brow_3(net305[0]), .Vgrow_0(net297[0]), .Vd_Pcol_0(net293[0:4]), .Vselrow_0(net298[0]), .Vincol_0(net246[0:4]), .Voutcol_0(net306[0:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(3), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net335), .decode_n0_n0_IN_1_(net300), .decode_n0_n0_IN_0_(net299));
	TSMC350nm_IndirectSwitches switch(.island_num(3), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net387), .switch_n0_RUN_IN_1_(net387), .switch_n0_GND_B_0_(net322[0]), .switch_n0_GND_B_1_(net322[0]), .switch_n0_CTRL_B_0_(net298[0]), .switch_n0_Vg_0_(net297[0]), .switch_n0_VINJ(net321[0]), .switch_n0_PROG(net396), .switch_n0_RUN(net397), .switch_n0_Vgsel(net388));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(3), .direction(vertical), .bits(2), .decode_n0_IN_1_(net302), .decode_n0_IN_0_(net301), .decode_n0_ENABLE(net335));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(3), .direction(vertical), .num(1), .type(drain_select), .switch_n0_prog_drainrail(net406), .switch_n0_run_drainrail(net407));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(3), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net293[0]), .switch_n0_PR_1_(net293[1]), .switch_n0_PR_2_(net293[2]), .switch_n0_PR_3_(net293[3]), .switch_n0_VDD(net321[0]), .switch_n0_GND(net322[0]), .switch_n0_RUN(net397));


	/* Island 4 */
	TSMC350nm_LVLShift_x16 I__0 (.island_num(4), .row(0), .col(0), .Vin_0_(net323), .Vin_1_(net324), .Vin_2_(net325), .Vin_3_(net326), .Vin_4_(net327), .Vin_5_(net328), .Vin_6_(net329), .Vin_7_(net330), .Vin_8_(net331), .Vin_9_(net332), .Vin_10_(net333), .DVDD(net320[0]), .GND(net322[0]), .VINJ(net321[0]), .OUT_0_(net335), .OUT_1_(net340), .OUT_2_(net352), .OUT_3_(net391), .OUT_4_(net369), .OUT_5_(net389), .OUT_6_(net390), .OUT_7_(net392), .OUT_8_(net393), .OUT_9_(net394), .OUT_10_(net395));

 	/*Programming Mux */ 


	/* Island 5 */
	QDAC_synth I__0 (.island_num(5), .row(0), .col(0), .s_avdd(net383), .s_vinj(net385), .s_gnd(net384), .n_VTUN(net339), .w_DrainB_0_(net392), .w_DrainB_1_(net393), .w_DrainB_2_(net394), .w_DrainB_3_(net395), .w_DrainEnable(net340), .n_GateEnable(net340), .w_GateB_0_(net389), .w_GateB_1_(net390), .n_Prog(net396), .n_Run(net397), .n_RST(net341), .n_Code_0_(net398), .n_Code_1_(net399), .n_Code_2_(net400), .n_Code_3_(net401), .n_Code_4_(net402), .e_DEBUG_0_(net342[0]), .e_DEBUG_1_(net229[0]), .e_DEBUG_2_(net230[0]), .e_DEBUG_3_(net231[0]), .e_DEBUG_4_(net342[1]), .s_Vout(net246[1]), .s_Prog_Drainline(net406), .s_Prog_Drainline(net407), .n_VGRUN(net387), .n_VGPROG(net388));

 	/*Programming Mux */ 


	/* Island 6 */
	RampADC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net383), .s_vinj(net385), .s_gnd(net384), .n_VTUN(net386), .w_DrainB_0_(net392), .w_DrainB_1_(net393), .w_DrainEnable(net352), .n_GateEnable(net352), .w_GateB_0_(net389), .w_GateB_1_(net390), .n_Prog(net396), .n_Run(net397), .w_RST(net354), .w_CLK(net353), .w_Vin(net363), .s_Code_0_(net355), .s_Code_1_(net356), .s_Code_2_(net357), .s_Code_3_(net358), .s_Code_4_(net359), .s_Code_5_(net360), .s_Code_6_(net361), .s_Code_7_(net362), .e_DEBUG_0_(net229[1]), .e_DEBUG_1_(net230[1]), .s_Prog_Drainline(net406), .s_Prog_Drainline(net407), .n_VGRUN(net387), .n_VGPROG(net388));

 	/*Programming Mux */ 


	/* Island 7 */
	AlgorithmicADC_synth I__0 (.island_num(7), .row(0), .col(0), .s_avdd(net383), .s_vinj(net385), .s_gnd(net384), .n_VTUN(net386), .w_DrainB_0_(net392), .w_DrainB_1_(net393), .w_DrainB_2_(net394), .w_DrainB_3_(net395), .w_DrainEnable(net369), .n_GateEnable(net369), .w_GateB_0_(net389), .w_GateB_1_(net390), .n_PROG(net396), .n_RUN(net397), .w_Vin(net374), .s_Code(net375), .e_CLK_Sample(net370), .e_CLK_Amp(net373), .e_CLK_Load(net372), .s_CLK_RST(net371), .s_VRES(net342[3]), .e_DEBUG_0_(net231[1]), .e_DEBUG_1_(net342[2]), .e_DEBUG_2_(net229[2]), .s_Prog_Drainline(net406), .s_Prog_Drainline(net407), .n_VGRUN(net387), .n_VGPROG(net388));

 	/*Programming Mux */ 


	/* Island 8 */
	AveragerDAC_synth I__0 (.island_num(8), .row(0), .col(0), .s_avdd(net383), .s_vinj(net385), .s_gnd(net384), .n_VTUN(net386), .w_DrainB_0_(net392), .w_DrainB_1_(net393), .w_DrainB_2_(net394), .w_DrainB_3_(net395), .w_DrainEnable(net391), .n_GateEnable(net391), .w_GateB_0_(net389), .w_GateB_1_(net390), .n_Prog(net396), .n_Run(net397), .n_Code_0_(net398), .n_Code_1_(net399), .n_Code_2_(net400), .n_Code_3_(net401), .n_Code_4_(net402), .e_DEBUG_0_(net230[2]), .e_DEBUG_1_(net231[2]), .s_Vout(net246[2]), .s_Prog_Drainline(net406), .s_Prog_Drainline(net407), .n_VGRUN(net387), .n_VGPROG(net388));

 	/*Programming Mux */ 

 endmodule