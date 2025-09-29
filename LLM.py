import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.class_lib_LLM as lib_LLM
import ashes_fg.asic.asic_systems as algs

import numpy as np

def Q_Layer(circuit, numStages=1,dim=[4,2],island=None,islandLoc = [0,0],decoderPlace=False, inputs=None):
    if (dim[0] % 4) != 0:
            raise Exception("Error: Q Layer VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: Q Layer VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)
    
    Q_Layer_Island = island
    if island == None:
         Q_Layer_Island = Island(circuit)

    Q_VMM = lib_new.TSMC350nm_4x2_Indirect(Top,Q_Layer_Island,dim=[numRows,numCols])
    Q_VMM.place([islandLoc[0],islandLoc[1]])

    Q_Output = lib_LLM.Q_layer_output(Top,Q_Layer_Island,dim=[numRows,1])
    Q_Output.place([islandLoc[0],islandLoc[1]+numCols])

    if decoderPlace == True:
         gateBits = int(np.ceil(np.log2(dim[1])))
         GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,Q_Layer_Island,gateBits)
         GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,Q_Layer_Island,numCols)

         drainBits = int(np.ceil(np.log2(dim[0])))
         DrainDecoder = lib_mux.STD_DrainDecoder(circuit,Q_Layer_Island,drainBits)
         DrainSel = lib_mux.STD_DrainSelect(circuit,Q_Layer_Island,numRows)
         DrainSwitches = lib_mux.STD_DrainSwitch(circuit,Q_Layer_Island,numRows)
    return Q_VMM

def K_Layer(circuit, numStages=1,dim=[4,2],island=None,islandLoc = [0,0],decoderPlace=False, inputs=None):
    if (dim[0] % 4) != 0:
            raise Exception("Error: Q Layer VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: Q Layer VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)
    
    K_Layer_Island = island
    if island == None:
         K_Layer_Island = Island(circuit)

    K_Output = lib_LLM.K_layer_output(Top,K_Layer_Island,dim=[numRows,1])
    K_Output.place([islandLoc[0],islandLoc[1]])

    K_VMM = lib_new.TSMC350nm_4x2_Indirect(Top,K_Layer_Island,dim=[numRows,numCols])
    K_VMM.place([islandLoc[0],islandLoc[1]+1])

    

    if decoderPlace == True:
         gateBits = int(np.ceil(np.log2(dim[1])))
         GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,K_Layer_Island,gateBits)
         GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,K_Layer_Island,numCols)

         #drainBits = int(np.ceil(np.log2(dim[0])))
         #DrainDecoder = lib_mux.STD_DrainDecoder(circuit,K_Layer_Island,drainBits)
         #DrainSel = lib_mux.STD_DrainSelect(circuit,K_Layer_Island,numRows)
         #DrainSwitches = lib_mux.STD_DrainSwitch(circuit,K_Layer_Island,numRows)
    return K_VMM

def DotprodArray(circuit,numStages=1,p=0,q=0,m=0,island=None,islandLoc = [0,0]):
    DotprodIsland = island
    if island == None:
        DotprodIsland = ac.Island(circuit)
    dotprod_L = lib_LLM.dotproduct_L(circuit,DotprodIsland,dim=[p,1])
    dotprod_L.place([islandLoc[0],islandLoc[1]])

    dotprod_mid = lib_LLM.dotproduct_mid(circuit,DotprodIsland,dim=[p,m-2])
    dotprod_mid.place([islandLoc[0],islandLoc[1]+1])

    dotprod_R = lib_LLM.dotproduct_R(circuit, DotprodIsland,dim=[p,1])
    dotprod_R.place([islandLoc[0],islandLoc[1]+m-1])

#keep m>=3 for now

def DiscTimeTransformer(circuit,numStages=1,p=0,q=0,m=0,island=None,islandLoc = [0,0],decoderPlace=False):
    
    SaliencyIsland = island
    if island == None:
        SaliencyIsland = ac.Island(circuit)
    
    Q_layer = Q_Layer(circuit,dim=[p,q],island=SaliencyIsland,islandLoc = [islandLoc[0], islandLoc[1]], decoderPlace=decoderPlace)
    DotProduct = DotprodArray(circuit,p=p,q=q,m=m,island=SaliencyIsland,islandLoc = [islandLoc[0],islandLoc[1]+q+1])
    '''
    Q_layer = lib_new.TSMC350nm_4x2_Indirect(Top,SaliencyIsland,dim=[p,q])
    Q_layer.place([islandLoc[0],islandLoc[1]])
    
    Q_output = lib_LLM.Q_layer_output(Top,SaliencyIsland,dim=[p,1])
    Q_output.place([islandLoc[0],islandLoc[1]+q])
    
    Dotproduct = DotprodArray(circuit,p=p,q=q,m=m,island=SaliencyIsland,islandLoc = [islandLoc[0],islandLoc[1]+q+1])

    K_output = lib_LLM.K_layer_output(Top,SaliencyIsland,dim=[p,1])
    K_output.place([islandLoc[0],islandLoc[1]+1+q+m+1])

    K_layer = lib_new.TSMC350nm_4x2_Indirect(Top,SaliencyIsland,dim=[p,q])
    K_layer.place([islandLoc[0],islandLoc[1]+1+q+m+2])
    
    output

    SoftWTAOut = lib_new.TSMC350nm_4SoftWTA_IndirectProg_Vertical(Top,SaliencyIsland,dim=[1,q])
    SoftWTAOut.place([islandLoc[0],islandLoc[1]])
    '''
    # Pins
    # -------------------------------------------------------------------------------
    #outerPins = lib_mux.frame(Top)

    # Pin Connections
    # -------------------------------------------------------------------------------

    
    
    # Island Placement
    # -------------------------------------------------------------------------------
    #Pitch = 22000
    X = islandLoc[0]
    Y = islandLoc[1]
    K_output_width = 9550
    #location_islands = ((X,Y),(X+Pitch,Y),(X+(m-1)*Pitch,Y),(X+m*Pitch,Y),(X+m*Pitch+K_output_width,Y))
    location_islands = ((X,Y))
    return location_islands


Top = ac.Circuit()

#location_islands = Transformer(Top,1,islandLoc=[50000,25000])
design_limits = [62e5, 42e5]
DiscTimeTransformerCircuit = DiscTimeTransformer(Top,p=16,q=8,m=4,decoderPlace=True)
location_islands=None
ac.compile_asic(Top,process="TSMC350nm",fileName="DiscTimeSaliency",p_and_r = True,design_limits = design_limits, location_islands = location_islands)




