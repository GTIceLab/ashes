module TOP(port1);


	/* Island 0 */
	Full_Macro_Edit I__0 (.island_num(0), .row(0), .col(0), .cpu_en(net186), .dbg_en(net187), .dbg_uart_rxd(net188), .dbg_uart_txd(net189), .dco_clk(net190), .lfxt_clk(net191), .nmi(net192), .reset_n(net193), .scan_enable(net194), .scan_mode(net195), .wkup(net196), .scan_in1(net197), .scan_in2(net198), .scan_out1(net199), .scan_out2(net200), .mclk(net201), .DVDD(net241), .GND(net238), .AVDD_AM(net239), .VINJ(net240), .VTUN_AM(net298), .VTUN_fgmem(net214), .VGPROG_IO(net210), .fgmem_CS_VBIAS(net209), .ADC_Trim(net212), .Bias_Trim(net213), .Cal_IO(net208), .Cal_Vin(net207), .Debug_IO(net206), .I_IO(net205), .VD_IO(net204), .VGRUN(net381), .VG_IO(net203), .V_IO(net202), .irq_acc_12_(net233), .irq_acc_13_(net232), .irq_10_(net231), .irq_11_(net230), .irq_12_(net229), .irq_13_(net228), .fast_ADC_clk(net237), .drain_pulse_rst(net211), .sram_CS_VBIAS(net227), .peri_use_uP(net226), .peri_spi_rst(net225), .peri_spi_cpu_clk(net234), .peri_spi_slave_clk(net235), .peri_spi_slave_miso(net224), .peri_spi_slave_mosi(net223), .peri_spi_slave_cs_n(net222), .peri_spi_mstr_spiclk(net236), .peri_spi_mstr_miso(net221), .peri_spi_mstr_mosi(net220), .peri_spi_mstr_cs_n_0(net219), .peri_spi_mstr_cs_n_1(net218), .peri_spi_mstr_cs_n_2(net217), .peri_spi_mstr_cs_n_3(net216), .peri_spi_mstr_TX_Ready(net215), .peri_spi_mstr_RX_DV(net185), .peri_spi_slave_RX_DV(net184));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net238), .avdd_N_2_(net239), .VINJ_N_2_(net240), .DVDD_N_2_(net241), .IO_N_CLK_0_(net234), .IO_N_CLK_1_(net235), .IO_N_CLK_2_(net236), .IO_N_CLK_3_(net237), .IO_N_0_(net184), .IO_N_1_(net185), .IO_N_2_(net186), .IO_N_3_(net187), .IO_N_4_(net188), .IO_N_5_(net189), .IO_N_6_(net190), .IO_N_7_(net191), .IO_N_8_(net192), .IO_N_9_(net193), .IO_N_10_(net194), .IO_N_11_(net195), .IO_N_12_(net196), .IO_N_13_(net197), .IO_N_14_(net198), .IO_N_15_(net199), .IO_N_16_(net200), .IO_N_17_(net201), .IO_N_19_(net202), .gnd_S_0_(net378), .avdd_S_0_(net377), .VINJ_S_0_(net379), .IO_S_0_(net224), .IO_S_1_(net225), .IO_S_2_(net226), .IO_S_3_(net227), .IO_S_4_(net228), .IO_S_5_(net229), .IO_S_6_(net230), .IO_S_7_(net231), .IO_S_8_(net232), .IO_S_9_(net233), .IO_Bare_E_0_(net212), .IO_Bare_E_1_(net213), .IO_E_RES_0_(net298), .IO_E_RES_1_(net214), .IO_E_0_(net203), .IO_E_1_(net204), .IO_E_2_(net205), .IO_E_3_(net206), .IO_E_4_(net207), .IO_E_5_(net208), .IO_E_6_(net209), .IO_E_7_(net210), .IO_E_8_(net211), .IO_W_RES_0_(net380), .IO_W_0_(net215), .IO_W_1_(net216), .IO_W_2_(net217), .IO_W_3_(net218), .IO_W_4_(net219), .IO_W_5_(net220), .IO_W_6_(net221), .IO_W_7_(net222), .IO_W_8_(net223));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_VerticalScanner I__0 (.island_num(2), .row(0), .col(0), .matrix_row(4), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 3 */
	QDAC_synth I__0 (.island_num(3), .row(0), .col(0), .s_avdd(net377), .s_vinj(net379), .s_gnd(net378), .n_VTUN(net298), .n_VGRUN(net381));

 	/*Programming Mux */ 


	/* Island 4 */
	RampADC_synth I__0 (.island_num(4), .row(0), .col(0), .s_avdd(net377), .s_vinj(net379), .s_gnd(net378), .n_VTUN(net380), .n_VGRUN(net381));

 	/*Programming Mux */ 


	/* Island 5 */
	AlgorithmicADC_synth I__0 (.island_num(5), .row(0), .col(0), .s_avdd(net377), .s_vinj(net379), .s_gnd(net378), .n_VTUN(net380), .n_VGRUN(net381));

 	/*Programming Mux */ 


	/* Island 6 */
	AveragerDAC_synth I__0 (.island_num(6), .row(0), .col(0), .s_avdd(net377), .s_vinj(net379), .s_gnd(net378), .n_VTUN(net380), .n_VGRUN(net381));

 	/*Programming Mux */ 

 endmodule