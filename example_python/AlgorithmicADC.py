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
Buffer = lib_dc.TSMC350nm_AnalogBuffer(Top,ADCIsland)
Buffer.markAbut()
Buffer.place([7,0])


# Open-loop TA-based comparator
Comparator = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,ADCIsland) 
Comparator.place([4,0])
Comparator.markAbut()

# Inverting Amplifier
InvAmp = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,ADCIsland) 
InvAmp.place([5,0])
InvAmp.markAbut()

TgateIsland = ac.Island(Top)
Tgates = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland,dim=[6,1])
Tgates.place([0,0])

CapIsland = ac.Island(Top)
Caps = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapIsland,dim=[5,1])
Caps.place([0,0])

GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,ADCIsland,2)
GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,ADCIsland,1)

drainLineNum = 13
drainBits = int(np.ceil(np.log2(drainLineNum)))

DrainDecoder = lib_mux.STD_DrainDecoder(Top,ADCIsland,bits=drainBits)
DrainSelect = lib_mux.RunDrainSwitch(Top,ADCIsland,num=int(np.ceil(drainLineNum/4)))
DrainSwitch = lib_cab.DrainCutoff(Top,ADCIsland,num=int(np.ceil(drainLineNum/4)))

EPOTWidth = 85000
DecoderWidth = int(43000 + ((drainBits/2)*25000))+15000

location_islands= ( (0,0) , (DecoderWidth+EPOTWidth+5000,0) , (DecoderWidth+EPOTWidth+20000,0) )

design_limits = [5e5, 6e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="AlgorithmicADC",design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=15,gateSpaceIdx=0,gateSpace=15)
