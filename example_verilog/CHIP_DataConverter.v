module TOP(port1);


	/* Island 0 */
	Full_Macro_Edit I__0 (.island_num(0), .row(0), .col(0), .cpu_en(net187), .dbg_en(net188), .dbg_uart_rxd(net189), .dbg_uart_txd(net190), .dco_clk(net191), .lfxt_clk(net192), .nmi(net193), .reset_n(net194), .scan_enable(net195), .scan_mode(net196), .wkup(net197), .scan_in1(net198), .scan_in2(net199), .scan_out1(net200), .scan_out2(net201), .mclk(net202), .DVDD(net242), .GND(net239), .AVDD_AM(net240), .VINJ(net241), .VTUN_AM(net246), .VTUN_fgmem(net215), .VGPROG_IO(net211), .fgmem_CS_VBIAS(net210), .ADC_Trim(net213), .Bias_Trim(net214), .Cal_IO(net209), .Cal_Vin(net208), .Debug_IO(net207), .I_IO(net206), .VD_IO(net205), .VG_IO(net204), .V_IO(net203), .irq_acc_12_(net234), .irq_acc_13_(net233), .irq_10_(net232), .irq_11_(net231), .irq_12_(net230), .irq_13_(net229), .fast_ADC_clk(net238), .drain_pulse_rst(net212), .sram_CS_VBIAS(net228), .peri_use_uP(net227), .peri_spi_rst(net226), .peri_spi_cpu_clk(net235), .peri_spi_slave_clk(net236), .peri_spi_slave_miso(net225), .peri_spi_slave_mosi(net224), .peri_spi_slave_cs_n(net223), .peri_spi_mstr_spiclk(net237), .peri_spi_mstr_miso(net222), .peri_spi_mstr_mosi(net221), .peri_spi_mstr_cs_n_0(net220), .peri_spi_mstr_cs_n_1(net219), .peri_spi_mstr_cs_n_2(net218), .peri_spi_mstr_cs_n_3(net217), .peri_spi_mstr_TX_Ready(net216), .peri_spi_mstr_RX_DV(net186), .peri_spi_slave_RX_DV(net185));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net239), .avdd_N_2_(net240), .VINJ_N_2_(net241), .DVDD_N_2_(net242), .IO_N_CLK_0_(net235), .IO_N_CLK_1_(net236), .IO_N_CLK_2_(net237), .IO_N_CLK_3_(net238), .IO_N_0_(net185), .IO_N_1_(net186), .IO_N_2_(net187), .IO_N_3_(net188), .IO_N_4_(net189), .IO_N_5_(net190), .IO_N_6_(net191), .IO_N_7_(net192), .IO_N_8_(net193), .IO_N_9_(net194), .IO_N_10_(net195), .IO_N_11_(net196), .IO_N_12_(net197), .IO_N_13_(net198), .IO_N_14_(net199), .IO_N_15_(net200), .IO_N_16_(net201), .IO_N_17_(net202), .IO_N_19_(net203), .gnd_S_0_(net257), .avdd_S_0_(net256), .VINJ_S_0_(net258), .IO_S_0_(net225), .IO_S_1_(net226), .IO_S_2_(net227), .IO_S_3_(net228), .IO_S_4_(net229), .IO_S_5_(net230), .IO_S_6_(net231), .IO_S_7_(net232), .IO_S_8_(net233), .IO_S_9_(net234), .IO_Bare_E_0_(net213), .IO_Bare_E_1_(net214), .IO_E_RES_0_(net246), .IO_E_RES_1_(net215), .IO_E_0_(net204), .IO_E_1_(net205), .IO_E_2_(net206), .IO_E_3_(net207), .IO_E_4_(net208), .IO_E_5_(net209), .IO_E_6_(net210), .IO_E_7_(net211), .IO_E_8_(net212), .IO_W_RES_0_(net259), .IO_W_0_(net216), .IO_W_1_(net217), .IO_W_2_(net218), .IO_W_3_(net219), .IO_W_4_(net220), .IO_W_5_(net221), .IO_W_6_(net222), .IO_W_7_(net223), .IO_W_8_(net224));

 	/*Programming Mux */ 


	/* Island 2 */
	QDAC_synth I__0 (.island_num(2), .row(0), .col(0), .s_avdd(net256), .s_vinj(net258), .s_gnd(net257), .n_VTUN(net246));

 	/*Programming Mux */ 


	/* Island 3 */
	RampADC_synth I__0 (.island_num(3), .row(0), .col(0), .s_avdd(net256), .s_vinj(net258), .s_gnd(net257), .n_VTUN(net259));

 	/*Programming Mux */ 


	/* Island 4 */
	AlgorithmicADC_synth I__0 (.island_num(4), .row(0), .col(0), .s_avdd(net256), .s_vinj(net258), .s_gnd(net257), .n_VTUN(net259));

 	/*Programming Mux */ 


	/* Island 5 */
	AveragerDAC_synth I__0 (.island_num(5), .row(0), .col(0), .s_avdd(net256), .s_vinj(net258), .s_gnd(net257), .n_VTUN(net259));

 	/*Programming Mux */ 

 endmodule