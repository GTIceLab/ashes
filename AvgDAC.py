import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


def AvgDAC(circuit,numStages=1,AvgDACIsland=None,islandLoc = [0,0]):
    Top = circuit

    AvgDACIsland = ac.Island(Top)
    EPOTs = lib_dc.TSMC350nm_EPOT(Top,AvgDACIsland,dim=[numStages,1])
    EPOTs.place([0,0])

    TgateIsland = ac.Island(Top)
    SEL_Code = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland,dim=[5,1])
    SEL_Code.place([0,0])

    EPOTIsland2 = ac.Island(Top)
    EPOTs2 = lib_dc.TSMC350nm_EPOT(Top,EPOTIsland2,dim=[5,1])
    EPOTs2.place([0,0])

    BufferIsland = ac.Island(Top)
    Buffer = lib_dc.TSMC350nm_AnalogBuffer(Top,BufferIsland,dim=[1,1])
    Buffer.place([0,0])
	# FG Programming
    # -------------------------------------------------------------------------------
    #GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,QDACIsland,2)
    #GateSwitches0 = lib_mux.STD_IndirectGateSwitch(Top,QDACIsland,1)
    #GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,QDACIsland,1,col=0)

    #drainLineNum = (numStages+1)*2+1
    #drainBits = int(np.ceil(np.log2(drainLineNum)))

    #DrainDecoder = lib_mux.STD_DrainDecoder(Top,QDACIsland,bits=drainBits)
    #DrainSelect = lib_mux.RunDrainSwitch(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))
    #DrainSwitch = lib_cab.DrainCutoff(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))

    #for i in range(numStages+1):
    #    DrainSwitch.PR[2*i] += EPOTs.VD_P[2*i]
    #    DrainSwitch.PR[2*i+1] += EPOTs.VD_P[2*i+1]

    #DrainSwitch.PR[2*(numStages+1)] += InvertingAmp.VD_P
    #DrainSwitch.In[2*(numStages+1)] += InvertingAmp.VD_R 

    # Pins
    # -------------------------------------------------------------------------------
    outerPins = lib_mux.frame(Top)

    #PROG = outerPins.createPort("N","Prog")
    #RUN = outerPins.createPort("N","Run")
    #VGRUN = outerPins.createPort("N","VGRUN")
    #VGPROG = outerPins.createPort("N","VGPROG")
    VTUN = outerPins.createPort("N","VTUN")
    AVDD = outerPins.createPort("N","AVDD")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    #VINJ_N = outerPins.createPort("N","vinj")
    #VINJ_S = outerPins.createPort("S","vinj")
    VOUT = outerPins.createPort("E","Vout")
    # Pin Connections
    # -------------------------------------------------------------------------------
    EPOTs.VDD += AVDD
    #EPOTs.VINJ += VINJ_N
    EPOTs.GND_b += GND_S
    EPOTs2.GND += GND_N
    SEL_Code.GND_b += GND_S
    EPOTs.VTUN += VTUN
    #Buffer.Vin += Vx
    EPOTs2.VDD += AVDD
    EPOTs.VTUN_b += EPOTs2.VTUN_b
    Buffer.Vout += VOUT
    
    
    # Island Placement
    # -------------------------------------------------------------------------------

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000

    XEPOT = islandLoc[0]

    YEPOT = islandLoc[1]

    location_islands = ((XEPOT,YEPOT),(150000,YEPOT),(170000,YEPOT),(250000,YEPOT+20000))

    return location_islands


Top = ac.Circuit()

location_islands = AvgDAC(Top,2,islandLoc=[50000,25000])

design_limits = [5e5, 5e5]


ac.compile_asic(Top,process="TSMC350nm",fileName="AvgDAC",p_and_r = True,design_limits = design_limits, location_islands = location_islands)




