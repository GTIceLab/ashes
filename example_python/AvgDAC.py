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
    EPOTs = lib_dc.TSMC350nm_EPOT(Top,AvgDACIsland,dim=[numStages+1,1])
    EPOTs.place([0,0])

    # Pins
    # -------------------------------------------------------------------------------
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
    VOUT = outerPins.createPort("S","Vout")
    RST = outerPins.createPort("N","RST")
    Code = outerPins.createPort("N","Code",dimension=numStages)

    # Pin Connections
    # -------------------------------------------------------------------------------
    EPOTs.VDD += AVDD
    EPOTs.VINJ += VINJ_N
    EPOTs.VINJ_b += VINJ_S
    EPOTs.GND += GND_N
    EPOTs.GND_b += GND_S
    EPOTs.Prog += PROG


    # Island Placement
    # -------------------------------------------------------------------------------

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000

    XEPOT = islandLoc[0]

    YEPOT = islandLoc[1]

    location_islands = ((XEPOT,YEPOT))

    return location_islands


Top = ac.Circuit()

location_islands = AvgDAC(Top,5,islandLoc=[50000,25000])

design_limits = [5e5, 5e5]


ac.compile_asic(Top,process="TSMC350nm",fileName="AvgDAC",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 15,gateSpaceIdx=0,gateSpace=10)




