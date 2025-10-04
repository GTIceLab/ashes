import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
Top = Circuit()

MacroIsland = Island(Top)
macro = Macro_abs(Top,MacroIsland,[1,1])
macro.place([0,0])

# TODO Fix the instances pin names:[0] to <0> or add another parsing method

# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
chipframe = ChipFrame(Top,FrameIsland,[1,1])
chipframe.place([0,0])
chipframe.markChipFrame()

# Macro <--> Frame Connections
# --------------------------------------------------------------------------------
# ___ IO Pins ___
# North IO Pins
macro.dco_enable_bout += chipframe.IO_N[0]
macro.dco_wkup_bout += chipframe.IO_N[1]
macro.lfxt_enable_bout += chipframe.IO_N[2]
macro.lfxt_wkup_bout += chipframe.IO_N[3]
macro.scan_out2_bout += chipframe.IO_N[4]
macro.scan_out1_bout += chipframe.IO_N[5]
macro.fgmem_CS_VBIAS += chipframe.IO_N[6]
macro.mmio_reg_in_5[1] += chipframe.IO_N[7] 
macro.mmio_reg_in_5[0] += chipframe.IO_N[8]

macro.cpu_en += chipframe.IO_N[9]
macro.dbg_en += chipframe.IO_N[10]
macro.dbg_uart_rxd += chipframe.IO_N[11]
macro.nmi += chipframe.IO_N[12]
macro.reset_n += chipframe.IO_N[13]
macro.scan_enable += chipframe.IO_N[14]
macro.dbg_uart_txd += chipframe.IO_N[15]
macro.scan_mode += chipframe.IO_N[16]
macro.wkup += chipframe.IO_N[17]
macro.scan_in1 += chipframe.IO_N[18]
macro.scan_in2 += chipframe.IO_N[19] 

# West IO pins
macro.dbg_freeze_bout += chipframe.IO_W[0]
macro.Macro_dbg_Scan_RST += chipframe.IO_W[1]
macro.Macro_dbg_Scan_Din += chipframe.IO_W[2]
macro.Macro_dbg_Scan_CLK += chipframe.IO_W[3]
macro.Macro_dbg_Scan_Vout += chipframe.IO_W[4]
macro.mmio_reg_7_bout[1] += chipframe.IO_W[5] 
macro.mmio_reg_7_bout[0] += chipframe.IO_W[6] 

macro.peri_spi_mstr_cs_n_3 += chipframe.IO_W[7]
macro.peri_spi_mstr_cs_n_2 += chipframe.IO_W[8]
macro.peri_spi_mstr_cs_n_1 += chipframe.IO_W[9]
macro.peri_spi_mstr_cs_n_0 += chipframe.IO_W[10]
macro.peri_spi_mstr_mosi += chipframe.IO_W[11]
macro.peri_spi_slave_miso += chipframe.IO_W[12]
macro.peri_spi_slave_cs_n += chipframe.IO_W[13]
macro.peri_spi_slave_mosi += chipframe.IO_W[14]
macro.peri_spi_mstr_miso += chipframe.IO_W[15]
macro.peri_spi_slave_clk += chipframe.IO_W[16]
macro.peri_use_uP += chipframe.IO_W[17]
macro.sram_CS_VBIAS += chipframe.IO_W[18]

# East IO Pins
# bottom right macro pins to east frame pins
macro.Cal_IO += chipframe.IO_E[0]
macro.Cal_Vin += chipframe.IO_E[1]
macro.Debug_IO += chipframe.IO_E[2]
macro.I_IO += chipframe.IO_E[3]
macro.VD_IO += chipframe.IO_E[4]
macro.VGPROG_IO += chipframe.IO_E[5]
macro.VG_IO += chipframe.IO_E[6]
macro.V_IO += chipframe.IO_E[7]
macro.pulse_fr_drain += chipframe.IO_E[8]

macro.puc_rst_bout += chipframe.IO_E[9]
macro.irq[0] += chipframe.gnd_N[2]#####################could change
macro.irq[1] += chipframe.gnd_N[2]#######################could change
macro.irq[2] += chipframe.IO_E[10]
macro.irq[3] += chipframe.IO_E[11]
macro.irq[4] += chipframe.IO_E[12]

# East special pads
macro.ADC_Trim += chipframe.IO_Bare_E[0]
macro.Bias_Trim += chipframe.IO_Bare_E[1]
macro.VTUN_AM += chipframe.IO_E_RES[0]
macro.VTUN_fgmem += chipframe.IO_E_RES[1]

# ___ clk lines ___
macro.peri_spi_mstr_spiclk += chipframe.IO_N_CLK[0] # TODO could change
macro.lfxt_clk += chipframe.IO_N_CLK[1]
macro.fast_clk += chipframe.IO_N_CLK[2]
macro.dco_clk += chipframe.IO_N_CLK[3]

