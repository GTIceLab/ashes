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
# Analog Buffers

BufferIsland = ac.Island(Top)
Buffers,BufGateDecoder,BufGateSwitch,BufDrainDecoder,BufDrainSel,BufDrainSwitch = wafer.AnalogBuffers(Top,BufferIsland,7)

BufGateSwitch.RUN += macro.RUN_HV
BufGateSwitch.PROG += macro.PROG_HV
BufGateSwitch.GND += chipframe.gnd_S[2]
BufGateSwitch.Vgsel += macro.VGPROG
BufGateSwitch.RUN_IN += macro.VGRUN[0]

BufDrainSwitch.RUN += macro.RUN_HV
BufDrainSwitch.GND += chipframe.gnd_S[2]
BufDrainSwitch.VDD += chipframe.VINJ_S[2]
BufDrainSel.prog_drainrail += macro.SystemDrainline[0]
BufDrainSel.run_drainrail += macro.SystemDrainline[1]

Buffers.VDD_b += chipframe.avdd_S[1]
Buffers.GND_b += chipframe.gnd_S[1]
Buffers.VINJ_b += chipframe.VINJ_S[1]
Buffers.VTUN += chipframe.IO_W_RES[0]

# print(f"Number of outputs {len(Buffers.Vout)} \n Number of io pads {len(chipframe.IO_S[12:19])}")

Buffers.Vout += chipframe.IO_S[12:19] 


BufferLocation = (4500e3,230e3)

# Level Shifters
LVLIsland = ac.Island(Top)
LVLShift = lib_new.TSMC350nm_LVLShift_x16(Top,LVLIsland)
LVLShift.place([0,0])

LVLShift.DVDD += chipframe.DVDD_S[2]
LVLShift.VINJ += chipframe.VINJ_S[2]
LVLShift.GND += chipframe.gnd_S[2]

for i in range(11):
    LVLShift.Vin[i] += macro.mmio_reg_9_bout[i]

LVL_Location = (3800e3,350e3)

BufGateDecoder.ENABLE += LVLShift.OUT[0]
BufDrainDecoder.ENABLE += LVLShift.OUT[0]

BufGateDecoder.IN += LVLShift.OUT[3:5]

BufDrainDecoder.IN += LVLShift.OUT[5:8]


# Filters
#----------------------------------------------------------------------

# LPF Delay Block
LPFDelayIsland = ac.Island(Top)
LPFDelay = lib_new.Top_DelayLPF(Top,LPFDelayIsland)
LPFDelay.place([0,0])
LPFDelay_location = (400e3, 320e3)

LPFDelay.AVDD += chipframe.avdd_S[0]
LPFDelay.GND_S += chipframe.gnd_S[0]
LPFDelay.VINJ_S += chipframe.VINJ_S[0]
LPFDelay.VTUN += chipframe.IO_W_RES[0]
LPFDelay.VGRUN += macro.VGRUN
LPFDelay.VGPROG += macro.VGPROG

LPFDelay.GateEnable += LVLShift.OUT[1]
LPFDelay.GateB += LVLShift.OUT[3:5]
LPFDelay.DrainEnable += LVLShift.OUT[1]
LPFDelay.DrainB += LVLShift.OUT[5:11]
LPFDelay.Prog += macro.PROG_HV
LPFDelay.Run += macro.RUN_HV

LPFDelay.Drainline_Prog += macro.SystemDrainline[0]
LPFDelay.Drainline_Run += macro.SystemDrainline[1]

LPFDelay.Vout += Buffers.Vin[0]
for i in range(5):
    LPFDelay.Vout_tap[i] += Buffers.Vin[i+1]

LPFDelay.Vin += chipframe.IO_W[7]

# MeadSOS
MeadSOSIsland = ac.Island(Top)
MeadSOS = lib_new.Top_MeadSOS(Top,MeadSOSIsland)
MeadSOS.place([0,0])
MeadSOS_location = (1000e3, 235e3)

MeadSOS.AVDD += chipframe.avdd_S[0]
MeadSOS.GND_S += chipframe.gnd_S[0]
MeadSOS.VINJ_S += chipframe.VINJ_S[0]
MeadSOS.VTUN += chipframe.IO_W_RES[0]
MeadSOS.VGRUN += macro.VGRUN
MeadSOS.VGPROG += macro.VGPROG

MeadSOS.GateEnable += LVLShift.OUT[2]
MeadSOS.GateB += LVLShift.OUT[3:5]
MeadSOS.DrainEnable += LVLShift.OUT[2]
MeadSOS.DrainB += LVLShift.OUT[5:10]
MeadSOS.Prog += macro.PROG_HV
MeadSOS.Run += macro.RUN_HV

MeadSOS.Drainline_Prog += macro.SystemDrainline[0]

MeadSOS.Vout += Buffers.Vin[6]
MeadSOS.Vout_buf += chipframe.IO_S[19:24]

MeadSOS.Vin += chipframe.IO_W[8]

# Compilation
#-------------------------------------------------------------------------------
#design_limits = [7e6, 6.21e6]:
design_limits = [7e6,7e6]
location_islands = (location_macro,location_chipframe,BufferLocation,LVL_Location, LPFDelay_location, MeadSOS_location)


with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 100
qparams["via"] = 10
qparams["jog"] = 35
qparams["conflict"] = 40
qparams["stage2"] = "mask none force effort 500"
qparams["stage3"] = "mask none force effort 500"

ac.compile_asic(Top,process="TSMC350nm",fileName="CHIP_Filters",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=2,drainSpace=15,gateSpaceIdx=2,gateSpace=15,route=True,qparams=qparams)
