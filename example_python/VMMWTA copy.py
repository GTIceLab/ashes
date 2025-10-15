import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

Top = Circuit()

# Placement

DrainDecoder = True
V_NW=None
decoderPlace = True

# Delay Line Sizing
rows = 32
columns = 9

# VMMDemod Sizing
dim = [280,320]

# VMMWTA Sizing
dim2 = [256,280]

# VMMWTA
if (dim2[0] % 4) != 0:
    raise Exception("Error: VMM rows must be divisible by 4")
if (dim2[1] % 2) != 0:
    raise Exception("Error: VMM columns must be divisible by 2")

numRows2 = int(dim2[0]/4)
numCols2 = int(dim2[1]/2)

loc = [0,0]

VMMWTAIsland = Island(Top)

VMM2 = TSMC350nm_4x2_Indirect(Top,dim=(numRows2,numCols2),island=VMMWTAIsland)
VMM2.place([0,0])

WTA = TSMC350nm_4WTA_IndirectProg_noncab_extended(Top,island=VMMWTAIsland,dim=[numRows2,1])
WTA.place([0,numCols2+1])
        
if decoderPlace == True:
    # Add decoders
    gateBits_WTA = int(np.ceil(np.log2(dim2[1])))
    GateDecoder_WTA= STD_IndirectGateDecoder(Top,VMMWTAIsland,gateBits_WTA)
    GateSwitches_WTA = STD_IndirectGateSwitch(Top,VMMWTAIsland,numCols2)

    drainBits_WTA = int(np.ceil(np.log2(dim2[0])))
    DrainDecoder_WTA = STD_DrainDecoder(Top,VMMWTAIsland,drainBits_WTA)
    DrainSel_WTA = RunDrainSwitch(Top,VMMWTAIsland,numRows2)
    DrainSwitches_WTA = DrainCutoff(Top,VMMWTAIsland,numRows2)

Scanner_Island = Island(Top)
Scanner = [0]*numRows2
for i in range(numRows2):
    Scanner[i] = "Scanner_"+str(i)
for i in range(numRows2):
    Scanner[i] = TSMC350nm_VerticalScanner(Top, Scanner_Island)
    Scanner[i].place([i,0])

for i in range(numRows2):
    WTA.Vout[i*4] += Scanner[i].In[0]
    WTA.Vout[i*4+1] += Scanner[i].In[1]
    WTA.Vout[i*4+2] += Scanner[i].In[2]
    WTA.Vout[i*4+3] += Scanner[i].In[3]

Gate_Route_WTA = Island(Top)
GR_WTA = Gate_Routing(Top,dim=(1,int((numCols2+1)/2)),island=Gate_Route_WTA)
GR_WTA.place([0,0])

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
GateB = outerPins.createPort("N","GateB",dimension=gateBits_WTA)
DrainB = outerPins.createPort("W","DrainB",dimension=drainBits_WTA)
DrainlineP = outerPins.createPort("W","Drainline_Prog")
DrainlineR = outerPins.createPort("W","Drainline_Run")
# VMMWTA
# --------------------------------------------------------------------------------------
GateEnable_WTA = outerPins.createPort("N","GateEnable_WTA")
DrainEnable_WTA = outerPins.createPort("W","DrainEnable_WTA")

WTA_out = outerPins.createPort("E","WTA_out")
Din = outerPins.createPort("E","Din")
CLK = outerPins.createPort("E","CLK")
RSTBar = outerPins.createPort("E","RSTBar")

#VMMWTA
# ------------------------------------------------------------------------
#for i in range(2*columns-1):
    #GateSwitches_WTA.RUN_IN[i] += VGRUN
GateSwitches_WTA.Vgsel += VGPROG
GateSwitches_WTA.PROG += PROG
GateSwitches_WTA.RUN += RUN
GateSwitches_WTA.vtun_l += VTUN
GateDecoder_WTA.VINJV += VINJ_N
GateDecoder_WTA.GNDV += GND_N
GateDecoder_WTA.ENABLE += GateEnable_WTA
for i in range(gateBits_WTA):
    GateDecoder_WTA.IN[i] += GateB[i]
DrainSwitches_WTA.VDD += VINJ_S
DrainSwitches_WTA.GND += GND_S
DrainSwitches_WTA.RUN += RUN
DrainSel_WTA.VINJ += VINJ_N
DrainSel_WTA.GND += GND_N
DrainSel_WTA.prog_drainrail += DrainlineP
DrainSel_WTA.run_drainrail += DrainlineR
DrainDecoder_WTA.VINJ += VINJ_N
DrainDecoder_WTA.GND += GND_N
for i in range(drainBits_WTA):
    DrainDecoder_WTA.IN[i] += DrainB[i]
#DrainDecoder_Del.IN += DrainB
DrainDecoder_WTA.ENABLE += DrainEnable_WTA

Scanner[0].Out += WTA_out
Scanner[0].Din += Din
Scanner[0].CLK += CLK
Scanner[0].RSTBar += RSTBar
Scanner[0].VDD += AVDD
Scanner[0].GND += GND_N

# Island Placement Offsets
# ------------------------------------------------------------------------
offset = 50000
#offset = 50000
mult = 1.2
#mult = 4.4
#design_limits = [7e5, 8e5]
design_limits = [7e6, 7e6]
#location_islands = ((200000,offset),(240000,(22000*10)+10000+offset),(100000,320000),(mult*X_val,320000))
location_islands = ((50000,offset),(4170000,offset),(191390,1480000))
#design_limits = [1e6, 3e6]
#location_islands = ((50000,25000),(240000,22000*130))
compile_asic(Top,process="TSMC350nm",fileName="VMMWTA",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=0)