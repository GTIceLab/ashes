import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
import ashes_fg.class_lib_beamform as lib_dc

import json

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
#FabricIsland = Island(Top)
#Fabric = TILE_analog(Top,FabricIsland,[7,7])
#Fabric.place([0,0])

#LVL shifter
#LVLShifter1Island = Island(Top)
#LVLShifter1 = TSMC350nm_LVLShift_x16(Top,LVLShifter1Island,[1,1])
#LVLShifter1.place([0,0])

#LVLShifter1.DVDD += chipframe.DVDD_W
#LVLShifter1.GND += chipframe.gnd_W[2]
#LVLShifter1.VINJ += chipframe.VINJ_W
#for i in range(2,15):
	##LVLShifter1.Vin[i-2] += macro.mmio_reg_7_bout[i]


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
AnalogBuffer1 = [0]*3
for i in range(3):
	AnalogBuffer1[i] = "AnalogBuffer1_"+str(i)
for i in range(3):
	AnalogBuffer1[i] = AnalogBuffer(Top,AnalogBuffer1Island,[1,1])
	AnalogBuffer1[i].place([i,0])
	AnalogBuffer1[i].markAbut()

DrainDecoder_buf = STD_DrainDecoder(Top,AnalogBuffer1Island,bits=2)
DrainSelect_buf = RunDrainSwitch(Top,AnalogBuffer1Island,num=1)
DrainSwitch_buf = DrainCutoff(Top,AnalogBuffer1Island,num=1)    

GateSwitch_buf = STD_IndirectGateSwitch(Top,AnalogBuffer1Island,1)

AnalogBuffer1[0].VTUN += GateSwitch_buf.VTUN
AnalogBuffer1[0].VDD += GateSwitch_buf.VDD[0]
GateSwitch_buf.VPWR[0] += chipframe.avdd_E
GateSwitch_buf.VPWR[1] += chipframe. avdd_E
AnalogBuffer1[0].GND += GateSwitch_buf.GND[0]
AnalogBuffer1[0].VINJ += GateSwitch_buf.VINJ
AnalogBuffer1[0].Vg += GateSwitch_buf.Vg[0]
AnalogBuffer1[0].Vsel += GateSwitch_buf.CTRL_B[0]
for i in range(3):
	AnalogBuffer1[i].Vd_P += DrainSwitch_buf.PR[i]

GateSwitch_buf.VTUN_T += chipframe.IO_E_RES[0]
GateSwitch_buf.Vgsel += macro.VGPROG
GateSwitch_buf.PROG += DigBuffer.Out[0]
GateSwitch_buf.RUN += DigBuffer.Out[1]
GateSwitch_buf.VINJ_T += chipframe.VINJ_E
GateSwitch_buf.GND_T += chipframe.gnd_E[2]
GateSwitch_buf.RUN_IN[0] += macro.VGRUN
GateSwitch_buf.RUN_IN[1] += macro.VGRUN
GateSwitch_buf.decode[0] += LVLShifter3.OUT[15]

DrainSwitch_buf.VDD += chipframe.VINJ_E
DrainSwitch_buf.GND += chipframe.gnd_E[2]
DrainSwitch_buf.RUN += DigBuffer.Out[1]

DrainSelect_buf.VINJ += chipframe.VINJ_E
DrainSelect_buf.GND += chipframe.gnd_E[2]
DrainSelect_buf.prog_drainrail += macro.SystemDrainline[0]
DrainSelect_buf.run_drainrail += macro.SystemDrainline[1]

#DrainDecoder_buf1.VINJ += chipframe.VINJ_W
#DrainDecoder_buf1.GND += chipframe.gnd_N[8]
DrainDecoder_buf.ENABLE += LVLShifter3.OUT[14]
DrainDecoder_buf.IN += LVLShifter3.OUT[12:14]

RingOscIsland = Island(Top)
RingOsc = TSMC350nm_CS_RingOsc(Top,RingOscIsland,[1,1])
RingOsc.place([0,0])

RingOsc.Vd_P += DrainSwitch_buf.PR[3]
AnalogBuffer1[2].VDD_b += RingOsc.AVDD
AnalogBuffer1[2].GND_b += RingOsc.GND
AnalogBuffer1[2].VINJ_b += RingOsc.VINJ
AnalogBuffer1[2].VTUN_b += RingOsc.VTUN
AnalogBuffer1[2].Vsel_b += RingOsc.Vsel
AnalogBuffer1[2].Vg_b  += RingOsc.Vg