# ___ Macro power/gnd pins ___
macro.GND += chipframe.gnd_N[8]
macro.AVDD += chipframe.avdd_N[2]
macro.VINJ += chipframe.VINJ_N[2]
macro.DVDD += chipframe.DVDD_N[2]

#ALICE Left
ALICELeftIsland = Island(Top)
ALICELeft = ALICE(Top,ALICELeftIsland,[1,1])
ALICELeft.place([0,0])

#ALICE right
ALICERightIsland = Island(Top)
ALICERight = ALICE(Top,ALICERightIsland,[1,1])
ALICERight.place([0,0])

#LVL shifter
LVLShifter1Island = Island(Top)
LVLShifter1 = TSMC350nm_LVLShift_x16(Top,LVLShifter1Island,[1,1])
LVLShifter1.place([0,0])

LVLShifter1.DVDD += chipframe.DVDD_N[0]
LVLShifter1.GND += chipframe.gnd_N[0]
LVLShifter1.VINJ += chipframe.VINJ_N[0]

LVLShifter2Island = Island(Top)
LVLShifter2 = TSMC350nm_LVLShift_x16(Top,LVLShifter2Island,[1,1])
LVLShifter2.place([0,0])

LVLShifter2.DVDD += chipframe.DVDD_N[2]
LVLShifter2.GND += chipframe.gnd_N[8]
LVLShifter2.VINJ += chipframe.VINJ_N[2]

#PROG/Run buffer

DigBufferIsland = Island(Top)
DigBuffer = TSMC350nm_DigBuffer_x2(Top,DigBufferIsland,[1,1])
DigBuffer.place([0,0])

DigBuffer.GND += chipframe.gnd_N[0]
DigBuffer.VINJ += chipframe.VINJ_N[0]

#Analog buffer

AnalogBufferIsland = Island(Top)
AnalogBuffer = AnalogBuffer(Top,AnalogBufferIsland,[4,1])
AnalogBuffer.place([0,0])

DrainDecoder_buf = STD_DrainDecoder(Top,AnalogBufferIsland,bits=2)
DrainSelect_buf = RunDrainSwitch(Top,AnalogBufferIsland,num=1)
DrainSwitch_buf = DrainCutoff(Top,AnalogBufferIsland,num=1)    

GateSwitch_buf = STD_IndirectGateSwitch(Top,AnalogBufferIsland,1)

AnalogBuffer.VTUN += GateSwitch_buf.VTUN
AnalogBuffer.VDD += GateSwitch_buf.VDD[0]
GateSwitch_buf.VPWR[0] += avdd_S[2]
GateSwitch_buf.VPWR[1] += avdd_S[2]
AnalogBuffer.GND += GateSwitch_buf.GND[0]
AnalogBuffer.VINJ += GateSwitch_buf.VINJ
AnalogBuffer.Vg += GateSwitch_buf.Vg[0]
AnalogBuffer.Vsel += GateSwitch_buf.CTRL_B[0]
AnalogBuffer.Vd_P += DrainSwitch_buf.PR

GateSwitch_buf.VTUN_T += chipframe.IO_E_RES[0]
GateSwitch_buf.Vgsel += macro.VGPROG
GateSwitch_buf.PROG += DigBuffer.Out[0]
GateSwitch_buf.RUN += DigBuffer.Out[1]
GateSwitch_buf.VINJ_T += chipframe.VINJ_N[2]
GateSwitch_buf.GND_T += chipframe.gnd_N[8]
GateSwitch_buf.RUN_IN[0] += macro.VGRUN
GateSwitch_buf.RUN_IN[1] += macro.VGRUN
GateSwitch_buf.decode[0] += LVLShifter1.OUT[13]

DrainSwitch_buf.VDD += chipframe.VINJ_N[2]
DrainSwitch_buf.GND += chipframe.gnd_N[8]
DrainSwitch_buf.RUN += DigBuffer.Out[1]

DrainSelect_buf.VINJ += chipframe.VINJ_N[2]
DrainSelect_buf.GND += chipframe.gnd_N[8]
DrainSelect_buf.prog_drainrail += LVLShifter1.OUT[15]
DrainSelect_buf.run_drainrail += LVLShifter2.OUT[15]

DrainDecoder_buf.VINJ += chipframe.VINJ_N[2]
DrainDecoder_buf.GND += chipframe.gnd_N[8]
DrainDecoder_buf.ENABLE += LVLShifter1.OUT[14]
DrainDecoder_buf.IN += LVLShifter2.OUT[12:14]

