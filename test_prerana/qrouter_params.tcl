read_lef test_prerana/test_prerana.lef
read_def test_prerana/test_prerana.def
cost via 20
cost jog 40
cost block 40
stage1 mask none force
stage2 mask none limit 100 force
stage3 mask none force
layers 4
write_def test_prerana/test_prerana_qroute.def
quit