#GateDecoder_RO.VTUN += VMMWTA.n_VTUN

#RingOscConnIsland = Island(Top)
RingOscConn = RingOscDiffGen(Top,RingOscIsland,[1,1])
RingOscConn.place([0,1])

#Delay lines

DelaylinesIsland = Island(Top)

Delaylines = DelayLinesAlgFlip(Top,DelaylinesIsland,[1,1])

Delaylines.place([0,0])



#VMMWTAA

VMMWTAIsland = Island(Top)

VMMWTA = VMMWTAAlgFullRoute(Top,VMMWTAIsland,[1,1])

VMMWTA.place([0,0])

#VMMDemodulation

ModulationIsland = Island(Top)

Modulation = ModulationAlgFlip(Top,ModulationIsland,[1,1])

Modulation.place([0,0])

#Ring Oscillator + Switching circuitry

RingOsc.AVDD += VMMWTA.n_AVDD
RingOsc.GND += Modulation.n_gnd
RingOsc.VINJ += Modulation.n_vinj

RingOscConn.CLKP += Modulation.e_VG_P
RingOscConn.CLKN += Modulation.e_VG_N
RingOsc.OUT += RingOscConn.CLK[0]
chipframe.IO_W[20] += RingOscConn.CLK[1]
RingOscConn.SelCLK += chipframe.IO_W[21]
RingOscConn.VDD += Modulation.n_AVDD
RingOscConn.GND += Modulation.n_gnd

RingOsc.VTUN += VMMWTA.n_VTUN

#WTA nFET Connections
Term = Island(Top)
nFET_Mod = TSMC350nm_Termination_bot(Top,Term,[1,1])
nFET_Mod.place([0,0])

nFET_Mod.IOUT += Modulation.e_VC
nFET_Mod.GND += Modulation.n_gnd
nFET_Mod.GATE += chipframe.IO_W[19]


Term2 = Island(Top)
nFET_WTA = TSMC350nm_Termination_bot(Top,Term2,[1,1])
nFET_WTA.place([0,0])

nFET_WTA.IOUT += VMMWTA.Vbias
nFET_WTA.GND += VMMWTA.n_gnd
nFET_WTA.GATE += chipframe.IO_S[22]


#Between Algorithm Connections
#--------------------------------------------------------------------------------

Delaylines.n_OUTS += Modulation.RUNO

Modulation.VOUT += VMMWTA.RUNO

VMMWTA.Vsel_WTA += Delaylines.e_WTA_CTRL_B[0]
VMMWTA.Vg_WTA += Delaylines.e_WTA_Vg[0]

VMMWTA.n_AVDD += VMMWTA.Vs_WTA

# Power/GND Connections
#--------------------------------------------------------------------------------
Modulation.n_AVDD += chipframe.avdd_S[2]
Modulation.n_gnd += chipframe.gnd_S[2]
Modulation.n_vinj += chipframe.VINJ_S[2]

VMMWTA.n_AVDD += chipframe.avdd_S[0]
VMMWTA.n_gnd += chipframe.gnd_S[0]
VMMWTA.n_vinj += chipframe.VINJ_S[0]

Delaylines.n_AVDD += chipframe.avdd_S[1]
Delaylines.n_gnd += chipframe.gnd_S[1]
Delaylines.n_vinj += chipframe.VINJ_S[1]

# Macro Connections
#--------------------------------------------------------------------------------
Modulation.n_VTUN += chipframe.IO_W_RES[0]
Modulation.n_VGPROG += macro.VGPROG
Modulation.n_Prog += DigBuffer.Out[0]
Modulation.n_Run += DigBuffer.Out[1]
Modulation.w_Drainline_Prog += macro.SystemDrainline[0]
Modulation.w_Drainline_Run += macro.SystemDrainline[1]

VMMWTA.n_VTUN += chipframe.IO_W_RES[0]
VMMWTA.n_VGPROG += macro.VGPROG
VMMWTA.n_Prog += DigBuffer.Out[0]
VMMWTA.n_Run += DigBuffer.Out[1]
VMMWTA.w_Drainline_Prog += macro.SystemDrainline[0]
VMMWTA.w_Drainline_Run += macro.SystemDrainline[1]
VMMWTA.Prog_WTA += DigBuffer.Out[0]

