
import ashes_fg as af

from ashes_fg.asic.asic_compile import *

from ashes_fg.class_lib_new import *

from ashes_fg.class_lib_mux import *

from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *

import json

Top = Circuit()



MacroIsland = Island(Top)

macro = Macro_abs(Top,MacroIsland,[1,1])

macro.place([0,0])



# TODO Fix the instances pin names:[0] to <0> or add another parsing method



# Frame

# -------------------------------------------------------------------------------

FrameIsland = Island(Top)

chipframe = ChipFrame(Top,FrameIsland,[1,1])

chipframe.place([0,0])

chipframe.markChipFrame()







#ALICE Left

DelaylinesIsland = Island(Top)

Delaylines = DelayLinesAlgFlip(Top,DelaylinesIsland,[1,1])

Delaylines.place([0,0])



#ALICE right

VMMWTAIsland = Island(Top)

VMMWTA = VMMWTAAlgFullRoute(Top,VMMWTAIsland,[1,1])

VMMWTA.place([0,0])



ModulationIsland = Island(Top)

Modulation = ModulationAlgFlip(Top,ModulationIsland,[1,1])

Modulation.place([0,0])



Delaylines.n_OUTS += Modulation.RUNO

Modulation.VOUT += VMMWTA.RUNO





# Compilation

#-------------------------------------------------------------------------------



with open('./ashes_fg/asic/qrouter_default.json') as file:

    qparams = json.load(file)



qparams["passes"] = 50

qparams["via"] = 10

qparams["jog"] = 35

qparams["conflict"] = 40

qparams["stage1"] = "mask auto force"

qparams["stage2"] = "mask bbox force effort 500"

qparams["stage3"] = "mask bbox force effort 500"



design_limits = [12e6, 7e6]





location_islands = ((250600, 4500000), (20600, 20000),(4850000,650000),(250000,250000),(700000,2600000))

# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))

# location_islands = None



compile_asic(Top,process="TSMC350nm",fileName="test_prerana",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=7,drainSpace =20,gateSpaceIdx=7,gateSpace=15)