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

    FNN_input = [ Wire(Top) for _ in range(input_size)]

    ActF_sel = Wire(Top)
    ActF_sel_b = Wire(Top)
    ActF_Vg_bias = Wire(Top)

    FNN_output = [ Wire(Top) for _ in range(no_of_neurons)]

    Act_scan_out =  Wire(Top)
    Act_scan_Din =  Wire(Top)
    Act_scan_CLK =  Wire(Top)
    Act_scan_RSTB =  Wire(Top)
    Act_scan_Qout =  Wire(Top)

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
    
    for i in range(input_size):
        FNN_input[i] += GateDecoder.VGRUN[i]

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
    gateBits_Relu_Sig = int(np.ceil(np.log2(4)))

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

    ## Taking these extra bits out for WTA if needed
    GateSwc_RnSig_Vg_b2 = Wire(Top)
    GateSwc_RnSig_Vg_b2+= GateSwitches_R_n_Sig.Vg[2]

    GateSwc_RnSig_CTRLB_b2 = Wire(Top)
    GateSwc_RnSig_CTRLB_b2 += GateSwitches_R_n_Sig.CTRL_B[2]

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

    # for i in range(1):
    #     GateSwitches_R_n_Sig.VINJ_T[i] += GateDecoder_R_n_Sig.VINJ_b[i]
    #     GateSwitches_R_n_Sig.GND_T[i] += GateDecoder_R_n_Sig.GND_b[i]
    #     GateSwitches_R_n_Sig.RUN_IN[i] += GateDecoder_R_n_Sig.RUN_OUT[i]
    #     GateSwitches_R_n_Sig.decode[i] += GateDecoder_R_n_Sig.OUT[i]


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


    ## Between Gateswcs and Decoders routing 
    Gate_Route_Island = ac.Island(Top)
    Gate_Route = lib_new.Gate_Routing(Top,dim=(1,int(np.ceil(input_size/4))),island=Gate_Route_Island)
    Gate_Route.place([0,0])
    Gate_Route.AVDD += AVDD


    # Island Placement
    # -------------------------------------------------------------------------------

    Neuron_scanner_start_x = islandLoc[0]+(140+(27.46*input_size/2)+400)*1e3
    Neuron_Swcs_start_x = islandLoc[0]+(140+(27.46*input_size/2)+80)*1e3
    Neuron_Swcs_start_y = islandLoc[1]+((22*no_of_neurons/2)+20)*1e3

    location_islands = ((islandLoc[0],islandLoc[1]), 
                        (Neuron_scanner_start_x,islandLoc[1]), 
                        (Neuron_Swcs_start_x,Neuron_Swcs_start_y),
                        (islandLoc[0]+62580+26270*(int(np.ceil(drainBits/2)-1)),islandLoc[1]+int((no_of_neurons*2/4)+1)*22000))
    
    return {
        "location_islands": location_islands,
        "FNN_G_En": FNN_G_En,
        "FNN_G_bit": FNN_G_bit,
        "FNN_Dr_En": FNN_Dr_En,
        "FNN_Dr_bit": FNN_Dr_bit,
        "FNN_Prog_Drln": FNN_Prog_Drln,
        "FNN_Run_Drln": FNN_Run_Drln,
        "FNN_input": FNN_input,
        "FNN_ActF_G_En": FNN_ActF_G_En,
        "FNN_ActF_G_bit": FNN_ActF_G_bit,
        "GateSwc_RnSig_Vg_b2": GateSwc_RnSig_Vg_b2,
        "GateSwc_RnSig_CTRLB_b2": GateSwc_RnSig_CTRLB_b2,
        "ActF_sel": ActF_sel,
        "ActF_sel_b": ActF_sel_b,
        "ActF_Vg_bias": ActF_Vg_bias,
        "FNN_output": FNN_output,
        "Act_scan_out": Act_scan_out,
        "Act_scan_Din": Act_scan_Din,
        "Act_scan_CLK": Act_scan_CLK,
        "Act_scan_RSTB": Act_scan_RSTB,
        "Act_scan_Qout": Act_scan_Qout,
        "VTUN": VTUN,
        "DVDD": DVDD,
        "AVDD": AVDD,
        "GND": GND,
        "VINJ": VINJ,
        "VGPROG": VGPROG,
        "VGRUN": VGRUN,
        "prog_hv": prog_hv,
        "run_hv": run_hv,
    }

