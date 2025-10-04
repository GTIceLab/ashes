import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs
import Wafer5_Synthesis.WaferCommon as wafer

import numpy as np
import json


Top = ac.Circuit()

macro,chipframe,location_macro,location_chipframe = wafer.SmallChip(Top)

# Supporting Circuitry
# ---------------------------------------------------------------------
# Debug Scanner
DebugScannerIsland = ac.Island(Top)
DebugScanner = lib_new.TSMC350nm_VerticalScanner(Top,DebugScannerIsland,dim=(4,1))
DebugScanner.place([0,0])

DebugScanner.VDD += chipframe.DVDD_S[2]
DebugScanner.GND += chipframe.gnd_S[2]
DebugScanner.CLK += macro.mmio_reg_9_bout[13]
DebugScanner.RSTBar += macro.mmio_reg_9_bout[14]
DebugScanner.Din += macro.mmio_reg_9_bout[15]


DebugScannerLocation = (2000e3,300e3)

# Analog Buffers

BufferIsland = ac.Island(Top)
Buffers,BufGateDecoder,BufGateSwitch,BufDrainDecoder,BufDrainSel,BufDrainSwitch = wafer.AnalogBuffers(Top,BufferIsland,4)

BufGateDecoder.IN += macro.mmio_reg_5_vinj[0:2]
BufGateSwitch.RUN += macro.RUN_HV
BufGateSwitch.PROG += macro.PROG_HV
BufGateSwitch.GND += chipframe.gnd_S[2]
BufGateSwitch.Vgsel += macro.VGPROG
BufGateSwitch.RUN_IN += macro.VGRUN[0]

BufDrainDecoder.IN += macro.mmio_reg_5_vinj[2:4]
BufDrainSwitch.RUN += macro.RUN_HV
BufDrainSwitch.GND += chipframe.gnd_S[2]
BufDrainSwitch.VDD += chipframe.VINJ_S[2]
BufDrainSel.prog_drainrail += macro.SystemDrainline[0]
BufDrainSel.run_drainrail += macro.SystemDrainline[1]

Buffers.VDD_b += chipframe.avdd_S[1]
Buffers.GND_b += chipframe.gnd_S[1]
Buffers.VINJ_b += chipframe.VINJ_S[1]

Buffers.Vout += chipframe.IO_S[14:18] 

BufferLocation = (4500e3,270e3)
# Level Shifters
LVLIsland = ac.Island(Top)
LVLShift = TSMC350nm_LVLShift_x16(Top,LVLIsland)
LVLShift.place([0,0])

LVLShift.DVDD += chipframe.DVDD_S[2]
LVLShift.VINJ += chipframe.VINJ_S[2]
LVLShift.GND += chipframe.gnd_S[2]

for i in range(11):
    LVLShift.Vin[i] += macro.mmio_reg_9_bout[i]

LVL_Location = (3800e3,350e3)

# Extra Pins
DebugScanner.Out += Buffers.Vin[0]

BufGateDecoder.ENABLE += LVLShift.OUT[0]
BufDrainDecoder.ENABLE += LVLShift.OUT[0]


# Data Converters
#----------------------------------------------------------------------

# QDAC
QDACIsland = ac.Island(Top)
QDAC = lib_dc.QDAC(Top,QDACIsland)
QDAC.place([0,0])
QDAC_location = (650e3, 275e3)

QDAC.AVDD_S += chipframe.avdd_S[0]
QDAC.GND_S += chipframe.gnd_S[0]
QDAC.VINJ_S += chipframe.VINJ_S[0]
QDAC.VTUN += chipframe.IO_E_RES[0]
QDAC.VGRUN += macro.VGRUN
QDAC.VGPROG += macro.VGPROG

QDAC.GateEnable += LVLShift.OUT[1]
QDAC.GateB += LVLShift.OUT[5:7]
QDAC.DrainEnable += LVLShift.OUT[1]
QDAC.DrainB += LVLShift.OUT[7:11]
QDAC.Prog += macro.PROG_HV
QDAC.Run += macro.RUN_HV

QDAC.RST += macro.mmio_reg_10_bout[0]
QDAC.Code += macro.mmio_reg_10_bout[1:6]

QDAC.DEBUG += DebugScanner.In[0:5]
QDAC.Drainline_Prog += macro.SystemDrainline[0]
QDAC.Drainline_Run += macro.SystemDrainline[1]

QDAC.Vout += Buffers.Vin[1]


# Ramp ADC
RampADCIsland = ac.Island(Top)
RampADC = lib_dc.RampADC(Top,RampADCIsland)
RampADC.place([0,0])
RampADC_location = (250e3, 350e3)

RampADC.AVDD_S += chipframe.avdd_S[0]
RampADC.GND_S += chipframe.gnd_S[0]
RampADC.VINJ_S += chipframe.VINJ_S[0]
RampADC.VTUN += chipframe.IO_W_RES[0]
RampADC.VGRUN += macro.VGRUN
RampADC.VGPROG += macro.VGPROG

