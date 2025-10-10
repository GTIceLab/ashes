import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

import numpy as np
import json

Top = Circuit()

M = Island(Top)

Mod = Mod_Adjust(Top,dim=(1,1),island=M)
Mod.place([0,0])

W = Island(Top)

WTA = VMMWTA_Adjust(Top,dim=(1,1),island=W)
WTA.place([0,0])

for i in range(280):
    Mod.VOUT[i] += WTA.VGRUN[i]

with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 50
qparams["via"] = 10
qparams["jog"] = 35
qparams["conflict"] = 40
qparams["stage1"] = "mask auto force"
qparams["stage2"] = "mask bbox force effort 500"
qparams["stage3"] = "mask bbox force effort 500"

design_limits = [8e6, 5e6]

location_islands = ((200000,2100000),(1600000,0))
compile_asic(Top,process="TSMC350nm",fileName="Mod_WTA",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=0,route=True,qparams=qparams)
