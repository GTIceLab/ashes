import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

Top = Circuit()

# VMMDemod Sizing
dim = [280,400]

# Modulation Cell
decoderPlace = True
inputs = None
if (dim[0] % 4) != 0:
    raise Exception("Error: VMM rows must be divisible by 4")
if (dim[1] % 2) != 0:
    raise Exception("Error: VMM columns must be divisible by 2")
numRows = int(dim[0]/4)
numCols = int(dim[1]/2)
VMMIsland = Island(Top)
# Create VMM and place in an island
VMM = TSMC350nm_4x2_Indirect(Top,dim=(numRows,numCols),island=VMMIsland)
VMM.place([0,0])
#VMM.markAbut()
Tgate_4 = ST_BMatrix(Top,dim=(numRows,1),island=VMMIsland)
Tgate_4.place([0,numCols])
if decoderPlace == True:
    # Add decoders
    #if inputs != None:
        #inputs += GateDecoder.VGRUN[0:numCols*2]
    gateBits_Mod = int(np.ceil(np.log2(dim[1])))
    print(gateBits_Mod)
    GateDecoder_Mod = STD_IndirectGateDecoder(Top,VMMIsland,gateBits_Mod)
    GateSwitches_Mod = STD_IndirectGateSwitch(Top,VMMIsland,numCols)
    drainBits_Mod = int(np.ceil(np.log2(dim[0])))
    print(drainBits_Mod)
    DrainDecoder_Mod = STD_DrainDecoder(Top,VMMIsland,drainBits_Mod)
    DrainSel_Mod = RunDrainSwitch(Top,VMMIsland,num=numRows)
    DrainSwitches_Mod = DrainCutoff(Top,VMMIsland,num=numRows)
Mod = Island(Top)
Modulation = TSMC350nm_Modulation(Top,dim=(numRows,1),island=Mod)
Modulation.place([0,numCols+3])
for i in range(numRows):
    Tgate_4.A[4*i] += Modulation.I1_P[i]
    Tgate_4.A[4*i+1] += Modulation.I1_N[i]
    Tgate_4.A[4*i+2] += Modulation.I3_P[i]
    Tgate_4.A[4*i+3] += Modulation.I3_N[i]

Gate_Route_Mod = Island(Top)
GR_Mod = Gate_Routing(Top,dim=(1,int((numCols+1)/2)),island=Gate_Route_Mod)
GR_Mod.place([0,0])

outerPins = frame(Top)
# General
# --------------------------------------------------------------------------------------
PROG = outerPins.createPort("N","Prog")
RUN = outerPins.createPort("N","Run")
VGRUN = outerPins.createPort("N","VGRUN")
VGPROG = outerPins.createPort("N","VGPROG")
VTUN = outerPins.createPort("N","VTUN")
AVDD = outerPins.createPort("N","AVDD")
GND_N = outerPins.createPort("N","gnd")
GND_S = outerPins.createPort("S","gnd")
VINJ_N = outerPins.createPort("N","vinj")
VINJ_S = outerPins.createPort("S","vinj")
GateB = outerPins.createPort("N","GateB",dimension=gateBits_Mod)
DrainB = outerPins.createPort("W","DrainB",dimension=drainBits_Mod)
DrainlineP = outerPins.createPort("W","Drainline_Prog")
DrainlineR = outerPins.createPort("W","Drainline_Run")

# VMMDemod
# --------------------------------------------------------------------------------------
GateEnable_Mod = outerPins.createPort("N","GateEnable_Mod")
DrainEnable_Mod = outerPins.createPort("W","DrainEnable_Mod")
#DemodOUT = outerPins.createPort("E","DemodOUT",dimension = dim[0])
VG_N = outerPins.createPort("E","VG_N")
VG_P = outerPins.createPort("E","VG_P")
VC = outerPins.createPort("E","VC")

# Pin Connections Modulation
# -------------------------------------------------------------------------------
GateSwitches_Mod.Vgsel += VGPROG
GateSwitches_Mod.PROG += PROG
GateSwitches_Mod.RUN += RUN
GateSwitches_Mod.vtun_l += VTUN
GateDecoder_Mod.VINJV += VINJ_N
GateDecoder_Mod.GNDV += GND_N
GateDecoder_Mod.ENABLE += GateEnable_Mod
for i in range(gateBits_Mod):
    GateDecoder_Mod.IN[i] += GateB[i]
DrainSwitches_Mod.VDD += VINJ_S
DrainSwitches_Mod.GND += GND_S
DrainSwitches_Mod.RUN += RUN
DrainSel_Mod.VINJ += VINJ_N
DrainSel_Mod.GND += GND_N
DrainSel_Mod.prog_drainrail += DrainlineP
DrainSel_Mod.run_drainrail += DrainlineR
DrainDecoder_Mod.VINJ += VINJ_N
DrainDecoder_Mod.GND += GND_N
for i in range(drainBits_Mod):
    DrainDecoder_Mod.IN[i] += DrainB[i]
#DrainDecoder_Del.IN += DrainB
DrainDecoder_Mod.ENABLE += DrainEnable_Mod

Tgate_4.Prog += PROG
Tgate_4.VDD += AVDD
Tgate_4.GND += GND_N

GR_Mod.AVDD += AVDD

Modulation.VC += VC
Modulation.GND_b += GND_S
Modulation.VPWR += AVDD
Modulation.VG_N += VG_N
Modulation.VG_P += VG_P
 
design_limits = [9e6, 4e6]

offset = 50000

location_islands = ((70000,offset),(5750000, offset),(237660,1612000))
compile_asic(Top,process="TSMC350nm",fileName="Modulation",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace=0,gateSpaceIdx=0,gateSpace=0)