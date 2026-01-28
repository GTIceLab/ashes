import ashes_fg as af
import numpy as np
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *
import re
#------------------------------CAB merge procedure:
#------------------------------cd into example_json and "python json2py.py" (to make cab1 and cab2 python files)
#------------------------------cd .., uncomment line 17 and 18, comment line 20, "python py2asic.py" (to make cab1 and cab2 gds files)
#------------------------------cd into example_json and "python cab_merge.py" (copy the gds into vis350 library as a cell, then produce Fabric.py)
#------------------------------cd .., comment line 17 and 18, uncomment line 20, "python py2asic.py" (place Fabric.py to make a final fabric)



#exec(open("./Wafer5_Synthesis/Macro_SmallFrame_Route.py").read())

#exec(open("./example_python/AlgorithmicADC.py").read())

#exec(open("./example_python/Mod_WTA.py").read())

#exec(open("./example_python/FPAA_Optimized.py").read())

#exec(open("./example_python/FPAA_Sensor.py").read())

#exec(open("./example_python/FPAA_PDE.py").read())

#exec(open("./example_python/FPAA_NN.py").read())

#exec(open("./example_python/Stdcell_Frame.py").read())

#exec(open("./example_python/ALICEtoFrame.py").read())

#exec(open("./example_python/CHIP_DataConverter.py").read())

#exec(open("./Wafer5_Synthesis/Macro2_SmallFrame_Route.py").read())

#exec(open("./Wafer5_Synthesis/11_SML_DataConverters.py").read())

#exec(open("./example_python/ConvNN_AvgPool.py").read())

#exec(open("./example_python/ConvNN.py").read())

#exec(open("./example_python/ConvNN_Layers.py").read())

#exec(open("./example_python/TestFullRoute.py").read())

#exec(open("./example_python/CHIP_ConvNN.py").read())

#exec(open("./example_python/CHIP_ConvNN_nonflip.py").read())

#exec(open("./example_python/Top_ConvNN.py").read())

#exec(open("./example_python/sky130/Trail.py").read())

#exec(open("./example_python/Trail.py").read())
#

exec(open("./py2asic_test/LPF_MeadSOS.py").read())