def VMMWTA_Layer(circuit,input_size=128,no_of_outputs=80,VMMWTA_Island=None,islandLoc=[0,0],debug=False):

    Top = circuit
    VMMWTA_Island = ac.Island(Top)

    # Make sure the Input and neuron size can be created with 4x2 core cell
    if ((input_size % 2) !=0):
        raise Exception("Error: The input size should be divisible by 2")
    elif (no_of_outputs < 2):
        raise Exception("Error: No of neurons should be greater than 2")
    elif ((no_of_outputs % 2) !=0):
        raise Exception("Error: No of neurons should be divisible by 2")
    
    #################  Defining VMM #################
    VMM = lib_new.TSMC350nm_4x2_Indirect(Top,VMMWTA_Island,dim=[(no_of_outputs)//4,input_size//2])
    VMM.place([0,0])
    track_col = input_size//2

    #################  Defining WTA #################
    WTA = lib_new.TSMC350nm_4WTA_IndirectProg_noncab(Top,VMMWTA_Island,dim=[(no_of_outputs)//4,1])
    WTA.place([0,track_col])
    track_col = track_col + 1

    #################  ScanChain for Neuron Debug  #################
    WTA_scanner_Island = ac.Island(Top)

    WTA_scanner = lib_new.TSMC350nm_VerticalScanner(Top,WTA_scanner_Island,dim=[no_of_outputs//4,1])
    WTA_scanner.place([0,0])

    #track_col = track_col + 1

    #################  Outer Pins  #################


    ## Creating wires to share pins and create ports outside the function

    VMM_G_En = Wire(Top)
    VMM_G_bit = [Wire(Top) for _ in range(int(np.ceil(np.log2(input_size))))]

    VMM_WTA_Dr_En = Wire(Top)
    VMM_WTA_Dr_bit = [Wire(Top) for _ in range(int(np.ceil(np.log2(no_of_outputs * 2))))]

    VMM_WTA_Prog_Drln = Wire(Top)
    VMM_WTA_Run_Drln = Wire(Top)

    VMM_WTA_input = [Wire(Top) for _ in range(input_size)]

    VMM_WTA_output = [Wire(Top) for _ in range(no_of_outputs)]

    WTA_Vmid = Wire(Top)
    WTA_Vbias = Wire(Top)
    WTA_Vsel = Wire(Top)
    WTA_Vg = Wire(Top)

    WTA_scan_out =  Wire(Top)
    WTA_scan_Din =  Wire(Top)
    WTA_scan_CLK =  Wire(Top)
    WTA_scan_RSTB =  Wire(Top)
    WTA_scan_Qout =  Wire(Top)

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


    #################  Defining GateSwcs, DrainSwcs and Decoders  #################

    GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,VMMWTA_Island,input_size//2)
    gateBits = int(np.ceil(np.log2(input_size)))
    GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,VMMWTA_Island,gateBits)

    drainBits = int(np.ceil(np.log2(no_of_outputs)))
    DrainDecoder = lib_mux.STD_DrainDecoder(circuit,VMMWTA_Island,drainBits)
    DrainSel = lib_mux.RunDrainSwitch(circuit,VMMWTA_Island,(no_of_outputs)//4)
    DrainSwitches = lib_cab.DrainCutoff(circuit,VMMWTA_Island,(no_of_outputs)//4)


    ###### Gate Swcs and Decoders ########
    GateSwitches.vtun_l += VTUN
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += prog_hv
    GateSwitches.RUN += run_hv

    GateDecoder.VINJV += VINJ
    GateDecoder.GNDV += GND
    GateDecoder.ENABLE += VMM_G_En

    for i in range(gateBits):
        GateDecoder.IN[i] += VMM_G_bit[i]

    for i in range(input_size):
        VMM_WTA_input[i] += GateDecoder.VGRUN[i]

    # for i in range(input_size//2):
    #     GateSwitches.VINJ_T[i] += GateDecoder.VINJ_b[i]
    #     GateSwitches.GND_T[i] += GateDecoder.GND_b[i]
    #     GateSwitches.RUN_IN[i] += GateDecoder.RUN_OUT[i]
    #     GateSwitches.decode[i] += GateDecoder.OUT[i]

    ###### Drain Swcs and Decoders ########
    DrainSwitches.VDD_b += VINJ
    DrainSwitches.GND_b += GND
    DrainSwitches.RUN += run_hv

    DrainSel.VINJ += VINJ
    DrainSel.GND += GND
    DrainSel.prog_drainrail += VMM_WTA_Prog_Drln
    DrainSel.run_drainrail += VMM_WTA_Run_Drln

    DrainDecoder.VINJ += VINJ
    DrainDecoder.GND += GND
    DrainDecoder.ENABLE += VMM_WTA_Dr_En

    for i in range(drainBits):
        DrainDecoder.IN[i] += VMM_WTA_Dr_bit[i]

    
    ###### Connections for WTA ########
    for i in range(no_of_outputs):
        VMM_WTA_output[i] += WTA.Vout[i]


    WTA_Vmid+=WTA.Vmid[0]

    for i in range(no_of_outputs//4):
        WTA_Vbias+=WTA.Vbias[i]

    WTA_Vsel+=WTA.Vsel[0]
    WTA_Vg+=WTA.Vg[0]
    VTUN+=WTA.VTUN[0]
    prog_hv+=WTA.PROG[0]

    AVDD+=WTA.Vs[0]
    VINJ+=WTA.VINJ[0]
    GND+=WTA.GND[0]

    ###### Connections for WTA Scanner ########

    for i in range(no_of_outputs):
        VMM_WTA_output[i] += WTA_scanner.In[i]

    GND += WTA_scanner.GND[0]
    DVDD += WTA_scanner.VDD[0]
    WTA_scan_out += WTA_scanner.Out[0]
    WTA_scan_Din += WTA_scanner.Din[0]
    WTA_scan_CLK += WTA_scanner.CLK[0]
    WTA_scan_RSTB += WTA_scanner.RSTBar[0]
    WTA_scan_Qout += WTA_scanner.Qout[0]


    ## Between Gateswcs and Decoders routing 
    Gate_Route_Island = ac.Island(Top)
    Gate_Route = lib_new.Gate_Routing(Top,dim=(1,int(np.ceil(input_size/4))),island=Gate_Route_Island)
    Gate_Route.place([0,0])
    Gate_Route.AVDD += AVDD

    # Island Placement
    # -------------------------------------------------------------------------------

    WTA_scanner_start_x = islandLoc[0]+(140+(27.46*input_size/2)+100)*1e3

    location_islands = ((islandLoc[0],islandLoc[1]), 
                        (WTA_scanner_start_x,islandLoc[1]),
                        (islandLoc[0]+62580+26270*(int(np.ceil(drainBits/2)-1)),islandLoc[1]+int((no_of_outputs/4)+1)*22000))
    
    return {
        "location_islands": location_islands,
        "VMM_G_En": VMM_G_En,
        "VMM_G_bit": VMM_G_bit,
        "VMM_WTA_Dr_En": VMM_WTA_Dr_En,
        "VMM_WTA_Dr_bit": VMM_WTA_Dr_bit,
        "VMM_WTA_Prog_Drln": VMM_WTA_Prog_Drln,
        "VMM_WTA_Run_Drln": VMM_WTA_Run_Drln,
        "VMM_WTA_input": VMM_WTA_input,
        "VMM_WTA_output": VMM_WTA_output,
        "WTA_Vmid": WTA_Vmid,
        "WTA_Vbias": WTA_Vbias,
        "WTA_Vsel": WTA_Vsel,
        "WTA_Vg": WTA_Vg,
        "WTA_scan_out": WTA_scan_out,
        "WTA_scan_Din": WTA_scan_Din,
        "WTA_scan_CLK": WTA_scan_CLK,
        "WTA_scan_RSTB": WTA_scan_RSTB,
        "WTA_scan_Qout": WTA_scan_Qout,
        "VTUN": VTUN,
        "DVDD": DVDD,
        "AVDD": AVDD,
        "GND": GND,
        "VINJ": VINJ,
        "VGPROG": VGPROG,
        "VGRUN": VGRUN,
        "prog_hv": prog_hv,
        "run_hv": run_hv
    }


### Layer sizes ####
first_layer = (178,96)
second_layer = (96,64)
final_layer = (64,12)

Top = ac.Circuit()
FNN_layer0 = FullyCon_Layer(Top,islandLoc=[50.5*1e3,50.5*1e3],input_size=first_layer[0],no_of_neurons=first_layer[1],debug=True)
FNN_layer1 = FullyCon_Layer(Top,islandLoc=[50.5*1e3+3400*1e3,50.5*1e3+400*1e3],input_size=second_layer[0],no_of_neurons=second_layer[1],debug=True)
Final_layer = VMMWTA_Layer(Top,islandLoc=[50.5*1e3+3400*1e3,50.5*1e3],input_size=final_layer[0],no_of_outputs=final_layer[1],debug=True)


################ Write down conenctions between the layers and Create Ports #######################

outerPins = frame(Top)

## Global Signals
VTUN = outerPins.createPort("N","VTUN")
DVDD = outerPins.createPort("N","DVDD")
AVDD = outerPins.createPort("N","AVDD")
GND = outerPins.createPort("N","GND")
VINJ = outerPins.createPort("N","VINJ")

VGPROG = outerPins.createPort("N","VGPROG")
VGRUN = outerPins.createPort("N","VGRUN")

prog_hv = outerPins.createPort("N","prog_hv")
run_hv = outerPins.createPort("N","run_hv")


## Shared btwn layers
FNN_shr_G_bit = outerPins.createPort("N","FNN_shr_G_bit",dimension=int(np.ceil(np.log2(first_layer[0]))))
FNN_shr_Dr_bit = outerPins.createPort("N","FNN_shr_Dr_bit",dimension=int(np.ceil(np.log2(first_layer[1]*2))))
Prog_Drainline =  outerPins.createPort("N","Prog_Drainline")
Run_Drainline =  outerPins.createPort("N","Run_Drainline")
ActF_sel = outerPins.createPort("N","ActF_sel")
ActF_sel_b = outerPins.createPort("N","ActF_selb")
ActF_Vg_bias = outerPins.createPort("N","ActF_Vg_bias")

## Layer0 
FNN_ly0_G_En = outerPins.createPort("N","FNN_ly0_G_En")
FNN_ly0_Dr_En = outerPins.createPort("N","FNN_ly0_Dr_En")
FNN_input = outerPins.createPort("N","FNN_input", dimension=first_layer[0])
FNN_ly0_ActF_G_En = outerPins.createPort("N","FNN_ly0_ActF_G_En")

Act_ly0_scan_out = outerPins.createPort("N","Act_ly0_scan_out")
Act_ly0_scan_Din = outerPins.createPort("N","Act_ly0_scan_Din")
Act_ly0_scan_CLK = outerPins.createPort("N","Act_ly0_scan_CLK")
Act_ly0_scan_RSTB = outerPins.createPort("N","Act_ly0_scan_RSTB")
Act_ly0_scan_Qout = outerPins.createPort("N","Act_ly0_scan_Qout")

## Layer1
FNN_ly1_G_En = outerPins.createPort("N","FNN_ly1_G_En")
FNN_ly1_Dr_En = outerPins.createPort("N","FNN_ly1_Dr_En")
FNN_ly1_ActF_G_En = outerPins.createPort("N","FNN_ly1_ActF_G_En")

Act_ly1_scan_out = outerPins.createPort("N","Act_ly1_scan_out")
Act_ly1_scan_Din = outerPins.createPort("N","Act_ly1_scan_Din")
Act_ly1_scan_CLK = outerPins.createPort("N","Act_ly1_scan_CLK")
Act_ly1_scan_RSTB = outerPins.createPort("N","Act_ly1_scan_RSTB")
Act_ly1_scan_Qout = outerPins.createPort("N","Act_ly1_scan_Qout")


## FinalLayer
FNN_final_G_En = outerPins.createPort("N","FNN_final_G_En")
FNN_final_Dr_En = outerPins.createPort("N","FNN_final_Dr_En")

WTA_final_scan_out = outerPins.createPort("N","WTA_final_scan_out")
WTA_final_scan_Din = outerPins.createPort("N","WTA_final_scan_Din")
WTA_final_scan_CLK = outerPins.createPort("N","WTA_final_scan_CLK")
WTA_final_scan_RSTB = outerPins.createPort("N","WTA_final_scan_RSTB")
WTA_final_scan_Qout = outerPins.createPort("N","WTA_final_scan_Qout")

WTA_final_Vmid = outerPins.createPort("N","WTA_final_Vmid")
WTA_final_Vbias = outerPins.createPort("N","WTA_final_Vbias")


######## Layer0 connections #########

FNN_ly0_G_En += FNN_layer0["FNN_G_En"]

for i in range(int(np.ceil(np.log2(first_layer[0])))):
    FNN_shr_G_bit[i]+=FNN_layer0["FNN_G_bit"][i]

FNN_ly0_Dr_En += FNN_layer0["FNN_Dr_En"]

for i in range(int(np.ceil(np.log2(first_layer[1])))):
    FNN_shr_Dr_bit[i]+=FNN_layer0["FNN_Dr_bit"][i]

Prog_Drainline += FNN_layer0["FNN_Prog_Drln"]
Run_Drainline += FNN_layer0["FNN_Run_Drln"]

for i in range(first_layer[0]):
    FNN_input[i]+=FNN_layer0["FNN_input"][i]

FNN_ly0_ActF_G_En += FNN_layer0["FNN_ActF_G_En"]

for i in range(int(np.ceil(np.log2(4)))):
    FNN_shr_G_bit[i]+=FNN_layer0["FNN_ActF_G_bit"][i]

ActF_sel += FNN_layer0["ActF_sel"]
ActF_sel_b += FNN_layer0["ActF_sel_b"]
ActF_Vg_bias += FNN_layer0["ActF_Vg_bias"]


first_layer_FNN_out = [Wire(Top) for _ in range(first_layer[1])]
for i in range(first_layer[1]):
    first_layer_FNN_out[i]+=FNN_layer0["FNN_output"][i]

Act_ly0_scan_out += FNN_layer0["Act_scan_out"]
Act_ly0_scan_Din += FNN_layer0["Act_scan_Din"]
Act_ly0_scan_CLK += FNN_layer0["Act_scan_CLK"]
Act_ly0_scan_RSTB += FNN_layer0["Act_scan_RSTB"]
Act_ly0_scan_Qout += FNN_layer0["Act_scan_Qout"]


VTUN += FNN_layer0["VTUN"]
DVDD += FNN_layer0["DVDD"]
AVDD += FNN_layer0["AVDD"]
GND += FNN_layer0["GND"]
VINJ += FNN_layer0["VINJ"]
VGPROG += FNN_layer0["VGPROG"]
VGRUN += FNN_layer0["VGRUN"]
prog_hv += FNN_layer0["prog_hv"]
run_hv += FNN_layer0["run_hv"]

######## Layer1 connections #########

FNN_ly1_G_En += FNN_layer1["FNN_G_En"]

for i in range(int(np.ceil(np.log2(second_layer[0])))):
    FNN_shr_G_bit[i]+=FNN_layer1["FNN_G_bit"][i]

FNN_ly1_Dr_En += FNN_layer1["FNN_Dr_En"]

for i in range(int(np.ceil(np.log2(second_layer[1])))):
    FNN_shr_Dr_bit[i]+=FNN_layer1["FNN_Dr_bit"][i]

Prog_Drainline += FNN_layer1["FNN_Prog_Drln"]
Run_Drainline += FNN_layer1["FNN_Run_Drln"]

for i in range(second_layer[0]):
    first_layer_FNN_out[i]+=FNN_layer1["FNN_input"][i]

FNN_ly1_ActF_G_En += FNN_layer1["FNN_ActF_G_En"]

for i in range(int(np.ceil(np.log2(4)))):
    FNN_shr_G_bit[i]+=FNN_layer1["FNN_ActF_G_bit"][i]

ActF_sel += FNN_layer1["ActF_sel"]
ActF_sel_b += FNN_layer1["ActF_sel_b"]
ActF_Vg_bias += FNN_layer1["ActF_Vg_bias"]

second_layer_FNN_out = [Wire(Top) for _ in range(second_layer[1])]
for i in range(second_layer[1]):
    second_layer_FNN_out[i]+=FNN_layer1["FNN_output"][i]

Act_ly1_scan_out += FNN_layer1["Act_scan_out"]
Act_ly1_scan_Din += FNN_layer1["Act_scan_Din"]
Act_ly1_scan_CLK += FNN_layer1["Act_scan_CLK"]
Act_ly1_scan_RSTB += FNN_layer1["Act_scan_RSTB"]
Act_ly1_scan_Qout += FNN_layer1["Act_scan_Qout"]


VTUN += FNN_layer1["VTUN"]
DVDD += FNN_layer1["DVDD"]
AVDD += FNN_layer1["AVDD"]
GND += FNN_layer1["GND"]
VINJ += FNN_layer1["VINJ"]
VGPROG += FNN_layer1["VGPROG"]
VGRUN += FNN_layer1["VGRUN"]
prog_hv += FNN_layer1["prog_hv"]
run_hv += FNN_layer1["run_hv"]

######## Final Layer connections #########

FNN_final_G_En += Final_layer["VMM_G_En"]

for i in range(int(np.ceil(np.log2(final_layer[0])))):
    FNN_shr_G_bit[i]+=Final_layer["VMM_G_bit"][i]

FNN_final_Dr_En += Final_layer["VMM_WTA_Dr_En"]

for i in range(int(np.ceil(np.log2(final_layer[1])))):
    FNN_shr_Dr_bit[i]+=Final_layer["VMM_WTA_Dr_bit"][i]

Prog_Drainline += Final_layer["VMM_WTA_Prog_Drln"]
Run_Drainline += Final_layer["VMM_WTA_Run_Drln"]

for i in range(final_layer[0]):
    second_layer_FNN_out[i]+=Final_layer["VMM_WTA_input"][i]

final_layer_FNN_out = [Wire(Top) for _ in range(final_layer[1])]
for i in range(final_layer[1]):
    final_layer_FNN_out[i]+=Final_layer["VMM_WTA_output"][i]

WTA_final_Vmid += Final_layer["WTA_Vmid"]

WTA_final_Vbias += Final_layer["WTA_Vbias"]

FNN_layer1["GateSwc_RnSig_CTRLB_b2"] += Final_layer["WTA_Vsel"]
FNN_layer1["GateSwc_RnSig_Vg_b2"] += Final_layer["WTA_Vg"]


WTA_final_scan_out += Final_layer["WTA_scan_out"]
WTA_final_scan_Din += Final_layer["WTA_scan_Din"]
WTA_final_scan_CLK += Final_layer["WTA_scan_CLK"]
WTA_final_scan_RSTB += Final_layer["WTA_scan_RSTB"]
WTA_final_scan_Qout += Final_layer["WTA_scan_Qout"]


VTUN += Final_layer["VTUN"]
DVDD += Final_layer["DVDD"]
AVDD += Final_layer["AVDD"]
GND += Final_layer["GND"]
VINJ += Final_layer["VINJ"]
VGPROG += Final_layer["VGPROG"]
VGRUN += Final_layer["VGRUN"]
prog_hv += Final_layer["prog_hv"]
run_hv += Final_layer["run_hv"]

#####################################################################################################




design_limits = [5e6, 5e6]

with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 50
qparams["via"] = 80
qparams["jog"] = 20
qparams["conflict"] = 10
qparams["stage2"] = "mask none force effort 100"
qparams["stage3"] = "mask none force effort 100"



ac.compile_asic(Top,process="TSMC350nm", fileName="FullyCon_NN", p_and_r = True, route=False, design_limits = design_limits, location_islands = FNN_layer0["location_islands"] + FNN_layer1["location_islands"] + Final_layer["location_islands"], qparams=qparams)

