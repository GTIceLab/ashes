import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np
import json

def FullyCon_Layer(circuit,input_size=128,no_of_neurons=80,FNN_Island=None,islandLoc=[0,0],debug=False):

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
    track_col = input_size//2

    #################  Defining Diodeconnected FETs on the TA/Neuron inputs #################
    Diodeconn_fr_Neurons = lib_new.FNN_DiodeConn(Top,FNN_Island,dim=[(no_of_neurons*2)//4,1])
    Diodeconn_fr_Neurons.place([0,track_col])
    track_col = track_col + 1

    #################  Defining Neurons #################
    Neurons = lib_new.FNN_Relu_and_Sig(Top,FNN_Island,dim=[no_of_neurons//2,1])
    Neurons.place([0,track_col])
    track_col = track_col + 1

    #################  ScanChain for Neuron Debug  #################
    Neuron_scanner_Island = ac.Island(Top)

    Neuron_scanner = lib_new.TSMC350nm_VerticalScanner(Top,Neuron_scanner_Island,dim=[no_of_neurons//2,1])
    Neuron_scanner.place([0,0])

    #track_col = track_col + 1

    #################  Outer Pins  #################
    # outerPins = frame(Top)

    # ## G/D Decoder and Swcs Signals
    # FNN_G_En = outerPins.createPort("N","FNN_G_En")
    # FNN_G_bit = outerPins.createPort("N","FNN_G_bit",dimension= int(np.ceil(np.log2(input_size))))

    # FNN_Dr_En = outerPins.createPort("N","FNN_Dr_En")
    # FNN_Dr_bit = outerPins.createPort("N","FNN_Dr_bit",dimension= int(np.ceil(np.log2(no_of_neurons*2))))

    # FNN_Prog_Drln = outerPins.createPort("N","FNN_Prog_Drln")
    # FNN_Run_Drln = outerPins.createPort("N","FNN_Run_Drln")


    # FNN_ActF_G_En = outerPins.createPort("N","FNN_ActF_G_En")
    # FNN_ActF_G_bit = outerPins.createPort("N","FNN_ActF_G_bit",dimension=2)


    # ## Global Signals
    # VTUN = outerPins.createPort("N","VTUN")
    # DVDD = outerPins.createPort("N","DVDD")
    # AVDD = outerPins.createPort("N","AVDD")
    # GND = outerPins.createPort("N","GND")
    # VINJ = outerPins.createPort("N","VINJ")

    # VGPROG = outerPins.createPort("N","VGPROG")
    # VGRUN = outerPins.createPort("N","VGRUN")

    # prog_hv = outerPins.createPort("N","prog_hv")
    # run_hv = outerPins.createPort("N","run_hv")


    ## Creating wires to share pins and create ports outside the function

    FNN_G_En = Wire(Top)
    FNN_G_bit = [Wire(Top) for _ in range(int(np.ceil(np.log2(input_size))))]

    FNN_Dr_En = Wire(Top)
    FNN_Dr_bit = [Wire(Top) for _ in range(int(np.ceil(np.log2(no_of_neurons * 2))))]

    FNN_Prog_Drln = Wire(Top)
    FNN_Run_Drln = Wire(Top)

    FNN_ActF_G_En = Wire(Top)
    FNN_ActF_G_bit = [Wire(Top) for _ in range(2)]

    ## Global Signals
    VTUN = Wire(Top)
    DVDD = Wire(Top)
    AVDD = Wire(Top)
    GND = Wire(Top)
    VINJ = Wire(Top)

    VGPROG = Wire(Top)
    VGRUN = Wire(Top)

    prog_hv = Wire(Top)
    run_hv = Wire(Top)

    ActF_sel = Wire(Top)
    ActF_sel_b = Wire(Top)
    ActF_Vg_bias = Wire(Top)

    FNN_output = [ Wire(Top) for _ in range(no_of_neurons)]

    Act_scan_out =  Wire(Top)
    Act_scan_Din =  Wire(Top)
    Act_scan_CLK =  Wire(Top)
    Act_scan_RSTB =  Wire(Top)
    Act_scan_Qout =  Wire(Top)


    #################  Defining GateSwcs, DrainSwcs and Decoders  #################

    GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,FNN_Island,input_size//2)
    gateBits = int(np.ceil(np.log2(input_size)))
    GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,FNN_Island,gateBits)

    drainBits = int(np.ceil(np.log2(no_of_neurons*2)))
    DrainDecoder = lib_mux.STD_DrainDecoder(circuit,FNN_Island,drainBits)
    DrainSel = lib_mux.RunDrainSwitch(circuit,FNN_Island,(no_of_neurons*2)//4)
    DrainSwitches = lib_cab.DrainCutoff(circuit,FNN_Island,(no_of_neurons*2)//4)


    ###### Gate Swcs and Decoders ########
    GateSwitches.vtun_l += VTUN
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += prog_hv
    GateSwitches.RUN += run_hv

    GateDecoder.VINJV += VINJ
    GateDecoder.GNDV += GND
    GateDecoder.ENABLE += FNN_G_En

    for i in range(gateBits):
        GateDecoder.IN[i] += FNN_G_bit[i]

    for i in range(input_size//2):
        GateSwitches.VINJ_T[i] += GateDecoder.VINJ_b[i]
        GateSwitches.GND_T[i] += GateDecoder.GND_b[i]
        GateSwitches.RUN_IN[i] += GateDecoder.RUN_OUT[i]
        GateSwitches.decode[i] += GateDecoder.OUT[i]

    ###### Drain Swcs and Decoders ########
    DrainSwitches.VDD_b += VINJ
    DrainSwitches.GND_b += GND
    DrainSwitches.RUN += run_hv

    DrainSel.VINJ += VINJ
    DrainSel.GND += GND
    DrainSel.prog_drainrail += FNN_Prog_Drln
    DrainSel.run_drainrail += FNN_Run_Drln

    DrainDecoder.VINJ += VINJ
    DrainDecoder.GND += GND
    DrainDecoder.ENABLE += FNN_Dr_En

    for i in range(drainBits):
        DrainDecoder.IN[i] += FNN_Dr_bit[i]
        


    ##-------------- For Relu/Sigmoid Activation Function circuit --------------##

    Relu_Sig_Gswcs_Island = ac.Island(Top)
    gateBits_Relu_Sig = int(np.ceil(np.log2(2)))

    ## Fake cell definition for the island
    num_G_col = 4

    Fake_Cells_for_Relu_Sig_Gswcs = lib_new.FakeCellGateDecoder(circuit,Relu_Sig_Gswcs_Island, dim=[1,num_G_col//2])
    Fake_Cells_for_Relu_Sig_Gswcs.place([0,0])
    #Fake_Cells_for_AvgP_Gswcs.markAbut()

    Tgts_fr_Vsel_drtG = lib_cab.ST_BMatrix(circuit,Relu_Sig_Gswcs_Island,dim=[1,1])
    Tgts_fr_Vsel_drtG.place([0,num_G_col//2 + 2])

    GateDecoder_R_n_Sig = lib_mux.STD_IndirectGateDecoder(circuit,Relu_Sig_Gswcs_Island,gateBits_Relu_Sig)
    GateSwitches_R_n_Sig  = lib_mux.STD_IndirectGateSwitch(circuit,Relu_Sig_Gswcs_Island,num_G_col//2)


    ## Internal Connections
    for j in range(num_G_col//2):
        GateSwitches_R_n_Sig.Vg[j]+=Neurons.Vg[j]
        GateSwitches_R_n_Sig.CTRL_B[j]+=Neurons.Vsel[j]


    ###### Gate Swcs and Decoders ########
    GateSwitches_R_n_Sig.vtun_l += VTUN
    GateSwitches_R_n_Sig.Vgsel += VGPROG
    GateSwitches_R_n_Sig.PROG += prog_hv
    GateSwitches_R_n_Sig.RUN += run_hv

    GateDecoder_R_n_Sig.VINJV += VINJ
    GateDecoder_R_n_Sig.GNDV += GND
    GateDecoder_R_n_Sig.ENABLE += FNN_ActF_G_En

    for i in range(gateBits_Relu_Sig):
        GateDecoder_R_n_Sig.IN[i] += FNN_ActF_G_bit[i]

    for i in range(1):
        GateSwitches_R_n_Sig.VINJ_T[i] += GateDecoder_R_n_Sig.VINJ_b[i]
        GateSwitches_R_n_Sig.GND_T[i] += GateDecoder_R_n_Sig.GND_b[i]
        GateSwitches_R_n_Sig.RUN_IN[i] += GateDecoder_R_n_Sig.RUN_OUT[i]
        GateSwitches_R_n_Sig.decode[i] += GateDecoder_R_n_Sig.OUT[i]


    ###### Connections for the Direct VMM Vsel lines ########

    Vsel_0 = Wire(Top)
    Vsel_1 = Wire(Top)

    Vsel_0+=Neurons.Vsel_drt[0]
    Vsel_1+=Neurons.Vsel_drt[1]

    Vsel_0 += Tgts_fr_Vsel_drtG.In[0]
    Vsel_1 += Tgts_fr_Vsel_drtG.In[1]
    Vsel_0 += Tgts_fr_Vsel_drtG.In[2]
    Vsel_1 += Tgts_fr_Vsel_drtG.In[3]
    
    Tgts_fr_Vsel_drtG.A[0]+=GateSwitches_R_n_Sig.CTRL_B[0]
    Tgts_fr_Vsel_drtG.A[1]+=GateSwitches_R_n_Sig.CTRL_B[1]
    Tgts_fr_Vsel_drtG.A[2]+=VGRUN
    Tgts_fr_Vsel_drtG.A[3]+=VGRUN
    
    prog_hv+=Tgts_fr_Vsel_drtG.Prog
    VINJ+=Tgts_fr_Vsel_drtG.VDD
    GND+=Tgts_fr_Vsel_drtG.GND

    
    ###### Connections for Neurons ########

    AVDD += Neurons.AVDD[0]
    AVDD += Neurons.AVDD[1]
    GND += Neurons.GND[0]
    VINJ += Neurons.VINJ[0]
    ActF_sel += Neurons.sel[0] 
    ActF_sel_b += Neurons.selb[0] 
    ActF_Vg_bias += Neurons.Vg_bias[0]
    prog_hv += Neurons.prog[0]
    run_hv += Neurons.run[0]
    VTUN += Neurons.VTUN[0]

    for i in range(no_of_neurons):
        FNN_output[i] += Neurons.Output[i]

    ###### Connections for Neuron Vertical Scannel ########

    for i in range(no_of_neurons//2):
        FNN_output[i*2] += Neuron_scanner.In[i*4]
        FNN_output[2*i+1] += Neuron_scanner.In[i*4+1]
        GND+= Neuron_scanner.In[i*4+2]
        DVDD += Neuron_scanner.In[i*4+3]


    GND += Neuron_scanner.GND[0]
    DVDD += Neuron_scanner.VDD[0]
    Act_scan_out += Neuron_scanner.Out[0]
    Act_scan_Din += Neuron_scanner.Din[0]
    Act_scan_CLK += Neuron_scanner.CLK[0]
    Act_scan_RSTB += Neuron_scanner.RSTBar[0]
    Act_scan_Qout += Neuron_scanner.Qout[0]



    # Island Placement
    # -------------------------------------------------------------------------------

    Neuron_scanner_start_x = islandLoc[0]+(140+(27.46*input_size/2)+400)*1e3
    Neuron_Swcs_start_x = islandLoc[0]+(140+(27.46*input_size/2)+80)*1e3
    Neuron_Swcs_start_y = islandLoc[1]+((22*no_of_neurons/2)+20)*1e3

    location_islands = ((islandLoc[0],islandLoc[1]), (Neuron_scanner_start_x,islandLoc[1]), (Neuron_Swcs_start_x,Neuron_Swcs_start_y))
    

    return location_islands


#location_islands = ((5e4,5e4),(5e4+22e3*input_size/2,5e4+22e3*(no_of_neurons+1),0))

#location_islands = ((5e4,5e4),(5e4+20e5,5e4+9e5,0)) # 128 to 80
#location_islands = ((5e4,5e4),(5e4+20e5,5e4+9e5,0)) # 256 to 128
#location_islands = ((50*1e3,50*1e3), (50*1e3+(140+(27.46*input_size/2)+400)*1e3,50*1e3), (50*1e3+(140+(27.46*input_size/2)+40)*1e3,50*1e3+((22*no_of_neurons/2)+20)*1e3)) # 178 to 96


Top = ac.Circuit()
location_islands = FullyCon_Layer(Top,islandLoc=[50*1e3,50*1e3],input_size=96,no_of_neurons=64,debug=True)

design_limits = [6e6, 6e6]


with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 50
qparams["via"] = 20
qparams["jog"] = 80
qparams["conflict"] = 10
qparams["stage2"] = "mask none force effort 100"
qparams["stage3"] = "mask none force effort 100"



ac.compile_asic(Top,process="TSMC350nm", fileName="FullyCon_NN", p_and_r = True, route=True, design_limits = design_limits, location_islands = location_islands, qparams=qparams)

