read_lef ConvNN_AvgPool/ConvNN_AvgPool.lef
read_def ConvNN_AvgPool/ConvNN_AvgPool.def
cost via 20
cost jog 80
cost block 40
cost conflict 500
passes 100
stage1 mask none force
stage2 mask none force effort 100
stage3 mask none force effort 100
layers 4
write_def ConvNN_AvgPool/ConvNN_AvgPool_qroute.def
quit
