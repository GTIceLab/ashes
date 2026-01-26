read_lef Sky130_Trail/Sky130_Trail.lef
read_def Sky130_Trail/Sky130_Trail.def
cost via 80
cost jog 30
cost conflict 50
passes 100
stage1 mask none
stage2 mask none force effort 100
stage3 mask none force effort 100
write_def Sky130_Trail/Sky130_Trail_qroute.def
write_failed Sky130_Trail/Sky130_Trail_report.txt
quit
