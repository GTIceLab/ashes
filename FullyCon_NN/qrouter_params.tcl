read_lef FullyCon_NN/FullyCon_NN.lef
read_def FullyCon_NN/FullyCon_NN.def
cost via 80
cost jog 20
cost block 40
cost conflict 10
passes 50
stage1 mask none force
stage2 mask none force effort 100
stage3 mask none force effort 100
layers 4
write_def FullyCon_NN/FullyCon_NN_qroute.def
quit
