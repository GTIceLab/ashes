grid 0.05um 0.05um
snap user
load "../../../ASHES-Skywater130nm/sky130_cells/IndirectVMM_4x2/IndirectVMM_4x2_ashes.mag"
gds write "./gds_output/IndirectVMM_4x2_ashes.gds"
load "../../../ASHES-Skywater130nm/sky130_cells/TA_FGbias_1x2/TA_FGbias_1x2_ashes.mag"
gds write "./gds_output/TA_FGbias_1x2_ashes.gds"
quit -noprompt
