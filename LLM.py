import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
#import ashes_fg.class_lib_cab as lib_cab
#import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.class_lib_LLM as lib_LLM
#import ashes_fg.asic.asic_systems as algs

import numpy as np

def Q_Layer(circuit, dim=[4,2],island=None,islandLoc = [0,0],decoderPlace=False, inputs=None):
    if (dim[0] % 4) != 0:
            raise Exception("Error: Q Layer VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: Q Layer VMM columns must be divisible by 2")
    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)
    
    Q_Layer_Island = island
    if island == None:
         Q_Layer_Island = island(circuit)

    Q_VMM = lib_new.TSMC350nm_4x2_Indirect(circuit,Q_Layer_Island,dim=[numRows,numCols])
    Q_VMM.place([islandLoc[0],islandLoc[1]])
    Q_Output = lib_LLM.Q_layer_output(circuit,Q_Layer_Island,dim=[numRows,1])
    Q_Output.place([islandLoc[0],islandLoc[1]+numCols])

    if decoderPlace == True:
        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder_Q = lib_mux.STD_IndirectGateDecoder(circuit,Q_Layer_Island,gateBits)
        GateSwitches_Q = lib_mux.STD_IndirectGateSwitch(circuit,Q_Layer_Island,numCols)

        if inputs != None:
            inputs += GateDecoder_Q.VGRUN[0:numCols*2]

        drainBits = int(np.ceil(np.log2(dim[0])))
        DrainDecoder_Q = lib_mux.STD_DrainDecoder(circuit,Q_Layer_Island,drainBits)
        DrainSel_Q = lib_mux.STD_DrainSelect(circuit,Q_Layer_Island,numRows)
        DrainSwitches_Q = lib_mux.STD_DrainSwitch(circuit,Q_Layer_Island,numRows)
    return {
         "gateBits": gateBits,
         "GateSwitches_Q": GateSwitches_Q,
         "GateDecoder_Q": GateDecoder_Q,
         "DrainDecoder_Q": DrainDecoder_Q,
         "DrainSel_Q": DrainSel_Q,
         "DrainSwitches_Q": DrainSwitches_Q,
         "Q_Output": Q_Output,
         "drainBits": drainBits
    }

