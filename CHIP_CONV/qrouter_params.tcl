read_lef CHIP_CONV/CHIP_CONV.lef
read_def CHIP_CONV/CHIP_CONV.def
cost via 30
cost jog 60
cost block 40
stage1 mask none force
stage2 mask none force
stage3 mask none force
layers 4
write_def CHIP_CONV/CHIP_CONV_qroute.def
quit
