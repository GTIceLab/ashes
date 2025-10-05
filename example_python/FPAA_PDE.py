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

#Fabric
FabricIsland = Island(Top)
Fabric = TILE_analog(Top,FabricIsland,[9,9])
Fabric.place([0,0])

#LVL shifter
LVLShifter1Island = Island(Top)
LVLShifter1 = TSMC350nm_LVLShift_x16(Top,LVLShifter1Island,[1,1])
LVLShifter1.place([0,0])

LVLShifter1.DVDD += chipframe.DVDD_W
LVLShifter1.GND += chipframe.gnd_W[2]
LVLShifter1.VINJ += chipframe.VINJ_W
LVLShifter1.Vin += macro.mmio_reg_9_bout[0:16]

LVLShifter2Island = Island(Top)
LVLShifter2 = TSMC350nm_LVLShift_x16(Top,LVLShifter2Island,[1,1])
LVLShifter2.place([0,0])
LVLShifter2.Vin += macro.mmio_reg_10_bout[0:16]

LVLShifter2.DVDD += chipframe.DVDD_W
LVLShifter2.GND += chipframe.gnd_W[2]
LVLShifter2.VINJ += chipframe.VINJ_W

LVLShifter3Island = Island(Top)
LVLShifter3 = TSMC350nm_LVLShift_x16(Top,LVLShifter3Island,[1,1])
LVLShifter3.place([0,0])
for i in range(2,15):
	LVLShifter3.Vin[i] += macro.mmio_reg_7_bout[i]

LVLShifter3.DVDD += chipframe.DVDD_E
LVLShifter3.GND += chipframe.gnd_E[2]
LVLShifter3.VINJ += chipframe.VINJ_E


#PROG/Run buffer

DigBufferIsland = Island(Top)
DigBuffer = TSMC350nm_DigBuffer_x2(Top,DigBufferIsland,[1,1])
DigBuffer.place([0,0])

DigBuffer.GND += chipframe.gnd_W[2]
DigBuffer.VINJ += chipframe.VINJ_W
DigBuffer.In[0] += macro.PROG_HV
DigBuffer.In[1] += macro.RUN_HV

#Analog buffer

AnalogBuffer1Island = Island(Top)
AnalogBuffer1 = AnalogBuffer(Top,AnalogBuffer1Island,[16,1])
AnalogBuffer1.place([0,0])

DrainDecoder_buf1 = STD_DrainDecoder(Top,AnalogBuffer1Island,bits=4)
DrainSelect_buf1 = RunDrainSwitch(Top,AnalogBuffer1Island,num=4)
DrainSwitch_buf1 = DrainCutoff(Top,AnalogBuffer1Island,num=4)    

GateSwitch_buf1 = STD_IndirectGateSwitch(Top,AnalogBuffer1Island,1)

AnalogBuffer1.VTUN += GateSwitch_buf1.VTUN
AnalogBuffer1.VDD += GateSwitch_buf1.VDD[0]
GateSwitch_buf1.VPWR[0] += chipframe.avdd_E
GateSwitch_buf1.VPWR[1] += chipframe. avdd_E
AnalogBuffer1.GND += GateSwitch_buf1.GND[0]
AnalogBuffer1.VINJ += GateSwitch_buf1.VINJ
AnalogBuffer1.Vg += GateSwitch_buf1.Vg[0]
AnalogBuffer1.Vsel += GateSwitch_buf1.CTRL_B[0]
AnalogBuffer1.Vd_P += DrainSwitch_buf1.PR

GateSwitch_buf1.VTUN_T += chipframe.IO_E_RES[0]
GateSwitch_buf1.Vgsel += macro.VGPROG
GateSwitch_buf1.PROG += DigBuffer.Out[0]
GateSwitch_buf1.RUN += DigBuffer.Out[1]
GateSwitch_buf1.VINJ_T += chipframe.VINJ_E
GateSwitch_buf1.GND_T += chipframe.gnd_E[2]
GateSwitch_buf1.RUN_IN[0] += macro.VGRUN
GateSwitch_buf1.RUN_IN[1] += macro.VGRUN
GateSwitch_buf1.decode[0] += LVLShifter3.OUT[2]

DrainSwitch_buf1.VDD += chipframe.VINJ_E
DrainSwitch_buf1.GND += chipframe.gnd_E[2]
DrainSwitch_buf1.RUN += DigBuffer.Out[1]

DrainSelect_buf1.VINJ += chipframe.VINJ_E
DrainSelect_buf1.GND += chipframe.gnd_E[2]
DrainSelect_buf1.prog_drainrail += LVLShifter3.OUT[13]
DrainSelect_buf1.run_drainrail += LVLShifter3.OUT[14]

