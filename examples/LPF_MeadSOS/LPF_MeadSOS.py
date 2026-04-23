import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import LPF as lpf

design_limits = (5e5,5e5)
location_islands = ((50000,25000),(0,0))

Top = ac.Circuit()
lpf.LPF_MeadSOS(Top,5)
