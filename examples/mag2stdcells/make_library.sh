#!/bin/bash

# clean temp dirs
rm ./mag2gds/* ./fixed_pins/*

# mag -> gds
python ../../ashes_fg/layout2gds/mag2gds.py  --output mag2gds  --files \
    ../../../ASHES-Skywater130nm/sky130_cells/Cap_Bank/Cap_Bank.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/G_or_S_IndrctSwcs/G_or_S_IndrctSwcs.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirctGswc_OutMat/IndirectGswc_OutMat.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_4x1/IndirectVMM_4x1.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_4x2/IndirectVMM_4x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_Bot_Bmat_4x2/IndirectVMM_Bot_Bmat_4x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_GSwcs_1x2/IndirectVMM_GSwcs_1x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_Top_AorBmat_4x2/IndirectVMM_Top_AorBmat_4x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Level_Shifter/Horizontal_LS/level_shifter_horizontal.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Level_Shifter/Vertical_LS/level_shifter_vertical.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Pcells/*.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_east.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_filler_off_diagonal.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_NS_routing_diagonal.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_west.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/TA_FGbias_1x2/TA_FGbias_1x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/TGate_2nMirror/TGate_2nMirror.mag
    # ../../../ASHES-Skywater130nm/sky130_cells/Mux/Layout/GateMuxSwc.mag \
    # magic couldn't convert the above one to gds - probably an absolute path issue with the cell

# gds -> gds with disambiguated pins
python ../../ashes_fg/layout2gds/fix_gds.py --output fixed_pins mag2gds/*.gds