#DrainDecoder_buf1.VINJ += chipframe.VINJ_W
#DrainDecoder_buf1.GND += chipframe.gnd_N[8]
DrainDecoder_buf1.ENABLE += LVLShifter3.OUT[3]
DrainDecoder_buf1.IN += LVLShifter3.OUT[4:8]

#west and east non-IO Fabric Connections
for i in range(9):
	Fabric.e_vgrun[i] += macro.VGRUN
	Fabric.w_drainbit0[i] += LVLShifter1.OUT[0]
	Fabric.w_drainbit1[i] += LVLShifter1.OUT[1]
	Fabric.w_drainbit2[i] += LVLShifter1.OUT[2]
	Fabric.w_drainbit3[i] += LVLShifter1.OUT[3]
	Fabric.w_drainbit4[i] += LVLShifter1.OUT[4]
	Fabric.w_drainbit5[i] += LVLShifter1.OUT[5]
	Fabric.w_drainbit6[i] += LVLShifter1.OUT[6]
	Fabric.w_drainbit7[i] += LVLShifter1.OUT[7]
	Fabric.w_drainbit8[i] += LVLShifter1.OUT[8]	
Fabric.w_vtun[0] += chipframe.IO_W_RES[0]
Fabric.s_vinj[0] += chipframe.VINJ_S[0]
Fabric.s_gnd[0] += chipframe.gnd_S[0]
Fabric.s_avdd[0] += chipframe.avdd_S[0]
Fabric.w_drainEN += LVLShifter2.OUT[0:9]

#north non-IO fabric connections 

Fabric.n_gateEN[0] += LVLShifter1.OUT[14]
Fabric.n_gateEN[1] += LVLShifter1.OUT[15]
Fabric.n_gateEN[2] += LVLShifter2.OUT[9]
Fabric.n_gateEN[3] += LVLShifter2.OUT[10]
Fabric.n_gateEN[4] += LVLShifter2.OUT[11]
Fabric.n_gateEN[5] += LVLShifter2.OUT[12]
Fabric.n_gateEN[6] += LVLShifter2.OUT[13]
Fabric.n_gateEN[7] += LVLShifter2.OUT[14]
Fabric.n_gateEN[8] += LVLShifter2.OUT[15]

for i in range(9):
	Fabric.n_gatebit0[i] += LVLShifter1.OUT[9]
	Fabric.n_gatebit1[i] += LVLShifter1.OUT[10]
	Fabric.n_gatebit2[i] += LVLShifter1.OUT[11]
	Fabric.n_gatebit3[i] += LVLShifter1.OUT[12]
	Fabric.n_gatebit4[i] += LVLShifter1.OUT[13]
	Fabric.n_progdrain[i] += LVLShifter3.OUT[13]
	Fabric.n_rundrain[i] += LVLShifter3.OUT[14]
	Fabric.n_prog[i] += DigBuffer.Out[0]
	Fabric.n_run[i] += DigBuffer.Out[1]
	Fabric.n_vgsel[i] += macro.VGPROG

#west and east buffered IO
Fabric.e_s0[0] += AnalogBuffer1.Vin[0]
Fabric.e_s1[0] += AnalogBuffer1.Vin[1]
Fabric.e_s2[0] += AnalogBuffer1.Vin[2]
Fabric.e_s3[0] += AnalogBuffer1.Vin[3]
Fabric.e_s4[0] += AnalogBuffer1.Vin[4]
Fabric.e_s5[0] += AnalogBuffer1.Vin[5]
Fabric.e_s6[0] += AnalogBuffer1.Vin[6]
Fabric.e_s7[0] += AnalogBuffer1.Vin[7]
Fabric.e_s0[1] += AnalogBuffer1.Vin[8]
Fabric.e_s1[1] += AnalogBuffer1.Vin[9]
Fabric.e_s2[1] += AnalogBuffer1.Vin[10]
Fabric.e_s3[1] += AnalogBuffer1.Vin[11]
Fabric.e_s4[1] += AnalogBuffer1.Vin[12]
Fabric.e_s5[1] += AnalogBuffer1.Vin[13]
Fabric.e_s6[1] += AnalogBuffer1.Vin[14]
Fabric.e_s7[1] += AnalogBuffer1.Vin[15]

AnalogBuffer1.Vout[0] += chipframe.IO_W[21]
AnalogBuffer1.Vout[1] += chipframe.IO_W[22]
AnalogBuffer1.Vout[2] += chipframe.IO_W[23]
AnalogBuffer1.Vout[3] += chipframe.IO_W[24]
AnalogBuffer1.Vout[4] += chipframe.IO_W[25]
AnalogBuffer1.Vout[5] += chipframe.IO_W[26]
AnalogBuffer1.Vout[6] += chipframe.IO_W[27]
AnalogBuffer1.Vout[7] += chipframe.IO_W[28]

