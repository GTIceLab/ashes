read_lef ConvNN_AvgPool/ConvNN_AvgPool.lef
read_def ConvNN_AvgPool/ConvNN_AvgPool.def
cost via 40
cost jog 80
cost block 40
cost conflict 100
passes 100
stage1 mask none force
stage2 mask none force effort 150
stage3 mask none force effort 150
layers 4
write_def ConvNN_AvgPool/ConvNN_AvgPool_qroute.def
quit
