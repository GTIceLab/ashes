module TOP(port1);


	/* Island 0 */
	Full_Macro_Edit I__0 (.island_num(0), .row(0), .col(0), .cpu_en(net191), .dbg_en(net192), .dbg_uart_rxd(net193), .dbg_uart_txd(net194), .dco_clk(net195), .lfxt_clk(net196), .nmi(net197), .reset_n(net198), .scan_enable(net199), .scan_mode(net200), .wkup(net201), .scan_in1(net202), .scan_in2(net203), .scan_out1(net204), .scan_out2(net205), .mclk(net206), .DVDD(net247), .GND(net244), .AVDD_AM(net245), .VINJ(net246), .VTUN_AM(net219), .VTUN_fgmem(net220), .VGPROG_IO(net215), .fgmem_CS_VBIAS(net214), .ADC_Trim(net217), .Bias_Trim(net218), .Cal_IO(net213), .Cal_Vin(net212), .Debug_IO(net211), .I_IO(net210), .VD_IO(net209), .VG_IO(net208), .V_IO(net207), .irq_acc_12_(net239), .irq_acc_13_(net238), .irq_10_(net237), .irq_11_(net236), .irq_12_(net235), .irq_13_(net234), .fast_ADC_clk(net243), .drain_pulse_rst(net216), .sram_CS_VBIAS(net233), .peri_use_uP(net232), .peri_spi_rst(net231), .peri_spi_cpu_clk(net240), .peri_spi_slave_clk(net241), .peri_spi_slave_miso(net230), .peri_spi_slave_mosi(net229), .peri_spi_slave_cs_n(net228), .peri_spi_mstr_spiclk(net242), .peri_spi_mstr_miso(net227), .peri_spi_mstr_mosi(net226), .peri_spi_mstr_cs_n_0(net225), .peri_spi_mstr_cs_n_1(net224), .peri_spi_mstr_cs_n_2(net223), .peri_spi_mstr_cs_n_3(net222), .peri_spi_mstr_TX_Ready(net221), .peri_spi_mstr_RX_DV(net190), .peri_spi_slave_RX_DV(net189));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net244), .avdd_N_2_(net245), .VINJ_N_2_(net246), .DVDD_N_2_(net247), .IO_N_CLK_0_(net240), .IO_N_CLK_1_(net241), .IO_N_CLK_2_(net242), .IO_N_CLK_3_(net243), .IO_N_0_(net189), .IO_N_1_(net190), .IO_N_2_(net191), .IO_N_3_(net192), .IO_N_4_(net193), .IO_N_5_(net194), .IO_N_6_(net195), .IO_N_7_(net196), .IO_N_8_(net197), .IO_N_9_(net198), .IO_N_10_(net199), .IO_N_11_(net200), .IO_N_12_(net201), .IO_N_13_(net202), .IO_N_14_(net203), .IO_N_15_(net204), .IO_N_16_(net205), .IO_N_17_(net206), .IO_N_19_(net207), .IO_S_0_(net230), .IO_S_1_(net231), .IO_S_2_(net232), .IO_S_3_(net233), .IO_S_4_(net234), .IO_S_5_(net235), .IO_S_6_(net236), .IO_S_7_(net237), .IO_S_8_(net238), .IO_S_9_(net239), .IO_Bare_E_0_(net217), .IO_Bare_E_1_(net218), .IO_E_RES_0_(net219), .IO_E_RES_1_(net220), .IO_E_0_(net208), .IO_E_1_(net209), .IO_E_2_(net210), .IO_E_3_(net211), .IO_E_4_(net212), .IO_E_5_(net213), .IO_E_6_(net214), .IO_E_7_(net215), .IO_E_8_(net216), .IO_W_0_(net221), .IO_W_1_(net222), .IO_W_2_(net223), .IO_W_3_(net224), .IO_W_4_(net225), .IO_W_5_(net226), .IO_W_6_(net227), .IO_W_7_(net228), .IO_W_8_(net229));

 	/*Programming Mux */ 

 endmodule