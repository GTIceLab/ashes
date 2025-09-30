import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs
import Wafer5_Synthesis.WaferCommon as wafer

import numpy as np


Top = ac.Circuit()

macro,chipframe,location_macro,location_chipframe = wafer.SmallChip(Top)

# Supporting Circuitry
# ---------------------------------------------------------------------
# Debug Scanner
DebugScannerIsland = ac.Island(Top)
DebugScanner = lib_new.TSMC350nm_VerticalScanner(Top,DebugScannerIsland,dim=(4,1))
DebugScanner.place([0,0])
DebugScannerLocation = (3500e3,350e3)

DebugScanner.VDD += chipframe.DVDD_S[2]
DebugScanner.GND += chipframe.gnd_S[2]
DebugScanner.CLK += macro.mmio_reg_9_bout[13]
DebugScanner.RSTBar += macro.mmio_reg_9_bout[14]
DebugScanner.Din += macro.mmio_reg_9_bout[15]

# Drain Decoder
DrainSelIsland = ac.Island(Top)
DrainDecoder = lib_mux.STD_DrainDecoder(Top,DrainSelIsland,bits=3)
DrainSelect = lib_mux.RunDrainSwitch(Top,DrainSelIsland,num=2)
DrainSwitch = lib_cab.DrainCutoff(Top,DrainSelIsland,num=2)
DrainSelLocation = (5000e3,250e3)
FakeCell1=lib_new.FakeCellGateDecoder(Top,DrainSelIsland)
FakeCell1.place([0,0])

DrainSwitch.VDD += chipframe.VINJ_S[2]
DrainSwitch.GND += chipframe.gnd_S[2]

# Analog Buffers
BufferIsland = ac.Island(Top)
Buffers = lib_dc.TSMC350nm_AnalogBuffer(Top,BufferIsland,dim=(4,1))
Buffers.place([0,0])

GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,BufferIsland,2)
GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,BufferIsland,1)
GateDecoder.IN += macro.mmio_reg_5_vinj[0:2]
GateDecoder.ENABLE += macro.mmio_reg_5_vinj[2]
GateSwitches.RUN += macro.RUN_HV
GateSwitches.PROG += macro.PROG_HV
GateSwitches.GND += chipframe.gnd_S[2]
GateSwitches.VDD += chipframe.VINJ_S[2]
GateSwitches.Vgsel += macro.VGPROG
GateSwitches.RUN_IN += macro.VGRUN[0]


BufferLocation = (3250e3,270e3)

Buffers.VDD_b += chipframe.avdd_S[2]
Buffers.GND_b += chipframe.gnd_S[2]
Buffers.VINJ_b += chipframe.VINJ_S[2]
Buffers.VINJ += GateSwitches.VINJ
Buffers.Vg += GateSwitches.Vg[0]
Buffers.Vsel += GateSwitches.CTRL_B[0]

Buffers.Vd_P += DrainSwitch.PR[4:8]

Buffers.Vout += chipframe.IO_S[14:18] 

# Level Shifters
LVLIsland = ac.Island(Top)
LVLShift = TSMC350nm_LVLShift_x16(Top,LVLIsland)
LVLShift.place([0,0])
LVL_Location = (2750e3,350e3)

LVLShift.DVDD += chipframe.DVDD_S[2]
LVLShift.VINJ += chipframe.VINJ_S[2]
LVLShift.GND += chipframe.gnd_S[2]

for i in range(7):
    LVLShift.Vin[i] += macro.mmio_reg_9_bout[5+i]


# Extra Pins
DebugScanner.Out += Buffers.Vin[0]
DrainDecoder.IN += LVLShift.OUT[0:3]
DrainSelect.prog_drainrail += macro.SystemDrainline[0]
DrainSelect.run_drainrail += macro.SystemDrainline[1]

# Data Converters
#----------------------------------------------------------------------

# QDAC
QDACIsland = ac.Island(Top)
QDAC = lib_dc.QDAC(Top,QDACIsland)
QDAC.place([0,0])
QDAC_location = (300e3, 300e3)

QDAC.AVDD_S += chipframe.avdd_S[0]
QDAC.GND_S += chipframe.gnd_S[0]
QDAC.VINJ_S += chipframe.VINJ_S[0]
QDAC.VTUN += chipframe.IO_E_RES[0]
QDAC.VGRUN += macro.VGRUN
QDAC.VGPROG += macro.VGPROG

QDAC.GateEnable += macro.mmio_reg_5_vinj[6]
QDAC.GateB += macro.mmio_reg_5_vinj[0:2]
QDAC.DrainEnable += macro.mmio_reg_5_vinj[6]
QDAC.DrainB += macro.mmio_reg_5_vinj[2:6]
QDAC.Prog += macro.PROG_HV
QDAC.Run += macro.RUN_HV

QDAC.RST += macro.mmio_reg_10_bout[14]
QDAC.Code += macro.mmio_reg_10_bout[0:5]

QDAC.DEBUG += DebugScanner.In[0:5]
QDAC.Drainline_Prog += DrainSwitch.PR[0]
QDAC.Drainline_Run += DrainSwitch.In[0]

QDAC.Vout += Buffers.Vin[1]


# Ramp ADC
RampADCIsland = ac.Island(Top)
RampADC = lib_dc.RampADC(Top,RampADCIsland)
RampADC.place([0,0])
RampADC_location = (2000e3, 250e3)

