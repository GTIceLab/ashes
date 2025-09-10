import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


Top = ac.Circuit()

ADCIsland = ac.Island(Top)

# Sets comparator threshold
CompThreshold = lib_dc.TSMC350nm_EPOT(Top,ADCIsland)
CompThreshold.markAbut()
CompThreshold.place([0,0])

# Sets bottom place of capacitor for a comparator decision of 0
CapSwitch0 = lib_dc.TSMC350nm_EPOT(Top,ADCIsland)
CapSwitch0.markAbut()
CapSwitch0.place([1,0])

# RST voltage of switched-cap system
Vreset = lib_dc.TSMC350nm_EPOT(Top,ADCIsland)
Vreset.markAbut()
Vreset.place([2,0])

# Buffers out Sample and Hold
ADCIsland2 = ac.Island(Top)
Buffer = lib_dc.TSMC350nm_AnalogBuffer(Top,ADCIsland2)
Buffer.markAbut()
Buffer.place([0,0])


# Open-loop TA-based comparator
ADCIsland3 = ac.Island(Top)
Comparator = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,ADCIsland3) 
Comparator.place([0,0])
Comparator.markAbut()

# Inverting Amplifier
InvAmp = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,ADCIsland3)
InvAmp.place([1,0])
InvAmp.markAbut()

TgateIsland = ac.Island(Top)
Tgates = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland,dim=[6,1])
Tgates.place([0,0])


CapIsland = ac.Island(Top)
Caps = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapIsland,dim=[5,1])
Caps.place([0,0])

# FG Programming
# ----------------------------------------------------------------------

GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,ADCIsland,2)
GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,ADCIsland,1)

drainLineNum = 9 
drainBits = int(np.ceil(np.log2(drainLineNum)))

DrainDecoder = lib_mux.STD_DrainDecoder(Top,ADCIsland,bits=drainBits)
DrainSelect = lib_mux.RunDrainSwitch(Top,ADCIsland,num=int(np.ceil(drainLineNum/4)))
DrainSwitch = lib_cab.DrainCutoff(Top,ADCIsland,num=int(np.ceil(drainLineNum/4)))


# Pins
# ---------------------------------------------------------------------
outerPins = lib_mux.frame(Top)

PROG = outerPins.createPort("N","PROG")
RUN = outerPins.createPort("N","RUN")


DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
DrainEnable = outerPins.createPort("W","DrainEnable")
GateBits = outerPins.createPort("W","GateB",dimension=2)
GateEnable = outerPins.createPort("W","GateEnable")

VIN = outerPins.createPort("W","VIN")
CLK_Sample = outerPins.createPort("E","CLK_Sample")
CLK_Amp = outerPins.createPort("E","CLK_Amp")
CLK_RST = outerPins.createPort("E","CLK_RST")


# Pin Connections
# --------------------------------------------------------------------
GateSwitches.PROG += PROG
GateSwitches.RUN += RUN
DrainSwitch.RUN += RUN
Comparator.PROG += PROG
CompThreshold.Prog += PROG

DrainDecoder.IN += DrainBits
DrainDecoder.ENABLE += DrainEnable

GateDecoder.ENABLE += GateEnable
GateDecoder.IN += GateBits

CompThreshold.VD_P += DrainSwitch.PR[0:2]
CapSwitch0.VD_P += DrainSwitch.PR[2:4]
Vreset.VD_P += DrainSwitch.PR[4:6]

Comparator.VD_P += DrainSwitch.PR[6]
Comparator.VD_R += DrainSwitch.In[6]

InvAmp.VD_P += DrainSwitch.PR[7]
InvAmp.VD_R += DrainSwitch.In[7]

Buffer.Vd_P += DrainSwitch.PR[8]

VIN += Tgates.A[0]
Buffer.Vin += Tgates.C[0]
CLK_Sample += Tgates.SELA[0]

CinTop = ac.Wire(Top)
Caps.Top[0] += CinTop
Caps.Top[1] += CinTop
CinBot = ac.Wire(Top)
Caps.Bot[0] += CinBot
Caps.Bot[1] += CinBot

Buffer.Vout += Tgates.A[1]
Tgates.C[1] += CinTop
Tgates.SELA[1] += CLK_Amp

Tgates.A[2] += CinTop
Tgates.C[2] += CinBot
Tgates.SELA[2] += CLK_RST

CsubTop = ac.Wire(Top)
Caps.Top[2] += CsubTop 
Caps.Top[3] += CsubTop 
CsubTop += CinBot
CsubBot = ac.Wire(Top)
Caps.Bot[2] += CsubBot
Caps.Bot[3] += CsubBot 

CsubTop += InvAmp.VIN_MINUS





# Placement
# ------------------------------------------------------------------
EPOTWidth = 85000
Pitch = 22000
DecoderWidth = int(43000 + ((drainBits/2)*25000))+15000
xoffset = 5000
yoffset = 0

location_islands= ( (xoffset,4*Pitch) , (xoffset+DecoderWidth-4000,yoffset) , (xoffset+DecoderWidth-4000,1.5*Pitch), (xoffset+DecoderWidth+EPOTWidth+5000,yoffset), (xoffset+DecoderWidth+EPOTWidth+20000,yoffset) )

design_limits = [5e5, 6e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="AlgorithmicADC",design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=15,gateSpaceIdx=0,gateSpace=10)
