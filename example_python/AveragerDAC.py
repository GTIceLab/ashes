import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


def AvgDAC(circuit,numBits=1,AvgDACIsland=None,islandLoc=[0,0]):
    Top = circuit

    OTAIsland = ac.Island(Top)
    # One TA per bit
    TAs = lib_dc.TSMC350nm_Amplifier9T_FGInputs_Bias(Top,OTAIsland,dim=[numBits,1])
    TAs.place([0,0])

    
    EPOTIsland = ac.Island(Top)
    # 2 EPOTs to set input to linear range of OTAs
    EPOTA = lib_dc.TSMC350nm_EPOT(Top,EPOTIsland)
    EPOTB = lib_dc.TSMC350nm_EPOT(Top,EPOTIsland)
    EPOTA.place([0,0])
    EPOTB.place([1,0])
    EPOTA.markAbut()
    EPOTB.markAbut()

    BufferIsland = ac.Island(Top)
    # 1 analog buffer per DAC
    Buffer = lib_dc.TSMC350nm_AnalogBuffer(Top,BufferIsland)
    Buffer.place([0,0])
    Buffer.markAbut()


    # 1 Tgate per bit
    TgateIsland = ac.Island(Top)
    Tgates = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland,dim=[numBits,1])
    Tgates.place([0,0])

    # FG Programming
    #-----------------------------------------------------------------------------
    GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,OTAIsland,2)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,OTAIsland,1)

    drainLineNum = (numBits+2)*2+1
    drainBits = int(np.ceil(np.log2(drainLineNum)))

    DrainDecoder = lib_mux.STD_DrainDecoder(Top,OTAIsland,bits=drainBits)
    DrainSelect = lib_mux.RunDrainSwitch(Top,OTAIsland,num=int(np.ceil(drainLineNum/4)))
    DrainSwitch = lib_cab.DrainCutoff(Top,OTAIsland,num=int(np.ceil(drainLineNum/4)))

    # Drainline Routing

    for i in range(numBits):
        DrainSwitch.PR[2*i] += TAs.Vd_P[2*i]
        DrainSwitch.PR[2*i+1] += TAs.Vd_P[2*i+1]
        DrainSwitch.In[i] += TAs.Vd_R[i]

    
    DrainSwitch.PR[2*numBits] += EPOTA.VD_P[0]
    DrainSwitch.PR[2*numBits+1] += EPOTA.VD_P[1]
    
    DrainSwitch.PR[2*numBits+2] += EPOTB.VD_P[0]
    DrainSwitch.PR[2*numBits+3] += EPOTB.VD_P[1]

    DrainSwitch.PR[2*numBits+4] += Buffer.Vd_P

    # Gateline Routing
    GateSwitches.CTRL_B += TAs.Vsel
    GateSwitches.Vg += TAs.Vg

    TAs.Vg_b[0] += EPOTA.Vg[0]


    # Pins
    #-----------------------------------------------------------------------------
    outerPins = lib_mux.frame(Top)

    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","Run")
    VGRUN = outerPins.createPort("N","VGRUN")
    VGPROG = outerPins.createPort("N","VGPROG")
    VTUN = outerPins.createPort("N","VTUN")
    AVDD_N = outerPins.createPort("N","avdd")
    AVDD_S = outerPins.createPort("S","avdd")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("N","GateEnable")

    Run_Drainline = outerPins.createPort("S","Run_Drainline")
    Prog_Drainline = outerPins.createPort("S","Prog_Drainline")
    
    VOUT = outerPins.createPort("S","Vout")
    Code = outerPins.createPort("E","Code",dimension=numBits)

    # Connections
    #----------------------------------------------------------------------------

    TAs.Vout += Buffer.Vin[0]
    TAs.VIN_MINUS += Buffer.Vin[0]
    TAs.VIN_PLUS += Tgates.C

    Tgates.A += EPOTA.Vout[0]
    Tgates.B += EPOTB.Vout[0]
    Tgates.SELA += Code
    Tgates.VDD += AVDD_N
    Tgates.GND += GND_N

    EPOTB.VINJ_b += VINJ_S
    EPOTB.VIN_PLUS += AVDD_N
    EPOTA.VIN_PLUS += AVDD_N

    VOUT += Buffer.Vout
    Buffer.VDD += EPOTB.VDD_b
    Buffer.GND += EPOTB.GND_b 
    Buffer.GND += GND_S
    Buffer.VDD += AVDD_S
    Buffer.VTUN += EPOTB.VTUN_b
    Buffer.VINJ += EPOTB.VINJ_b
    Buffer.Vsel += EPOTB.Vsel_b[0]
    Buffer.Vg += EPOTB.Vg_b[0]

    TAs.VDD += AVDD_N 
    TAs.GND += GND_N
    TAs.VINJ += GateSwitches.VINJ
    TAs.VINJ += VINJ_N
    TAs.Prog += PROG
    TAs.VTUN += VTUN

    GateSwitches.VINJ_T += VINJ_N[0]
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN
    GateSwitches.GND_T += GND_N[0]
    GateSwitches.RUN_IN += VGRUN[0]
    GateSwitches.Vgsel += VGPROG

    DrainSwitch.RUN += RUN
    DrainSwitch.GND += TAs.GND
    DrainSwitch.VDD += VINJ_S

    DrainSelect.prog_drainrail += Prog_Drainline
    DrainSelect.run_drainrail += Run_Drainline
    DrainSelect.GND += GND_N
    DrainSelect.VINJ += VINJ_N

    DrainDecoder.IN += DrainBits
    DrainDecoder.ENABLE += DrainEnable

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateBits

    # Island Placement
    #----------------------------------------------------------------------------
    XStart = islandLoc[0]
    YStart = islandLoc[1]

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000

   # DrainCutoffWidth + ProgRunDrainWidth + 4to1Width 
    DecoderWidth = 42460 + 20120 + (np.round(numBits/2)-1)*26270
    
    #OTAIsland,EPOTIsland,BufferIsland,TgateIsland
    OTAIslandX = XStart 
    OTAIslandY = YStart+3*Pitch+(Pitch/2)
    loc_OTA = (OTAIslandX,OTAIslandY)

    EPOTIslandX = XStart + DecoderWidth+15000+1400
    EPOTIslandY = OTAIslandY - 2*Pitch 
    loc_EPOT = (EPOTIslandX,EPOTIslandY)
    
    BufferIslandX = EPOTIslandX
    BufferIslandY = EPOTIslandY - Pitch - Pitch/2
    loc_Buffer = (BufferIslandX,BufferIslandY)

    TgateIslandX = (EPOTWidth+25*XSpace+XStart+DecoderWidth) + 1000
    TgateIslandY = YStart+(2*Pitch)
    loc_Tgates = (TgateIslandX,TgateIslandY)
 

    location_islands = (loc_OTA,loc_EPOT,loc_Buffer,loc_Tgates)

    return location_islands

Top = ac.Circuit()

location_islands = AvgDAC(Top,5,islandLoc=[5000,1500])


design_limits = [5e5, 5e5]

ac.compile_asic(Top,process="TSMC350nm",fileName="AveragerDAC",design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=15,gateSpaceIdx=0,gateSpace=11)
