read_lef Top_Conv/Top_Conv.lef
read_def Top_Conv/Top_Conv.def
cost via 50
cost jog 30
cost block 40
cost conflict 10
passes 100
stage1 mask none force
stage2 mask none force effort 100
stage3 mask none force effort 100
layers 4
write_def Top_Conv/Top_Conv_qroute.def
quit
