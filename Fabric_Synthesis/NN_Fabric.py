import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
Top = Circuit()
FabricIsland = Island(Top)
col1 = NN_cab1(Top,FabricIsland,[7,1])
col1.place([0,0])
col2 = NN_cab2(Top,FabricIsland,[7,1])
col2.place([0,1])
col3 = NN_cab2(Top,FabricIsland,[7,1])
col3.place([0,2])
col4 = NN_cab2(Top,FabricIsland,[7,1])
col4.place([0,3])
col5 = NN_cab2(Top,FabricIsland,[7,1])
col5.place([0,4])
col6 = NN_cab2(Top,FabricIsland,[7,1])
col6.place([0,5])
col7 = NN_cab2(Top,FabricIsland,[7,1])
col7.place([0,6])
design_limits = [1e7, 6.21e6]
location_islands = None
compile_asic(Top,process="TSMC350nm",fileName="NN_Fabric",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
