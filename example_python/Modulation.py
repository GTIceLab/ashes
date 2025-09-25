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

    Mod = Island(circuit)

    Modualtion = TSMC350nm_Modulation(circuit,dim=(numRows,1),island=Mod)
    Modualtion.place([numRows,numCols+3]) 

    for i in range(numRows):
        Tgate_4.A[4*i] += Modualtion.I1_P[i]
        Tgate_4.A[4*i+1] += Modualtion.I1_N[i]
        Tgate_4.A[4*i+2] += Modualtion.I3_P[i]
        Tgate_4.A[4*i+3] += Modualtion.I3_N[i]

    outerPins = frame(Top)

    '''VTUN = outerPins.createPort("N","VTUN")
    AVDD = outerPins.createPort("N","AVDD")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N

    DrainSwitches.VDD += VINJ_S
    DrainSwitches.GND += GND_S

    DrainSel.VINJ_b += VINJ_N
    DrainSel.GND_b += GND_N

    DrainDecoder.VINJ += VINJ_S
    DrainDecoder.GND += GND_S'''

    if numRows < 5:
        X_val = ((numCols-1)*27000) + 125000
        Y_val = numRows*23000
    else:
        X_val = ((numCols-1)*3000)
        Y_val = (numRows*22000) + 250000 +750

    #GateSwitches.GND_T[0] += GND_N
    #GateSwitches.VTUN_T[0] += VTUN
    
    location_islands = ((X_val,500000),(2*X_val+4250000,500000),(2*X_val,Y_val))              
    
    #location_islands = ((0,0),(150000,0),(150000,50000)) #successful for 8 x 4 = m x n
    #location_islands = ((0,0),(120000,0),(120000,100000)) #successful for 16 x 2 = m x n
    #location_islands = ((0,0),(180000,0),(180000,50000)) #successful for 8 x 6 = m x n
    #location_islands = ((0,0),(210000,0),(210000,50000)) #successful for 8 x 8 = m x n
    #location_islands = ((0,0),(1920000,0),(1920000,100000)) #successful for 8 x 120 = m x n 


    return location_islands

Top = Circuit()
 
design_limits = [10e6, 10e6]

location_islands = DemodVMM(Top, dim=[300,320], island=None, decoderPlace=True, loc=[0,0], inputs=None, islandLoc=[0,0])

compile_asic(Top,process="TSMC350nm",fileName="Modulation",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0)