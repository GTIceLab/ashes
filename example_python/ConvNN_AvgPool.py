import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np
import json

def Conv_AvgPool(circuit,image_size=32,inp_channels=3,out_channels=8,kernel_size=4,AvgPool_size=2,Conv_AvgP_Island=None,islandLoc=[0,0],debug=False):
    
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


    for out_channel_no in range(0,out_channels*(kernel_rows//4),(kernel_rows//4)):

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
            Intgr = [[None for _ in range(intg_cols)] for _ in range(intg_rows)]
            Intgr[0][0] = lib_new.Integration_fr_AvgPool_start(Top,Conv_AvgP_Island,dim=[1,1])
            Intgr[0][0].place([out_channel_no,track_col])
            Intgr[0][0].markAbut()
            track_col=track_col+1  # Keeping track of the coloumn placement idx

            if no_of_intg > 1:
                for intg_var in range(no_of_intg - 1):
                    Intgr[0][intg_var + 1] = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,1])
                    Intgr[0][intg_var + 1].place([out_channel_no,track_col])
                    #Intgr_core.markAbut()
                    track_col = track_col + no_of_intg-1 # Keeping track of the coloumn placement idx
            
            # copy the first out_channel integrators to a global variable to access its pins
            if out_channel_no==0:
                Intgr_out_channel_1 = [[None for _ in range(intg_cols)] for _ in range(intg_rows)]
                Intgr_out_channel_1 = Intgr


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

            # copy the first out_channel integrators to a global variable
            if out_channel_no==0:
                Intgr_out_channel_1 = [[None for _ in range(intg_cols)] for _ in range(intg_rows)]
                Intgr_out_channel_1 = Intgr


        #################  Defining FinalAvgPool and Relu #################

        # We might have to create a filler cell and change it later
        Readout_Relu = lib_new.AvgPool_n_Relu(Top,Conv_AvgP_Island,dim=[intg_rows,1])
        Readout_Relu.place([out_channel_no,track_col])
        #Readout_Relu.markAbut()

        # copy the first out_channel integrators to a global variable to access its pins
        if out_channel_no==0:
            Readout_Relu_glb = [None for _ in range(out_channels)]

        Readout_Relu_glb[out_channel_no//(kernel_rows//4)] = Readout_Relu

        #################  Internal Connections within each output channels  #################

        ## Creating Dummmy nets to recognize all the metal3 Din and Q pins in integrator cells
        if(out_channel_no == 0):
           Dmmy0 = [[Wire(Top) for _ in range(intg_cols*intg_rows)] for _ in range(out_channels)]
           Dmmy1 = [[Wire(Top) for _ in range(intg_cols*intg_rows)] for _ in range(out_channels)]

        # Tieing the Din and Q of Shift Registers in end and start of rows
        if (intg_rows>1):
            for i in range(intg_rows):
                for j in range(intg_cols):
                    Dmmy0[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i] = Wire(Top)
                    Dmmy1[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i] = Wire(Top)
                    Intgr[i][j].Q += Dmmy0[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i]
                    Intgr[i][j].Din += Dmmy1[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i]

            for rows in range(intg_rows-1):
                Intgr[rows][intg_cols-1].Q += Intgr[rows+1][0].Din


    #################  Outer Pins  #################
    outerPins = frame(Top)

    ## Shift Registers for Kernel Coloumn
    SR_k_col_Din = outerPins.createPort("N","K_col_Din")
    SR_k_col_CLK = outerPins.createPort("N","K_col_CLK")
    SR_k_col_CLKB = outerPins.createPort("N","K_col_CLKB")
    SR_k_col_RST_B = outerPins.createPort("N","K_col_RST_B")

    ## Shift Registers for Integrators
    AVDD_by_2 = outerPins.createPort("N","AVDD_by_2")

    SR_Intg_Din = outerPins.createPort("N","SR_Intg_Din")
    SR_Intg_CLK = outerPins.createPort("N","SR_Intg_CLK")
    SR_Intg_CLKB = outerPins.createPort("N","SR_Intg_CLKB")
    SR_Intg_RST_B = outerPins.createPort("N","SR_Intg_RST_B")

    SR_Intg_nxt_row = outerPins.createPort("N","SR_Intg_nxt_row")

    ## Readout Relu for Integrators
    AvgPool_Relu_Vb = outerPins.createPort("N","AvgPool_Relu_Vb")

    ## Global Power lines
    VTUN = outerPins.createPort("N","VTUN")
    DVDD = outerPins.createPort("N","DVDD")
    AVDD = outerPins.createPort("N","AVDD")
    GND = outerPins.createPort("N","GND")
    VINJ = outerPins.createPort("N","VINJ")

    prog_hv = outerPins.createPort("N","prog_hv")
    run_hv = outerPins.createPort("N","run_hv")

    prog_lv = outerPins.createPort("N","prog_lv")
    run_lv = outerPins.createPort("N","run_lv")

    
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

    ## Internal Connections
    for i in range(0,intg_cols,2):
        GateSwitches_Avg_pool.Vg[i]+=Intgr_out_channel_1[0][i].Vg[0]
        GateSwitches_Avg_pool.Vg[i+1]+=Intgr_out_channel_1[0][i].Vg[1]

    ## Internal Connections
    for i in range(0,intg_cols,2):
        GateSwitches_Avg_pool.CTRL_B[i]+=Intgr_out_channel_1[0][i].Vsel_b[0]
        GateSwitches_Avg_pool.CTRL_B[i+1]+=Intgr_out_channel_1[0][i].Vsel_b[1]



    #################  Global Switches and Shift Reg for kernel col #################
    SR_k_col_island = ac.Island(Top)

    SR_k_col = lib_new.DynamicShiftReg_Rst_Lo(Top,SR_k_col_island,dim=[1,kernel_size])
    SR_k_col.place([0, 0])
    
    space_flag=0
    Tgate_fr_SR_k_col_ImgR = [None for _ in range(inp_channels*kernel_size)]


    for k_col_set in range(inp_channels):

        if k_col_set > 0:
            space_flag = space_flag + 1

        for k_col in range(kernel_size):

            Tgate_fr_SR_k_col_ImgR[k_col + (kernel_size)*k_col_set] = lib_new.Tgate_swc_fr_Kernel_Vert(Top,SR_k_col_island,dim=[1,1])
            Tgate_fr_SR_k_col_ImgR[k_col + (kernel_size)*k_col_set].place([1, k_col + (kernel_size)*(k_col_set) + space_flag])
           
            if k_col==0 and k_col_set==0:
                Tgate_fr_SR_k_col_ImgR[k_col + (kernel_size)*k_col_set].markAbut()

            elif k_col!=0:
                Tgate_fr_SR_k_col_ImgR[k_col + (kernel_size)*k_col_set].markAbut()


    ## Pin connections
    SR_k_col_Din+=SR_k_col.Din[0]
    SR_k_col_CLK+=SR_k_col.CLK[0]
    SR_k_col_CLKB+=SR_k_col.CLKB[0]
    SR_k_col_RST_B+=SR_k_col.RST_B[0]


    #################  Global Ties for Integrator blocks #################
'''

    ## Internal connections

    SR_Intg_Din+=Intgr_out_channel_1[0][0].Din

    for i in range(intg_cols):

        SR_Intg_CLK+=Intgr_out_channel_1[0][i].CLK
        SR_Intg_CLKB+=Intgr_out_channel_1[0][i].CLKB
        SR_Intg_RST_B+=Intgr_out_channel_1[0][i].RST_B
        SR_k_col_CLK+=Intgr_out_channel_1[0][i].Vimg_CLK

        #SR_Intg_nxt_row+=Intgr_out_channel_1[0][i].nxt_row[0] # Connect to global dig logic
        #SR_Intg_nxt_row+=Intgr_out_channel_1[0][i].nxt_row[1] # Connect to global dig logic

        GND+=Intgr_out_channel_1[0][i].GND

        AVDD_by_2+=Intgr_out_channel_1[0][i].AVDD_by_2[0]
        AVDD_by_2+=Intgr_out_channel_1[0][i].AVDD_by_2[1]

        prog_hv+=Intgr_out_channel_1[0][i].prog[0] #check if it is HV or LV
        prog_hv+=Intgr_out_channel_1[0][i].prog[1]  #check if it is HV or LV

        run_hv+=Intgr_out_channel_1[0][i].run[0] #check if it is HV or LV
        run_hv+=Intgr_out_channel_1[0][i].run[1]  #check if it is HV or LV

        ## Connected the Vg, Vsel_b lines under the Gateswcs definitions
        AVDD+=Intgr_out_channel_1[0][i].AVDD[0]
        AVDD+=Intgr_out_channel_1[0][i].AVDD[1]

        VINJ+=Intgr_out_channel_1[0][i].VINJ[0]
        VINJ+=Intgr_out_channel_1[0][i].VINJ[1]

        VTUN+=Intgr_out_channel_1[0][i].VTUN

        DVDD+=Intgr_out_channel_1[0][i].DVDD
        

    #################  Global Ties for Readout Relu blocks #################

    prog_lv +=  Readout_Relu_glb[0].prog_lv[0] 
    run_lv +=  Readout_Relu_glb[0].run_lv[0] 
    AvgPool_Relu_Vb += Readout_Relu_glb[0].Vb[0] 
    AVDD += Readout_Relu_glb[0].AVDD[0] 

    Out_En_b_glb = [Wire(Top) for _ in range(intg_rows)]
    Sub_Img_Out_glb = [Wire(Top) for _ in range(out_channels)]

    for i in range(out_channels):
        for local in range(intg_rows):
            GND+= Readout_Relu_glb[i].GND[local] 
            DVDD+= Readout_Relu_glb[i].DVDD[local] 
            Out_En_b_glb[local]+=Readout_Relu_glb[i].Out_En_b[local]
            Sub_Img_Out_glb[i]+=Readout_Relu_glb[i].Sub_img_out[local]

'''


    # Island Placement
    # -------------------------------------------------------------------------------

    #location_islands = (islandLoc[0],islandLoc[1])

    #return location_islands



Top = ac.Circuit()
Conv_AvgPool(Top,islandLoc=[100,100],debug=True)

location_islands = ((100,100),(0.6e6,3.8e5),(0.4e6,3.7e5))
#location_islands = ((100,100),(1e6,3.6e5))

design_limits = [3e6, 6e5]



with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 10
qparams["via"] = 20
qparams["jog"] = 20
qparams["conflict"] = 40
qparams["stage2"] = "mask none force effort 10"
qparams["stage3"] = "mask none force effort 10"


ac.compile_asic(Top,process="TSMC350nm", fileName="ConvNN_AvgPool", p_and_r = True, route=True, design_limits = design_limits, location_islands = location_islands, qparams=qparams,drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0)

