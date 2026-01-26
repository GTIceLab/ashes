read_lef tsmc350_Trail/tsmc350_Trail.lef
read_def tsmc350_Trail/tsmc350_Trail.def
cost via 30
cost jog 60
cost conflict 50
passes 10
stage1 mask none
stage2 mask none force effort 50
stage3 mask none force effort 50
write_def tsmc350_Trail/tsmc350_Trail_qroute.def
write_failed tsmc350_Trail/tsmc350_Trail_report.txt
quit
