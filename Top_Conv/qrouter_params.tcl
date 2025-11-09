read_lef Top_Conv/Top_Conv.lef
read_def Top_Conv/Top_Conv.def
cost via 50
cost jog 30
cost block 40
stage1 mask none force
stage2 mask none limit 100 force
stage3 mask none force
layers 4
write_def Top_Conv/Top_Conv_qroute.def
quit
