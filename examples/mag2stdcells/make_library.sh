#!/bin/bash

# Before running, make sure relative paths are correct,
# and that the following directories exist: mag2gds, fixed_pins, library

# clean temp dirs and output dir
rm ./mag2gds/* ./fixed_pins/* ./library/*

# mag -> gds (be careful with backslashes!)
python ../../ashes_fg/layout2gds/mag2gds.py  --output mag2gds  --files \
    ../../../ASHES-Skywater130nm/sky130_cells/TA_FGbias_1x2/TA_FGbias_1x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Cap_Bank/Cap_Bank.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/FETs/alexpmos/alexpmos.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/TGate_2nMirror/TGate_2nMirror.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_GSwcs_1x2/IndirectVMM_GSwcs_1x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_4x2/IndirectVMM_4x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_DrainSwcs/IndirectVMM_DrainSwcs.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Level_Shifter/Horizontal_LS/level_shifter_horizontal.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Level_Shifter/Vertical_LS/level_shifter_vertical.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Volatile_Swcs/Volatile_Swcs.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_Bot_Bmat_4x2/IndirectVMM_Bot_Bmat_4x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_Top_AorBmat_4x2/IndirectVMM_Top_AorBmat_4x2.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/IndirctGswc_OutMat/IndirectGswc_OutMat.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_east.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_filler_off_diagonal.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_NS_routing_diagonal.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block_west.mag \
    ../../../ASHES-Skywater130nm/sky130_cells/Sblock/S_Block.mag \
    # TODO Tgates_Cutoff_Drlines, Decoders

# gds -> gds with disambiguated pins
python ../../ashes_fg/layout2gds/fix_gds.py --output fixed_pins mag2gds/*.gds

# generate python and json
# TODO allow batch processing in gen_stdcell_defs
for gds in fixed_pins/*.gds; do
    gen_stdcell_defs -json library/lib.json -pydef library/lib.py -pn 130nm -foundry sky "$gds"
done
