import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *



def C4_Ampdet(circuit,numStages=1,LPFIsland=None):

    Top = circuit
    # Placement
    if LPFIsland == None:
        LPFIsland = Island(Top)
        
    FakeIsland=Island(Top)
    FakeCell0 = FakeCellGateDecoder(Top,FakeIsland)
    FakeCell0.place([0,0])
    FakeCell0.markAbut()
    FakeCell1 = FakeCellGateDecoder(Top,FakeIsland)
    FakeCell1.place([0,1])
    FakeCell1.markAbut()
     
    GateDecoder = STD_IndirectGateDecoder(Top,FakeIsland,2)
    GateSwitches = STD_IndirectGateSwitch(Top,FakeIsland,2)
        
        
    C4_instances = [0]*numStages
    Ampdet_instances = [0]*numStages
    for i in range(numStages):
        C4_instances[i] = "C4_"+str(i)
    for i in range(numStages):
        Ampdet_instances[i] = "Ampdet_"+str(i)
        
    for i in range(numStages):
        C4_instances[i] = TSMC350nm_C4(Top,LPFIsland)
        Ampdet_instances[i] = TSMC350nm_Ampdet_NoFG(Top,LPFIsland)
        C4_instances[i].place([i,0])
        Ampdet_instances[i].place([i,1])
        C4_instances[i].OUTPUT += Ampdet_instances[i].VIN
        
    # FG Programming
    # -------------------------------------------------------------------------------
    drainBits = int(np.ceil(np.log2(numStages*4)))
    DrainDecoder = STD_DrainDecoder(Top,LPFIsland,bits=drainBits)
    DrainSelect = RunDrainSwitch(Top,LPFIsland,num=numStages)
    DrainSwitch = DrainCutoff(Top,LPFIsland,num=numStages)

    # Connect program drains to drain switch
    for i in range(numStages):
        DrainSwitch.PR[4*i] += C4_instances[i].VD_P[0]
        DrainSwitch.PR[(4*i)+1] += C4_instances[i].VD_P[1]
        DrainSwitch.PR[(4*i)+2] += Ampdet_instances[i].VD_P[0]
        DrainSwitch.PR[(4*i)+3] += Ampdet_instances[i].VD_P[1]
        
    #GateDecoder = STD_IndirectGateDecoder(Top,LPFIsland,2)
    #GateSwitches = STD_IndirectGateSwitch(Top,LPFIsland,2)

    GateSwitches.Vg[0] += C4_instances[0].Vg[0]
    GateSwitches.Vg[1] += C4_instances[0].Vg[1]
    GateSwitches.Vg[2] += Ampdet_instances[0].Vg
    GateSwitches.CTRL_B[0] += C4_instances[0].Vsel[0]
    GateSwitches.CTRL_B[1] += C4_instances[0].Vsel[1]
    GateSwitches.CTRL_B[2] += Ampdet_instances[0].Vsel
    
    GateSwitches.VINJ[0] += C4_instances[0].VINJ
    GateSwitches.GND[0] += C4_instances[0].GND
    GateSwitches.VTUN[0] += C4_instances[0].VTUN
    GateSwitches.VDD[1] += C4_instances[0].VPWR
    
    GateSwitches.VINJ[1] += Ampdet_instances[0].VINJ
    GateSwitches.GND[1] += Ampdet_instances[0].GND
    GateSwitches.VTUN[1] += Ampdet_instances[0].VTUN
    GateSwitches.VDD[3] += Ampdet_instances[0].VPWR
    

    #Outerpins
    
    outerPins = frame(Top)
    Vin = outerPins.createPort("W","Vin")
    Vref = outerPins.createPort("W","Vref")
    for i in range(numStages):
        Vin += C4_instances[i].VIN
        Vref += C4_instances[i].VREF
        
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
    GateSwitches.VTUN_T[0] += VTUN
    GateSwitches.VTUN_T[1] += VTUN
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateB

    DrainSwitch.VDD_b += VINJ_S
    DrainSwitch.GND_b += GND_S
    DrainSwitch.RUN_b += RUN

    DrainSelect.VINJ += VINJ_N
    DrainSelect.GND += GND_N
    DrainSelect.prog_drainrail += Drainline

    DrainDecoder.VINJ += VINJ_N
    DrainDecoder.GND += GND_N
    #for i in range(drainBits):
    #    DrainDecoder.IN[i] += DrainB[i]
    DrainDecoder.IN += DrainB
    DrainDecoder.ENABLE += DrainEnable

    C4_instances[0].PROG += PROG
    C4_instances[0].RUN += RUN

    Ampdet_out = [0]*numStages
    for i in range(numStages):
        Ampdet_out[i] = Ampdet_instances[i].OUTPUT
        
    DrainPR0 = [0]*numStages
    DrainPR1 = [0]*numStages
    DrainPR2 = [0]*numStages
    DrainPR3 = [0]*numStages
    DrainRun0 = [0]*numStages
    DrainRun1 = [0]*numStages
    DrainRun2 = [0]*numStages
    DrainRun3 = [0]*numStages
    for i in range(numStages):
        DrainPR0 = DrainSwitch.PR[4*i]
        DrainPR1 = DrainSwitch.PR[(4*i)+1]
        DrainPR2 = DrainSwitch.PR[(4*i)+2]
        DrainPR3 = DrainSwitch.PR[(4*i)+3]
        DrainRun0 = DrainSwitch.In[4*i]
        DrainRun1 = DrainSwitch.In[(4*i)+1]
        DrainRun2 = DrainSwitch.In[(4*i)+2]
        DrainRun3 = DrainSwitch.In[(4*i)+3]
        
    return Ampdet_out,DrainPR0,DrainPR1,DrainPR2,DrainPR3,DrainRun0,DrainRun1,DrainRun2,DrainRun3
    

Top = Circuit()
C4_Ampdet(Top,32)
#Delayline_stages(Top,rows=5,columns=3)

design_limits = [5e6, 5e6]
location_islands = ((50000,25000),(280000,740000))


compile_asic(Top,process="TSMC350nm",fileName="C4_Ampdet",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=10)