RampADC.GateEnable += LVLShift.OUT[2]
RampADC.GateB += LVLShift.OUT[5:7]
RampADC.DrainEnable += LVLShift.OUT[2]
RampADC.DrainB += LVLShift.OUT[7:9]
RampADC.Prog += macro.PROG_HV
RampADC.Run += macro.RUN_HV

RampADC.CLK += macro.mmio_reg_10_bout[10]
RampADC.RST += macro.mmio_reg_10_bout[11]
RampADC.Code += macro.mmio_reg_in_5[2:10]

RampADC.Vin += chipframe.IO_S[12]

RampADC.DEBUG += DebugScanner.In[5:7]
RampADC.Drainline_Prog += macro.SystemDrainline[0]
RampADC.Drainline_Run += macro.SystemDrainline[1]

# Algorithcmic ADC
AlgorithmicADCIsland = ac.Island(Top)
AlgorithmicADC = lib_dc.AlgorithmicADC(Top,AlgorithmicADCIsland)
AlgorithmicADC.place([0,0])
AlgorithmicADC_location = (1250e3,275e3)

AlgorithmicADC.AVDD_S += chipframe.avdd_S[0]
AlgorithmicADC.GND_S += chipframe.gnd_S[0]
AlgorithmicADC.VINJ_S += chipframe.VINJ_S[0]
AlgorithmicADC.VTUN += chipframe.IO_W_RES[0]
AlgorithmicADC.VGRUN += macro.VGRUN
AlgorithmicADC.VGPROG += macro.VGPROG

AlgorithmicADC.GateEnable += LVLShift.OUT[4]
AlgorithmicADC.GateB += LVLShift.OUT[5:7]
AlgorithmicADC.DrainEnable += LVLShift.OUT[4]
AlgorithmicADC.DrainB += LVLShift.OUT[7:11]
AlgorithmicADC.Prog += macro.PROG_HV
AlgorithmicADC.Run += macro.RUN_HV

AlgorithmicADC.CLK_Sample += macro.mmio_reg_10_bout[6]
AlgorithmicADC.CLK_RST += macro.mmio_reg_10_bout[7]
AlgorithmicADC.CLK_Load += macro.mmio_reg_10_bout[8]
AlgorithmicADC.CLK_Amp += macro.mmio_reg_10_bout[9]

AlgorithmicADC.Vin += chipframe.IO_S[13]
AlgorithmicADC.Code+= macro.mmio_reg_in_5[10]

AlgorithmicADC.DEBUG += DebugScanner.In[7:10]
AlgorithmicADC.VRES += DebugScanner.In[12]

AlgorithmicADC.Drainline_Prog += macro.SystemDrainline[0]
AlgorithmicADC.Drainline_Run += macro.SystemDrainline[1]


# Averager DAC
AveragerDACIsland = ac.Island(Top)
AveragerDAC = lib_dc.AveragerDAC(Top,AveragerDACIsland)
AveragerDAC.place([0,0])
AveragerDAC_location = (960e3,275e3)

AveragerDAC.AVDD_S += chipframe.avdd_S[0]
AveragerDAC.GND_S += chipframe.gnd_S[0]
AveragerDAC.VINJ_S += chipframe.VINJ_S[0]
AveragerDAC.VTUN += chipframe.IO_W_RES[0]
AveragerDAC.VGRUN += macro.VGRUN
AveragerDAC.VGPROG += macro.VGPROG

AveragerDAC.GateEnable += LVLShift.OUT[3]
AveragerDAC.GateB += LVLShift.OUT[5:7]
AveragerDAC.DrainEnable += LVLShift.OUT[3]
AveragerDAC.DrainB += LVLShift.OUT[7:11]
AveragerDAC.Prog += macro.PROG_HV
AveragerDAC.Run += macro.RUN_HV

AveragerDAC.Code += macro.mmio_reg_10_bout[1:6]

AveragerDAC.Vout += Buffers.Vin[2]

AveragerDAC.DEBUG += DebugScanner.In[10:12]

AveragerDAC.Drainline_Prog += macro.SystemDrainline[0]
AveragerDAC.Drainline_Run += macro.SystemDrainline[1]


# Compilation
#-------------------------------------------------------------------------------
#design_limits = [7e6, 6.21e6]
design_limits = [7e6,7e6]
location_islands = (location_macro,location_chipframe, DebugScannerLocation,BufferLocation,LVL_Location, QDAC_location, RampADC_location, AlgorithmicADC_location, AveragerDAC_location)


with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 100
qparams["via"] = 25
qparams["conflict"] = 40
qparams["stage2"] = "mask none force effort 500"
qparams["stage3"] = "mask none force effort 500"

ac.compile_asic(Top,process="TSMC350nm",fileName="CHIP_DataConverter",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=3,drainSpace=15,gateSpaceIdx=3,gateSpace=15,route=True,qparams=qparams)
