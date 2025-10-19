import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np
import json

def Conv_AvgPool(circuit,image_size=32,inp_channels=3,out_channels=16,kernel_size=4,AvgPool_size=2,Conv_AvgP_Island=None,islandLoc=[0,0],debug=False):
    
    Top = circuit
    Conv_AvgP_Island = ac.Island(Top)

    # Make sure the Image size is not less than kernel size
    if (image_size < kernel_size):
        raise Exception("Error: The image_size is less than the kernel_size")
    elif ((image_size % kernel_size) != 0):
        raise Exception("Error: image_size should be divisble by kernel_size")
    
    # Make sure only Average Pooling of 2x2 is initialized
    if (AvgPool_size!=2):
        raise Exception("Error: Currently this algorithm only supports Average Pooling of 2x2 with Overlap=2")

    # Make sure the Kernel size can be made with VMM4X2 std cell
    if (kernel_size*2 % 4) != 0:
        raise Exception("Error: kernel_size must be divisible by 2")
    
    kernel_cols = int(kernel_size)*inp_channels
    kernel_rows = int(kernel_size*2)  # Accounting for negative kernel weights 

    for out_channel_no in range(0,out_channels,(kernel_rows//4)):

        #################  Defining VMM Kernel weights #################
        Kernel_VMM = lib_new.TSMC350nm_4x2_Indirect(Top,Conv_AvgP_Island,dim=[kernel_rows//4,kernel_cols//2])
        Kernel_VMM.place([out_channel_no,0])
        #Kernel_VMM.markAbut()
        track_col= (kernel_cols//2)

        # Defining Horizontal Tgates to choose between kernel rows
        if (kernel_rows == 4):
            TgateHoriz_VMMout = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_only(Top,Conv_AvgP_Island,dim=[1,1])
            TgateHoriz_VMMout.place([out_channel_no,track_col])
            TgateHoriz_VMMout.markAbut()
            track_col=track_col+1

        elif (kernel_rows == 8):
            TgateHoriz_VMMout_top = lib_new.Tgate_swc_fr_Kernel_Horiz_top_edge(Top,Conv_AvgP_Island,dim=[1,1])
            TgateHoriz_VMMout_top.place([out_channel_no,track_col])
            TgateHoriz_VMMout_top.markAbut()

            TgateHoriz_VMMout_bot = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_edge(Top,Conv_AvgP_Island,dim=[1,1])
            TgateHoriz_VMMout_bot.place([out_channel_no+1,track_col])
            TgateHoriz_VMMout_bot.markAbut()

            track_col=track_col+1

        else:
            TgateHoriz_VMMout_top = lib_new.Tgate_swc_fr_Kernel_Horiz_top_edge(Top,Conv_AvgP_Island,dim=[1,1])
            TgateHoriz_VMMout_top.place([out_channel_no,track_col])
            TgateHoriz_VMMout_top.markAbut()

            TgateHoriz_VMMout_core = lib_new.Tgate_swc_fr_Kernel_Horiz_core(Top,Conv_AvgP_Island,dim=[(kernel_rows//4)-2,1])
            TgateHoriz_VMMout_core.place([out_channel_no+1,track_col])
            #TgateHoriz_VMMout_core.markAbut()

            TgateHoriz_VMMout_bot = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_edge(Top,Conv_AvgP_Island,dim=[1,1])
            TgateHoriz_VMMout_bot.place([(out_channel_no)+((kernel_rows//4)-2),track_col])
            TgateHoriz_VMMout_bot.markAbut()

            track_col=track_col+1


        ################# Defining CurrentMirror Subtractor block for positive and negative VMM outputs #################

        Isub_top = lib_new.I_Subtractor_AvgPool_top(Top,Conv_AvgP_Island,dim=[1,1])
        Isub_top.place([out_channel_no,track_col])
        Isub_top.markAbut()

        if (kernel_rows > 4):
            Isub_fill = lib_new.I_Subtractor_AvgPool_core(Top,Conv_AvgP_Island,dim=[(kernel_rows//4)-1,1])
            Isub_fill.place([out_channel_no+1,track_col])
            Isub_fill.markAbut()

        track_col=track_col+1

        #################  Defining Integration and AvgPooling blocks #################

        no_of_intg = image_size//kernel_size
        intg_rows = kernel_rows//4

        #intg_cols = (no_of_intg + intg_rows - 1)//intg_rows #Finds the total no of coloumns required in the grid


        if (no_of_intg % intg_rows == 0) | (no_of_intg < intg_rows):
            no_of_fillers= no_of_intg % intg_rows # Finding the remaining area to be filled in the grid
            intg_cols = no_of_intg //intg_rows  #Finds the total no of coloumns required in the grid

        else:
            intg_cols = ((no_of_intg + (intg_rows - (no_of_intg % intg_rows)))//intg_rows ) #Finds the total no of coloumns required in the grid
            no_of_fillers= intg_rows - (no_of_intg % intg_rows) # Finding the remaining area to be filled in the grid


        if (intg_rows == 1):
            Intgr = [None for _ in range(intg_cols)]
            Intgr[0] = lib_new.Integration_fr_AvgPool_start(Top,Conv_AvgP_Island,dim=[1,1])
            Intgr[0].place([out_channel_no,track_col])
            Intgr[0].markAbut()
            track_col=track_col+1  # Keeping track of the coloumn placement idx

            if no_of_intg > 1:
                for intg_var in range(no_of_intg - 1):
                    Intgr[intg_var + 1] = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,1])
                    Intgr[intg_var + 1].place([out_channel_no,track_col])
                    #Intgr_core.markAbut()
                    track_col = track_col + no_of_intg-1 # Keeping track of the coloumn placement idx

        else:
            Intgr = [[None for _ in range(intg_cols)] for _ in range(intg_rows)]
            Intgr[0][0] = lib_new.Integration_fr_AvgPool_start(Top,Conv_AvgP_Island,dim=[1,1])
            Intgr[0][0].place([out_channel_no,track_col])
            Intgr[0][0].markAbut()
            track_col=track_col+1  # Keeping track of the coloumn placement idx
            
            start_flag=1
            #Intgr_core=[]
            if (no_of_fillers == 0):
                rows=0
                cols=0

                for rows in range(intg_rows):
                    if (rows > 0 ):
                        track_col = track_col - intg_cols   # Keeping track of the coloumn placement idx
                        start_flag=0     
                    
                    for cols in range(intg_cols - start_flag):
                        #Im not vectorizing here since I need to take out pins from each cell definition
                        Intgr[rows][cols + start_flag] = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,1])
                        Intgr[rows][cols + start_flag].place([out_channel_no+rows,track_col])
                        Intgr[rows][cols + start_flag].markAbut()
                        track_col = track_col + 1  # Keeping track of the coloumn placement idx


            else:
                filler_flag=0
                rows=0
                cols=0
                for rows in range(intg_rows):

                    if (rows > 0 ):
                        track_col = track_col - intg_cols # Keeping track of the coloumn placement idx
                        start_flag=0

                    for cols in range(intg_cols - start_flag):

                        if (filler_flag < ((intg_cols*intg_rows)-no_of_fillers-1)):
                            Intgr[rows][cols + start_flag] = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,1])
                            Intgr[rows][cols + start_flag].place([out_channel_no+rows,track_col])
                            Intgr[rows][cols + start_flag].markAbut()
                            Intgr[rows][cols + start_flag] = track_col + 1 # Keeping track of the coloumn placement idx

                        else:
                            Intgr[rows][cols + start_flag] = lib_new.Integration_fr_AvgPool_filler(Top,Conv_AvgP_Island,dim=[1,1])
                            Intgr[rows][cols + start_flag].place([out_channel_no+rows,track_col])
                            Intgr[rows][cols + start_flag].markAbut()
                            track_col = track_col + 1 # Keeping track of the coloumn placement idx

                        filler_flag = filler_flag + 1

                    if (rows == 0):
                            intg_cols = intg_cols + 1 # Need to account for the next row start block



        #################  Defining FinalAvgPool and Relu #################

        # We might have to create a filler cell and change it later
        Readout_Relu = lib_new.AvgPool_n_Relu(Top,Conv_AvgP_Island,dim=[kernel_rows//4,1])
        Readout_Relu.place([out_channel_no,track_col])
        #Readout_Relu.markAbut()



        #################  Pin Connections  #################

        if(out_channel_no == 0):
           Dmmy0 = [[Wire(Top) for _ in range(intg_cols*intg_rows)] for _ in range(out_channels)]
           Dmmy1 = [[Wire(Top) for _ in range(intg_cols*intg_rows)] for _ in range(out_channels)]

        # Tieing the Din and Q of Shift Registers in end and start of rows
        if (intg_rows>1):

            ## I need to create dummy wires for qrouter to recognize these M3 pins
            for i in range(intg_rows):
                for j in range(intg_cols):
                    Dmmy0[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i] = Wire(Top)
                    Dmmy1[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i] = Wire(Top)
                    Intgr[i][j].Q += Dmmy0[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i]
                    Intgr[i][j].Din += Dmmy1[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i]

            for rows in range(intg_rows-1):
                Intgr[rows][intg_cols-1].Q += Intgr[rows+1][0].Din


    
    #################  Defining GateSwcs, DrainSwcs and Decoders  #################

    ## For Kernel VMM FGs
    gateBits = int(np.ceil(np.log2(inp_channels*kernel_size)))
    GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,Conv_AvgP_Island,gateBits)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,Conv_AvgP_Island,(inp_channels*kernel_size)//2)

    drainBits = int(np.ceil(np.log2(out_channels*kernel_size)))
    DrainDecoder = lib_mux.STD_DrainDecoder(circuit,Conv_AvgP_Island,drainBits)
    DrainSel = lib_mux.STD_DrainSelect(circuit,Conv_AvgP_Island,(out_channels*kernel_size)//4)
    DrainSwitches = lib_mux.STD_DrainSwitch(circuit,Conv_AvgP_Island,(out_channels*kernel_size)//4)




    ## For AvgPooling FGs

    AvgP_Gswcs_Island = ac.Island(Top)
    gateBits_Avg_pool = int(np.ceil(np.log2(intg_cols*2)))

    ## Fake cell definition for the island
    Fake_Cells_for_AvgP_Gswcs = lib_new.FakeCellGateDecoder(circuit,AvgP_Gswcs_Island, dim=[1,intg_cols])
    Fake_Cells_for_AvgP_Gswcs.place([0,0])
    Fake_Cells_for_AvgP_Gswcs.markAbut()

    GateDecoder_Avg_pool = lib_mux.STD_IndirectGateDecoder(circuit,AvgP_Gswcs_Island,gateBits_Avg_pool)
    GateSwitches_Avg_pool = lib_mux.STD_IndirectGateSwitch(circuit,AvgP_Gswcs_Island,intg_cols)


    for i in range(0,intg_cols,2):
        GateSwitches_Avg_pool.Vg[i]+=Intgr[0][i].Vg[0]
        GateSwitches_Avg_pool.Vg[i+1]+=Intgr[0][i].Vg[1]



    #################  Global Switches and Shift Reg for kernel col #################
    SR_k_col_island = ac.Island(Top)
    
    SR_k_col = lib_new.DynamicShiftReg_Rst_Lo(Top,SR_k_col_island,dim=[1,inp_channels*kernel_size])
    SR_k_col.place([0,0])

    Tgate_fr_SR_k_col = lib_new.Tgate_swc_fr_Kernel_Vert(Top,SR_k_col_island,dim=[1,inp_channels*kernel_size])
    Tgate_fr_SR_k_col.place([1,0])

    for i in range(inp_channels*kernel_size):
        GateDecoder.VGRUN[i]+=Tgate_fr_SR_k_col.Vg_R[i]



    #################  Outer Pins  #################
    
    outerPins = frame(Top)
    Q_0 = outerPins.createPort("N","Q_0")
    Q_1 = outerPins.createPort("N","Q_1")
    Q_2 = outerPins.createPort("N","Q_2")
    K_col_Din = outerPins.createPort("N","K_col_Din")
    K_col_CLK = outerPins.createPort("N","K_col_CLK")
    K_col_CLKB = outerPins.createPort("N","K_col_CLKB")
    K_col_RST_B = outerPins.createPort("N","K_col_RST_B")


    Q_0 += Intgr[0][2].Q
    Q_1 += Intgr[1][0].Q
    Q_2 += Intgr[1][3].Q

    K_col_Din+=SR_k_col.Din[0]
    K_col_CLK+=SR_k_col.CLK[0]
    K_col_CLKB+=SR_k_col.CLKB[0]
    K_col_RST_B+=SR_k_col.RST_B[0]


    # Island Placement
    # -------------------------------------------------------------------------------

    #location_islands = (islandLoc[0],islandLoc[1])

    #return location_islands



Top = ac.Circuit()
Conv_AvgPool(Top,islandLoc=[100,100],debug=True)

location_islands = ((100,100),(0.6e6,3.8e5),(0.4e6,3.7e5))
#location_islands = ((100,100),(1e6,3.6e5))

design_limits = [2e6, 6e5]



with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 100
qparams["via"] = 20
qparams["jog"] = 20
qparams["conflict"] = 40
qparams["stage2"] = "mask none force effort 500"
qparams["stage3"] = "mask none force effort 500"


ac.compile_asic(Top,process="TSMC350nm", fileName="ConvNN_AvgPool", p_and_r = True, route=True, design_limits = design_limits, location_islands = location_islands, qparams=qparams)

