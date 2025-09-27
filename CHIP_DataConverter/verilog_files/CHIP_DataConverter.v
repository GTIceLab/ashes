module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0 I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net243), .fast_clk(net244), .cpu_en(net197), .dbg_en(net198), .dbg_uart_rxd(net199), .nmi(net200), .reset_n(net201), .scan_enable(net202), .dbg_uart_txd(net203), .scan_mode(net204), .wkup(net205), .scan_in1(net206), .scan_in2(net207), .dco_clk(net245), .AVDD(net247), .Cal_IO(net227), .VINJ(net248), .ADC_Trim(net239), .Bias_Trim(net240), .Cal_Vin(net228), .Debug_IO(net229), .I_IO(net230), .VD_IO(net231), .VGPROG(net341), .VGPROG_IO(net232), .VGRUN(net340), .VG_IO(net233), .VTUN_AM(net289), .pulse_fr_drain(net234), .GND(net246), .VTUN_fgmem(net241), .DVDD(net249), .mmio_reg_5_vinj_0_(net342), .mmio_reg_5_vinj_1_(net343), .mmio_reg_5_vinj_2_(net345), .mmio_reg_5_vinj_3_(net346), .mmio_reg_5_vinj_4_(net347), .mmio_reg_5_vinj_5_(net348), .mmio_reg_5_vinj_6_(net290), .mmio_reg_5_vinj_7_(net344), .mmio_reg_5_vinj_9_(net321), .mmio_reg_9_bout_0_(net301), .mmio_reg_9_bout_1_(net322), .mmio_reg_9_bout_2_(net323), .mmio_reg_9_bout_3_(net324), .mmio_reg_9_bout_4_(net325), .mmio_reg_10_bout_0_(net351), .mmio_reg_10_bout_1_(net352), .mmio_reg_10_bout_2_(net353), .mmio_reg_10_bout_3_(net354), .mmio_reg_10_bout_4_(net355), .mmio_reg_10_bout_5_(net303), .mmio_reg_10_bout_6_(net304), .mmio_reg_10_bout_7_(net305), .mmio_reg_10_bout_8_(net306), .mmio_reg_10_bout_9_(net307), .mmio_reg_10_bout_10_(net308), .mmio_reg_10_bout_11_(net309), .mmio_reg_10_bout_12_(net310), .mmio_reg_10_bout_13_(net327), .mmio_reg_10_bout_14_(net291), .mmio_reg_10_bout_15_(net302), .puc_rst_bout(net235), .irq_0_(net195), .irq_1_(net196), .irq_2_(net236), .irq_3_(net237), .irq_4_(net238), .PROG_HV(net349), .RUN_HV(net350), .sram_CS_VBIAS(net226), .peri_use_uP(net225), .peri_spi_slave_clk(net224), .peri_spi_mstr_miso(net220), .peri_spi_slave_mosi(net222), .peri_spi_slave_cs_n(net221), .peri_spi_mstr_spiclk(net242), .peri_spi_slave_miso(net223), .peri_spi_mstr_mosi(net219), .peri_spi_mstr_cs_n_0(net218), .peri_spi_mstr_cs_n_1(net217), .peri_spi_mstr_cs_n_2(net326), .peri_spi_mstr_cs_n_3(net311), .mmio_reg_7_bout_0_(net216), .mmio_reg_7_bout_1_(net215), .Macro_dbg_Scan_Vout(net214), .Macro_dbg_Scan_CLK(net213), .Macro_dbg_Scan_Din(net212), .Macro_dbg_Scan_RST(net211), .dbg_freeze_bout(net210), .dco_enable_bout(net209), .dco_wkup_bout(net208), .lfxt_enable_bout(net189), .lfxt_wkup_bout(net190), .scan_out2_bout(net191), .fgmem_CS_VBIAS(net192), .mmio_reg_in_5_0_(net194), .mmio_reg_in_5_1_(net193));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net246), .avdd_N_2_(net247), .VINJ_N_2_(net248), .DVDD_N_2_(net249), .IO_N_CLK_0_(net242), .IO_N_CLK_1_(net243), .IO_N_CLK_2_(net244), .IO_N_CLK_3_(net245), .IO_N_0_(net189), .IO_N_1_(net190), .IO_N_2_(net191), .IO_N_3_(net191), .IO_N_4_(net192), .IO_N_5_(net193), .IO_N_6_(net194), .IO_N_7_(net195), .IO_N_8_(net196), .IO_N_9_(net197), .IO_N_10_(net198), .IO_N_11_(net199), .IO_N_12_(net200), .IO_N_13_(net201), .IO_N_14_(net202), .IO_N_15_(net203), .IO_N_16_(net204), .IO_N_17_(net205), .IO_N_18_(net206), .IO_N_19_(net207), .gnd_S_0_(net337), .avdd_S_0_(net336), .VINJ_S_0_(net338), .IO_S_0_(net311), .IO_S_1_(net326), .IO_S_2_(net217), .IO_S_3_(net218), .IO_S_4_(net219), .IO_S_5_(net220), .IO_S_6_(net221), .IO_S_7_(net222), .IO_S_8_(net223), .IO_S_9_(net224), .IO_S_10_(net225), .IO_S_11_(net226), .IO_S_26_(net238), .IO_S_27_(net237), .IO_S_44_(net236), .IO_S_45_(net235), .IO_Bare_E_0_(net239), .IO_Bare_E_1_(net240), .IO_E_RES_0_(net289), .IO_E_RES_1_(net241), .IO_E_0_(net227), .IO_E_1_(net228), .IO_E_2_(net229), .IO_E_3_(net230), .IO_E_4_(net231), .IO_E_5_(net232), .IO_E_6_(net341), .IO_E_7_(net233), .IO_E_8_(net234), .IO_W_RES_0_(net339), .IO_W_0_(net208), .IO_W_1_(net209), .IO_W_2_(net210), .IO_W_3_(net211), .IO_W_4_(net212), .IO_W_5_(net213), .IO_W_6_(net214), .IO_W_7_(net215), .IO_W_8_(net216));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_VerticalScanner I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 3 */
	QDAC_synth I__0 (.island_num(3), .row(0), .col(0), .s_avdd(net336), .s_vinj(net338), .s_gnd(net337), .n_VTUN(net289), .w_DrainB_0_(net345), .w_DrainB_1_(net346), .w_DrainB_2_(net347), .w_DrainB_3_(net348), .w_DrainEnable(net290), .n_GateEnable(net290), .w_GateB_0_(net342), .w_GateB_1_(net343), .n_Prog(net349), .n_Run(net350), .n_RST(net291), .n_Code_0_(net351), .n_Code_1_(net352), .n_Code_2_(net353), .n_Code_3_(net354), .n_Code_4_(net355), .n_VGRUN(net340), .n_VGPROG(net341));

 	/*Programming Mux */ 


	/* Island 4 */
	RampADC_synth I__0 (.island_num(4), .row(0), .col(0), .s_avdd(net336), .s_vinj(net338), .s_gnd(net337), .n_VTUN(net339), .w_DrainB_0_(net345), .w_DrainB_1_(net346), .w_DrainEnable(net344), .n_GateEnable(net344), .w_GateB_0_(net342), .w_GateB_1_(net343), .n_Prog(net349), .w_RST(net302), .w_CLK(net301), .w_Vin(net311), .s_Code_0_(net303), .s_Code_1_(net304), .s_Code_2_(net305), .s_Code_3_(net306), .s_Code_4_(net307), .s_Code_5_(net308), .s_Code_6_(net309), .s_Code_7_(net310), .n_VGRUN(net340), .n_VGPROG(net341));

 	/*Programming Mux */ 


	/* Island 5 */
	AlgorithmicADC_synth I__0 (.island_num(5), .row(0), .col(0), .s_avdd(net336), .s_vinj(net338), .s_gnd(net337), .n_VTUN(net339), .w_DrainB_0_(net345), .w_DrainB_1_(net346), .w_DrainB_2_(net347), .w_DrainB_3_(net348), .w_DrainEnable(net321), .n_GateEnable(net321), .w_GateB_0_(net342), .w_GateB_1_(net343), .n_PROG(net349), .n_RUN(net350), .w_Vin(net326), .s_Code(net327), .e_CLK_Sample(net322), .e_CLK_Amp(net325), .e_CLK_Load(net324), .s_CLK_RST(net323), .n_VGRUN(net340), .n_VGPROG(net341));

 	/*Programming Mux */ 


	/* Island 6 */
	AveragerDAC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net336), .s_vinj(net338), .s_gnd(net337), .n_VTUN(net339), .w_DrainB_0_(net345), .w_DrainB_1_(net346), .w_DrainB_2_(net347), .w_DrainB_3_(net348), .w_DrainEnable(net344), .n_GateEnable(net344), .w_GateB_0_(net342), .w_GateB_1_(net343), .n_Prog(net349), .n_Run(net350), .n_Code_0_(net351), .n_Code_1_(net352), .n_Code_2_(net353), .n_Code_3_(net354), .n_Code_4_(net355), .n_VGRUN(net340), .n_VGPROG(net341));

 	/*Programming Mux */ 

 endmodule