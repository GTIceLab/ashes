import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import LPF as lpf

Top = ac.Circuit()
lpf.LPF_MeadSOS(Top,5)
