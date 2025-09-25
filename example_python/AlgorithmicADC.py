import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


Top = ac.Circuit()


def AlgorithmicADC(circuit,numBits=1,islandLoc= [0,0],debug=False):
    Top = circuit
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

    Tgates = [0]*6
    for i in range(6):
        Tgates[i] = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland)
        Tgates[i].place([i,0])
        Tgates[i].markAbut()



    CapIsland = ac.Island(Top)
    Cin = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapIsland,dim=[2,1])
    Cin.place([0,0])
    Csub = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapIsland,dim=[2,1])
    Csub.place([2,0])
    Cfb = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapIsland)
    Cfb.place([4,0])
    Cfb.markAbut()

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

    VGRUN = outerPins.createPort("N","VGRUN")
    VGPROG = outerPins.createPort("N","VGPROG")

    VTUN = outerPins.createPort("N","VTUN")

    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")

    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    AVDD_N = outerPins.createPort("N","avdd")
    AVDD_S = outerPins.createPort("S","avdd")

    DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("N","GateEnable")

    Drainline_Prog = outerPins.createPort("S","Drainline_Prog")
    Drainline_Run= outerPins.createPort("S","Drainline_Run")

    VIN = outerPins.createPort("W","VIN")
    CLK_Sample = outerPins.createPort("E","CLK_Sample")
    CLK_Amp = outerPins.createPort("E","CLK_Amp")
    CLK_RST = outerPins.createPort("S","CLK_RST")
    CLK_Load = outerPins.createPort("E","CLK_Load")
    VRES = outerPins.createPort("S","VRES")

    Code = outerPins.createPort("S","Code")

    if debug == True:
        DEBUG = outerPins.createPort("E","DEBUG",dimension=3)
        DEBUG[0] += CompThreshold.Vout
        DEBUG[1] += CapSwitch0.Vout
        DEBUG[2] += Vreset.Vout


    # Pin Connections
    # --------------------------------------------------------------------
    DrainSelect.prog_drainrail += Drainline_Prog
    DrainSelect.run_drainrail += Drainline_Run
    DrainSelect.VINJ += VINJ_S
    DrainSelect.GND += GND_S

    DrainSwitch.RUN += RUN
    DrainSwitch.GND += GND_S
    DrainSwitch.VDD += VINJ_S

    GateSwitches.GND_T += GND_N
    GateSwitches.VINJ += CompThreshold.VINJ
    GateSwitches.VINJ_T += GateDecoder.VINJ_b[0]
    GateSwitches.Vgsel += VGPROG
    GateSwitches.RUN_IN += VGRUN[0]
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN

    DrainDecoder.IN += DrainBits
    DrainDecoder.ENABLE += DrainEnable

    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateBits
    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N

    # ------------------------------------------
    CompThreshold.Vg += GateSwitches.Vg
    CompThreshold.Vsel += GateSwitches.CTRL_B
    CompThreshold.GND += GND_N
    CompThreshold.VDD += AVDD_N
    CompThreshold.Prog += PROG
    CompThreshold.VTUN += VTUN
    CompThreshold.VIN_PLUS += AVDD_S

    Vreset.VIN_PLUS += AVDD_S
    CapSwitch0.VIN_PLUS += AVDD_S

    Comparator.PROG += Vreset.Prog_b
    Comparator.VTUN += Vreset.VTUN_b
    Comparator.Vsel += Vreset.Vsel_b[0]
    Comparator.Vg += Vreset.Vg_b[0]
    Comparator.GND += Vreset.GND_b
    Comparator.VINJ += Vreset.VINJ_b
    Comparator.VPWR += Vreset.VDD_b
    Comparator.VPWR += AVDD_S

    Buffer.VTUN += InvAmp.VTUN_b
    Buffer.Vg += InvAmp.Vg_b
    Buffer.Vsel += InvAmp.Vsel_b
    Buffer.VINJ += InvAmp.VINJ_b
    Buffer.VDD += InvAmp.VPWR_b
    Buffer.GND += InvAmp.GND_b

    CompThreshold.VD_P += DrainSwitch.PR[0:2]
    CapSwitch0.VD_P += DrainSwitch.PR[2:4]
    Vreset.VD_P += DrainSwitch.PR[4:6]

    Comparator.VD_P += DrainSwitch.PR[6]
    Comparator.VD_R += DrainSwitch.In[6]

    InvAmp.VD_P += DrainSwitch.PR[7]
    InvAmp.VD_R += DrainSwitch.In[7]

    Buffer.Vd_P += DrainSwitch.PR[8]
    Buffer.VINJ_b += VINJ_S

    # Tgate0 = SWCIN 
    VIN += Tgates[0].C
    Buffer.Vin += Tgates[0].A
    CLK_Sample += Tgates[0].SELA

    Vx = ac.Wire(Top)
    CinTop = ac.Wire(Top)

    Cin.Top[0] += CinTop
    Cin.Top[1] += CinTop
    Comparator.VIN_PLUS += CinTop 

    Cin.Bot[0] += Vx
    Cin.Bot[1] += Vx
    
    # Tgate1 = SWCBUF
    Buffer.Vout += Tgates[1].C
    Tgates[1].A += CinTop
    Tgates[1].SELA += CLK_Amp

    # Tgate2 = SWCRST0
    Tgates[2].C += CinTop
    Tgates[2].A += Vx
    Tgates[2].SELA += CLK_RST

    Csub.Top[0] += Vx
    Csub.Top[1] += Vx

    CsubBot = ac.Wire(Top)
    Csub.Bot[0] += CsubBot
    Csub.Bot[1] += CsubBot

    # Tgate4 = SWCSUB
    CsubBot += Tgates[4].C
    Tgates[4].B += CapSwitch0.Vout
    Tgates[4].SELA += Comparator.Vout
    Tgates[4].A += GND_S

    Comparator.VIN_MINUS += CompThreshold.Vout

    InvAmp.VIN_MINUS += Vx
    Cfb.Top += Vx

    # Tgate3 = SWCRST1
    Tgates[3].C += Vx
    Tgates[3].A += VRES
    Tgates[3].SELA += CLK_RST

    InvAmp.VIN_PLUS += Vreset.Vout

    VRES += InvAmp.Vout
    VRES += Cfb.Bot

    # Tgate5 = SWCLOAD
    VRES += Tgates[5].A
    Tgates[5].C += Buffer.Vin
    Tgates[5].SELA += CLK_Load

    Tgates[0].VDD += AVDD_N
    Tgates[0].GND += GND_N

    Comparator.Vout += Code


    # Placement
    # ------------------------------------------------------------------
    EPOTWidth = 85000
    Pitch = 22000
    DecoderWidth = int(43000 + ((drainBits/2)*25000))+15000
    xoffset = islandLoc[0]  
    yoffset = islandLoc[1] 

    location_islands= ( (xoffset,4*Pitch) , (xoffset+DecoderWidth-5000,yoffset) , (xoffset+DecoderWidth-5000,1.5*Pitch), (xoffset+DecoderWidth+EPOTWidth+5000,yoffset+2000), (xoffset+DecoderWidth+EPOTWidth+28000,yoffset+15000) )

    return location_islands

Top = ac.Circuit()
location_islands = AlgorithmicADC(Top,5,islandLoc=[5000,4000],debug=True)

design_limits = [8e5, 8e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="AlgorithmicADC",design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=15,gateSpaceIdx=0,gateSpace=10)
