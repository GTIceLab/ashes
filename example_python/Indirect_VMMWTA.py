import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

IndirectVMMWTACircuit = Indirect_VMMWTA(Top,[8,4],decoderPlace=True,soft=False)


design_limits = [2e6, 5e6]
location_islands=None

compile_asic(Top,process="TSMC350nm",fileName="Indirect_VMMWTA",p_and_r = True,design_limits = design_limits, location_islands = location_islands, drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=5) #keep gateSpace=5!
