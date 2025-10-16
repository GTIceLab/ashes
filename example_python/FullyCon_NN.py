import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np

def FullyCon_Layer(circuit,input_size=10,no_of_neurons=10,FNN_Island=None,islandLoc=[0,0],debug=False):

    Top = circuit
    FNN_Island = ac.Island(Top)

    # Make sure the Input and neuron size can be created with 4x2 core cell
    if ((input_size % 2) !=0):
        raise Exception("Error: The input size should be divisible by 2")
    elif (no_of_neurons < 2):
        raise Exception("Error: No of neurons should be greater than 2")
    elif ((no_of_neurons % 2) !=0):
        raise Exception("Error: No of neurons should be divisible by 2")
    
    #################  Defining VMM for the Neurons #################
    VMM_fr_Neurons = lib_new.TSMC350nm_4x2_Indirect(Top,FNN_Island,dim=[(no_of_neurons*2)//4,input_size//2])
    VMM_fr_Neurons.place([0,0])
    VMM_fr_Neurons.markAbut()
    track_col = input_size//2

    #################  Defining Diodeconnected FETs on the TA/Neuron inputs #################
    Diodeconn_fr_Neurons = lib_new.FNN_DiodeConn(Top,FNN_Island,dim=[(no_of_neurons*2)//4,1])
    Diodeconn_fr_Neurons.place([0,track_col])
    Diodeconn_fr_Neurons.markAbut()
    track_col = track_col + 1

    #################  Defining Neurons #################
    Neurons = lib_new.FNN_Relu_and_Sig(Top,FNN_Island,dim=[no_of_neurons//2,1])
    Neurons.place([0,track_col])
    Neurons.markAbut()
    track_col = track_col + 1


    #################  Defining GateSwcs, DrainSwcs and Decoders  #################
    GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,FNN_Island,input_size//2)
    gateBits = int(np.ceil(np.log2(input_size)))
    GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,FNN_Island,gateBits)

    drainBits = int(np.ceil(np.log2(no_of_neurons//2)))
    DrainDecoder = lib_mux.STD_DrainDecoder(circuit,FNN_Island,drainBits)
    DrainSel = lib_mux.STD_DrainSelect(circuit,FNN_Island,(no_of_neurons*2)//4)
    DrainSwitches = lib_mux.STD_DrainSwitch(circuit,FNN_Island,(no_of_neurons*2)//4)


    # Island Placement
    # -------------------------------------------------------------------------------

    #location_islands = (islandLoc[0],islandLoc[1])

    #return location_islands


Top = ac.Circuit()
FullyCon_Layer(Top,islandLoc=[100,100],debug=True)

location_islands = ((100,100),(0,0))

design_limits = [4e7, 4e7]

ac.compile_asic(Top,process="TSMC350nm", fileName="FullyCon_NN", p_and_r = True, route=False, design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0)

