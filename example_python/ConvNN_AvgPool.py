import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np
import math

def Conv_AvgPool(circuit,image_size=4,inp_channels=3,out_channels=16,kernel_size=2,Conv_AvgP_Island=None,islandLoc=[0,0],debug=False):
    
    Top = circuit
    Conv_AvgP_Island = ac.Island(Top)

    # Make sure the Image size is not less than kernel size
    if (image_size < kernel_size):
        raise Exception("Error: The image_size is less than the kernel_size")
    elif ((image_size % kernel_size) != 0):
        raise Exception("Error: image_size should be divisble by kernel_size")
    
    # Make sure the Kernel size can be made with VMM4X2 std cell
    if (kernel_size*2 % 4) != 0:
        raise Exception("Error: kernel_size must be divisible by 2")
    
    kernel_cols = int(kernel_size)*inp_channels
    kernel_rows = int(kernel_size*2)  # Accounting for negative kernel weights 

    #################  Defining VMM Kernel weights #################
    Kernel_VMM = lib_new.TSMC350nm_4x2_Indirect(Top,Conv_AvgP_Island,dim=[kernel_rows//4,kernel_cols//2])
    Kernel_VMM.place([0,0])
    Kernel_VMM.markAbut()
    track_col= (kernel_cols//2)

    # Defining Horizontal Tgates to choose between kernel rows
    if (kernel_rows == 4):
        TgateHoriz_VMMout = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_only(Top,Conv_AvgP_Island,dim=[1,1])
        TgateHoriz_VMMout.place([0,track_col])
        TgateHoriz_VMMout.markAbut()
        track_col=track_col+1

    elif (kernel_rows == 8):
        TgateHoriz_VMMout_top = lib_new.Tgate_swc_fr_Kernel_Horiz_top_edge(Top,Conv_AvgP_Island,dim=[1,1])
        TgateHoriz_VMMout_top.place([0,track_col])
        TgateHoriz_VMMout_top.markAbut()

        TgateHoriz_VMMout_bot = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_edge(Top,Conv_AvgP_Island,dim=[1,1])
        TgateHoriz_VMMout_bot.place([1,track_col])
        TgateHoriz_VMMout_bot.markAbut()

        track_col=track_col+1

    else:
        TgateHoriz_VMMout_top = lib_new.Tgate_swc_fr_Kernel_Horiz_top_edge(Top,Conv_AvgP_Island,dim=[1,1])
        TgateHoriz_VMMout_top.place([0,track_col])
        TgateHoriz_VMMout_top.markAbut()

        TgateHoriz_VMMout_core = lib_new.Tgate_swc_fr_Kernel_Horiz_core(Top,Conv_AvgP_Island,dim=[(kernel_rows//4)-2,1])
        TgateHoriz_VMMout_core.place([1,track_col])
        TgateHoriz_VMMout_core.markAbut()

        TgateHoriz_VMMout_bot = lib_new.Tgate_swc_fr_Kernel_Horiz_bot_edge(Top,Conv_AvgP_Island,dim=[1,1])
        TgateHoriz_VMMout_bot.place([(1)+((kernel_rows//4)-2),track_col])
        TgateHoriz_VMMout_bot.markAbut()

        track_col=track_col+1


    ################# Defining CurrentMirror Subtractor block for positive and negative VMM outputs #################

    Isub_top = lib_new.I_Subtractor_AvgPool_top(Top,Conv_AvgP_Island,dim=[1,1])
    Isub_top.place([0,track_col])
    Isub_top.markAbut()

    if (kernel_rows > 4):
        Isub_fill = lib_new.I_Subtractor_AvgPool_core(Top,Conv_AvgP_Island,dim=[(kernel_rows//4)-1,1])
        Isub_fill.place([1,track_col])
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
        Intgr_start = lib_new.Integration_fr_AvgPool_start(Top,Conv_AvgP_Island,dim=[1,1])
        Intgr_start.place([0,track_col])
        Intgr_start.markAbut()
        track_col=track_col+1  # Keeping track of the coloumn placement idx

        if no_of_intg > 1:
            Intgr_core = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,no_of_intg-1])
            Intgr_core.place([0,track_col])
            Intgr_core.markAbut()
            track_col = track_col + no_of_intg-1 # Keeping track of the coloumn placement idx

    else:
        Intgr_start = lib_new.Integration_fr_AvgPool_start(Top,Conv_AvgP_Island,dim=[1,1])
        Intgr_start.place([0,track_col])
        Intgr_start.markAbut()
        track_col=track_col+1  # Keeping track of the coloumn placement idx
        
        start_flag=1
        if (no_of_fillers == 0):
            rows=0
            for rows in range(intg_rows):
                if (rows > 0 ):
                    track_col = track_col - intg_cols   # Keeping track of the coloumn placement idx
                    start_flag=0

                Intgr_core = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,intg_cols - (1*start_flag)])
                Intgr_core.place([rows,track_col])
                Intgr_core.markAbut()
                track_col = track_col + intg_cols - (1*start_flag) # Keeping track of the coloumn placement idx

        else:
            filler_flag=0
            rows=0
            cols=0
            for rows in range(intg_rows):

                if (rows > 0 ):
                    track_col = track_col - intg_cols # Keeping track of the coloumn placement idx
                    start_flag=0

                for cols in range(intg_cols- (1*start_flag)):

                    if (filler_flag < ((intg_cols*intg_rows)-no_of_fillers-1)):
                        Intgr_core = lib_new.Integration_fr_AvgPool_core(Top,Conv_AvgP_Island,dim=[1,1])
                        Intgr_core.place([rows,track_col])
                        Intgr_core.markAbut()
                        track_col = track_col + 1 # Keeping track of the coloumn placement idx

                    else:
                        Intgr_fill = lib_new.Integration_fr_AvgPool_filler(Top,Conv_AvgP_Island,dim=[1,1])
                        Intgr_fill.place([rows,track_col])
                        Intgr_fill.markAbut()
                        track_col = track_col + 1 # Keeping track of the coloumn placement idx

                    filler_flag = filler_flag + 1

                if (rows == 0):
                        intg_cols = intg_cols + 1 # Need to account for the next row start block


    #################  Defining FinalAvgPool and Relu #################

    # We might have to create a filler cell and change it later
    Readout_Relu = lib_new.AvgPool_n_Relu(Top,Conv_AvgP_Island,dim=[kernel_rows//4,1])
    Readout_Relu.place([0,track_col])
    Readout_Relu.markAbut()


    # Island Placement
    # -------------------------------------------------------------------------------

    #location_islands = (islandLoc[0],islandLoc[1])

    #return location_islands



Top = ac.Circuit()
Conv_AvgPool(Top,islandLoc=[100,100],debug=True)

location_islands = ((100,100),(0,0))

design_limits = [4e7, 4e7]

ac.compile_asic(Top,process="TSMC350nm", fileName="ConvNN_AvgPool", p_and_r = True, route=False, design_limits = design_limits, location_islands = location_islands)

