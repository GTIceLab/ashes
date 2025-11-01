read_lef ConvNN_Layers/ConvNN_Layers.lef
read_def ConvNN_Layers/ConvNN_Layers.def
cost via 30
cost jog 60
cost block 40
cost conflict 50
passes 10
stage1 mask none force
stage2 mask none force effort 100
stage3 mask none force effort 100
layers 4
write_def ConvNN_Layers/ConvNN_Layers_qroute.def
quit
