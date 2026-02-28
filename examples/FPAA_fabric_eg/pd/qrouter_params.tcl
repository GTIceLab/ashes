read_lef /home/payyappan3/ashes/examples/FPAA_fabric_eg/pd/cab.lef
read_def /home/payyappan3/ashes/examples/FPAA_fabric_eg/pd/cab.def
cost via 50
cost jog 30
cost block 40
stage1 mask none force
stage2 mask none limit 100 force
stage3 mask none
write_def /home/payyappan3/ashes/examples/FPAA_fabric_eg/pd/cab_qroute.def
write_failed /home/payyappan3/ashes/examples/FPAA_fabric_eg/pd/cab_report.txt
quit
