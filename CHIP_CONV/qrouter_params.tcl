read_lef CHIP_CONV/CHIP_CONV.lef
read_def CHIP_CONV/CHIP_CONV.def
cost via 20
cost jog 80
cost block 40
cost conflict 50
passes 100
stage1 mask none force
stage2 mask none force effort 100
stage3 mask none force effort 100
layers 4
write_def CHIP_CONV/CHIP_CONV_qroute.def
quit
