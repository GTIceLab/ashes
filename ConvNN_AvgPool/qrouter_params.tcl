read_lef ConvNN_AvgPool/ConvNN_AvgPool.lef
read_def ConvNN_AvgPool/ConvNN_AvgPool.def
cost via 90
cost block 40
stage1 mask none force
stage2 mask none limit 100 force
stage3 mask none force
layers 4
write_def ConvNN_AvgPool/ConvNN_AvgPool_qroute.def
quit
