import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *



def DelayLineCell(circuit,LPFIsland=None,loc=[0,0],Vin_N=None,Vin_S=None):

    Top = circuit
    # Placement
    if LPFIsland == None:
        LPFIsland = Island(Top)

    DelayLine0 = DelayLine(Top,LPFIsland)

    #DelayLine0.markAbut()

    DelayLine0.place([loc[0],loc[1]])
    
    # Connections
	# 
    # -------------------------------------------------------------------------------
    if Vin_N != None:
        DelayLine0.V_NW += Vin_N
    if Vin_S != None:
        DelayLine0.V_SW += Vin_S

    # Input Connections
    Vmid_N = Wire(Top)
    Vmid_S = Wire(Top)

    DelayLine0.V_NW += Vmid_N
    DelayLine0.V_SW += Vmid_S

    # Output Connections
    Vout_N = Wire(Top)
    Vout_S = Wire(Top)

    DelayLine0.V_NE += Vout_N
    DelayLine0.V_SE += Vout_S

    return Vout_N, Vout_S,[DelayLine0]

def LPF_DelayBlock(Top,numStages=1,Vin=None):
    LPFIsland = Island(Top)

    if Vin == None:
        Vin = Wire(Top)

    Vouts_N = [0]*numStages
    Vouts_S = [0]*numStages
    instances = [0]*numStages

    for i in range(numStages):  
        MeadVin_N = None
        MeadVin_S = None
        if i == 0:
            MeadVin_N = Vin
            MeadVin_S = None
        else:
            MeadVin_N = Vouts_N[i-1]
            MeadVin_S = Vouts_S[i-1]
            
        Vouts_N[i],Vouts_S[i],instances[i] = DelayLineCell(Top,LPFIsland,Vin_N=MeadVin_N,Vin_S=MeadVin_S,loc=[i,0])
    
    Vouts = Wire(Top)
    Vouts_N[numStages-1] += Vouts
    Vouts_S[numStages-1] += Vouts

    Vout=Vouts
    # FG Programming
    # -------------------------------------------------------------------------------
    drainBits = int(np.ceil(np.log2(numStages*4)))+1
    DrainDecoder = STD_DrainDecoder(Top,LPFIsland,bits=drainBits)
    DrainSelect = RunDrainSwitch(Top,LPFIsland,num=numStages)
    DrainSwitch = DrainCutoff(Top,LPFIsland,num=numStages)

    # Connect program drains to drain switch
    for i in range(numStages):
        DrainSwitch.PR[4*i] += instances[i][0].VD_P[0]
        DrainSwitch.PR[(4*i)+1] += instances[i][0].VD_P[1]
        DrainSwitch.PR[(4*i)+2] += instances[i][0].VD_P[2]
        DrainSwitch.PR[(4*i)+3] += instances[i][0].VD_P[3]

        DrainSwitch.In[(4*i)] += instances[i][0].VD_R[0]
        DrainSwitch.In[(4*i)+1] += instances[i][0].VD_R[1]
        
    GateDecoder = STD_IndirectGateDecoder(Top,LPFIsland,2)
    #GateSwitches0 = STD_IndirectGateSwitch(Top,LPFIsland,1)
    GateSwitches = STD_IndirectGateSwitch(Top,LPFIsland,1)

    GateSwitches.Vg[0] += instances[0][0].Vg[0]
    GateSwitches.Vg[1] += instances[0][0].Vg[1]
    GateSwitches.CTRL_B += instances[0][0].Vsel

    # Pins
    # -------------------------------------------------------------------------------
    outerPins = frame(Top)
    outerPins.createPort("W","Vin",connection = Vin)
    VOUT = outerPins.createPort("E","Vout",connection = Vout)

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

    Drainline_prog = outerPins.createPort("S","Drainline_Prog")
    Drainline_run = outerPins.createPort("S","Drainline_Run")

    GateEnable = outerPins.createPort("N","GateEnable")
    GateB = outerPins.createPort("W","GateB",dimension=2)

    DrainEnable = outerPins.createPort("W","DrainEnable")
    DrainB = outerPins.createPort("W","DrainB",dimension=drainBits)

    # Pin Connections
    # -------------------------------------------------------------------------------
    GateSwitches.RUN_IN += VGRUN[0]
    GateSwitches.VINJ_T += GateDecoder.VINJ_b[0]
    GateSwitches.VINJ += instances[0][0].VINJ
    GateSwitches.GND_T += GND_N
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN
    GateSwitches.VTUN += instances[0][0].VTUN
    GateSwitches.VPWR[0] += AVDD
    GateSwitches.VPWR[1] += AVDD

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateB

    DrainSwitch.VDD += VINJ_S
    DrainSwitch.GND += GND_S
    DrainSwitch.RUN += RUN

    DrainSelect.VINJ += VINJ_S
    DrainSelect.GND += GND_S
    DrainSelect.prog_drainrail += Drainline_prog
    DrainSelect.run_drainrail += Drainline_run

    #DrainDecoder.VINJ += VINJ_S
    #DrainDecoder.GND += GND_S
    DrainDecoder.IN += DrainB
    DrainDecoder.ENABLE += DrainEnable

    instances[numStages-1][0].GND_b += GND_S
    instances[numStages-1][0].VINJ_b += VINJ_S
    instances[0][0].VINJ += VINJ_N
    instances[0][0].GND += GND_N
    instances[0][0].VTUN += VTUN
    instances[0][0].VDD += AVDD[0]
    instances[0][0].PROG += PROG
    # instances[0][0].RUN += RUN

    return VOUT

Top = Circuit()
LPF_DelayBlock(Top,5)

'''MacroIsland = Island(Top)
macro = Macro(Top,MacroIsland,[1,1])
macro.place([0,0])

# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
chipframe = SmallPadFrame(Top,FrameIsland,[1,1])
chipframe.place([0,0])
chipframe.markChipFrame()'''

"""design_limits = [7e6, 6.21e6]
location_islands = ((210600,230000), (210600, 410000), (20600, 20000))"""

design_limits = [3.86e5, 2.34e5]
location_islands = ((10000,9000),(0,0))

compile_asic(Top,process="TSMC350nm",fileName="LPF_DelayBlock",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 15,gateSpaceIdx=0,gateSpace=10)
