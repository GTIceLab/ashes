import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


def QDAC(circuit,numStages=1,QDACIsland=None,islandLoc = [0,0]):
    Top = circuit

    QDACIsland = ac.Island(Top)


    EPOTs = lib_dc.TSMC350nm_EPOT(Top,QDACIsland,dim=[numStages,1])
    EPOTs.place([0,0])

    EPOTRST = lib_dc.TSMC350nm_EPOT(Top,QDACIsland)
    EPOTRST.markAbut()
    EPOTRST.place([numStages,0])

    InvertingAmp = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,QDACIsland)
    InvertingAmp.place([numStages+2,0])

    TgateIsland0 = ac.Island(Top)
    SEL_Code = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland0,dim=[numStages,1])
    SEL_Code.place([0,0])

    TgateIsland1 = ac.Island(Top)
    SEL_RST = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland1,dim=[numStages,1])
    SEL_RST.place([0,0])

    EPOTCapIsland = ac.Island(Top)
    EPOTCap = lib_dc.TSMC350nm_Capacitor_80ff(Top,EPOTCapIsland,dim=[numStages,1])
    EPOTCap.place([0,0])

    TgateIsland2 = ac.Island(Top)
    Amp_RST = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland2)
    Amp_RST.place([0,0])

    CapFBIsland = ac.Island(Top)
    CapFB = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapFBIsland)
    CapFB.place([0,0])

    # FG Programming
    # -------------------------------------------------------------------------------
    GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,QDACIsland,2)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,QDACIsland,1)

    drainLineNum = (numStages+1)*2+1
    drainBits = int(np.ceil(np.log2(drainLineNum)))

    DrainDecoder = lib_mux.STD_DrainDecoder(Top,QDACIsland,bits=drainBits)
    DrainSelect = lib_mux.RunDrainSwitch(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))
    DrainSwitch = lib_cab.DrainCutoff(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))

    for i in range(numStages):
        DrainSwitch.PR[2*i] += EPOTs.VD_P[2*i]
        DrainSwitch.PR[2*i+1] += EPOTs.VD_P[2*i+1]

    DrainSwitch.PR[2*(numStages)] += EPOTRST.VD_P[0]
    DrainSwitch.PR[2*(numStages)+1] += EPOTRST.VD_P[1]

    DrainSwitch.PR[2*(numStages+1)] += InvertingAmp.VD_P
    DrainSwitch.In[2*(numStages+1)] += InvertingAmp.VD_R 



    # Pins
    # -------------------------------------------------------------------------------
    outerPins = lib_mux.frame(Top)

    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","Run")
    VGPROG = outerPins.createPort("N","VGPROG")
    VGRUN = outerPins.createPort("N","VGRUN")
    VTUN = outerPins.createPort("N","VTUN")
    AVDD_N = outerPins.createPort("N","avdd")
    AVDD_S = outerPins.createPort("S","avdd")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("N","GateEnable")

    DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    Run_Drainline = outerPins.createPort("S","Run_Drainline")
    Prog_Drainline = outerPins.createPort("S","Prog_Drainline")

    
    VOUT = outerPins.createPort("S","Vout")
    RST = outerPins.createPort("N","RST")
    Code = outerPins.createPort("N","Code",dimension=numStages)

    # Pin Connections
    # -------------------------------------------------------------------------------
    EPOTs.VDD += AVDD_N
    EPOTs.VINJ += VINJ_N
    EPOTRST.VINJ_b += VINJ_S
    EPOTs.GND += GND_N
    EPOTs.Prog += PROG
    EPOTs.VTUN += VTUN
    for i in range(numStages):
        EPOTs.VIN_PLUS[i] += AVDD_N

    EPOTRST.VIN_PLUS += AVDD_N

    Vref = ac.Wire(Top)
    EPOTRST.Vout += Vref

    EPOTs.Vout += SEL_Code.A

    SEL_Code.VDD += AVDD_N 
    SEL_Code.GND += GND_N
    SEL_Code.GND_b += GND_S
    SEL_Code.C += SEL_RST.B
    SEL_Code.SELA += Code
    SEL_Code.B += Vref

    SEL_RST.VDD += AVDD_N
    SEL_RST.GND += GND_N
    SEL_RST.C += EPOTCap.Top
    SEL_RST.SELA += RST[0]
    SEL_RST.A += Vref
    
    for i in range(numStages):
        EPOTCap.Bot[i] += InvertingAmp.VIN_MINUS

    Amp_RST.VDD += AVDD_N
    Amp_RST.GND += GND_N
    Amp_RST.SELA += RST[0]
    Amp_RST.C += VOUT[0]

    InvertingAmp.VINJ += EPOTRST.VINJ_b
    InvertingAmp.VPWR_b += EPOTRST.VDD_b
    InvertingAmp.VPWR += AVDD_S
    InvertingAmp.GND += EPOTRST.GND_b
    InvertingAmp.GND += GND_S
    InvertingAmp.PROG += EPOTRST.Prog_b
    InvertingAmp.VTUN += EPOTRST.VTUN_b
    InvertingAmp.Vg += EPOTRST.Vg_b[0]
    InvertingAmp.Vsel += EPOTRST.Vsel_b[0]
    InvertingAmp.VIN_MINUS += Amp_RST.A
    InvertingAmp.VIN_MINUS += CapFB.Top
    InvertingAmp.Vout += CapFB.Bot
    InvertingAmp.Vout += VOUT
    InvertingAmp.VIN_PLUS += Vref

    GateSwitches.VINJ_T += VINJ_N
    GateSwitches.VINJ[0] += EPOTs.VINJ
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN
    GateSwitches.GND_T += GND_N[0]
    GateSwitches.CTRL_B += EPOTs.Vsel
    GateSwitches.Vg += EPOTs.Vg
    GateSwitches.Vgsel += VGPROG
    GateSwitches.RUN_IN += VGRUN[0]

    DrainSwitch.RUN += RUN
    DrainSwitch.GND += GND_S
    DrainSwitch.VDD += VINJ_S

    DrainSelect.prog_drainrail += Prog_Drainline
    DrainSelect.run_drainrail += Run_Drainline
    DrainSelect.GND += GND_N
    DrainSelect.VINJ += VINJ_N

    DrainDecoder.IN += DrainBits
    DrainDecoder.ENABLE += DrainEnable

    GateDecoder.VINJ_b[0] += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateBits




    # Island Placement
    # -------------------------------------------------------------------------------

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000
    DecoderWidth = int(43000 + ((drainBits/2)*25000))

    XEPOT = islandLoc[0]
    XTGate0 = DecoderWidth+15000+XEPOT+EPOTWidth+5*XSpace
    XTGate1 = XTGate0 + TGateWidth + 3*XSpace
    XEPOTCap = XTGate1 + TGateWidth + 2*XSpace
    XAmpRST = DecoderWidth+15000+XEPOT+75000
    XCap = XAmpRST+2*XSpace+TGateWidth

    YEPOT = islandLoc[1]
    YIslands2 = YEPOT + 2*Pitch
    Ybottom = YEPOT

    location_islands = ((XEPOT,YEPOT),(XTGate0,YIslands2),(XTGate1,YIslands2),(XEPOTCap,YIslands2),(XAmpRST,Ybottom),(XCap,Ybottom))

    return location_islands


Top = ac.Circuit()

location_islands = QDAC(Top,5,islandLoc=[2750,3050])

design_limits = [4e5, 4e5]


ac.compile_asic(Top,process="TSMC350nm",fileName="QDAC",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 15,gateSpaceIdx=0,gateSpace=15)




