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
Fabric1 = optimized_cab1(Top,FabricIsland,[7,1])
Fabric1.place([0,0])

Fabric2 = optimized_cab2(Top,FabricIsland,[7,6])
Fabric2.place([0,1])

#LVL shifter
LVLShifter1Island = Island(Top)
LVLShifter1 = TSMC350nm_LVLShift_x16(Top,LVLShifter1Island,[1,1])
LVLShifter1.place([0,0])

LVLShifter1.DVDD += chipframe.DVDD_W
LVLShifter1.GND += chipframe.gnd_W[2]
LVLShifter1.VINJ += chipframe.VINJ_W
for i in range(2,15):
	LVLShifter1.Vin[i-2] += macro.mmio_reg_7_bout[i]


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
LVLShifter3.Vin += macro.mmio_reg_9_bout[0:16]


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
AnalogBuffer1 = [0]*16
for i in range(16):
	AnalogBuffer1[i] = "AnalogBuffer1_"+str(i)
for i in range(16):
	AnalogBuffer1[i] = AnalogBuffer(Top,AnalogBuffer1Island,[1,1])
	AnalogBuffer1[i].place([i,0])
	AnalogBuffer1[i].markAbut()

DrainDecoder_buf = STD_DrainDecoder(Top,AnalogBuffer1Island,bits=4)
DrainSelect_buf = RunDrainSwitch(Top,AnalogBuffer1Island,num=4)
DrainSwitch_buf = DrainCutoff(Top,AnalogBuffer1Island,num=4)    

GateSwitch_buf = STD_IndirectGateSwitch(Top,AnalogBuffer1Island,1)

AnalogBuffer1[0].VTUN += GateSwitch_buf.VTUN
AnalogBuffer1[0].VDD += GateSwitch_buf.VDD[0]
GateSwitch_buf.VPWR[0] += chipframe.avdd_E
GateSwitch_buf.VPWR[1] += chipframe. avdd_E
AnalogBuffer1[0].GND += GateSwitch_buf.GND[0]
AnalogBuffer1[0].VINJ += GateSwitch_buf.VINJ
AnalogBuffer1[0].Vg += GateSwitch_buf.Vg[0]
AnalogBuffer1[0].Vsel += GateSwitch_buf.CTRL_B[0]
for i in range(16):
	AnalogBuffer1[i].Vd_P += DrainSwitch_buf.PR[i]

GateSwitch_buf.VTUN_T += chipframe.IO_E_RES[0]
GateSwitch_buf.Vgsel += macro.VGPROG
GateSwitch_buf.PROG += DigBuffer.Out[0]
GateSwitch_buf.RUN += DigBuffer.Out[1]
GateSwitch_buf.VINJ_T += chipframe.VINJ_E
GateSwitch_buf.GND_T += chipframe.gnd_E[2]
GateSwitch_buf.RUN_IN[0] += macro.VGRUN
GateSwitch_buf.RUN_IN[1] += macro.VGRUN
GateSwitch_buf.decode[0] += LVLShifter3.OUT[6]

DrainSwitch_buf.VDD += chipframe.VINJ_E
DrainSwitch_buf.GND += chipframe.gnd_E[2]
DrainSwitch_buf.RUN += DigBuffer.Out[1]

DrainSelect_buf.VINJ += chipframe.VINJ_E
DrainSelect_buf.GND += chipframe.gnd_E[2]
DrainSelect_buf.prog_drainrail += macro.SystemDrainline[0]
DrainSelect_buf.run_drainrail += macro.SystemDrainline[1]

#DrainDecoder_buf1.VINJ += chipframe.VINJ_W
#DrainDecoder_buf1.GND += chipframe.gnd_N[8]
DrainDecoder_buf.ENABLE += LVLShifter3.OUT[7]
DrainDecoder_buf.IN += LVLShifter3.OUT[8:12]

#west and east non-IO Fabric Connections
for i in range(7):
	Fabric2.e_vgrun[i] += macro.VGRUN
	Fabric1.w_drainbit0[i] += LVLShifter1.OUT[0]
	Fabric1.w_drainbit1[i] += LVLShifter1.OUT[1]
	Fabric1.w_drainbit2[i] += LVLShifter1.OUT[2]
	Fabric1.w_drainbit3[i] += LVLShifter1.OUT[3]
	Fabric1.w_drainbit4[i] += LVLShifter1.OUT[4]
	Fabric1.w_drainbit5[i] += LVLShifter1.OUT[5]
	Fabric1.w_drainbit6[i] += LVLShifter1.OUT[6]
	Fabric1.w_drainbit7[i] += LVLShifter1.OUT[7]
	Fabric1.w_drainbit8[i] += LVLShifter1.OUT[8]
	Fabric1.w_drainbit9[i] += LVLShifter1.OUT[9]
	Fabric1.w_drainbit10[i] += LVLShifter1.OUT[10]	
