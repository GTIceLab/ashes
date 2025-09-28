module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0 I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net236), .fast_clk(net237), .cpu_en(net190), .dbg_en(net191), .dbg_uart_rxd(net192), .nmi(net193), .reset_n(net194), .scan_enable(net195), .dbg_uart_txd(net196), .scan_mode(net197), .wkup(net198), .scan_in1(net199), .scan_in2(net200), .dco_clk(net238), .AVDD(net240), .Cal_IO(net220), .VINJ(net241), .ADC_Trim(net232), .Bias_Trim(net233), .Cal_Vin(net221), .Debug_IO(net222), .I_IO(net223), .VD_IO(net224), .VGPROG(net453), .VGPROG_IO(net225), .VGRUN(net452), .VG_IO(net226), .VTUN_AM(net398), .pulse_fr_drain(net227), .GND(net239), .VTUN_fgmem(net234), .DVDD(net242), .mmio_reg_5_vinj_0_(net454), .mmio_reg_5_vinj_1_(net455), .mmio_reg_5_vinj_2_(net457), .mmio_reg_5_vinj_3_(net458), .mmio_reg_5_vinj_4_(net459), .mmio_reg_5_vinj_5_(net460), .mmio_reg_5_vinj_6_(net399), .mmio_reg_5_vinj_7_(net456), .mmio_reg_5_vinj_9_(net432), .mmio_reg_9_bout_0_(net414), .mmio_reg_9_bout_1_(net433), .mmio_reg_9_bout_2_(net434), .mmio_reg_9_bout_3_(net435), .mmio_reg_9_bout_4_(net436), .mmio_reg_9_bout_13_(net253[0]), .mmio_reg_9_bout_14_(net254[0]), .mmio_reg_9_bout_15_(net255[0]), .mmio_reg_10_bout_0_(net463), .mmio_reg_10_bout_1_(net464), .mmio_reg_10_bout_2_(net465), .mmio_reg_10_bout_3_(net466), .mmio_reg_10_bout_4_(net467), .mmio_reg_10_bout_5_(net416), .mmio_reg_10_bout_6_(net417), .mmio_reg_10_bout_7_(net418), .mmio_reg_10_bout_8_(net419), .mmio_reg_10_bout_9_(net420), .mmio_reg_10_bout_10_(net421), .mmio_reg_10_bout_11_(net422), .mmio_reg_10_bout_12_(net423), .mmio_reg_10_bout_13_(net438), .mmio_reg_10_bout_14_(net400), .mmio_reg_10_bout_15_(net415), .puc_rst_bout(net228), .irq_0_(net188), .irq_1_(net189), .irq_2_(net229), .irq_3_(net230), .irq_4_(net231), .PROG_HV(net461), .RUN_HV(net462), .sram_CS_VBIAS(net219), .peri_use_uP(net218), .peri_spi_slave_clk(net217), .peri_spi_mstr_miso(net213), .peri_spi_slave_mosi(net215), .peri_spi_slave_cs_n(net214), .peri_spi_mstr_spiclk(net235), .peri_spi_slave_miso(net216), .peri_spi_mstr_mosi(net212), .peri_spi_mstr_cs_n_0(net211), .peri_spi_mstr_cs_n_1(net210), .peri_spi_mstr_cs_n_2(net437), .peri_spi_mstr_cs_n_3(net424), .mmio_reg_7_bout_0_(net209), .mmio_reg_7_bout_1_(net208), .Macro_dbg_Scan_Vout(net207), .Macro_dbg_Scan_CLK(net206), .Macro_dbg_Scan_Din(net205), .Macro_dbg_Scan_RST(net204), .dbg_freeze_bout(net203), .dco_enable_bout(net202), .dco_wkup_bout(net201), .lfxt_enable_bout(net182), .lfxt_wkup_bout(net183), .scan_out2_bout(net184), .fgmem_CS_VBIAS(net185), .mmio_reg_in_5_0_(net187), .mmio_reg_in_5_1_(net186));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net239), .avdd_N_2_(net240), .VINJ_N_2_(net241), .DVDD_N_2_(net242), .IO_N_CLK_0_(net235), .IO_N_CLK_1_(net236), .IO_N_CLK_2_(net237), .IO_N_CLK_3_(net238), .IO_N_0_(net182), .IO_N_1_(net183), .IO_N_2_(net184), .IO_N_3_(net184), .IO_N_4_(net185), .IO_N_5_(net186), .IO_N_6_(net187), .IO_N_7_(net188), .IO_N_8_(net189), .IO_N_9_(net190), .IO_N_10_(net191), .IO_N_11_(net192), .IO_N_12_(net193), .IO_N_13_(net194), .IO_N_14_(net195), .IO_N_15_(net196), .IO_N_16_(net197), .IO_N_17_(net198), .IO_N_18_(net199), .IO_N_19_(net200), .gnd_S_0_(net449), .gnd_S_2_(net394[0]), .avdd_S_0_(net448), .avdd_S_2_(net357[0]), .VINJ_S_0_(net450), .VINJ_S_2_(net393[0]), .DVDD_S_2_(net392[0]), .IO_S_0_(net424), .IO_S_1_(net437), .IO_S_2_(net210), .IO_S_3_(net211), .IO_S_4_(net212), .IO_S_5_(net213), .IO_S_6_(net214), .IO_S_7_(net215), .IO_S_8_(net216), .IO_S_9_(net217), .IO_S_10_(net218), .IO_S_11_(net219), .IO_S_26_(net231), .IO_S_27_(net230), .IO_S_44_(net229), .IO_S_45_(net228), .IO_Bare_E_0_(net232), .IO_Bare_E_1_(net233), .IO_E_RES_0_(net398), .IO_E_RES_1_(net234), .IO_E_0_(net220), .IO_E_1_(net221), .IO_E_2_(net222), .IO_E_3_(net223), .IO_E_4_(net224), .IO_E_5_(net225), .IO_E_6_(net453), .IO_E_7_(net226), .IO_E_8_(net227), .IO_W_RES_0_(net451), .IO_W_0_(net201), .IO_W_1_(net202), .IO_W_2_(net203), .IO_W_3_(net204), .IO_W_4_(net205), .IO_W_5_(net206), .IO_W_6_(net207), .IO_W_7_(net208), .IO_W_8_(net209));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_VerticalScanner I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .In_0_col_0(net401[0:4]), .In_1_col_0(net243[0:4]), .In_2_col_0(net244[0:4]), .In_3_col_0(net245[0:4]), .Dinrow_0(net255[0]), .VDDrow_0(net392[0]), .GNDrow_0(net394[0]), .CLKrow_0(net253[0]), .RSTBarrow_0(net254[0]));

 	/*Programming Mux */ 


	/* Island 3 */
	FakeCellGateDecoder I__3 (.island_num(3), .row(0), .col(0));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(3), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(3), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(3), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net406[0]), .switch_n0_PR_1_(net427[0]), .switch_n0_PR_2_(net443[0]), .switch_n0_PR_3_(net471[0]), .switch_n0_In_0_(net407[0]), .switch_n0_In_1_(net428[0]), .switch_n0_In_2_(net444[0]), .switch_n0_In_3_(net472[0]), .switch_n0_VDD(net393[0]), .switch_n0_GND(net394[0]));


	/* Island 4 */
	AnalogBuffer I__0 (.island_num(4), .row(0), .col(0), .matrix_row(4), .matrix_col(1), .VDD_brow_3(net357[0]), .GND_brow_3(net394[0]), .VINJrow_0(net358[0]), .VINJ_brow_3(net393[0]), .Vgrow_0(net359[0]), .Vincol_0(net307[0:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(4), .direction(horizontal), .bits(2));
	TSMC350nm_IndirectSwitches switch(.island_num(4), .direction(horizontal), .num(1), .switch_n0_Vg_0_(net359[0]), .switch_n0_VINJ(net358[0]));


	/* Island 5 */
	TSMC350nm_LVLShift_x16 I__0 (.island_num(5), .row(0), .col(0), .DVDD(net392[0]), .GND(net394[0]), .VINJ(net393[0]));

 	/*Programming Mux */ 


	/* Island 6 */
	QDAC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net448), .s_vinj(net450), .s_gnd(net449), .n_VTUN(net398), .w_DrainB_0_(net457), .w_DrainB_1_(net458), .w_DrainB_2_(net459), .w_DrainB_3_(net460), .w_DrainEnable(net399), .n_GateEnable(net399), .w_GateB_0_(net454), .w_GateB_1_(net455), .n_Prog(net461), .n_Run(net462), .n_RST(net400), .n_Code_0_(net463), .n_Code_1_(net464), .n_Code_2_(net465), .n_Code_3_(net466), .n_Code_4_(net467), .e_DEBUG_0_(net401[0]), .e_DEBUG_1_(net243[0]), .e_DEBUG_2_(net244[0]), .e_DEBUG_3_(net245[0]), .e_DEBUG_4_(net401[1]), .s_Vout(net307[1]), .s_Prog_Drainline(net406[0]), .s_Prog_Drainline(net407[0]), .n_VGRUN(net452), .n_VGPROG(net453));

 	/*Programming Mux */ 


	/* Island 7 */
	RampADC_synth I__0 (.island_num(7), .row(0), .col(0), .s_avdd(net448), .s_vinj(net450), .s_gnd(net449), .n_VTUN(net451), .w_DrainB_0_(net457), .w_DrainB_1_(net458), .w_DrainEnable(net456), .n_GateEnable(net456), .w_GateB_0_(net454), .w_GateB_1_(net455), .n_Prog(net461), .w_RST(net415), .w_CLK(net414), .w_Vin(net424), .s_Code_0_(net416), .s_Code_1_(net417), .s_Code_2_(net418), .s_Code_3_(net419), .s_Code_4_(net420), .s_Code_5_(net421), .s_Code_6_(net422), .s_Code_7_(net423), .e_DEBUG_0_(net243[1]), .e_DEBUG_1_(net244[1]), .s_Prog_Drainline(net427[0]), .s_Prog_Drainline(net428[0]), .n_VGRUN(net452), .n_VGPROG(net453));

 	/*Programming Mux */ 


	/* Island 8 */
	AlgorithmicADC_synth I__0 (.island_num(8), .row(0), .col(0), .s_avdd(net448), .s_vinj(net450), .s_gnd(net449), .n_VTUN(net451), .w_DrainB_0_(net457), .w_DrainB_1_(net458), .w_DrainB_2_(net459), .w_DrainB_3_(net460), .w_DrainEnable(net432), .n_GateEnable(net432), .w_GateB_0_(net454), .w_GateB_1_(net455), .n_PROG(net461), .n_RUN(net462), .w_Vin(net437), .s_Code(net438), .e_CLK_Sample(net433), .e_CLK_Amp(net436), .e_CLK_Load(net435), .s_CLK_RST(net434), .s_VRES(net401[3]), .e_DEBUG_0_(net245[1]), .e_DEBUG_1_(net401[2]), .e_DEBUG_2_(net243[2]), .s_Prog_Drainline(net443[0]), .s_Prog_Drainline(net444[0]), .n_VGRUN(net452), .n_VGPROG(net453));

 	/*Programming Mux */ 


	/* Island 9 */
	AveragerDAC_synth I__0 (.island_num(9), .row(0), .col(0), .s_avdd(net448), .s_vinj(net450), .s_gnd(net449), .n_VTUN(net451), .w_DrainB_0_(net457), .w_DrainB_1_(net458), .w_DrainB_2_(net459), .w_DrainB_3_(net460), .w_DrainEnable(net456), .n_GateEnable(net456), .w_GateB_0_(net454), .w_GateB_1_(net455), .n_Prog(net461), .n_Run(net462), .n_Code_0_(net463), .n_Code_1_(net464), .n_Code_2_(net465), .n_Code_3_(net466), .n_Code_4_(net467), .e_DEBUG_0_(net244[2]), .e_DEBUG_1_(net245[2]), .s_Vout(net307[2]), .s_Prog_Drainline(net471[0]), .s_Prog_Drainline(net472[0]), .n_VGRUN(net452), .n_VGPROG(net453));

 	/*Programming Mux */ 

 endmodule