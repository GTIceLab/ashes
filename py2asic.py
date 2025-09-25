import ashes_fg as af
import numpy as np
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *

#------------------------------CAB merge procedure:
#------------------------------cd into example_json and "python json2py.py" (to make cab1 and cab2 python files)
#------------------------------cd .., uncomment line 17 and 18, comment line 20, "python py2asic.py" (to make cab1 and cab2 gds files)
#------------------------------cd into example_json and "python cab_merge.py" (copy the gds into vis350 library as a cell, then produce Fabric.py)
#------------------------------cd .., comment line 17 and 18, uncomment line 20, "python py2asic.py" (place Fabric.py to make a final fabric)




exec(open("./example_python/CHIP_DataConverter.py").read())