AnalogBuffer1.Vout[8] += chipframe.IO_E[21]
AnalogBuffer1.Vout[9] += chipframe.IO_E[22]
AnalogBuffer1.Vout[10] += chipframe.IO_E[23]
AnalogBuffer1.Vout[11] += chipframe.IO_E[24]
AnalogBuffer1.Vout[12] += chipframe.IO_E[25]
AnalogBuffer1.Vout[13] += chipframe.IO_E[26]
AnalogBuffer1.Vout[14] += chipframe.IO_E[27]
AnalogBuffer1.Vout[15] += chipframe.IO_E[28]

#west unbuffered IO
Fabric.w_s0[5] += chipframe.IO_W[31]
Fabric.w_s1[5] += chipframe.IO_W[32]
Fabric.w_s2[5] += chipframe.IO_W[33]
Fabric.w_s10[5] += chipframe.IO_W[34]
Fabric.w_s17[5] += chipframe.IO_W[35]
Fabric.w_s19[5] += chipframe.IO_W[36]
Fabric.w_s0[6] += chipframe.IO_W[37]
Fabric.w_s1[6] += chipframe.IO_W[38]
Fabric.w_s4[6] += chipframe.IO_W[39]
Fabric.w_s11[6] += chipframe.IO_W[40]
Fabric.w_s18[6] += chipframe.IO_W[41]
Fabric.w_s19[6] += chipframe.IO_W[42]


#east unbuffered IO
Fabric.e_s0[5] += chipframe.IO_E[31]
Fabric.e_s1[5] += chipframe.IO_E[32]
Fabric.e_s2[5] += chipframe.IO_E[33]
Fabric.e_s10[5] += chipframe.IO_E[34]
Fabric.e_s17[5] += chipframe.IO_E[35]
Fabric.e_s19[5] += chipframe.IO_E[36]
Fabric.e_s0[6] += chipframe.IO_E[37]
Fabric.e_s1[6] += chipframe.IO_E[38]
Fabric.e_s4[6] += chipframe.IO_E[39]
Fabric.e_s11[6] += chipframe.IO_E[40]
Fabric.e_s18[6] += chipframe.IO_E[41]
Fabric.e_s19[6] += chipframe.IO_E[42]

#north unbuffered IO
Fabric.n_s7[8] += chipframe.IO_N[35]
Fabric.n_s6[8] += chipframe.IO_N[34]
Fabric.n_s5[8] += chipframe.IO_N[33]
Fabric.n_s4[8] += chipframe.IO_N[32]
Fabric.n_s3[8] += chipframe.IO_N[31]
Fabric.n_s2[8] += chipframe.IO_N[30]
Fabric.n_s1[8] += chipframe.IO_N[29]
Fabric.n_s0[8] += chipframe.IO_N[28]
Fabric.n_s7[7] += chipframe.IO_N[27]
Fabric.n_s6[7] += chipframe.IO_N[26]
Fabric.n_s5[7] += chipframe.IO_N[25]
Fabric.n_s4[7] += chipframe.IO_N[24]

#south unbuffered IO
Fabric.s_s3[8] += chipframe.IO_S[43]
Fabric.s_s2[8] += chipframe.IO_S[42]
Fabric.s_s1[8] += chipframe.IO_S[41]
Fabric.s_s0[8] += chipframe.IO_S[40]
Fabric.s_s7[7] += chipframe.IO_S[39]
Fabric.s_s6[7] += chipframe.IO_S[38]
Fabric.s_s5[7] += chipframe.IO_S[37]
Fabric.s_s4[7] += chipframe.IO_S[36]
Fabric.s_s3[6] += chipframe.IO_S[35]
Fabric.s_s2[6] += chipframe.IO_S[34]
Fabric.s_s1[6] += chipframe.IO_S[33]
Fabric.s_s0[6] += chipframe.IO_S[32]




# Compilation
#-------------------------------------------------------------------------------
design_limits = [15e6, 15e6]
location_islands = ((250600, 4500000), #macro
(20600, 20000), #frame
(300000,220000), #Fabric
(1600000,4510000), #LVLShifter1
(2200000,4510000), #LVLShifter2
(3400000,4510000), #LVLShifter3
(2800000,4510000), #DigBuffer
(6470000,4000000)) #Analog BUffer
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="FPAA_PDE",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=7,drainSpace =20,gateSpaceIdx=7,gateSpace=15)
