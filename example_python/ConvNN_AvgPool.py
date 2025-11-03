import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np
import json

def Conv_AvgPool(circuit,image_size=32,inp_channels=3,out_channels=34,kernel_size=4,AvgPool_size=2,Conv_AvgP_Island=None,islandLoc=[0,0],debug=False):
    
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
            TgateHoriz_VMMout_top = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_only(Top,Conv_AvgP_Island,dim=[1,1])
            TgateHoriz_VMMout_top.place([out_channel_no,track_col])
            TgateHoriz_VMMout_top.markAbut()
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

        # copy the first out_channel horiz tgate to a global variable to access its pins
        if out_channel_no==0:
            TgateHoriz_VMMout_top_glb = TgateHoriz_VMMout_top


        ################# Defining CurrentMirror Subtractor block for positive and negative VMM outputs #################

        Isub_top = lib_new.I_Subtractor_AvgPool_top(Top,Conv_AvgP_Island,dim=[1,1])
        Isub_top.place([out_channel_no,track_col])
        Isub_top.markAbut()

        if (kernel_rows > 4):
            Isub_fill = lib_new.I_Subtractor_AvgPool_core(Top,Conv_AvgP_Island,dim=[(kernel_rows//4)-1,1])
            Isub_fill.place([out_channel_no+1,track_col])
            Isub_fill.markAbut()

        track_col=track_col+1

        # copy the first out_channel horiz tgate to a global variable to access its pins
        if out_channel_no==0:
            Isub_top_glb = Isub_top

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

           Intgr_Din_tie = Wire(Top)

        # Tieing the Din and Q of Shift Registers in end and start of rows
        for i in range(intg_rows):
            for j in range(intg_cols):
                #Dmmy0[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i] = Wire(Top)
                #Dmmy1[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i] = Wire(Top)
                Intgr[i][j].Q += Dmmy0[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i]
                Intgr[i][j].Din += Dmmy1[out_channel_no//(kernel_rows//4)][j + (intg_cols)*i]

        # Tie all Din pins of integrators within all output channels
        Intgr_Din_tie += Intgr[0][0].Din

        if (intg_rows>1):
            for rows in range(intg_rows-1):
                Intgr[rows][intg_cols-1].Q += Intgr[rows+1][0].Din


    #################  Creating Nets  #################

    ## G/D Decoder and Swcs Signals
    Kvmm_G_En = Wire(Top)
    Kvmm_G_bit = [Wire(Top) for _ in range(int(np.ceil(np.log2(inp_channels*kernel_size))))]

    AP_G_En = Wire(Top)
    AP_G_bit = [Wire(Top) for _ in range(int(np.ceil(np.log2(intg_cols*2))))]
    
    Kvmm_AP_Dr_En =  Wire(Top)
    Kvmm_AP_Dr_bit =  [Wire(Top) for _ in range(int(np.ceil(np.log2(out_channels*kernel_size*2))))]

    Kvmm_AP_Prog_Drln = Wire(Top)
    Kvmm_AP_Run_Drln =  Wire(Top)
    
    ## Kernel Coloumn Shift Registers
    SR_k_col_Din = Wire(Top)
    SR_k_col_CLKB = Wire(Top)
    SR_k_col_RST_B = Wire(Top)
    SR_k_col_CLK = Wire(Top)

    Vin_inp_Ch = [Wire(Top) for _ in range(inp_channels)]

    ## Integrator Shift Registers
    SR_Intg_RST_B = Wire(Top)
    SR_Intg_Din = Wire(Top)
    SR_Intg_CLK = Wire(Top)
    SR_Intg_CLKB = Wire(Top)

    ## Shift Registers for Kernel Row
    SR_k_rw_Din = Wire(Top)
    SR_k_rw_CLKB = Wire(Top)
    SR_k_rw_RST_B = Wire(Top)
    SR_k_rw_CLK = Wire(Top)

    # AvgPooling and Readout signals
    AP_Relu_Vb = Wire(Top)
    Sub_Img_Out_glb = [Wire(Top) for _ in range(out_channels)]
    

    ## Global Power lines
    VTUN = Wire(Top)
    DVDD = Wire(Top)
    AVDD = Wire(Top)
    GND = Wire(Top)
    VINJ = Wire(Top)

    VGPROG = Wire(Top)
    VGRUN = Wire(Top)

    prog_hv = Wire(Top)
    run_hv = Wire(Top)

    AVDD_by_2 = Wire(Top)

    ## Top_Digital
    Global_rst_b = Wire(Top)



    #################  Outer Pins  #################
    # outerPins = frame(Top)

    # ## G/D Decoder and Swcs Signals
    # Kvmm_G_En = outerPins.createPort("N","Kvmm_G_En")
    # AP_G_En = outerPins.createPort("N","AP_G_En")


    # # Checking which island is bigger and assigning the Most bits needed
    # if intg_cols*2 < (inp_channels*kernel_size):
    #     Kvmm_AvgP_G_bit = outerPins.createPort("N","Kvmm_G_bit",dimension=int(np.ceil(np.log2(inp_channels*kernel_size))))
    # else:
    #     Kvmm_AvgP_G_bit = outerPins.createPort("N","Kvmm_G_bit",dimension=int(np.ceil(np.log2(intg_cols*2))))

    # Kvmm_AP_Dr_En =  outerPins.createPort("N","Kvmm_AP_Dr_En")
    # Kvmm_AP_Dr_bit = outerPins.createPort("N","Kvmm_AP_Dr_bit",dimension=int(np.ceil(np.log2(out_channels*kernel_size*2))))

    # Kvmm_AP_Prog_Drln =  outerPins.createPort("N","Kvmm_AP_Prog_Drln")
    # Kvmm_AP_Run_Drln =  outerPins.createPort("N","Kvmm_AP_Run_Drln")

    # ## Shift Registers for Kernel Coloumn
    # SR_k_col_Din = outerPins.createPort("N","K_col_Din")
    # SR_k_col_CLKB = outerPins.createPort("N","K_col_CLKB")
    # SR_k_col_RST_B = outerPins.createPort("N","K_col_RST_B")
    # SR_k_col_CLK = outerPins.createPort("N","K_col_CLK")

    # Vin_inp_Ch = outerPins.createPort("E", "Vin_inp_Ch",dimension=inp_channels)

    # ## Shift Registers for Integrators
    # AVDD_by_2 = outerPins.createPort("N","AVDD_by_2")


    # SR_Intg_RST_B = outerPins.createPort("N","SR_Intg_RST_B")
    # SR_Intg_Din = outerPins.createPort("N","SR_Intg_Din")
    # SR_Intg_CLK = outerPins.createPort("N","SR_Intg_CLK")
    # SR_Intg_CLKB = outerPins.createPort("N","SR_Intg_CLKB")

    # SR_Intg_nxt_rw = outerPins.createPort("N","SR_Intg_nxt_rw")
    # Vimg_CLK = outerPins.createPort("N","Vimg_CLK")

    # ## Shift Registers for Kernel Row
    # SR_k_rw_Din = outerPins.createPort("N","K_rw_Din")
    # SR_k_rw_CLKB = outerPins.createPort("N","K_rw_CLKB")
    # SR_k_rw_RST_B = outerPins.createPort("N","K_rw_RST_B")
    # SR_k_rw_CLK = outerPins.createPort("N","K_rw_CLK")


    # ## Readout Relu for Integrators
    # AP_Relu_Vb = outerPins.createPort("N","AP_Relu_Vb")
    
    # Sub_Img_Out_glb = outerPins.createPort("E", "Sub_img_out",dimension=out_channels)

    # # Sub_Img_Out_glb = [None for _ in range(out_channels)]
    # # for i in range(out_channels):
    # #     Sub_Img_Out_glb[i] = outerPins.createPort("E", f"Sub_img_out_{i}")


    # ## Global Power lines
    # VTUN = outerPins.createPort("N","VTUN")
    # DVDD = outerPins.createPort("N","DVDD")
    # AVDD = outerPins.createPort("N","AVDD")
    # GND = outerPins.createPort("N","GND")
    # VINJ = outerPins.createPort("N","VINJ")

    # VGPROG = outerPins.createPort("N","VGPROG")

    # prog_hv = outerPins.createPort("N","prog_hv")
    # run_hv = outerPins.createPort("N","run_hv")

    # prog_lv = outerPins.createPort("N","prog_lv")
    # run_lv = outerPins.createPort("N","run_lv")

    
    #################  Defining GateSwcs, DrainSwcs and Decoders  #################

    ##-------------- For Kernel VMM FGs --------------##
    gateBits = int(np.ceil(np.log2(inp_channels*kernel_size)))
    GateDecoder = lib_mux.STD_IndirectGateDecoder(circuit,Conv_AvgP_Island,gateBits)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(circuit,Conv_AvgP_Island,(inp_channels*kernel_size)//2)

    drainBits = int(np.ceil(np.log2(out_channels*kernel_size*2)))
    DrainDecoder = lib_mux.STD_DrainDecoder(circuit,Conv_AvgP_Island,drainBits)
    DrainSel = lib_mux.RunDrainSwitch(circuit,Conv_AvgP_Island,(out_channels*kernel_size*2)//4)
    DrainSwitches = lib_cab.DrainCutoff(circuit,Conv_AvgP_Island,(out_channels*kernel_size*2)//4)
    
    ## Pin Connections

    ###### Gate Swcs and Decoders ########
    GateSwitches.vtun_l += VTUN
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += prog_hv
    GateSwitches.RUN += run_hv

    GateDecoder.VINJV += VINJ
    GateDecoder.GNDV += GND
    GateDecoder.ENABLE += Kvmm_G_En

    for i in range(gateBits):
        GateDecoder.IN[i] += Kvmm_G_bit[i]

    # VGRUN connections of the decoders are written below where SR_K_Col cells are defined.

    # for i in range((inp_channels*kernel_size)//2):
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
    DrainSel.prog_drainrail += Kvmm_AP_Prog_Drln
    DrainSel.run_drainrail += Kvmm_AP_Run_Drln

    DrainDecoder.VINJ += VINJ
    DrainDecoder.GND += GND
    DrainDecoder.ENABLE += Kvmm_AP_Dr_En

    for i in range(drainBits):
        DrainDecoder.IN[i] += Kvmm_AP_Dr_bit[i]
        

    ##-------------- For AvgPooling FGs --------------##

    AvgP_Gswcs_Island = ac.Island(Top)
    gateBits_Avg_pool = int(np.ceil(np.log2(intg_cols*2)))

    ## Fake cell definition for the island
    Fake_Cells_for_AvgP_Gswcs = lib_new.FakeCellGateDecoder(circuit,AvgP_Gswcs_Island, dim=[1,intg_cols])
    Fake_Cells_for_AvgP_Gswcs.place([0,0])
    #Fake_Cells_for_AvgP_Gswcs.markAbut()

    GateDecoder_Avg_pool = lib_mux.STD_IndirectGateDecoder(circuit,AvgP_Gswcs_Island,gateBits_Avg_pool)
    GateSwitches_Avg_pool = lib_mux.STD_IndirectGateSwitch(circuit,AvgP_Gswcs_Island,intg_cols)


    ## Internal Connections
    for i in range(0,intg_cols,1):
        for j in range(2):
            GateSwitches_Avg_pool.Vg[j + (2)*i]+=Intgr_out_channel_1[0][i].Vg[j]
           # GateSwitches_Avg_pool.CTRL_B[j + (2)*i]+=Intgr_out_channel_1[0][i].Vsel_b[j]

    for i in range(intg_cols):
        VGRUN += GateDecoder_Avg_pool.VGRUN[i]


    ## Pin Connections

    ###### Gate Swcs and Decoders ########
    GateSwitches_Avg_pool.vtun_l += VTUN
    GateSwitches_Avg_pool.Vgsel += VGPROG
    GateSwitches_Avg_pool.PROG += prog_hv
    GateSwitches_Avg_pool.RUN += run_hv

    GateDecoder_Avg_pool.VINJV += VINJ
    GateDecoder_Avg_pool.GNDV += GND
    GateDecoder_Avg_pool.ENABLE += AP_G_En

    for i in range(gateBits_Avg_pool):
        GateDecoder_Avg_pool.IN[i] += AP_G_bit[i]

    # for i in range(intg_cols):
    #     GateSwitches_Avg_pool.VINJ_T[i] += GateDecoder_Avg_pool.VINJ_b[i]
    #     GateSwitches_Avg_pool.GND_T[i] += GateDecoder_Avg_pool.GND_b[i]
    #     GateSwitches_Avg_pool.RUN_IN[i] += GateDecoder_Avg_pool.RUN_OUT[i]
    #     GateSwitches_Avg_pool.decode[i] += GateDecoder_Avg_pool.OUT[i]
        

    #################  Placing the Shift Reg and Tgate cells for kernel col #################
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


    #################  Placing and Routing the Top level Digital cell and Tgates for direct scheme #################

    ## Placement
    Top_Digital_island = ac.Island(Top)
    Top_Digital = lib_new.AvgPool_TopDig(Top,Top_Digital_island,dim=[1,1])
    Top_Digital.place([0,0])

    Tgts_fr_Vsel_drtG = [None for _ in range(int(np.ceil(intg_cols)))]

    for i in range(intg_cols):
        Tgts_fr_Vsel_drtG[i] = lib_cab.ST_BMatrix(circuit,Top_Digital_island,dim=[1,1])
        Tgts_fr_Vsel_drtG[i].place([0,i+1])

    ## Connections
    # Top Digital block
    SR_k_rw_CLK += Top_Digital.SR_k_rw_CLK
    SR_k_rw_RST_B += Top_Digital.SR_k_rw_RST_B
    SR_k_rw_CLKB += Top_Digital.SR_k_rw_CLKB
    TgateHoriz_VMMout_top_glb.Final_rw_out += Top_Digital.Final_rw

    SR_Intg_RST_B+=Top_Digital.SR_int_RST_B
    SR_Intg_CLK+=Top_Digital.SR_int_CLK
    SR_Intg_CLKB+=Top_Digital.SR_int_CLKB
    
    for i in range(intg_rows):
        for j in range(intg_cols):
            Intgr_out_channel_1[i][j].Q += Top_Digital.SR_int_0_Q[j + (i*intg_cols)]

    int_rst_1 = Wire(Top)
    int_rst_1 += Top_Digital.int_rst[1]

    int_rst_0 = Wire(Top)
    int_rst_0 += Top_Digital.int_rst[0]

    Relu_en_b_1 = Wire(Top)
    Relu_en_b_1 += Top_Digital.Relu_en_b[1]

    Relu_en_b_0 = Wire(Top)
    Relu_en_b_0 += Top_Digital.Relu_en_b[0]

    Global_rst_b += Top_Digital.Global_rst_b
    
    intg_nxt_rw = Wire(Top)
    intg_nxt_rw += Top_Digital.intg_nxt_rw

    DVDD += Top_Digital.DVDD
    GND += Top_Digital.GND

    # Tgates for direct scheme
    for i in range(intg_cols):
        Intgr_out_channel_1[0][i].Vsel_b[0] += Tgts_fr_Vsel_drtG[i].In[0]
        Intgr_out_channel_1[0][i].Vsel_b[1] += Tgts_fr_Vsel_drtG[i].In[1]
        Intgr_out_channel_1[0][i].Vsel_b[0] += Tgts_fr_Vsel_drtG[i].In[2]
        Intgr_out_channel_1[0][i].Vsel_b[1] += Tgts_fr_Vsel_drtG[i].In[3]
        
        for j in range(2):
            GateSwitches_Avg_pool.CTRL_B[j + (2)*i]+=Tgts_fr_Vsel_drtG[i].A[j]

            if (i<intg_cols/2):
                Top_Digital.AvgPool_col_ctrl[0]+=Tgts_fr_Vsel_drtG[i].A[j+2]
            else:
                Top_Digital.AvgPool_col_ctrl[1]+=Tgts_fr_Vsel_drtG[i].A[j+2]

    
        prog_hv+=Tgts_fr_Vsel_drtG[i].Prog
        VINJ+=Tgts_fr_Vsel_drtG[i].VDD
        GND+=Tgts_fr_Vsel_drtG[i].GND

    ################# Starting Internal Connections #################

    ## Shift Registor Kernel Col Tgates
    SR_k_col_Din+=SR_k_col.Din[0]
    SR_k_col_CLK+=SR_k_col.CLK[0]
    SR_k_col_CLKB+=SR_k_col.CLKB[0]
    SR_k_col_RST_B+=SR_k_col.RST_B[0]
    
    DVDD+=SR_k_col.DVDD
    GND+=SR_k_col.GND


    ## Shift Registor Kernel Col Tgates
    for i in range(inp_channels*kernel_size):
        GateDecoder.VGRUN[i] += Tgate_fr_SR_k_col_ImgR[i].Vg_R

    for i in range(0,inp_channels*kernel_size,kernel_size):
        DVDD += Tgate_fr_SR_k_col_ImgR[i].DVDD
        AVDD += Tgate_fr_SR_k_col_ImgR[i].AVDD 
        GND += Tgate_fr_SR_k_col_ImgR[i].GND
        Vin_inp_Ch[i//kernel_size] += Tgate_fr_SR_k_col_ImgR[i].Vimg

    for i in range(1,inp_channels,1):
        for j in range(kernel_size):
            Tgate_fr_SR_k_col_ImgR[j].Q_bot+= Tgate_fr_SR_k_col_ImgR[j + i*(kernel_size)].Q_bot


    ### Tgate Horizontal Swcs
    VINJ+=TgateHoriz_VMMout_top_glb.VINJ
    run_hv+=TgateHoriz_VMMout_top_glb.RUN_HV
    GND+=TgateHoriz_VMMout_top_glb.GND
    SR_k_rw_CLKB+=TgateHoriz_VMMout_top_glb.CLKB
    SR_k_rw_CLK+=TgateHoriz_VMMout_top_glb.CLK
    SR_k_rw_RST_B+=TgateHoriz_VMMout_top_glb.RST_B
    DVDD+=TgateHoriz_VMMout_top_glb.DVDD
    SR_k_rw_Din+=TgateHoriz_VMMout_top_glb.Din
    SR_k_rw_Din+=TgateHoriz_VMMout_top_glb.Din_Glb

    ### I_subtractor 
    GND+=Isub_top_glb.GND
    prog_hv+=Isub_top_glb.prog_hv
    VINJ+=Isub_top_glb.VINJ
    run_hv+=Isub_top_glb.run_hv

    ## Integrator blocks

    Intgr_Din_tie += SR_Intg_Din
    for i in range(intg_cols):

        SR_Intg_CLK+=Intgr_out_channel_1[0][i].CLK
        SR_Intg_CLKB+=Intgr_out_channel_1[0][i].CLKB
        SR_Intg_RST_B+=Intgr_out_channel_1[0][i].RST_B
        SR_k_col_CLK+=Intgr_out_channel_1[0][i].Vimg_CLK

        intg_nxt_rw+=Intgr_out_channel_1[0][i].nxt_rw[0] # Connect to global dig logic
        intg_nxt_rw+=Intgr_out_channel_1[0][i].nxt_rw[1] # Connect to global dig logic

        GND+=Intgr_out_channel_1[0][i].GND

        AVDD_by_2+=Intgr_out_channel_1[0][i].AVDD_by_2[0]
        AVDD_by_2+=Intgr_out_channel_1[0][i].AVDD_by_2[1]

        prog_hv+=Intgr_out_channel_1[0][i].prog[0]
        prog_hv+=Intgr_out_channel_1[0][i].prog[1] 

        run_hv+=Intgr_out_channel_1[0][i].run[0]
        run_hv+=Intgr_out_channel_1[0][i].run[1] 

        ## Connected the Vg, Vsel_b lines under the Gateswcs definitions
        VINJ+=Intgr_out_channel_1[0][i].VINJ[0]
        VINJ+=Intgr_out_channel_1[0][i].VINJ[1]

        VTUN+=Intgr_out_channel_1[0][i].VTUN

        DVDD+=Intgr_out_channel_1[0][i].DVDD
        

    #################  Global Ties for Readout Relu blocks #################

    prog_hv +=  Readout_Relu_glb[0].prog_hv[0] 
    run_hv +=  Readout_Relu_glb[0].run_hv[0] 
    AP_Relu_Vb += Readout_Relu_glb[0].Vb[0] 
    AVDD += Readout_Relu_glb[0].AVDD[0]    
    VINJ += Readout_Relu_glb[0].VINJ[0] 


    Out_En_b_glb = [Wire(Top) for _ in range(intg_rows)]

    for i in range(out_channels):
        for local in range(intg_rows):
            Sub_Img_Out_glb[i] +=Readout_Relu_glb[i].Sub_img_out[local]
            GND += Readout_Relu_glb[i].GND[local] 
            DVDD += Readout_Relu_glb[i].DVDD[local]

            if (local%2==0):
                Relu_en_b_0 += Readout_Relu_glb[i].Out_En_b[local]
                int_rst_0 += Readout_Relu_glb[i].int_rst_out[local]

            else:
                int_rst_0 += Readout_Relu_glb[i].int_rst_out[local]
                Relu_en_b_1 += Readout_Relu_glb[i].Out_En_b[local]

   ################    Between Gateswcs and Decoders routing    ################

    Gate_Route_Island_fr_Kvmm = ac.Island(Top)
    Gate_Route_kvmm = lib_new.Gate_Routing(Top,dim=(1,(inp_channels*kernel_size)//4),island=Gate_Route_Island_fr_Kvmm)
    Gate_Route_kvmm.place([0,0])
    Gate_Route_kvmm.AVDD += AVDD
    

    Gate_Route_Island_fr_AvgP = ac.Island(Top)
    Gate_Route_AvgP = lib_new.Gate_Routing(Top,dim=(1,intg_cols//2),island=Gate_Route_Island_fr_AvgP)
    Gate_Route_AvgP.place([0,0])
    Gate_Route_AvgP.AVDD += AVDD


    # Island Placement
    # -------------------------------------------------------------------------------
    Kernel_VMM_X = islandLoc[0]
    Kernel_VMM_Y = islandLoc[1]

    ShftReg_Krnl_col_X = islandLoc[0] + (170+(27.46*(inp_channels*kernel_size)/2)+80)*1e3
    ShftReg_Krnl_col_Y = islandLoc[1] + (22*(kernel_size*2*out_channels)/4 + 30)*1e3

    AvgPool_Gswcs_X = ShftReg_Krnl_col_X + (((kernel_size*inp_channels)/4)*(44.52 + 20.5))*1e3
    AvgPool_Gswcs_Y = ShftReg_Krnl_col_Y

    Top_Dig_X = AvgPool_Gswcs_X + 250*1e3
    Top_Dig_Y = ShftReg_Krnl_col_Y

    #AvgP_Gswcs_Island_xloc = start_x + 
    location_islands = ((Kernel_VMM_X, Kernel_VMM_Y),
                        (AvgPool_Gswcs_X, AvgPool_Gswcs_Y),
                        (ShftReg_Krnl_col_X,ShftReg_Krnl_col_Y),
                        (Top_Dig_X,Top_Dig_Y),
                        (islandLoc[0]+62580+26270*(int(np.ceil(drainBits/2)-1)),islandLoc[1]+ (22*((kernel_size*2*out_channels)/4 + 1))*1e3),
                        (AvgPool_Gswcs_X, AvgPool_Gswcs_Y + 22*1e3))

    return {
        "location_islands": location_islands,
        "Kvmm_G_En": Kvmm_G_En,
        "Kvmm_G_bit": Kvmm_G_bit,
        "AP_G_En": AP_G_En,
        "AP_G_bit": AP_G_bit,
        "Kvmm_AP_Dr_En": Kvmm_AP_Dr_En,
        "Kvmm_AP_Dr_bit": Kvmm_AP_Dr_bit,
        "Kvmm_AP_Prog_Drln": Kvmm_AP_Prog_Drln,
        "Kvmm_AP_Run_Drln": Kvmm_AP_Run_Drln,
        "SR_k_col_Din": SR_k_col_Din,
        "SR_k_col_CLKB": SR_k_col_CLKB,
        "SR_k_col_RST_B": SR_k_col_RST_B,
        "SR_k_col_CLK": SR_k_col_CLK,
        "Vin_inp_Ch": Vin_inp_Ch,
        "SR_Intg_RST_B": SR_Intg_RST_B,
        "SR_Intg_Din": SR_Intg_Din,
        "SR_Intg_CLK": SR_Intg_CLK,
        "SR_Intg_CLKB": SR_Intg_CLKB,
        "SR_k_rw_Din": SR_k_rw_Din,
        "SR_k_rw_CLKB": SR_k_rw_CLKB,
        "SR_k_rw_RST_B": SR_k_rw_RST_B,
        "SR_k_rw_CLK": SR_k_rw_CLK,
        "AP_Relu_Vb": AP_Relu_Vb,
        "Sub_Img_Out_glb": Sub_Img_Out_glb,
        "VTUN": VTUN,
        "DVDD": DVDD,
        "AVDD": AVDD,
        "GND": GND,
        "VINJ": VINJ,
        "VGPROG": VGPROG,
        "prog_hv": prog_hv,
        "run_hv": run_hv,
        "AVDD_by_2": AVDD_by_2,
        "Global_rst_b": Global_rst_b
    }




#Top = ac.Circuit()
#CNN_layer0 = Conv_AvgPool(Top,islandLoc=[5e4,4.1e4],debug=True)

### Layer sizes ####
first_layer = (32,3,38,4)
Top = ac.Circuit()
Conv_AP = Conv_AvgPool(Top,image_size=first_layer[0],inp_channels=first_layer[1],out_channels=first_layer[2],kernel_size=first_layer[3],AvgPool_size=2,Conv_AvgP_Island=None,islandLoc=[80*1e3,80*1e3],debug=False)

################ Frame Pins if needed #######################

outerPins = frame(Top)

Kvmm_G_En = outerPins.createPort("N","Kvmm_G_En")
Kvmm_G_bit = outerPins.createPort("N","Kvmm_G_bit", dimension = int(np.ceil(np.log2(first_layer[1]*first_layer[3]))) )  
AP_G_En = outerPins.createPort("N","AP_G_En")
AP_G_bit = outerPins.createPort("N","AP_G_bit", dimension=3) ## Need to return intg_Cols to avoid hard coding
Kvmm_AP_Dr_En = outerPins.createPort("N","Kvmm_AP_Dr_En")
Kvmm_AP_Dr_bit = outerPins.createPort("N","Kvmm_AP_Dr_bit", dimension = int(np.ceil(np.log2(first_layer[2]*first_layer[3]*2))) )
Kvmm_AP_Prog_Drln = outerPins.createPort("N","Kvmm_AP_Prog_Drln")
Kvmm_AP_Run_Drln = outerPins.createPort("N","Kvmm_AP_Run_Drln")
SR_k_col_Din = outerPins.createPort("N","SR_k_col_Din")
SR_k_col_CLKB = outerPins.createPort("N","SR_k_col_CLKB")
SR_k_col_RST_B = outerPins.createPort("N","SR_k_col_RST_B")
SR_k_col_CLK = outerPins.createPort("N","SR_k_col_CLK")
Vin_inp_Ch = outerPins.createPort("N","Vin_inp_Ch", dimension = first_layer[1])
SR_Intg_RST_B = outerPins.createPort("N","SR_Intg_RST_B")
SR_Intg_Din = outerPins.createPort("N","SR_Intg_Din")
SR_Intg_CLK = outerPins.createPort("N","SR_Intg_CLK")
SR_Intg_CLKB = outerPins.createPort("N","SR_Intg_CLKB")
SR_k_rw_Din = outerPins.createPort("N","SR_k_rw_Din")
SR_k_rw_CLKB = outerPins.createPort("N","SR_k_rw_CLKB")
SR_k_rw_RST_B = outerPins.createPort("N","SR_k_rw_RST_B")
SR_k_rw_CLK = outerPins.createPort("N","SR_k_rw_CLK")
AP_Relu_Vb = outerPins.createPort("N","AP_Relu_Vb")
Sub_Img_Out = outerPins.createPort("E","sub_img_out",dimension=first_layer[2])
VTUN = outerPins.createPort("N","VTUN")
DVDD = outerPins.createPort("N","DVDD")
AVDD = outerPins.createPort("N","AVDD")
GND = outerPins.createPort("N","GND")
VINJ = outerPins.createPort("N","VINJ")
VGPROG = outerPins.createPort("N","VGPROG")
prog_hv = outerPins.createPort("N","prog_hv")
run_hv = outerPins.createPort("N","run_hv")
AVDD_by_2 = outerPins.createPort("N","AVDD_by_2")
Global_rst_b = outerPins.createPort("N","Global_rst_b")



############### Connections to Frame Pins ###############

Kvmm_G_En += Conv_AP["Kvmm_G_En"]

for i in range(int(np.ceil(np.log2(first_layer[1]*first_layer[3])))):
    Kvmm_G_bit[i] += Conv_AP["Kvmm_G_bit"][i]

AP_G_En += Conv_AP["AP_G_En"]

for i in range(3):
    AP_G_bit[i] += Conv_AP["AP_G_bit"][i]

Kvmm_AP_Dr_En += Conv_AP["Kvmm_AP_Dr_En"]

for i in range( int(np.ceil(np.log2(first_layer[2]*first_layer[3])))):
    Kvmm_AP_Dr_bit[i] += Conv_AP["Kvmm_AP_Dr_bit"][i]

Kvmm_AP_Prog_Drln += Conv_AP["Kvmm_AP_Prog_Drln"]
Kvmm_AP_Run_Drln += Conv_AP["Kvmm_AP_Run_Drln"]
SR_k_col_Din += Conv_AP["SR_k_col_Din"]
SR_k_col_RST_B += Conv_AP["SR_k_col_RST_B"]
SR_k_col_CLK += Conv_AP["SR_k_col_CLK"]

for i in range(first_layer[1]):
    Vin_inp_Ch[i] += Conv_AP["Vin_inp_Ch"][i]

SR_Intg_RST_B += Conv_AP["SR_Intg_RST_B"]
SR_Intg_Din += Conv_AP["SR_Intg_Din"]
SR_Intg_CLK += Conv_AP["SR_Intg_CLK"]
SR_Intg_CLKB += Conv_AP["SR_Intg_CLKB"]
SR_k_rw_Din += Conv_AP["SR_k_rw_Din"]
SR_k_rw_CLKB += Conv_AP["SR_k_rw_CLKB"]
SR_k_rw_RST_B += Conv_AP["SR_k_rw_RST_B"]
SR_k_rw_CLK += Conv_AP["SR_k_rw_CLK"]
AP_Relu_Vb += Conv_AP["AP_Relu_Vb"]

for i in range(first_layer[2]):
    Sub_Img_Out[i] += Conv_AP["Sub_Img_Out_glb"][i]

VTUN += Conv_AP["VTUN"]
DVDD += Conv_AP["DVDD"]
AVDD += Conv_AP["AVDD"]
GND += Conv_AP["GND"]
VINJ += Conv_AP["VINJ"]
VGPROG += Conv_AP["VGPROG"]
prog_hv += Conv_AP["prog_hv"]
run_hv += Conv_AP["run_hv"]
AVDD_by_2 += Conv_AP["AVDD_by_2"]
Global_rst_b += Conv_AP["Global_rst_b"]


################################################################################


#location_islands = ((5e4,4.1e4),(6e5,15.8e5),(4e5,15.7e5))
#location_islands = ((5e4,4.1e4),(6e5,8e5),(4e5,7.9e5))
#location_islands = ((100,100),(1e6,3.6e5))

design_limits = [4e3*1e3, 2e3*1e3]


with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 100
qparams["via"] = 20
qparams["jog"] = 60
qparams["conflict"] = 50
qparams["stage2"] = "mask none force effort 100"
qparams["stage3"] = "mask none force effort 100"


ac.compile_asic(Top,process="TSMC350nm", fileName="ConvNN_AvgPool", p_and_r = True, route=True, design_limits = design_limits, location_islands = Conv_AP["location_islands"], qparams=qparams,drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0)

