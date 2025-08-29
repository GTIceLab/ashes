module TOP(port1);


	/* Island 0 */
	Full_Macro_Edit I__0 (.island_num(0), .row(0), .col(0), .cpu_en(net267), .dbg_en(net268), .dbg_uart_rxd(net269), .dbg_uart_txd(net270), .dco_clk(net271), .lfxt_clk(net272), .nmi(net273), .reset_n(net274), .scan_enable(net275), .scan_mode(net276), .wkup(net277), .scan_in1(net278), .scan_in2(net279), .scan_out1(net280), .scan_out2(net281), .mclk(net282), .DVDD(net325), .GND(net322), .AVDD_AM(net323), .VINJ(net324), .VTUN_AM(net316), .VTUN_fgmem(net317), .VGPROG_IO(net291), .fgmem_CS_VBIAS(net290), .ADC_Trim(net314), .Bias_Trim(net315), .Cal_IO(net289), .Cal_Vin(net288), .Debug_IO(net287), .I_IO(net286), .VD_IO(net285), .VG_IO(net284), .V_IO(net283), .irq_acc_12_(net298), .irq_acc_13_(net297), .irq_10_(net296), .irq_11_(net295), .irq_12_(net294), .irq_13_(net293), .fast_ADC_clk(net321), .drain_pulse_rst(net292), .sram_CS_VBIAS(net313), .peri_use_uP(net312), .peri_spi_rst(net311), .peri_spi_cpu_clk(net318), .peri_spi_slave_clk(net319), .peri_spi_slave_miso(net310), .peri_spi_slave_mosi(net309), .peri_spi_slave_cs_n(net308), .peri_spi_mstr_spiclk(net320), .peri_spi_mstr_miso(net307), .peri_spi_mstr_mosi(net306), .peri_spi_mstr_cs_n_0(net305), .peri_spi_mstr_cs_n_1(net304), .peri_spi_mstr_cs_n_2(net303), .peri_spi_mstr_cs_n_3(net302), .peri_spi_mstr_TX_Ready(net301), .peri_spi_mstr_RX_DV(net300), .peri_spi_slave_RX_DV(net299));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_6p2mm_edit frame (.island_num(1), .row(0), .col(0), .gnd_N_8_(net322), .avdd_N_2_(net323), .VINJ_N_2_(net324), .DVDD_N_2_(net325), .IO_N_CLK_0_(net318), .IO_N_CLK_1_(net319), .IO_N_CLK_2_(net320), .IO_N_CLK_3_(net321), .IO_N_0_(net267), .IO_N_1_(net268), .IO_N_2_(net269), .IO_N_3_(net270), .IO_N_4_(net271), .IO_N_5_(net272), .IO_N_6_(net273), .IO_N_7_(net274), .IO_N_8_(net275), .IO_N_9_(net276), .IO_N_10_(net277), .IO_N_11_(net278), .IO_N_12_(net279), .IO_N_13_(net280), .IO_N_14_(net281), .IO_N_15_(net282), .IO_N_17_(net283), .IO_Bare_E_0_(net314), .IO_Bare_E_1_(net315), .IO_E_RES_0_(net316), .IO_E_RES_1_(net317), .IO_E_0_(net284), .IO_E_1_(net285), .IO_E_2_(net286), .IO_E_3_(net287), .IO_E_4_(net288), .IO_E_5_(net289), .IO_E_6_(net290), .IO_E_7_(net291), .IO_E_8_(net292), .IO_W_0_(net293), .IO_W_1_(net294), .IO_W_2_(net295), .IO_W_3_(net296), .IO_W_4_(net297), .IO_W_5_(net298), .IO_W_6_(net299), .IO_W_7_(net300), .IO_W_8_(net301), .IO_W_9_(net302), .IO_W_10_(net303), .IO_W_11_(net304), .IO_W_12_(net305), .IO_W_13_(net306), .IO_W_14_(net307), .IO_W_15_(net308), .IO_W_16_(net309), .IO_W_17_(net310), .IO_W_18_(net311), .IO_W_19_(net312), .IO_W_20_(net313));

 	/*Programming Mux */ 

 endmodule