def K_Layer(circuit, dim=[4,2],island=None,islandLoc = [0,0],decoderPlace=False, inputs=None):
    if (dim[0] % 4) != 0:
            raise Exception("Error: Q Layer VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: Q Layer VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)
    
    K_Layer_Island = island
    if island == None:
         K_Layer_Island = island(circuit)

    #K_Output = lib_LLM.K_layer_output(circuit,K_Layer_Island,dim=[numRows,1])
    #K_Output.place([islandLoc[0],islandLoc[1]])

    K_VMM = lib_new.TSMC350nm_4x2_Indirect(circuit,K_Layer_Island,dim=[numRows,numCols])
    #K_VMM.place([islandLoc[0],islandLoc[1]+1])
    K_VMM.place([islandLoc[0],islandLoc[1]])

    if decoderPlace == True:
        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder_K = lib_mux.STD_IndirectGateDecoder(circuit,K_Layer_Island,gateBits)
        GateSwitches_K = lib_mux.STD_IndirectGateSwitch(circuit,K_Layer_Island,numCols)

        if inputs != None:
            inputs += GateDecoder_K.VGRUN[0:numCols*2]

        drainBits = int(np.ceil(np.log2(dim[0])))
        DrainDecoder = lib_mux.STD_DrainDecoder(circuit,K_Layer_Island,drainBits)
        DrainSel = lib_mux.STD_DrainSelect(circuit,K_Layer_Island,numRows)
        DrainSwitches = lib_mux.STD_DrainSwitch(circuit,K_Layer_Island,numRows)
    return {
         "gateBits": gateBits,
         "GateSwitches": GateSwitches_K,
         "GateDecoder": GateDecoder_K,
         "DrainDecoder": DrainDecoder,
         "DrainSel": DrainSel,
         "DrainSwitches": DrainSwitches,
         "drainBits": drainBits
    }

def DotprodArray(circuit,dim=[4,2],island=None,islandLoc = [0,0]):
    if (dim[0] % 4) != 0:
            raise Exception("Error: Q Layer VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: Q Layer VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)
    
    DotprodIsland = island
    if island == None:
        DotprodIsland = ac.Island(circuit)
    dotprod_L = lib_LLM.dotproduct_L(circuit,DotprodIsland,dim=[numRows,1])
    dotprod_L.place([islandLoc[0],islandLoc[1]])

    dotprod_mid = lib_LLM.dotproduct_mid(circuit,DotprodIsland,dim=[numRows,numCols-2])
    dotprod_mid.place([islandLoc[0],islandLoc[1]+1])

    dotprod_R = lib_LLM.dotproduct_R(circuit, DotprodIsland,dim=[numRows,1])
    dotprod_R.place([islandLoc[0],islandLoc[1]+numCols-1])

    K_Output = lib_LLM.K_layer_output(circuit,DotprodIsland,dim=[numRows,1])
    K_Output.place([islandLoc[0],islandLoc[1]+numCols])

    return {
         "dotprod_L": dotprod_L,
         "dotprod_mid": dotprod_mid,
         "dotprod_R": dotprod_R,
         "K_Output": K_Output
    }

def SampleControl(circuit,dim=[0,0],island=None,islandLoc = [0,0]):
    
    numCols = int(dim[1]/2)
    
    SampleControlIsland = island
    if island == None:
        SampleControlIsland = ac.Island(circuit)
    SampleControl_L = lib_LLM.SampleControl(circuit,SampleControlIsland,dim=[1,1])
    SampleControl_L.place([islandLoc[0],islandLoc[1]])

    SampleControl_mid = lib_LLM.SampleControl(circuit,SampleControlIsland,dim=[1,numCols-2])
    SampleControl_mid.place([islandLoc[0],islandLoc[1]+1])

    SampleControl_R = lib_LLM.SampleControl(circuit, SampleControlIsland,dim=[1,1])
    SampleControl_R.place([islandLoc[0],islandLoc[1]+numCols-1])

    return {
         "SampleControl_L": SampleControl_L,
         "SampleControl_mid": SampleControl_mid,
         "SampleControl_R": SampleControl_R
    }

def Input_Layer(circuit, dim=[4,2],island=None,islandLoc = [0,0],decoderPlace=False, inputs=None):
    if (dim[0] % 4) != 0:
            raise Exception("Error: Input Layer VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: Input Layer VMM columns must be divisible by 2")
    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)
    
    Input_Layer_Island = island
    if island == None:
         Input_Layer_Island = island(circuit)

    Input_VMM = lib_new.TSMC350nm_4x2_Indirect(circuit,Input_Layer_Island,dim=[numRows,numCols])
    Input_VMM.place([islandLoc[0],islandLoc[1]])

    if decoderPlace == True:
        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder_InputVMM = lib_mux.STD_IndirectGateDecoder(circuit,Input_Layer_Island,gateBits)
        GateSwitches_InputVMM = lib_mux.STD_IndirectGateSwitch(circuit,Input_Layer_Island,numCols)

        if inputs != None:
            inputs += GateDecoder_InputVMM.VGRUN[0:numCols*2]

        drainBits = int(np.ceil(np.log2(dim[0])))
        DrainDecoder_InputVMM = lib_mux.STD_DrainDecoder(circuit,Input_Layer_Island,drainBits)
        DrainSel_InputVMM = lib_mux.STD_DrainSelect(circuit,Input_Layer_Island,numRows)
        DrainSwitches_InputVMM = lib_mux.STD_DrainSwitch(circuit,Input_Layer_Island,numRows)
    return {
         "Input_VMM": Input_VMM,
         "GateSwitches": GateSwitches_InputVMM,
         "GateDecoder": GateDecoder_InputVMM,
         "DrainDecoder": DrainDecoder_InputVMM,
         "DrainSel": DrainSel_InputVMM,
         "DrainSwitches": DrainSwitches_InputVMM,
         "gateBits": gateBits,
         "drainBits": drainBits
    }
#keep m>=3 for now
#check edge cases later pls

def DiscTimeTransformer(circuit,numStages=1,p=0,q=0,m=0,r=0,island=None,islandLoc = [0,0],decoderPlace=False):
    
    Input_Island = ac.Island(circuit)
    Input_layer = Input_Layer(circuit,dim=[q,r],island=Input_Island,islandLoc=[islandLoc[0],islandLoc[1]],decoderPlace=decoderPlace)
    
    SaliencyIsland = ac.Island(circuit)
    Q_layer = Q_Layer(circuit,dim=[p,q],island=SaliencyIsland,islandLoc = [islandLoc[0], islandLoc[1]],decoderPlace=decoderPlace) #,inputs=Input_layer["Input_VMM"].Vd_R
    DotProduct = DotprodArray(circuit,dim=[p,m],island=SaliencyIsland,islandLoc = [islandLoc[0],islandLoc[1]+q+1])

    K_Island = ac.Island(circuit)
    K_layer = K_Layer(circuit,dim=[p,q],island=K_Island,islandLoc = [0,0],decoderPlace=decoderPlace)
    
    SampleControl_Island = ac.Island(circuit)
    #SampleController=SampleControl(circuit,dim=[1,m],island=SampleControl_Island,islandLoc=[0,0])
    SampleControl_L=lib_LLM.SampleControl(circuit,SampleControl_Island,dim=[1,1])
    SampleControl_L.place([0,0])
    SampleControl_mid=lib_LLM.SampleControl(circuit,SampleControl_Island,dim=[1,int(m/2)-2]) #int(m/2)
    SampleControl_mid.place([0,1])
    SampleControl_R=lib_LLM.SampleControl(circuit,SampleControl_Island,dim=[1,1]) #int(m/2)
    num=int(m/2)
    SampleControl_R.place([0,1+int(m/2)-2])
    
    Q_Output_ScannerIsland = ac.Island(circuit)
    Q_Output_Scanner = lib_LLM.HorizontalScanner(circuit,island=Q_Output_ScannerIsland,dim=[1,int(m/2)])
    Q_Output_Scanner.place([0,0])

    K_Output_ScannerIsland = ac.Island(circuit)
    K_Output_Scanner = lib_LLM.HorizontalScanner(circuit,island=K_Output_ScannerIsland,dim=[1,int(m/2)])
    K_Output_Scanner.place([0,0])
    
    # Pins
    # -------------------------------------------------------------------------------
    outerPins = lib_mux.frame(Top)
    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","RUN")
    VGPROG = outerPins.createPort("N","VGPROG")
    VGRUN = outerPins.createPort("N","VGRUN")
    VTUN = outerPins.createPort("N","VTUN")
    AVDD_N = outerPins.createPort("N","avdd")
    AVDD_S = outerPins.createPort("S","avdd")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")
    
    #Input VMM Decoder Pins & Input
    INPUT_VMM = {}
    for i in range(r):
        name = f"InputVMM{i}"
        INPUT_VMM[i] = outerPins.createPort("N", name)

    INPUT_GATEBIT = {}
    for i in range(Input_layer["gateBits"]):
        name = f"INPUT_GATEBIT{i}"
        INPUT_GATEBIT[i] = outerPins.createPort("W", name)
    
    INPUT_DRAINBIT = {}
    for i in range(Input_layer["drainBits"]):
        name = f"INPUT_DRAINBIT{i}"
        INPUT_DRAINBIT[i] = outerPins.createPort("W", name)
        
    #Q Layer Decoder Pins
    
    Q_DRAINBIT = {}
    for i in range(Q_layer["drainBits"]):
        name = f"Q_DRAINBIT{i}"
        Q_DRAINBIT[i] = outerPins.createPort("N", name)

    Q_GATEBIT = {}
    for i in range(Q_layer["gateBits"]):
        name = f"Q_GATEBIT{i}"
        Q_GATEBIT[i] = outerPins.createPort("N", name)
    
    Q_ENABLE = outerPins.createPort("N","Q_enable")

    #Q Layer Output Bias Pins
    VBIAS = outerPins.createPort("E","vbias")
    VDBIAS = outerPins.createPort("E","vdbias")
    VGBIAS = outerPins.createPort("E","vgbias")

    #Sample Controller Pins
    CLK = outerPins.createPort("S","CLK")
    SAMPLE = outerPins.createPort("S","Sample")
    Q = outerPins.createPort("S","Q")
    D = outerPins.createPort("S","D")
    


    # Pin Connections
    # -------------------------------------------------------------------------------
    
    VINJ_N += VINJ_S
    GND_N += GND_S
    
    
    Q_layer["GateSwitches_Q"].RUN += RUN
    Q_layer["GateSwitches_Q"].PROG += PROG
    Q_layer["GateSwitches_Q"].Vgsel += VGPROG
    Q_layer["GateDecoder_Q"].ENABLE += Q_ENABLE
    Q_layer["GateDecoder_Q"].VINJV += VINJ_N
    '''
    for i in range(Q_layer["gateBits"]): 
        Q_layer["GateDecoder_Q"].IN[i] += Q_GATEBIT[i]
    for i in range(Q_layer["drainBits"]): 
        Q_layer["DrainDecoder_Q"].IN[i] += Q_DRAINBIT[i]
    '''
    Q_layer["Q_Output"].Vbias[0] += VBIAS
    Q_layer["Q_Output"].Vbias[1] += VBIAS
    Q_layer["Q_Output"].Vdbias[0] += VDBIAS
    Q_layer["Q_Output"].Vdbias[1] += VDBIAS
    Q_layer["Q_Output"].Vgbias += VGBIAS
    Q_layer["Q_Output"].VPWR[0] += Q_layer["Q_Output"].VPWR[1]
    Q_layer["Q_Output"].VPWR[1] += AVDD_N
    Q_layer["Q_Output"].GND[0] += GND_N
    Q_layer["Q_Output"].GND[1] += GND_N
    Q_layer["Q_Output"].Q_out[0] += Q_Output_Scanner.In[0]
    Q_layer["Q_Output"].Q_out[1] += Q_Output_Scanner.In[1]
    Q_layer["Q_Output"].Q_out[2] += Q_Output_Scanner.In[2]
    Q_layer["Q_Output"].Q_out[3] += Q_Output_Scanner.In[3]
    #DotProduct["K_Output"].K[0] += K_Output_Scanner.In[0]
    #DotProduct["K_Output"].K[1] += K_Output_Scanner.In[1]
    #DotProduct["K_Output"].K[2] += K_Output_Scanner.In[2]
    #DotProduct["K_Output"].K[3] += K_Output_Scanner.In[3]

    '''
    #Input VMM Connections
    for i in range(Input_layer["gateBits"]):
        Input_layer["GateDecoder"].IN[i] += INPUT_GATEBIT[i]
    
    for i in range(r):
        Input_layer["GateDecoder"].VGRUN[i] += INPUT_VMM[i]
    for i in range(Input_layer["drainBits"]):
        Input_layer["DrainDecoder"].IN[i] += INPUT_DRAINBIT[i] 
    '''
    SampleControl_L.phi1 += DotProduct["dotprod_L"].phi1_B
    SampleControl_R.phi1 += DotProduct["dotprod_R"].phi1_B
    SampleControl_mid.phi1 += DotProduct["dotprod_mid"].phi1_B
    SampleControl_L.phi2 += DotProduct["dotprod_L"].phi2_B
    SampleControl_R.phi2 += DotProduct["dotprod_R"].phi2_B
    SampleControl_mid.phi2 += DotProduct["dotprod_mid"].phi2_B
    SampleControl_L.GND += DotProduct["dotprod_L"].GND_B
    SampleControl_R.GND += DotProduct["dotprod_R"].GND_B
    SampleControl_mid.GND += DotProduct["dotprod_mid"].GND_B
    
    AVDD_N += AVDD_S
    #SampleControl_L.VDD +=AVDD_N
    #SampleControl_L.VDD +=AVDD_S
    SampleControl_L.CLK += CLK
    SampleControl_L.Sample += SAMPLE
    SampleControl_L.D += D
    SampleControl_L.Q += Q
    SampleControl_R.GND += GND_S

    #K_layer.Vd_R[0] += TEST
    
    
    
    # Island Placement
    # -------------------------------------------------------------------------------
    Pitch = 22000
    X = islandLoc[0]
    Y = islandLoc[1]
    draindec_width = 100000
    gatedec_height = 100000
    vmm_width = 27460
    Q_output_width = 112460
    K_output_width = 9550

    SampleControl_height = 60000

    location_islands = ((20000,SampleControl_height),
                        (20000+draindec_width+vmm_width*int(r/2)+20000,SampleControl_height),
                        (20000+draindec_width+vmm_width*int(r/2)+20000+draindec_width+vmm_width*int(q/2)+Q_output_width+int(m/2)*Pitch+K_output_width+50000,SampleControl_height), 
                        (20000+draindec_width+vmm_width*int(r/2)+20000+draindec_width+vmm_width*int(q/2)+Q_output_width,0),
                        (20000+draindec_width+vmm_width*int(r/2)+20000,SampleControl_height+int(p/4)*Pitch+gatedec_height+100000),
                        (20000+draindec_width+vmm_width*int(r/2)+20000+draindec_width+vmm_width*int(q/2)+Q_output_width+int(m/2)*Pitch+K_output_width+50000,SampleControl_height+int(p/4)*Pitch+gatedec_height+100000))
    return location_islands


Top = ac.Circuit()

#location_islands = Transformer(Top,1,islandLoc=[50000,25000])
design_limits = [1e7, 1e7]
location_islands = DiscTimeTransformer(Top,p=600,q=100,m=100,r=100,decoderPlace=True)
ac.compile_asic(Top,process="TSMC350nm",fileName="DiscTimeSaliency",p_and_r = True,design_limits = design_limits, location_islands = location_islands)




