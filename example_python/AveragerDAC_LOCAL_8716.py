import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


def AvgDAC(circuit,numStages=1,AvgDACIsland=None,islandLoc=[0,0]):
    Top = circuit

    AvgDACIsland = ac.Island(Top)
    # 1 EPOT per bit, and 2 more for shifting digital input to TA linear range
    EPOTs= lib_dc.TSMC350nm_EPOT(Top,AvgDACIsland,dim=[numStages+2,1])
    EPOTs.place([0,0])

    # 1 analog buffer per DAC
    #Buffer = lib_dc.TSMC350nm_AnalogBuffer(Top,AvgDACIsland)
    #Buffer.place([numStages+3,0])


    # 1 Tgate per bit
    TgateIsland = ac.Island(Top)
    Tgates = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland,dim=[numStages,1])
    Tgates.place([numStages+4,0])

    # FG Programming
    #-----------------------------------------------------------------------------
    GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,AvgDACIsland,2)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,AvgDACIsland,1)

    drainLineNum = (numStages+2)*2+1
    drainBits = int(np.ceil(np.log2(drainLineNum)))

    DrainDecoder = lib_mux.STD_DrainDecoder(Top,AvgDACIsland,bits=drainBits)
    DrainSelect = lib_mux.RunDrainSwitch(Top,AvgDACIsland,num=int(np.ceil(drainLineNum/4)))
    DrainSwitch = lib_cab.DrainCutoff(Top,AvgDACIsland,num=int(np.ceil(drainLineNum/4)))



    # Pins
    #-----------------------------------------------------------------------------


    # Connections
    #----------------------------------------------------------------------------


    # Island Placement
    #----------------------------------------------------------------------------
    XFGs = islandLoc[0]
    YFGs = islandLoc[1]

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000
    DecoderWidth = int(43000 + ((drainBits/2)*25000))

    XTgate = EPOTWidth+25*XSpace+XFGs+DecoderWidth
    YTgate = YFGs+((numStages*Pitch)

    location_islands = ((XFGs,YFGs),(XTgate,YTgate)) 


    return location_islands

Top = ac.Circuit()

location_islands = AvgDAC(Top,1,islandLoc=[50000,25000])

design_limits = [5e5, 5e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="AveragerDAC",design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=15,gateSpaceIdx=0,gateSpace=10)
