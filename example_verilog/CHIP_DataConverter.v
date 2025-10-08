module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0_abstract I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net219), .fast_clk(net220), .cpu_en(net171), .dbg_en(net172), .dbg_uart_rxd(net173), .nmi(net174), .reset_n(net175), .scan_enable(net176), .dbg_uart_txd(net177), .scan_mode(net178), .wkup(net179), .scan_in1(net180), .scan_in2(net181), .dco_clk(net221), .AVDD(net223), .Cal_IO(net201), .VINJ(net224), .ADC_Trim(net215), .Bias_Trim(net216), .Cal_Vin(net202), .Debug_IO(net203), .I_IO(net204), .VD_IO(net205), .VGPROG(net388), .VGPROG_IO(net206), .VGRUN(net387), .VG_IO(net207), .VTUN_AM(net339), .V_IO(net208), .SystemDrainline_0_(net406), .SystemDrainline_1_(net407), .pulse_fr_drain(net209), .GND(net222), .VTUN_fgmem(net217), .DVDD(net226), .mmio_reg_5_vinj_0_(net299), .mmio_reg_5_vinj_1_(net300), .mmio_reg_5_vinj_2_(net301), .mmio_reg_5_vinj_3_(net302), .mmio_reg_9_bout_0_(net323), .mmio_reg_9_bout_1_(net324), .mmio_reg_9_bout_2_(net325), .mmio_reg_9_bout_3_(net326), .mmio_reg_9_bout_4_(net327), .mmio_reg_9_bout_5_(net328), .mmio_reg_9_bout_6_(net329), .mmio_reg_9_bout_7_(net330), .mmio_reg_9_bout_8_(net331), .mmio_reg_9_bout_9_(net332), .mmio_reg_9_bout_10_(net333), .mmio_reg_9_bout_13_(net238[0]), .mmio_reg_9_bout_14_(net239[0]), .mmio_reg_9_bout_15_(net240[0]), .mmio_reg_10_bout_0_(net341), .mmio_reg_10_bout_1_(net398), .mmio_reg_10_bout_2_(net399), .mmio_reg_10_bout_3_(net400), .mmio_reg_10_bout_4_(net401), .mmio_reg_10_bout_5_(net402), .mmio_reg_10_bout_6_(net370), .mmio_reg_10_bout_7_(net371), .mmio_reg_10_bout_8_(net372), .mmio_reg_10_bout_9_(net373), .mmio_reg_10_bout_10_(net353), .mmio_reg_10_bout_11_(net354), .puc_rst_bout(net210), .irq_0_(net211), .irq_1_(net211), .irq_2_(net212), .irq_3_(net213), .irq_4_(net214), .PROG_HV(net396), .RUN_HV(net397), .sram_CS_VBIAS(net200), .peri_use_uP(net199), .peri_spi_slave_clk(net198), .peri_spi_mstr_miso(net194), .peri_spi_slave_mosi(net196), .peri_spi_slave_cs_n(net195), .peri_spi_mstr_spiclk(net218), .peri_spi_slave_miso(net197), .peri_spi_mstr_mosi(net193), .peri_spi_mstr_cs_n_0(net192), .peri_spi_mstr_cs_n_1(net191), .peri_spi_mstr_cs_n_2(net190), .peri_spi_mstr_cs_n_3(net189), .mmio_reg_7_bout_0_(net188), .mmio_reg_7_bout_1_(net187), .Macro_dbg_Scan_Vout(net186), .Macro_dbg_Scan_CLK(net185), .Macro_dbg_Scan_Din(net184), .Macro_dbg_Scan_RST(net183), .dbg_freeze_bout(net182), .dco_enable_bout(net162), .dco_wkup_bout(net163), .lfxt_enable_bout(net164), .lfxt_wkup_bout(net165), .scan_out2_bout(net166), .scan_out1_bout(net167), .fgmem_CS_VBIAS(net168), .mmio_reg_in_5_0_(net170), .mmio_reg_in_5_1_(net169), .mmio_reg_in_5_2_(net355), .mmio_reg_in_5_3_(net356), .mmio_reg_in_5_4_(net357), .mmio_reg_in_5_5_(net358), .mmio_reg_in_5_6_(net359), .mmio_reg_in_5_7_(net360), .mmio_reg_in_5_8_(net361), .mmio_reg_in_5_9_(net362), .mmio_reg_in_5_10_(net375));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_digbuf frame (.island_num(1), .row(0), .col(0), .gnd_N_2_(net211), .gnd_N_8_(net222), .avdd_N_2_(net223), .VINJ_N_2_(net224), .DVDD_N_0_(net227), .DVDD_N_1_(net225), .DVDD_N_2_(net226), .IO_N_CLK_0_(net218), .IO_N_CLK_1_(net219), .IO_N_CLK_2_(net220), .IO_N_CLK_3_(net221), .IO_N_0_(net162), .IO_N_1_(net163), .IO_N_2_(net164), .IO_N_3_(net165), .IO_N_4_(net166), .IO_N_5_(net167), .IO_N_6_(net168), .IO_N_7_(net169), .IO_N_8_(net170), .IO_N_9_(net171), .IO_N_10_(net172), .IO_N_11_(net173), .IO_N_12_(net174), .IO_N_13_(net175), .IO_N_14_(net176), .IO_N_15_(net177), .IO_N_16_(net178), .IO_N_17_(net179), .IO_N_18_(net180), .IO_N_19_(net181), .gnd_S_0_(net384), .gnd_S_1_(net304[0]), .gnd_S_2_(net322[0]), .avdd_S_0_(net383), .avdd_S_1_(net303[0]), .VINJ_S_0_(net385), .VINJ_S_1_(net305[0]), .VINJ_S_2_(net321[0]), .DVDD_S_0_(net228), .DVDD_S_2_(net320[0]), .IO_S_0_(net189), .IO_S_1_(net190), .IO_S_2_(net191), .IO_S_3_(net192), .IO_S_4_(net193), .IO_S_5_(net194), .IO_S_6_(net195), .IO_S_7_(net196), .IO_S_8_(net197), .IO_S_9_(net198), .IO_S_10_(net199), .IO_S_11_(net200), .IO_S_12_(net363), .IO_S_13_(net374), .IO_S_14_(net306[0]), .IO_S_15_(net306[1]), .IO_S_16_(net306[2]), .IO_S_17_(net306[3]), .IO_S_26_(net214), .IO_S_27_(net213), .IO_S_44_(net212), .IO_S_45_(net210), .IO_Bare_E_0_(net215), .IO_Bare_E_1_(net216), .IO_E_RES_0_(net339), .IO_E_RES_1_(net217), .IO_E_0_(net201), .IO_E_1_(net202), .IO_E_2_(net203), .IO_E_3_(net204), .IO_E_4_(net205), .IO_E_5_(net206), .IO_E_6_(net207), .IO_E_7_(net208), .IO_E_8_(net209), .IO_W_RES_0_(net386), .IO_W_0_(net182), .IO_W_1_(net183), .IO_W_2_(net184), .IO_W_3_(net185), .IO_W_4_(net186), .IO_W_5_(net187), .IO_W_6_(net188), .buf_vdd_N_0_(net225), .buf_vdd_N_1_(net225), .buf_vdd_N_2_(net225), .buf_vdd_N_3_(net225), .buf_vdd_N_4_(net225), .buf_vdd_N_5_(net226), .buf_vdd_W(net227), .buf_vdd_S_0_(net228), .buf_vdd_S_1_(net228), .buf_vdd_S_2_(net228), .buf_vdd_S_3_(net228), .buf_vdd_S_4_(net228), .buf_vdd_S_5_(net228), .buf_vdd_S_6_(net228), .buf_vdd_S_7_(net228), .buf_vdd_S_8_(net228), .buf_vdd_S_9_(net228), .buf_vdd_E(net320[0]));

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