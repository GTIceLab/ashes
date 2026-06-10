import numpy as np
import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.asic.asic_systems as algs
import MeadSOS as ms

def LPF_MeadSOS(Top,numStages=1,Vin=None):
    LPFIsland = ac.Island(Top)

    if Vin == None:
        Vin = ac.Wire(Top)

    Vouts = [0]*numStages
    Vout_Bufs = [0]*numStages
    instances = [0]*numStages

    for i in range(numStages):  
        MeadVin = None
        if i == 0:
            MeadVin = Vin
        else:
            MeadVin = Vouts[i-1]
            
        Vouts[i],Vout_Bufs[i],instances[i] = ms.MeadSOS(Top,LPFIsland,Vin=MeadVin,loc=[2*(i),0])

    Vout = Vouts[numStages-1]

    # FG Programming
    # -------------------------------------------------------------------------------
    drainBits = int(np.ceil(np.log2(numStages*4)))
    DrainDecoder = lib_mux.STD_DrainDecoder(Top,LPFIsland,bits=drainBits)
    DrainSelect = lib_mux.RunDrainSwitch(Top,LPFIsland,num=numStages)
    DrainSwitch = lib_cab.DrainCutoff(Top,LPFIsland,num=numStages)

    # Connect program drains to drain switch
    for i in range(numStages):
        DrainSwitch.PR[4*i] += instances[i][0].VD_P[0]
        DrainSwitch.PR[(4*i)+1] += instances[i][0].VD_P[1]
        
        DrainSwitch.PR[(4*i)+2] += instances[i][1].VD_P[0]
        DrainSwitch.PR[(4*i)+3] += instances[i][1].VD_P[1]
        
    GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,LPFIsland,2)
    GateSwitches0 = lib_mux.STD_IndirectGateSwitch(Top,LPFIsland,1)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,LPFIsland,1,col=0)

    GateSwitches0.Vg[0] += instances[0][0].Vg[0]
    GateSwitches0.Vg[1] += instances[0][0].Vg[1]
    GateSwitches0.CTRL_B += instances[0][0].Vsel

    # Pins
    # -------------------------------------------------------------------------------
    outerPins = lib_mux.frame(Top)
    outerPins.createPort("W","Vin",connection = Vin)
    VOUT = outerPins.createPort("E","Vout",connection = Vout)

    PIN_Vout_Buf = outerPins.createPort("E","Vout_Buf",dimension=numStages)
    for i in range(numStages):
        Vout_Bufs[i] += PIN_Vout_Buf[i]

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

    Drainline = outerPins.createPort("S","Drainline_Prog")

    GateEnable = outerPins.createPort("N","GateEnable")
    GateB = outerPins.createPort("W","GateB",dimension=2)

    DrainEnable = outerPins.createPort("W","DrainEnable")
    DrainB = outerPins.createPort("W","DrainB",dimension=drainBits)

    # Pin Connections
    # -------------------------------------------------------------------------------
    GateSwitches.RUN_IN += VGRUN[0]
    GateSwitches0.VINJ_T += GateDecoder.VINJ_b[0]
    GateSwitches0.GND_T += GND_N
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateB

    DrainSwitch.VDD += VINJ_S
    DrainSwitch.GND += GND_S
    DrainSwitch.RUN += RUN

    DrainSelect.VINJ += VINJ_S
    DrainSelect.GND += GND_S
    DrainSelect.prog_drainrail += Drainline

    DrainDecoder.VINJ += VINJ_S
    DrainDecoder.GND += GND_S
    DrainDecoder.IN += DrainB
    DrainDecoder.ENABLE += DrainEnable


    instances[numStages-1][1].GND_b += GND_S
    instances[numStages-1][1].VINJ_b += VINJ_S
    instances[0][0].VINJ += VINJ_N
    instances[0][0].GND += GND_N
    instances[0][0].VTUN += VTUN
    instances[0][0].VPWR += AVDD[0]
    instances[0][0].PROG += PROG
    instances[0][0].RUN += RUN

    return VOUT
