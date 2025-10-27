read_lef ConvNN/ConvNN.lef
read_def ConvNN/ConvNN.def
cost via 20
cost jog 80
cost block 40
cost conflict 50
passes 100
stage1 mask none force
stage2 mask none force effort 100
stage3 mask none force effort 100
layers 4
write_def ConvNN/ConvNN_qroute.def
quit
