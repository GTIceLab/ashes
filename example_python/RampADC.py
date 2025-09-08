import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np



def RampADC(Top,B,Vin=None):

    if Vin == None:
        Vin = Wire(Top)

    RampIsland = ac.Island(Top)

    # Generates ramp current
    RampBias = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,RampIsland)
    RampBias.place([0,0])
    RampBias.markAbut()

    # Open-loop TA-based comparator
    Comparator = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,RampIsland) 
    Comparator.place([1,0])
    Comparator.markAbut()

    # Capacitors to integrate ramp current

    capArray = [[None for _ in range(5)] for _ in range(2)]

    NonFGIsland=ac.Island(Top)
    numCapColumns = 3
    for j in range(numCapColumns):
            capArray[0][j] = lib_dc.TSMC350nm_Capacitor_80ff(Top,NonFGIsland)
            capArray[1][j] = lib_dc.TSMC350nm_Capacitor_80ff(Top,NonFGIsland)

            capArray[0][j].place([0,j])
            capArray[1][j].place([1,j])
            

    # TGate for ramp reset
    RampRST = lib_dc.TSMC350nm_TGate_DT(Top,NonFGIsland)
    RampRST.place([1,numCapColumns+1])

    # Ripple Counter
    CounterIsland = ac.Island(Top)
    Counter = lib_dc.TSMC350nm_RippleCounter(Top,CounterIsland,dim=[1,B])
    Counter.place([0,0])

    # FG Programming

    GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,RampIsland,2)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,RampIsland,1)


    DrainDecoder = lib_mux.STD_DrainDecoder(Top,RampIsland,bits=2)
    DrainSelect = lib_mux.RunDrainSwitch(Top,RampIsland,num=1)
    DrainSwitch = lib_cab.DrainCutoff(Top,RampIsland,num=1)

    # Pins 

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


    DrainBits = outerPins.createPort("W","DrainB",dimension=2)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("N","GateEnable")

    Code = outerPins.createPort("S","Code",dimension=B)
    CLK = outerPins.createPort("W","CLK")
    RST = outerPins.createPort("W","RST")

    VIN = outerPins.createPort("W","Vin")
    VIN += Vin
    # Pin Connections
    #----------------------------------------------------------------------------
    Counter.Count_B += Code
    Counter.CLK += CLK
    Counter.RST_L += RST
    Counter.VDD += AVDD
    Counter.GND += GND_S

    DrainSwitch.In[0] += RampBias.VD_R 
    DrainSwitch.In[1] += Comparator.VD_R
    DrainSwitch.PR[0] += RampBias.VD_P
    DrainSwitch.PR[1] += Comparator.VD_P
    DrainDecoder.IN += DrainBits
    DrainDecoder.GND += GND_S
    DrainDecoder.VINJ += VINJ_S

    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateBits
    GateDecoder.VINJV += VINJ_N
    GateDecoder.GND_b[1] += GND_N

    GateSwitches.VINJ += RampBias.VINJ
    GateSwitches.GND += RampBias.GND

    RampBias.Vg += GateSwitches.Vg[0]
    RampBias.Vsel += GateSwitches.CTRL_B[0]
    RampBias.VTUN += VTUN
    RampBias.PROG += PROG
    RampBias.GND += GND_N

    RampBias.VIN_MINUS += RST
    RampBias.VIN_PLUS += AVDD

    CapTop = ac.Wire(Top)
    CapBot = ac.Wire(Top)

    for i in range(numCapColumns):
        for j in range(2):
            capArray[j][i].Top+=CapTop
            capArray[j][i].Bot+=CapBot

    CapBot += GND_N
    CapTop += RampBias.Vout
    CapTop += Comparator.VIN_PLUS

    RampRST.A += CapTop
    RampRST.C += CapBot
    RampRST.SELA += RST
    RampRST.VDD += AVDD
    RampRST.GND += CapBot

    VIN += Comparator.VIN_MINUS

    # -----------------------------------------------------------------------------------------------
    XPadding = 5000
    YPadding = 5000
    FGWidth = 68940 
    Pitch = 22000
    DecoderWidth = int(43000 + ((2/2)*25000))

    location_islands = ( (XPadding,int(1.5*Pitch)) , (XPadding+DecoderWidth+FGWidth,int(1.5*Pitch)) , (XPadding,YPadding) )
    return location_islands


Top = ac.Circuit()
location_islands = RampADC(Top,8)
design_limits = [6e5, 5e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="RampADC",p_and_r = True,design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=15,gateSpaceIdx=0,gateSpace=10)

