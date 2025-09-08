import ashes_fg as af

from ashes_fg.asic.asic_compile import * # compile function required for all algorithms
from ashes_fg.class_lib_new import * # class library for standard cell definitions
import ashes_fg.class_lib_mux as lib_mux # class library for switches/decoders definitions
from ashes_fg.class_lib_cab import * # class library for CAB definitions
from ashes_fg.asic.asic_systems import * # class library for system definitions

def VMMsig(circuit,dim=[16,4], island=None,decoderPlace=True,loc=[0,0], inputs = None, islandLoc = [0,0]):

    if (dim[0] % 4) != 0:
            raise Exception("Error: VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)

    # Create VMMIsland definition

    VMMIsland = island
    if island == None:
          VMMIsland = Island(circuit)

    # Create VMM and place in above island

    VMM = TSMC350nm_4x2_Indirect(circuit,dim=(numRows,numCols),island=VMMIsland)
    VMM.place([loc[0],loc[0]])
    #VMM.markAbut()

    # Create T-Gates and place in VMMIsland

    Tgate_4 = ST_BMatrix(circuit,dim=(numRows,1),island=VMMIsland)
    Tgate_4.place([0,numCols+1])

    # Create Decoders + Gate Switches structure and place in VMMIsland abutting to VMM

    if decoderPlace == True:
        # Add decoders
        if inputs != None:
            inputs += GateDecoder.VGRUN[0:numCols*2]

        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder = STD_IndirectGateDecoder(circuit,VMMIsland,gateBits)
        GateSwitches = STD_IndirectGateSwitch(circuit,VMMIsland,numCols)

        drainBits = int(np.ceil(np.log2(dim[0])))
        
        DrainDecoder = STD_DrainDecoder(circuit,VMMIsland,drainBits)
        DrainSel = STD_DrainSelect(circuit,VMMIsland,numRows)
        DrainSwitches = STD_DrainSwitch(circuit,VMMIsland,numRows)

    # Create Termination Cell Island

    Term = Island(circuit)

    # Create Termination Cell definition and place in above island

    Termination = TSMC350nm_NeuralNetworkProgActFunc(circuit,dim=(numRows,1),island=Term)
    Termination.place([numRows,numCols+3]) 

    # Create WTA nFET Cell Island

    WTAnfetIsland = Island(circuit)

    # Create WTA nFET Cell definition and place in above island

    WTA_nfet = TSMC350nm_Termination_bot(circuit,dim=(1,1),island=WTAnfetIsland)
    WTA_nfet.place([0,numCols+4])

    # Pins -----------------------------------------------------------------------

    '''outerPins = lib_mux.frame(Top)

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

    DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("W","GateEnable")'''

    # Connections --------------------------------------------------------------

    #VMM.VINJ += VINJ_N
    #VMM.VINJ_b += VINJ_S
    #VMM.GND += GND_N
    #VMM.GND_b += GND_S
    #VMM.Prog += PROG
    #VMM.Run += RUN
    #VMM.VGRUN += VGRUN
    #VMM.VGPROG += VGPROG
    #VMM.VTUN += VTUN
    #VMM.AVDD += AVDD
    
    Tgate_4.A[0] += Termination.I1_P
    Tgate_4.A[1] += Termination.I1_N
    Tgate_4.A[2] += Termination.I3_P
    Tgate_4.A[3] += Termination.I3_N

    WTA_nfet.GATE += Termination.VC

    if numRows < 5:
        X_val = ((numCols-1)*27000) + 115000
        Y_val = numRows*23000
    else:
        X_val = ((numCols-1)*27000) + 115000 + 117000
        Y_val = (numRows*22000) + 750
    
    location_islands = ((0,0),(X_val,0),(X_val,Y_val))

    #location_islands = ((0,0),(X_val,0),(X_val,Y_val)), (250600, 4500000), (20600, 20000))

    return location_islands


Top = Circuit()

design_limits = [3e6, 3e6] # if algorithm takes long to run, adjust these parameters

# dim=[m,n] for m x n input VMM
# dimensions must be multiples of 4 and 2 respectively

location_islands = VMMsig(Top, dim=[240,80], island=None, decoderPlace=True, loc=[0,0], inputs=None, islandLoc=[0,0]) 

compile_asic(Top,process="TSMC350nm",fileName="IndirectVMM",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0) # drainSpace is space between drain mux/decoders and VMM, gateSpace is space between gate mux/decoders and VMM