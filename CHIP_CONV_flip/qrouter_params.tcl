read_lef CHIP_CONV/CHIP_CONV.lef
read_def CHIP_CONV/CHIP_CONV.def
cost via 20
cost jog 10
cost block 40
cost conflict 5
stage1 mask 6
stage2 mask bbox force effort 15 limit 45 break
stage3 mask none force effort 30
layers 4
write_def CHIP_CONV/CHIP_CONV_qroute.def
quit