#ALICE connection
AnalogBuffer.Vin[0] += ALICELeft.e_WTA_out
AnalogBuffer.Vin[1] += ALICELeft.e_AFE_out
AnalogBuffer.Vin[2] += ALICERight.e_WTA_out
AnalogBuffer.Vin[3] += ALICERight.e_AFE_out
AnalogBuffer.Vout[0] += chipframe.IO_E[13]
AnalogBuffer.Vout[1] += chipframe.IO_E[14]
AnalogBuffer.Vout[2] += chipframe.IO_E[15]
AnalogBuffer.Vout[3] += chipframe.IO_E[16]

DigBuffer.In[0] += macro.PROG_HV
DigBuffer.In[1] += macro.RUN_HV
ALICELeft.w_Prog += DigBuffer.Out[0]
ALICERight.w_Prog += DigBuffer.Out[0]
ALICELeft.w_Run += DigBuffer.Out[1]
ALICERight.w_Run += DigBuffer.Out[1]

ALICELeft.w_VGPROG += macro.VGPROG
ALICERight.w_VGPROG += macro.VGPROG
ALICELeft.w_VGRUN += macro.VGRUN
ALICERight.w_VGRUN += macro.VGRUN

ALICELeft.w_VTUN += chipframe.IO_E_RES[0]
ALICERight.w_VTUN += chipframe.IO_E_RES[0]

ALICELeft.w_AVDD += chipframe.avdd_S[0]
ALICERight.w_AVDD += chipframe.avdd_S[2]

LVLShifter1.Vin += macro.mmio_reg_9_bout[0:16]
LVLShifter2.Vin += macro.mmio_reg_10_bout[0:16]
ALICELeft.w_Drainline_Prog_VMM += LVLShifter1.OUT[15]
ALICERight.w_Drainline_Prog_VMM += LVLShifter1.OUT[15]
ALICELeft.n_Drainline_Prog_AFE += LVLShifter1.OUT[15]
ALICERight.n_Drainline_Prog_AFE += LVLShifter1.OUT[15]
ALICELeft.w_Drainline_Run_VMM += LVLShifter2.OUT[15]
ALICERight.w_Drainline_Run_VMM += LVLShifter2.OUT[15]
ALICELeft.n_Drainline_Run_AFE += LVLShifter2.OUT[15]
ALICERight.n_Drainline_Run_AFE += LVLShifter2.OUT[15]

ALICELeft.w_DrainEnable += LVLShifter1.OUT[0]
ALICELeft.w_DrainEnable_VMM += LVLShifter1.OUT[1]
ALICERight.w_DrainEnable += LVLShifter1.OUT[2]
ALICERight.w_DrainEnable_VMM += LVLShifter1.OUT[3]

ALICELeft.n_GateEnable += LVLShifter2.OUT[0]
ALICERight.n_GateEnable += LVLShifter2.OUT[1]
ALICELeft.n_GateEnable_VMM += LVLShifter2.OUT[2]
ALICERight.n_GateEnable_VMM += LVLShifter2.OUT[3]

ALICELeft.w_DrainB += LVLShifter1.OUT[4:13]
ALICERight.w_DrainB += LVLShifter1.OUT[4:13]
ALICELeft.n_GateB += LVLShifter2.OUT[4:12]
ALICERight.n_GateB += LVLShifter2.OUT[4:12]

ALICELeft.e_Din += chipframe.IO_E[17]
ALICERight.e_Din += chipframe.IO_E[17]
ALICELeft.e_CLK += chipframe.IO_E[18]
ALICERight.e_CLK += chipframe.IO_E[18]
ALICELeft.e_RSTBar += chipframe.IO_E[19]
ALICERight.e_RSTBar += chipframe.IO_E[19]
ALICELeft.e_WTA_Vbias += chipframe.IO_E[20]
ALICERight.e_WTA_Vbias += chipframe.IO_E[20]

ALICELeft.n_Vin += chipframe.IO_W[21]
ALICERight.n_Vin += chipframe.IO_W[22]
ALICELeft.n_Vref += chipframe.IO_W[23]
ALICERight.n_Vref += chipframe.IO_W[24]

ALICELeft.s_vinj += chipframe.VINJ_S[0]
ALICERight.s_vinj += chipframe.VINJ_S[2]
ALICELeft.s_gnd += chipframe.gnd_S[0]
ALICERight.s_gnd += chipframe.gnd_S[2]


# Compilation
#-------------------------------------------------------------------------------
design_limits = [15e6, 15e6]
location_islands = ((250600, 4500000), (20600, 20000),(400000,250000),(3600000,250000),(3000000,4100000),(3500000,4200000),(2500000,4300000),(5000000,4200000))
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="ALICEtoFrame",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=7,drainSpace =20,gateSpaceIdx=7,gateSpace=15)