Delaylines.n_VTUN += chipframe.IO_W_RES[0]
Delaylines.n_VGPROG += macro.VGPROG
Delaylines.n_Prog += DigBuffer.Out[0]
Delaylines.n_Run += DigBuffer.Out[1]
Delaylines.w_Drainline_Prog += macro.SystemDrainline[0]
Delaylines.w_Drainline_Run += macro.SystemDrainline[1]

# To Pads
#--------------------------------------------------------------------------------
Delaylines.w_Input[0:19] += chipframe.IO_E[0:20]
#Delaylines.w_Input[0:19] += chipframe.IO_E[22:42]
Delaylines.w_Input[20:39] += chipframe.IO_S[25:45]

VMMWTA.e_Out += AnalogBuffer1[0].Vin
AnalogBuffer1[0].Vout += chipframe.IO_W[22]

Delaylines.e_WTA_out += AnalogBuffer1[1].Vin
AnalogBuffer1[1].Vout += chipframe.IO_W[23]

Delaylines.e_CLK += chipframe.IO_S[24]
Delaylines.e_RSTBar += chipframe.IO_S[23]
Delaylines.e_Din += chipframe.IO_S[22]

VMMWTA.e_CLK += chipframe.IO_S[21]
VMMWTA.e_RSTBar += chipframe.IO_S[20]
VMMWTA.e_Din += chipframe.IO_S[19]

VMMWTA.Vmid += AnalogBuffer1[2].Vin
AnalogBuffer1[2].Vout += chipframe.IO_W[24]

# Drain Bit Handling 
#-------------------------------------------------------------------------------
Modulation.w_DrainB += LVLShifter2.OUT[0:9]
Delaylines.w_DrainB += LVLShifter2.OUT[0:8]
VMMWTA.w_DrainB += LVLShifter2.OUT[0:8]

# Drain Enable Handling
#-------------------------------------------------------------------------------
Modulation.w_DrainEnable_Mod += LVLShifter2.OUT[15]
Delaylines.w_DrainEnable_Del += LVLShifter2.OUT[14]
VMMWTA.w_DrainEnable_WTA += LVLShifter2.OUT[13]

# Gate Bit Handling
#-------------------------------------------------------------------------------

Modulation.n_GateB += LVLShifter3.OUT[0:9]
Delaylines.n_GateB += LVLShifter3.OUT[0:5]
VMMWTA.n_GateB += LVLShifter3.OUT[0:9]

# Gate Enable Handling
#-------------------------------------------------------------------------------
Modulation.n_GateEnable_Mod += LVLShifter2.OUT[12]
Delaylines.n_GateEnable_Del += LVLShifter2.OUT[11]
VMMWTA.n_GateEnable_WTA += LVLShifter2.OUT[10]

#Padframe buffer connections
for i in range(6):
	chipframe.buf_vdd_N[i] += chipframe.DVDD_N[2]
for i in range(11):
	chipframe.buf_vdd_W[i] += chipframe.DVDD_W
chipframe.buf_vdd_E += chipframe.DVDD_E
# Compilation

#-------------------------------------------------------------------------------



with open('./ashes_fg/asic/qrouter_default.json') as file:

    qparams = json.load(file)



qparams["passes"] = 50

qparams["via"] = 10

qparams["jog"] = 35

qparams["conflict"] = 40

qparams["stage1"] = "mask auto force"

qparams["stage2"] = "mask bbox force effort 500"

qparams["stage3"] = "mask bbox force effort 500"



design_limits = [12e6, 12e6]


'''(250600, 4500000), (20600, 20000),'''


location_islands = ((250600, 4500000), (20600, 20000),
(3300000,4510000), #LVLShifter2
(4100000,4510000), #LVLShifter3
(1500000,4510000), #DigBuffer
(320000,2360000), #Analog BUffer
(392000, 2300000), #Ring Osc
(4850000,650000), #Delay Lines
(270000,350000), #VMMWTA
(700000,2600000), #VMMDemod
(550000, 2780000), #nFET Termination for Modulation
(4870000, 2070000)) #nFET Termination for VMMWTA
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))

# location_islands = None



compile_asic(Top,process="TSMC350nm",fileName="test_prerana",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=5,drainSpace =30,gateSpaceIdx=5,gateSpace=20)