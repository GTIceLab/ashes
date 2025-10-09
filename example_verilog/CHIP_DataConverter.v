module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0_abstract I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net222), .fast_clk(net223), .cpu_en(net173), .dbg_en(net174), .dbg_uart_rxd(net175), .nmi(net176), .reset_n(net177), .scan_enable(net178), .dbg_uart_txd(net179), .scan_mode(net180), .wkup(net181), .scan_in1(net182), .scan_in2(net183), .dco_clk(net224), .AVDD(net226), .Cal_IO(net203), .VINJ(net227), .ADC_Trim(net217), .Bias_Trim(net218), .Cal_Vin(net204), .Debug_IO(net205), .I_IO(net206), .VD_IO(net207), .VGPROG(net385), .VGPROG_IO(net208), .VGRUN(net384), .VG_IO(net209), .VTUN_AM(net219), .V_IO(net210), .SystemDrainline_0_(net403), .SystemDrainline_1_(net404), .pulse_fr_drain(net211), .Signal_DAC_out_0_(net248[0]), .GND(net225), .VTUN_fgmem(net220), .DVDD(net229), .mmio_reg_9_bout_0_(net322), .mmio_reg_9_bout_1_(net323), .mmio_reg_9_bout_2_(net324), .mmio_reg_9_bout_3_(net325), .mmio_reg_9_bout_4_(net326), .mmio_reg_9_bout_5_(net327), .mmio_reg_9_bout_6_(net328), .mmio_reg_9_bout_7_(net329), .mmio_reg_9_bout_8_(net330), .mmio_reg_9_bout_9_(net331), .mmio_reg_9_bout_10_(net332), .mmio_reg_9_bout_13_(net241[0]), .mmio_reg_9_bout_14_(net242[0]), .mmio_reg_9_bout_15_(net243[0]), .mmio_reg_10_bout_0_(net338), .mmio_reg_10_bout_1_(net395), .mmio_reg_10_bout_2_(net396), .mmio_reg_10_bout_3_(net397), .mmio_reg_10_bout_4_(net398), .mmio_reg_10_bout_5_(net399), .mmio_reg_10_bout_6_(net367), .mmio_reg_10_bout_7_(net368), .mmio_reg_10_bout_8_(net369), .mmio_reg_10_bout_9_(net370), .mmio_reg_10_bout_10_(net350), .mmio_reg_10_bout_11_(net351), .puc_rst_bout(net212), .irq_0_(net213), .irq_1_(net213), .irq_2_(net214), .irq_3_(net215), .irq_4_(net216), .PROG_HV(net393), .RUN_HV(net394), .sram_CS_VBIAS(net202), .peri_use_uP(net201), .peri_spi_slave_clk(net200), .peri_spi_mstr_miso(net196), .peri_spi_slave_mosi(net198), .peri_spi_slave_cs_n(net197), .peri_spi_mstr_spiclk(net221), .peri_spi_slave_miso(net199), .peri_spi_mstr_mosi(net195), .peri_spi_mstr_cs_n_0(net194), .peri_spi_mstr_cs_n_1(net193), .peri_spi_mstr_cs_n_2(net192), .peri_spi_mstr_cs_n_3(net191), .mmio_reg_7_bout_0_(net190), .mmio_reg_7_bout_1_(net189), .Macro_dbg_Scan_Vout(net188), .Macro_dbg_Scan_CLK(net187), .Macro_dbg_Scan_Din(net186), .Macro_dbg_Scan_RST(net185), .dbg_freeze_bout(net184), .dco_enable_bout(net164), .dco_wkup_bout(net165), .lfxt_enable_bout(net166), .lfxt_wkup_bout(net167), .scan_out2_bout(net168), .scan_out1_bout(net169), .fgmem_CS_VBIAS(net170), .mmio_reg_in_5_0_(net172), .mmio_reg_in_5_1_(net171), .mmio_reg_in_5_2_(net352), .mmio_reg_in_5_3_(net353), .mmio_reg_in_5_4_(net354), .mmio_reg_in_5_5_(net355), .mmio_reg_in_5_6_(net356), .mmio_reg_in_5_7_(net357), .mmio_reg_in_5_8_(net358), .mmio_reg_in_5_9_(net359), .mmio_reg_in_5_10_(net372));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_digbuf frame (.island_num(1), .row(0), .col(0), .gnd_N_2_(net213), .gnd_N_8_(net225), .avdd_N_2_(net226), .VINJ_N_2_(net227), .DVDD_N_0_(net230), .DVDD_N_1_(net228), .DVDD_N_2_(net229), .IO_N_CLK_0_(net221), .IO_N_CLK_1_(net222), .IO_N_CLK_2_(net223), .IO_N_CLK_3_(net224), .IO_N_0_(net164), .IO_N_1_(net165), .IO_N_2_(net166), .IO_N_3_(net167), .IO_N_4_(net168), .IO_N_5_(net169), .IO_N_6_(net170), .IO_N_7_(net171), .IO_N_8_(net172), .IO_N_9_(net173), .IO_N_10_(net174), .IO_N_11_(net175), .IO_N_12_(net176), .IO_N_13_(net177), .IO_N_14_(net178), .IO_N_15_(net179), .IO_N_16_(net180), .IO_N_17_(net181), .IO_N_18_(net182), .IO_N_19_(net183), .gnd_S_0_(net381), .gnd_S_1_(net303[0]), .gnd_S_2_(net321[0]), .avdd_S_0_(net380), .avdd_S_1_(net302[0]), .VINJ_S_0_(net382), .VINJ_S_1_(net304[0]), .VINJ_S_2_(net320[0]), .DVDD_S_0_(net231), .DVDD_S_2_(net319[0]), .IO_S_0_(net191), .IO_S_1_(net192), .IO_S_2_(net193), .IO_S_3_(net194), .IO_S_4_(net195), .IO_S_5_(net196), .IO_S_6_(net197), .IO_S_7_(net198), .IO_S_8_(net199), .IO_S_9_(net200), .IO_S_10_(net201), .IO_S_11_(net202), .IO_S_12_(net360), .IO_S_13_(net371), .IO_S_14_(net305[0]), .IO_S_15_(net305[1]), .IO_S_16_(net305[2]), .IO_S_17_(net305[3]), .IO_S_18_(net400), .IO_S_26_(net216), .IO_S_27_(net215), .IO_S_44_(net214), .IO_S_45_(net212), .IO_Bare_E_0_(net217), .IO_Bare_E_1_(net218), .IO_E_RES_0_(net219), .IO_E_RES_1_(net220), .IO_E_0_(net203), .IO_E_1_(net204), .IO_E_2_(net205), .IO_E_3_(net206), .IO_E_4_(net207), .IO_E_5_(net208), .IO_E_6_(net209), .IO_E_7_(net210), .IO_E_8_(net211), .IO_W_RES_0_(net383[0]), .IO_W_0_(net184), .IO_W_1_(net185), .IO_W_2_(net186), .IO_W_3_(net187), .IO_W_4_(net188), .IO_W_5_(net189), .IO_W_6_(net190), .buf_vdd_N_0_(net228), .buf_vdd_N_1_(net228), .buf_vdd_N_2_(net228), .buf_vdd_N_3_(net228), .buf_vdd_N_4_(net228), .buf_vdd_N_5_(net229), .buf_vdd_W(net230), .buf_vdd_S_0_(net231), .buf_vdd_S_1_(net231), .buf_vdd_S_2_(net231), .buf_vdd_S_3_(net231), .buf_vdd_S_4_(net231), .buf_vdd_S_5_(net231), .buf_vdd_S_6_(net231), .buf_vdd_S_7_(net231), .buf_vdd_S_8_(net231), .buf_vdd_S_9_(net231), .buf_vdd_E(net319[0]));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_VerticalScanner_STD I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .In_0_col_0(net339[0:4]), .In_1_col_0(net232[0:4]), .In_2_col_0(net233[0:4]), .In_3_col_0(net234[0:4]), .Outrow_0(net248[0]), .Dinrow_0(net243[0]), .VDDrow_0(net319[0]), .GNDrow_0(net321[0]), .CLKrow_0(net241[0]), .RSTBarrow_0(net242[0]));

 	/*Programming Mux */ 


	/* Island 3 */
	TSMC350nm_AnalogBuffer I__0 (.island_num(3), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VTUNrow_0(net383[0]), .VDD_brow_3(net302[0]), .GNDrow_0(net321[0]), .GND_brow_3(net303[0]), .VINJrow_0(net320[0]), .VINJ_brow_3(net304[0]), .Vgrow_0(net300[0]), .Vd_Pcol_0(net296[0:4]), .Vselrow_0(net301[0]), .Vincol_0(net248[0:4]), .Voutcol_0(net305[0:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(3), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net333), .decode_n0_n0_IN_1_(net387), .decode_n0_n0_IN_0_(net386));
	TSMC350nm_IndirectSwitches switch(.island_num(3), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net384), .switch_n0_RUN_IN_1_(net384), .switch_n0_GND_B_0_(net321[0]), .switch_n0_GND_B_1_(net321[0]), .switch_n0_CTRL_B_0_(net301[0]), .switch_n0_Vg_0_(net300[0]), .switch_n0_VINJ(net320[0]), .switch_n0_PROG(net393), .switch_n0_RUN(net394), .switch_n0_Vgsel(net385));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(3), .direction(vertical), .bits(2), .decode_n0_IN_1_(net390), .decode_n0_IN_0_(net389), .decode_n0_ENABLE(net333));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(3), .direction(vertical), .num(1), .type(drain_select), .switch_n0_prog_drainrail(net403), .switch_n0_run_drainrail(net404));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(3), .direction(vertical), .num(1), .type(prog_switch), .switch_n0_PR_0_(net296[0]), .switch_n0_PR_1_(net296[1]), .switch_n0_PR_2_(net296[2]), .switch_n0_PR_3_(net296[3]), .switch_n0_VDD(net320[0]), .switch_n0_GND(net321[0]), .switch_n0_RUN(net394));


	/* Island 4 */
	TSMC350nm_LVLShift_x16 I__0 (.island_num(4), .row(0), .col(0), .Vin_0_(net322), .Vin_1_(net323), .Vin_2_(net324), .Vin_3_(net325), .Vin_4_(net326), .Vin_5_(net327), .Vin_6_(net328), .Vin_7_(net329), .Vin_8_(net330), .Vin_9_(net331), .Vin_10_(net332), .DVDD(net319[0]), .GND(net321[0]), .VINJ(net320[0]), .OUT_0_(net333), .OUT_1_(net337), .OUT_2_(net349), .OUT_3_(net388), .OUT_4_(net366), .OUT_5_(net386), .OUT_6_(net387), .OUT_7_(net389), .OUT_8_(net390), .OUT_9_(net391), .OUT_10_(net392));

 	/*Programming Mux */ 


	/* Island 5 */
	QDAC_synth I__0 (.island_num(5), .row(0), .col(0), .s_avdd(net380), .s_vinj(net382), .s_gnd(net381), .n_VTUN(net383[0]), .w_DrainB_0_(net389), .w_DrainB_1_(net390), .w_DrainB_2_(net391), .w_DrainB_3_(net392), .w_DrainEnable(net337), .n_GateEnable(net337), .w_GateB_0_(net386), .w_GateB_1_(net387), .n_Prog(net393), .n_Run(net394), .n_RST(net338), .n_Code_0_(net395), .n_Code_1_(net396), .n_Code_2_(net397), .n_Code_3_(net398), .n_Code_4_(net399), .e_DEBUG_0_(net339[0]), .e_DEBUG_1_(net232[0]), .e_DEBUG_2_(net233[0]), .e_DEBUG_3_(net234[0]), .e_DEBUG_4_(net339[1]), .s_Vout(net248[1]), .s_Prog_Drainline(net403), .s_Prog_Drainline(net404), .n_VGRUN(net384), .n_VGPROG(net385));

 	/*Programming Mux */ 


	/* Island 6 */
	RampADC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net380), .s_vinj(net382), .s_gnd(net381), .n_VTUN(net383[0]), .w_DrainB_0_(net389), .w_DrainB_1_(net390), .w_DrainEnable(net349), .n_GateEnable(net349), .w_GateB_0_(net386), .w_GateB_1_(net387), .n_Prog(net393), .n_Run(net394), .w_RST(net351), .w_CLK(net350), .w_Vin(net360), .s_Code_0_(net352), .s_Code_1_(net353), .s_Code_2_(net354), .s_Code_3_(net355), .s_Code_4_(net356), .s_Code_5_(net357), .s_Code_6_(net358), .s_Code_7_(net359), .e_DEBUG_0_(net232[1]), .e_DEBUG_1_(net233[1]), .s_Prog_Drainline(net403), .s_Prog_Drainline(net404), .n_VGRUN(net384), .n_VGPROG(net385));

 	/*Programming Mux */ 


	/* Island 7 */
	AlgorithmicADC_synth I__0 (.island_num(7), .row(0), .col(0), .s_avdd(net380), .s_vinj(net382), .s_gnd(net381), .n_VTUN(net383[0]), .w_DrainB_0_(net389), .w_DrainB_1_(net390), .w_DrainB_2_(net391), .w_DrainB_3_(net392), .w_DrainEnable(net366), .n_GateEnable(net366), .w_GateB_0_(net386), .w_GateB_1_(net387), .n_PROG(net393), .n_RUN(net394), .w_Vin(net371), .s_Code(net372), .e_CLK_Sample(net367), .e_CLK_Amp(net370), .e_CLK_Load(net369), .s_CLK_RST(net368), .s_VRES(net339[3]), .e_DEBUG_0_(net234[1]), .e_DEBUG_1_(net339[2]), .e_DEBUG_2_(net232[2]), .s_Prog_Drainline(net403), .s_Prog_Drainline(net404), .n_VGRUN(net384), .n_VGPROG(net385));

 	/*Programming Mux */ 


	/* Island 8 */
	AveragerDAC_synth I__0 (.island_num(8), .row(0), .col(0), .s_avdd(net380), .s_vinj(net382), .s_gnd(net381), .n_VTUN(net383[0]), .w_DrainB_0_(net389), .w_DrainB_1_(net390), .w_DrainB_2_(net391), .w_DrainB_3_(net392), .w_DrainEnable(net388), .n_GateEnable(net388), .w_GateB_0_(net386), .w_GateB_1_(net387), .n_Prog(net393), .n_Run(net394), .n_Code_0_(net395), .n_Code_1_(net396), .n_Code_2_(net397), .n_Code_3_(net398), .n_Code_4_(net399), .e_DEBUG_0_(net233[2]), .e_DEBUG_1_(net234[2]), .s_Vout(net400), .s_Prog_Drainline(net403), .s_Prog_Drainline(net404), .n_VGRUN(net384), .n_VGPROG(net385));

 	/*Programming Mux */ 

 endmodule