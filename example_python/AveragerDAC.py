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
    Buffer = lib_dc.TSMC350nm_AnalogBuffer(Top,AvgDACIsland)
    Buffer.place([numStages+3,0])
    Buffer.markAbut()


    # 1 Tgate per bit
    TgateIsland = ac.Island(Top)
    Tgates = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland,dim=[numStages,1])
    Tgates.place([0,1])

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
    outerPins = lib_mux.frame(Top)

    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","Run")
    VGRUN = outerPins.createPort("N","VGRUN")
    VGPROG = outerPins.createPort("N","VGPROG")
    VTUN = outerPins.createPort("N","VTUN")
    AVDD = outerPins.createPort("N","AVDD")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("W","GateEnable")
    
    VOUT = outerPins.createPort("S","Vout")
    TGATES = outerPins.createPort("N","Tgates",dimension=numStages)

    # Connections
    #----------------------------------------------------------------------------

    EPOTs.VDD += AVDD
    EPOTs.VINJ += VINJ_N
    EPOTs.VINJ_b += VINJ_S
    EPOTs.GND += GND_N
    EPOTs.GND_b += GND_S
    EPOTs.Prog += PROG

    Vref = ac.Wire(Top)
    EPOTs.Vout[numStages-1] += Vref
    EPOTs.Vout[0:numStages-2] += Tgates.A

    #Tgates.SELA += Code
    Tgates.A += EPOTs.Vout[0]
    Tgates.B += Vref

    VOUT += Buffer.Vout
    Buffer.VDD += AVDD
    Buffer.GND += GND_S


    GateSwitches.VINJ_T += VINJ_N[0]
    GateSwitches.VINJ += EPOTs.VINJ
    GateSwitches.PROG += PROG
    GateSwitches.GND_T += GND_N[0]
    GateSwitches.GND += GND_S[0]
    GateSwitches.CTRL_B += EPOTs.Vg

    DrainSwitch.RUN += RUN
    DrainSwitch.GND += EPOTs.GND
    DrainSwitch.VDD += AVDD

    for i in range(numStages+2):
        DrainSwitch.PR[2*i] += EPOTs.VD_P[2*i]
        DrainSwitch.PR[2*i+1] += EPOTs.VD_P[2*i+1]


    #DrainSelect.VINJ_b += VINJ_S
    #DrainSelect.GND_b += GND_S

    DrainDecoder.VINJ += VINJ_S
    DrainDecoder.GND += GND_S
    DrainDecoder.IN += DrainBits
    DrainDecoder.ENABLE += DrainEnable

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateBits

    # Island Placement
    #----------------------------------------------------------------------------
    XFGs = islandLoc[0]
    YFGs = islandLoc[1]

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000
    DecoderWidth = int(43000 + ((drainBits/2)*25000))

    XTgate = (EPOTWidth+25*XSpace+XFGs+DecoderWidth) + 45000
    YTgate = YFGs+(2*Pitch)

    location_islands = ((XFGs,YFGs),(XTgate,YTgate)) 


    return location_islands

Top = ac.Circuit()

location_islands = AvgDAC(Top,6,islandLoc=[5000,5000])

design_limits = [8e5, 6e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="AveragerDAC",design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=50,gateSpaceIdx=0,gateSpace=15)
