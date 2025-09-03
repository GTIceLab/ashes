import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *



def C4_Ampdet(circuit,numStages=1):

    Top = circuit
    # Placement
    C4Island = Island(Top)
    AmpdetIsland = Island(Top)
        
    FakeIsland=Island(Top)
    FakeCell0 = FakeCellGateDecoder(Top,FakeIsland,dim=(1,2))
    FakeCell0.place([0,0])
     
    GateDecoder = STD_IndirectGateDecoder(Top,FakeIsland,2)
    GateSwitches = STD_IndirectGateSwitch(Top,FakeIsland,2)
        
     
    C4 = TSMC350nm_C4(Top,C4Island,dim=(numStages,1))
    Ampdet = TSMC350nm_Ampdet_NoFG(Top,AmpdetIsland,dim=(numStages,1))
    C4.place([0,0])
    Ampdet.place([0,0])
    C4.OUTPUT += Ampdet.VIN
        
    # FG Programming
    # -------------------------------------------------------------------------------
    drainBits = int(np.ceil(np.log2(numStages*4)))
    DrainDecoder = STD_DrainDecoder(Top,C4Island,bits=drainBits)
    DrainSelect = RunDrainSwitch(Top,C4Island,num=numStages)
    DrainSwitch = DrainCutoff(Top,C4Island,num=numStages)

    # Connect program drains to drain switch
    DrainSwitch.PR[0] += C4.VD_P[0]
    DrainSwitch.PR[1] += C4.VD_P[1]
    DrainSwitch.PR[2] += Ampdet.VD_P[0]
    DrainSwitch.PR[3] += Ampdet.VD_P[1]
        
    #GateDecoder = STD_IndirectGateDecoder(Top,LPFIsland,2)
    #GateSwitches = STD_IndirectGateSwitch(Top,LPFIsland,2)

    GateSwitches.Vg[0] += C4.Vg[0]
    GateSwitches.Vg[1] += C4.Vg[1]
    GateSwitches.Vg[2] += Ampdet.Vg
    GateSwitches.CTRL_B[0] += C4.Vsel[0]
    GateSwitches.CTRL_B[1] += C4.Vsel[1]
    GateSwitches.CTRL_B[2] += Ampdet.Vsel
    
    GateSwitches.VINJ[0] += C4.VINJ
    GateSwitches.GND[0] += C4.GND
    GateSwitches.VTUN[0] += C4.VTUN
    GateSwitches.VDD[1] += C4.VPWR
    
    GateSwitches.VINJ[1] += Ampdet.VINJ
    GateSwitches.GND[1] += Ampdet.GND
    GateSwitches.VTUN[1] += Ampdet.VTUN
    GateSwitches.VDD[3] += Ampdet.VPWR
    

    #Outerpins
    
    outerPins = frame(Top)
    Vin = outerPins.createPort("W","Vin")
    Vref = outerPins.createPort("W","Vref")
    for i in range(numStages):
        Vin += C4.VIN[i]
        Vref += C4.VREF[i]
        
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

    Drainline = outerPins.createPort("W","Drainline_Prog")

    GateEnable = outerPins.createPort("N","GateEnable")
    GateB = outerPins.createPort("N","GateB",dimension=2)

    DrainEnable = outerPins.createPort("W","DrainEnable")
    DrainB = outerPins.createPort("W","DrainB",dimension=drainBits)
    
    
    # Pin Connections
    # -------------------------------------------------------------------------------
    GateSwitches.RUN_IN[0] += VGRUN
    GateSwitches.RUN_IN[1] += VGRUN
    GateSwitches.RUN_IN[2] += VGRUN
    GateSwitches.RUN_IN[3] += VGRUN
    GateSwitches.VINJ_T[0] += GateDecoder.VINJ_b[0]
    GateSwitches.VINJ_T[1] += GateDecoder.VINJ_b[1]
    
    GateSwitches.GND_T[0] += GND_N
    GateSwitches.GND_T[1] += GND_N
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

    DrainSelect.VINJ_b += VINJ_S
    DrainSelect.GND_b += GND_S
    DrainSelect.prog_drainrail += Drainline

    DrainDecoder.VINJ += VINJ_S
    DrainDecoder.GND += GND_S
    #for i in range(drainBits):
    #    DrainDecoder.IN[i] += DrainB[i]
    DrainDecoder.IN += DrainB
    DrainDecoder.ENABLE += DrainEnable

    C4.PROG += PROG
    C4.RUN += RUN
    
        
        
    return Ampdet.OUTPUT,DrainSwitch.PR[0],DrainSwitch.PR[1],DrainSwitch.PR[2],DrainSwitch.PR[3],DrainSwitch.In[0],DrainSwitch.In[1],DrainSwitch.In[2],DrainSwitch.In[3]
    

Top = Circuit()
C4_Ampdet(Top,16)
#Delayline_stages(Top,rows=5,columns=3)

design_limits = [5e6, 5e6]
location_islands = ((50000,25000),(360000,25000),(220000,380000))


compile_asic(Top,process="TSMC350nm",fileName="C4_Ampdet",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 10,gateSpaceIdx=0,gateSpace=10)