Fabric1.w_vtun[0] += chipframe.IO_W_RES[0]
Fabric1.s_vinj += chipframe.VINJ_S[0]
Fabric1.s_gnd += chipframe.gnd_S[0]
Fabric1.s_avdd += chipframe.avdd_S[0]
Fabric1.w_drainEN += LVLShifter2.OUT[0:7]

#north non-IO fabric connections 
Fabric1.n_gateEN += LVLShifter2.OUT[7]
Fabric2.n_gateEN += LVLShifter2.OUT[8:14]

Fabric1.n_gatebit0 += LVLShifter3.OUT[0]
Fabric1.n_gatebit1 += LVLShifter3.OUT[1]
Fabric1.n_gatebit2 += LVLShifter3.OUT[2]
Fabric1.n_gatebit3 += LVLShifter3.OUT[3]
Fabric1.n_gatebit4 += LVLShifter3.OUT[4]
Fabric1.n_gatebit5 += LVLShifter3.OUT[5]
Fabric1.n_progdrain += macro.SystemDrainline[0]
Fabric1.n_rundrain += macro.SystemDrainline[1]
Fabric1.n_prog += DigBuffer.Out[0]
Fabric1.n_run += DigBuffer.Out[1]
Fabric1.n_vgsel += macro.VGPROG
for i in range(6):
	Fabric2.n_gatebit0[i] += LVLShifter3.OUT[0]
	Fabric2.n_gatebit1[i] += LVLShifter3.OUT[1]
	Fabric2.n_gatebit2[i] += LVLShifter3.OUT[2]
	Fabric2.n_gatebit3[i] += LVLShifter3.OUT[3]
	Fabric2.n_gatebit4[i] += LVLShifter3.OUT[4]
	Fabric2.n_gatebit5[i] += LVLShifter3.OUT[5]
	Fabric2.n_progdrain[i] += macro.SystemDrainline[0]
	Fabric2.n_rundrain[i] += macro.SystemDrainline[1]
	Fabric2.n_prog[i] += DigBuffer.Out[0]
	Fabric2.n_run[i] += DigBuffer.Out[1]
	Fabric2.n_vgsel[i] += macro.VGPROG
	
macro.Signal_RampADC_inp[5] += Fabric2.n_s19[4]
macro.Signal_RampADC_inp[4] += Fabric2.n_s18[4]
macro.Signal_RampADC_inp[3] += Fabric2.n_s17[4]
macro.Signal_RampADC_inp[2] += Fabric2.n_s16[4]
macro.Signal_RampADC_inp[1] += Fabric2.n_s15[4]
macro.Signal_RampADC_inp[0] += Fabric2.n_s14[4]
macro.Signal_DAC_out[2] += Fabric2.n_s13[4]
macro.Signal_DAC_out[1] += Fabric2.n_s12[4]
macro.Signal_DAC_out[0] += Fabric2.n_s11[4]

#west and east buffered IO
Fabric2.e_s0[0] += AnalogBuffer1[0].Vin
Fabric2.e_s1[0] += AnalogBuffer1[1].Vin
Fabric2.e_s2[0] += AnalogBuffer1[2].Vin
Fabric2.e_s3[0] += AnalogBuffer1[3].Vin
Fabric2.e_s4[0] += AnalogBuffer1[4].Vin
Fabric2.e_s5[0] += AnalogBuffer1[5].Vin
Fabric2.e_s6[0] += AnalogBuffer1[6].Vin
Fabric2.e_s7[0] += AnalogBuffer1[7].Vin
Fabric2.e_s8[0] += AnalogBuffer1[8].Vin
Fabric2.e_s9[0] += AnalogBuffer1[9].Vin
Fabric2.e_s10[0] += AnalogBuffer1[10].Vin
Fabric2.e_s11[0] += AnalogBuffer1[11].Vin
Fabric2.e_s12[0] += AnalogBuffer1[12].Vin
Fabric2.e_s13[0] += AnalogBuffer1[13].Vin
Fabric2.e_s14[0] += AnalogBuffer1[14].Vin
Fabric2.e_s15[0] += AnalogBuffer1[15].Vin

AnalogBuffer1[0].Vout += chipframe.IO_E[13]
AnalogBuffer1[1].Vout += chipframe.IO_E[14]
AnalogBuffer1[2].Vout += chipframe.IO_E[15]
AnalogBuffer1[3].Vout += chipframe.IO_E[16]
AnalogBuffer1[4].Vout += chipframe.IO_E[17]
AnalogBuffer1[5].Vout += chipframe.IO_E[18]
AnalogBuffer1[6].Vout += chipframe.IO_E[19]
AnalogBuffer1[7].Vout += chipframe.IO_E[20]

