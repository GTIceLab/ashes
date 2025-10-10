module TOP(port1);


	/* Island 0 */
	Full_Macro_2p0_abstract I__0 (.island_num(0), .row(0), .col(0), .lfxt_clk(net241), .fast_clk(net242), .cpu_en(net192), .dbg_en(net193), .dbg_uart_rxd(net194), .nmi(net195), .reset_n(net196), .scan_enable(net197), .dbg_uart_txd(net198), .scan_mode(net199), .wkup(net200), .scan_in1(net201), .scan_in2(net202), .dco_clk(net243), .AVDD(net245), .Cal_IO(net222), .VINJ(net246), .ADC_Trim(net236), .Bias_Trim(net237), .Cal_Vin(net223), .Debug_IO(net224), .I_IO(net225), .VD_IO(net226), .VGPROG(net368), .VGPROG_IO(net227), .VGRUN(net367), .VG_IO(net228), .VTUN_AM(net238), .V_IO(net229), .SystemDrainline_0_(net379), .SystemDrainline_1_(net354), .pulse_fr_drain(net230), .GND(net244), .VTUN_fgmem(net239), .DVDD(net248), .mmio_reg_9_bout_0_(net338), .mmio_reg_9_bout_1_(net339), .mmio_reg_9_bout_2_(net340), .mmio_reg_9_bout_3_(net341), .mmio_reg_9_bout_4_(net342), .mmio_reg_9_bout_5_(net343), .mmio_reg_9_bout_6_(net344), .mmio_reg_9_bout_7_(net345), .mmio_reg_9_bout_8_(net346), .mmio_reg_9_bout_9_(net347), .mmio_reg_9_bout_10_(net348), .puc_rst_bout(net231), .irq_0_(net232), .irq_1_(net232), .irq_2_(net233), .irq_3_(net234), .irq_4_(net235), .PROG_HV(net377), .RUN_HV(net378), .sram_CS_VBIAS(net221), .peri_use_uP(net220), .peri_spi_slave_clk(net219), .peri_spi_mstr_miso(net215), .peri_spi_slave_mosi(net217), .peri_spi_slave_cs_n(net216), .peri_spi_mstr_spiclk(net240), .peri_spi_slave_miso(net218), .peri_spi_mstr_mosi(net214), .peri_spi_mstr_cs_n_0(net213), .peri_spi_mstr_cs_n_1(net212), .peri_spi_mstr_cs_n_2(net211), .peri_spi_mstr_cs_n_3(net210), .mmio_reg_7_bout_0_(net209), .mmio_reg_7_bout_1_(net208), .Macro_dbg_Scan_Vout(net207), .Macro_dbg_Scan_CLK(net206), .Macro_dbg_Scan_Din(net205), .Macro_dbg_Scan_RST(net204), .dbg_freeze_bout(net203), .dco_enable_bout(net183), .dco_wkup_bout(net184), .lfxt_enable_bout(net185), .lfxt_wkup_bout(net186), .scan_out2_bout(net187), .scan_out1_bout(net188), .fgmem_CS_VBIAS(net189), .mmio_reg_in_5_0_(net191), .mmio_reg_in_5_1_(net190));

 	/*Programming Mux */ 


	/* Island 1 */
	frame_6p9mm_2mm_digbuf frame (.island_num(1), .row(0), .col(0), .gnd_N_2_(net232), .gnd_N_8_(net244), .avdd_N_2_(net245), .VINJ_N_2_(net246), .DVDD_N_0_(net249), .DVDD_N_1_(net247), .DVDD_N_2_(net248), .IO_N_CLK_0_(net240), .IO_N_CLK_1_(net241), .IO_N_CLK_2_(net242), .IO_N_CLK_3_(net243), .IO_N_0_(net183), .IO_N_1_(net184), .IO_N_2_(net185), .IO_N_3_(net186), .IO_N_4_(net187), .IO_N_5_(net188), .IO_N_6_(net189), .IO_N_7_(net190), .IO_N_8_(net191), .IO_N_9_(net192), .IO_N_10_(net193), .IO_N_11_(net194), .IO_N_12_(net195), .IO_N_13_(net196), .IO_N_14_(net197), .IO_N_15_(net198), .IO_N_16_(net199), .IO_N_17_(net200), .IO_N_18_(net201), .IO_N_19_(net202), .gnd_S_0_(net364), .gnd_S_1_(net316[0]), .gnd_S_2_(net337[0]), .avdd_S_0_(net363), .avdd_S_1_(net315[0]), .VINJ_S_0_(net365), .VINJ_S_1_(net317[0]), .VINJ_S_2_(net336[0]), .DVDD_S_0_(net250), .DVDD_S_2_(net335), .IO_S_0_(net210), .IO_S_1_(net211), .IO_S_2_(net212), .IO_S_3_(net213), .IO_S_4_(net214), .IO_S_5_(net215), .IO_S_6_(net216), .IO_S_7_(net217), .IO_S_8_(net218), .IO_S_9_(net219), .IO_S_10_(net220), .IO_S_11_(net221), .IO_S_12_(net318[0]), .IO_S_13_(net318[1]), .IO_S_14_(net318[2]), .IO_S_15_(net318[3]), .IO_S_16_(net318[4]), .IO_S_17_(net318[5]), .IO_S_18_(net318[6]), .IO_S_19_(net381), .IO_S_20_(net382), .IO_S_21_(net383), .IO_S_22_(net384), .IO_S_23_(net385), .IO_S_26_(net235), .IO_S_27_(net234), .IO_S_44_(net233), .IO_S_45_(net231), .IO_Bare_E_0_(net236), .IO_Bare_E_1_(net237), .IO_E_RES_0_(net238), .IO_E_RES_1_(net239), .IO_E_0_(net222), .IO_E_1_(net223), .IO_E_2_(net224), .IO_E_3_(net225), .IO_E_4_(net226), .IO_E_5_(net227), .IO_E_6_(net228), .IO_E_7_(net229), .IO_E_8_(net230), .IO_W_RES_0_(net366[0]), .IO_W_0_(net203), .IO_W_1_(net204), .IO_W_2_(net205), .IO_W_3_(net206), .IO_W_4_(net207), .IO_W_5_(net208), .IO_W_6_(net209), .IO_W_7_(net386), .buf_vdd_N_0_(net247), .buf_vdd_N_1_(net247), .buf_vdd_N_2_(net247), .buf_vdd_N_3_(net247), .buf_vdd_N_4_(net247), .buf_vdd_N_5_(net248), .buf_vdd_W(net249), .buf_vdd_S_0_(net250), .buf_vdd_S_1_(net250), .buf_vdd_S_2_(net250), .buf_vdd_S_3_(net250), .buf_vdd_S_4_(net250), .buf_vdd_S_5_(net250), .buf_vdd_S_6_(net250), .buf_vdd_S_7_(net250), .buf_vdd_S_8_(net250), .buf_vdd_S_9_(net250), .buf_vdd_E(net335));

 	/*Programming Mux */ 


	/* Island 2 */
	TSMC350nm_AnalogBuffer I__0 (.island_num(2), .row(0), .col(0), .matrix_row(7), .matrix_col(1), .VTUNrow_0(net366[0]), .VDD_brow_6(net315[0]), .GNDrow_0(net337[0]), .GND_brow_6(net316[0]), .VINJrow_0(net336[0]), .VINJ_brow_6(net317[0]), .Vgrow_0(net313[0]), .Vd_Pcol_0(net306[0:7]), .Vselrow_0(net314[0]), .Vincol_0(net355[0:7]), .Voutcol_0(net318[0:7]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(2), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net349), .decode_n0_n0_IN_1_(net370), .decode_n0_n0_IN_0_(net369));
	TSMC350nm_IndirectSwitches switch(.island_num(2), .direction(horizontal), .num(1), .switch_n0_RUN_IN_0_(net367), .switch_n0_RUN_IN_1_(net367), .switch_n0_GND_B_0_(net337[0]), .switch_n0_GND_B_1_(net337[0]), .switch_n0_CTRL_B_0_(net314[0]), .switch_n0_Vg_0_(net313[0]), .switch_n0_VINJ(net336[0]), .switch_n0_PROG(net377), .switch_n0_RUN(net378), .switch_n0_Vgsel(net368));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(2), .direction(vertical), .bits(3), .decode_n0_IN_0_(net374), .decode_n2_IN_1_(net373), .decode_n2_IN_0_(net372), .decode_n0_ENABLE(net349));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(2), .direction(vertical), .num(2), .type(drain_select), .switch_n0_prog_drainrail(net379), .switch_n0_run_drainrail(net354));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(2), .direction(vertical), .num(2), .type(prog_switch), .switch_n0_PR_0_(net306[0]), .switch_n0_PR_1_(net306[1]), .switch_n0_PR_2_(net306[2]), .switch_n0_PR_3_(net306[3]), .switch_n1_PR_0_(net306[4]), .switch_n1_PR_1_(net306[5]), .switch_n1_PR_2_(net306[6]), .switch_n0_VDD(net336[0]), .switch_n0_GND(net337[0]), .switch_n0_RUN(net378));


	/* Island 3 */
	TSMC350nm_LVLShift_x16 I__0 (.island_num(3), .row(0), .col(0), .Vin_0_(net338), .Vin_1_(net339), .Vin_2_(net340), .Vin_3_(net341), .Vin_4_(net342), .Vin_5_(net343), .Vin_6_(net344), .Vin_7_(net345), .Vin_8_(net346), .Vin_9_(net347), .Vin_10_(net348), .DVDD(net335), .GND(net337[0]), .VINJ(net336[0]), .OUT_0_(net349), .OUT_1_(net352), .OUT_2_(net371), .OUT_3_(net369), .OUT_4_(net370), .OUT_5_(net372), .OUT_6_(net373), .OUT_7_(net374), .OUT_8_(net375), .OUT_9_(net376), .OUT_10_(net353));

 	/*Programming Mux */ 


	/* Island 4 */
	TOP_LPF_DelayBlock I__0 (.island_num(4), .row(0), .col(0), .n_Prog(net377), .n_Run(net378), .n_VGRUN(net367), .n_VGPROG(net368), .n_VTUN(net366[0]), .n_AVDD(net363), .n_GateEnable(net352), .s_gnd(net364), .s_vinj(net365), .s_Drainline_Prog(net379), .s_Drainline_Run(net354), .w_GateB_0_(net369), .w_GateB_1_(net370), .w_DrainEnable(net352), .w_DrainB_0_(net372), .w_DrainB_1_(net373), .w_DrainB_2_(net374), .w_DrainB_3_(net375), .w_DrainB_4_(net376), .w_DrainB_5_(net353), .w_Vin(net386), .e_Vout(net355[0]), .e_Vout_tap_0_(net355[1]), .e_Vout_tap_1_(net355[2]), .e_Vout_tap_2_(net355[3]), .e_Vout_tap_3_(net355[4]), .e_Vout_tap_4_(net355[5]));

 	/*Programming Mux */ 


	/* Island 5 */
	TOP_Filter_MeadSOS I__0 (.island_num(5), .row(0), .col(0), .n_Prog(net377), .n_Run(net378), .n_VGRUN(net367), .n_VGPROG(net368), .n_VTUN(net366[0]), .n_AVDD(net363), .n_GateEnable(net371), .s_gnd(net364), .s_vinj(net365), .s_Drainline_Prog(net379), .w_GateB_0_(net369), .w_GateB_1_(net370), .w_DrainEnable(net371), .w_DrainB_0_(net372), .w_DrainB_1_(net373), .w_DrainB_2_(net374), .w_DrainB_3_(net375), .w_DrainB_4_(net376), .w_Vin(net386), .e_Vout(net355[6]), .e_Vout_buf_0_(net381), .e_Vout_buf_1_(net382), .e_Vout_buf_2_(net383), .e_Vout_buf_3_(net384), .e_Vout_buf_4_(net385));

 	/*Programming Mux */ 

 endmodule