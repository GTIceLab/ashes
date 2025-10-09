import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

Top = Circuit()

M = Island(Top)

Mod = Mod_Adjust(Top,dim=(1,1),island=M)
Mod.place([0,0])

W = Island(Top)

WTA = VMMWTA_Adjust(Top,dim=(1,1),island=W)
WTA.place([0,0])

for i in range(280):
    Mod.VOUT[i] += WTA.VGRUN[i]


design_limits = [8e6, 8e6]
location_islands = ((200000,2100000),(1600000,0))
compile_asic(Top,process="TSMC350nm",fileName="Mod_WTA",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=0)