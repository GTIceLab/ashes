import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *


def DemodVMM(circuit,dim=[16,4], island=None,decoderPlace=True,loc=[0,0], inputs = None, islandLoc = [0,0]):
    if (dim[0] % 4) != 0:
            raise Exception("Error: VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)

    VMMIsland = island
    if island == None:
          VMMIsland = Island(circuit)

    # Create VMM and place in an island

    VMM = TSMC350nm_4x2_Indirect(circuit,dim=(numRows,numCols),island=VMMIsland)
    VMM.place([loc[0],loc[0]])
    #VMM.markAbut()

    Tgate_4 = ST_BMatrix(circuit,dim=(numRows,1),island=VMMIsland)
    Tgate_4.place([0,numCols+1])

    if decoderPlace == True:
        # Add decoders
        if inputs != None:
            inputs += GateDecoder.VGRUN[0:numCols*2]

        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder = STD_IndirectGateDecoder(circuit,VMMIsland,gateBits)
        GateSwitches = STD_IndirectGateSwitch(circuit,VMMIsland,numCols)

        drainBits = int(np.ceil(np.log2(dim[0])))
        DrainDecoder = STD_DrainDecoder(circuit,VMMIsland,drainBits)
        DrainSel = RunDrainSwitch(Top,VMMIsland,num=numRows)
        DrainSwitches = DrainCutoff(Top,VMMIsland,num=numRows)

    Gate_Route = Island(circuit)
    GR = Gate_Routing(circuit,dim=(1,int(dim[1]/4)),island=Gate_Route)
    GR.place([numRows+2,0])

    Mod = Island(circuit)

    Modualtion = TSMC350nm_Modulation(circuit,dim=(numRows,1),island=Mod)
    Modualtion.place([0,numCols+3]) 

    for i in range(numRows):
        Tgate_4.A[i*4] += Modualtion.I1_P[i]
        Tgate_4.A[i*4+1] += Modualtion.I1_N[i]
        Tgate_4.A[i*4+2] += Modualtion.I3_P[i]
        Tgate_4.A[i*4+3] += Modualtion.I3_N[i]

    #outerPins = frame(Top)

    outerPins = frame(Top)
    #Vin = outerPins.createPort("W","Vin")
    #Vref = outerPins.createPort("W","Vref")
    #for i in range(numStages):
    #    Vin += C4_instances[i].VIN
    #    Vref += C4_instances[i].VREF
        
    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","Run")
    VGRUN = outerPins.createPort("N","VGRUN")
    VGPROG = outerPins.createPort("N","VGPROG")


    VTUN = outerPins.createPort("N","VTUN")
    #AVDD = outerPins.createPort("N","AVDD")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    DrainlineP = outerPins.createPort("W","Drainline_Prog")
    DrainlineR = outerPins.createPort("W","Drainline_Run")
        
    #gateBits = int(np.ceil(np.log2(numCols*2)))
    GateEnable = outerPins.createPort("N","GateEnable")
    #GateB = outerPins.createPort("N","GateB",dimension=gateBits)

    DrainEnable = outerPins.createPort("W","DrainEnable")
    #DrainB = outerPins.createPort("W","DrainB",dimension=drainBits)

    '''V_NW = outerPins.createPort("N","V_NW", dimension=rows)
    V_SW = outerPins.createPort("N","V_SW", dimension=rows)
    V_NE = outerPins.createPort("N","V_NE", dimension=(rows*columns))
    V_SE = outerPins.createPort("N","V_SE", dimension=(rows*columns))'''
    #print(rows*columns)
    
    # Pin Connections
    # -------------------------------------------------------------------------------
    for i in range(2*numCols-1):
        GateSwitches.RUN_IN[i] += VGRUN
    #GateSwitches.VINJ_T[0] += GateDecoder.VINJ_b[0]
    #GateSwitches.VINJ_T[1] += GateDecoder.VINJ_b[1]
    
    #GateSwitches.GND_T[0] += GND_N
    #GateSwitches.GND_T[0] += GND_N
    #GateSwitches.GND_T[1] += GND_N
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN
    GateSwitches.vtun_l += VTUN


    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    #GateDecoder.IN += GateB

    DrainSwitches.VDD += VINJ_S
    DrainSwitches.GND += GND_S
    DrainSwitches.RUN += RUN

    DrainSel.VINJ += VINJ_N
    DrainSel.GND += GND_N
    DrainSel.prog_drainrail += DrainlineP
    DrainSel.run_drainrail += DrainlineR

    DrainDecoder.VINJ += VINJ_N
    DrainDecoder.GND += GND_N
    #for i in range(drainBits):
    #    DrainDecoder.IN[i] += DrainB[i]
    #DrainDecoder.IN += DrainB
    DrainDecoder.ENABLE += DrainEnable

    if numRows < 5:
        X_val = ((numCols-1)*27000) + 125000
        Y_val = numRows*23000
    else:
        X_val = ((numCols-1)*3000)
        Y_val = (numRows*22000) + 250000 +750

    #GateSwitches.GND_T[0] += GND_N
    #GateSwitches.VTUN_T[0] += VTUN
    
    location_islands = ((X_val,50000),(148120,182000),(2*X_val+200000,50000))              
    
    #location_islands = ((0,0),(150000,0),(150000,50000)) #successful for 8 x 4 = m x n
    #location_islands = ((0,0),(120000,0),(120000,100000)) #successful for 16 x 2 = m x n
    #location_islands = ((0,0),(180000,0),(180000,50000)) #successful for 8 x 6 = m x n
    #location_islands = ((0,0),(210000,0),(210000,50000)) #successful for 8 x 8 = m x n
    #location_islands = ((0,0),(1920000,0),(1920000,100000)) #successful for 8 x 120 = m x n 

    return location_islands

Top = Circuit()
 
design_limits = [7e5, 4e5]

location_islands = DemodVMM(Top, dim=[20,24], island=None, decoderPlace=True, loc=[0,0], inputs=None, islandLoc=[0,0])

compile_asic(Top,process="TSMC350nm",fileName="Modulation",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0)