AnalogBuffer1[8].Vout += chipframe.IO_E[21]
AnalogBuffer1[9].Vout += chipframe.IO_E[22]
AnalogBuffer1[10].Vout += chipframe.IO_E[23]
AnalogBuffer1[11].Vout += chipframe.IO_E[24]
AnalogBuffer1[12].Vout += chipframe.IO_E[25]
AnalogBuffer1[13].Vout += chipframe.IO_E[26]
AnalogBuffer1[14].Vout += chipframe.IO_E[27]
AnalogBuffer1[15].Vout += chipframe.IO_E[28]

#east unbuffered IO
Fabric2.e_s0[5] += chipframe.IO_E[31]
Fabric2.e_s1[5] += chipframe.IO_E[32]
Fabric2.e_s2[5] += chipframe.IO_E[33]
Fabric2.e_s8[5] += chipframe.IO_E[34]
Fabric2.e_s15[5] += chipframe.IO_E[35]
Fabric2.e_s19[5] += chipframe.IO_E[36]
Fabric2.e_s0[6] += chipframe.IO_E[37]
Fabric2.e_s1[6] += chipframe.IO_E[38]
Fabric2.e_s2[6] += chipframe.IO_E[39]
Fabric2.e_s9[6] += chipframe.IO_E[40]
Fabric2.e_s17[6] += chipframe.IO_E[41]
Fabric2.e_s19[6] += chipframe.IO_E[42]


#west unbuffered IO
Fabric1.w_s0[5] += chipframe.IO_W[31]
Fabric1.w_s1[5] += chipframe.IO_W[32]
Fabric1.w_s2[5] += chipframe.IO_W[33]
Fabric1.w_s8[5] += chipframe.IO_W[34]
Fabric1.w_s15[5] += chipframe.IO_W[35]
Fabric1.w_s19[5] += chipframe.IO_W[36]
Fabric1.w_s0[6] += chipframe.IO_W[37]
Fabric1.w_s1[6] += chipframe.IO_W[38]
Fabric1.w_s2[6] += chipframe.IO_W[39]
Fabric1.w_s9[6] += chipframe.IO_W[40]
Fabric1.w_s17[6] += chipframe.IO_W[41]
Fabric1.w_s19[6] += chipframe.IO_W[42]

#north unbuffered IO
Fabric2.n_s19[5] += chipframe.IO_N[35]
Fabric2.n_s18[5] += chipframe.IO_N[34]
Fabric2.n_s17[5] += chipframe.IO_N[33]
Fabric2.n_s16[5] += chipframe.IO_N[32]
Fabric2.n_s15[5] += chipframe.IO_N[31]
Fabric2.n_s14[5] += chipframe.IO_N[30]
Fabric2.n_s13[5] += chipframe.IO_N[29]
Fabric2.n_s12[5] += chipframe.IO_N[28]
Fabric2.n_s11[5] += chipframe.IO_N[27]
Fabric2.n_s10[5] += chipframe.IO_N[26]
Fabric2.n_s9[5] += chipframe.IO_N[25]
Fabric2.n_s8[5] += chipframe.IO_N[24]

#south unbuffered IO
Fabric2.s_s3[5] += chipframe.IO_S[43]
Fabric2.s_s2[5] += chipframe.IO_S[42]
Fabric2.s_s1[5] += chipframe.IO_S[41]
Fabric2.s_s0[5] += chipframe.IO_S[40]
Fabric2.s_s19[4] += chipframe.IO_S[39]
Fabric2.s_s18[4] += chipframe.IO_S[38]
Fabric2.s_s17[4] += chipframe.IO_S[37]
Fabric2.s_s12[4] += chipframe.IO_S[36]
Fabric2.s_s5[4] += chipframe.IO_S[35]
Fabric2.s_s4[4] += chipframe.IO_S[34]
Fabric2.s_s3[4] += chipframe.IO_S[33]
Fabric2.s_s2[4] += chipframe.IO_S[32]

#Padframe buffer connections
for i in range(6):
	chipframe.buf_vdd_N[i] += chipframe.DVDD_N[2]
for i in range(11):
	chipframe.buf_vdd_W[i] += chipframe.DVDD_W
chipframe.buf_vdd_E += chipframe.DVDD_E




# Compilation
#-------------------------------------------------------------------------------
design_limits = [15e6, 15e6]
location_islands = ((250600, 4520000), #macro
(20600, 20000), #frame
(400000,210000), #Fabric
(400000,4550000), #LVLShifter1
(3300000,4540000), #LVLShifter2
(4100000,4540000), #LVLShifter3
(1500000,4540000), #DigBuffer
(6550000,4000000)) #Analog BUffer
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="FPAA_Optimized",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=7,drainSpace =20,gateSpaceIdx=7,gateSpace=15)