RampADC.AVDD_S += chipframe.avdd_S[0]
RampADC.GND_S += chipframe.gnd_S[0]
RampADC.VINJ_S += chipframe.VINJ_S[0]
RampADC.VTUN += chipframe.IO_W_RES[0]
RampADC.VGRUN += macro.VGRUN
RampADC.VGPROG += macro.VGPROG

RampADC.GateEnable += macro.mmio_reg_5_vinj[7]
RampADC.GateB += macro.mmio_reg_5_vinj[0:2]
RampADC.DrainEnable += macro.mmio_reg_5_vinj[7]
RampADC.DrainB += macro.mmio_reg_5_vinj[2:4]
RampADC.Prog += macro.PROG_HV
RampADC.CLK += macro.mmio_reg_9_bout[0]
RampADC.RST += macro.mmio_reg_10_bout[15]
RampADC.Code += macro.mmio_reg_10_bout[5:13]

RampADC.Vin += chipframe.IO_S[12]

RampADC.DEBUG += DebugScanner.In[5:7]
RampADC.Drainline_Prog += DrainSwitch.PR[1]
RampADC.Drainline_Run += DrainSwitch.In[1]

# Algorithcmic ADC
AlgorithmicADCIsland = ac.Island(Top)
AlgorithmicADC = lib_dc.AlgorithmicADC(Top,AlgorithmicADCIsland)
AlgorithmicADC.place([0,0])
AlgorithmicADC_location = (700e3,300e3)

AlgorithmicADC.AVDD_S += chipframe.avdd_S[0]
AlgorithmicADC.GND_S += chipframe.gnd_S[0]
AlgorithmicADC.VINJ_S += chipframe.VINJ_S[0]
AlgorithmicADC.VTUN += chipframe.IO_W_RES[0]
AlgorithmicADC.VGRUN += macro.VGRUN
AlgorithmicADC.VGPROG += macro.VGPROG

AlgorithmicADC.GateEnable += macro.mmio_reg_5_vinj[9]
AlgorithmicADC.GateB += macro.mmio_reg_5_vinj[0:2]
AlgorithmicADC.DrainEnable += macro.mmio_reg_5_vinj[9]
AlgorithmicADC.DrainB += macro.mmio_reg_5_vinj[2:6]
AlgorithmicADC.Prog += macro.PROG_HV
AlgorithmicADC.Run += macro.RUN_HV

AlgorithmicADC.CLK_Sample += macro.mmio_reg_9_bout[1]
AlgorithmicADC.CLK_RST += macro.mmio_reg_9_bout[2]
AlgorithmicADC.CLK_Load += macro.mmio_reg_9_bout[3]
AlgorithmicADC.CLK_Amp += macro.mmio_reg_9_bout[4]

AlgorithmicADC.Vin += chipframe.IO_S[13]
AlgorithmicADC.Code+= macro.mmio_reg_10_bout[13]

AlgorithmicADC.DEBUG += DebugScanner.In[7:10]
AlgorithmicADC.VRES += DebugScanner.In[12]

AlgorithmicADC.Drainline_Prog += DrainSwitch.PR[2]
AlgorithmicADC.Drainline_Run += DrainSwitch.In[2]


# Averager DAC
AveragerDACIsland = ac.Island(Top)
AveragerDAC = lib_dc.AveragerDAC(Top,AveragerDACIsland)
AveragerDAC.place([0,0])
AveragerDAC_location = (1200e3,300e3)

AveragerDAC.AVDD_S += chipframe.avdd_S[0]
AveragerDAC.GND_S += chipframe.gnd_S[0]
AveragerDAC.VINJ_S += chipframe.VINJ_S[0]
AveragerDAC.VTUN += chipframe.IO_W_RES[0]
AveragerDAC.VGRUN += macro.VGRUN
AveragerDAC.VGPROG += macro.VGPROG

AveragerDAC.GateEnable += macro.mmio_reg_5_vinj[7]
AveragerDAC.GateB += macro.mmio_reg_5_vinj[0:2]
AveragerDAC.DrainEnable += macro.mmio_reg_5_vinj[7]
AveragerDAC.DrainB += macro.mmio_reg_5_vinj[2:6]
AveragerDAC.Prog += macro.PROG_HV
AveragerDAC.Run += macro.RUN_HV

AveragerDAC.Code += macro.mmio_reg_10_bout[0:5]

AveragerDAC.Vout += Buffers.Vin[2]

AveragerDAC.DEBUG += DebugScanner.In[10:12]

AveragerDAC.Drainline_Prog += DrainSwitch.PR[3]
AveragerDAC.Drainline_Run += DrainSwitch.In[3]


# Compilation
#-------------------------------------------------------------------------------
design_limits = [7e6, 6.21e6]
location_islands = (location_macro,location_chipframe, DebugScannerLocation,DrainSelLocation,BufferLocation,LVL_Location, QDAC_location, RampADC_location, AlgorithmicADC_location, AveragerDAC_location)

ac.compile_asic(Top,process="TSMC350nm",fileName="CHIP_DataConverter",p_and_r = True,design_limits = design_limits, location_islands = location_islands,gateSpaceIdx=4,gateSpace=15,route=False)
