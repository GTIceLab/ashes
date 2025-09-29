import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

Top = Circuit()

# Placement
DelayLineIsland = Island(Top)

DrainDecoder = True
V_NW=None

# Delay Line Sizing
rows = 32
columns = 9

# VMMDemod Sizing
dim = [300,320]

# VMMWTA Sizing
dim2 = [200,300]

FakeIsland=Island(Top)
FakeCells = [0]*columns
for i in range(columns):
    FakeCells[i]=FakeCellGateDecoder(Top,FakeIsland)
for i in range(columns):
    FakeCells[i].place([0,i])
    FakeCells[i].markAbut()
gateBits_Del = int(np.ceil(np.log2(columns*2)))
print(gateBits_Del)
GateDecoder_Del = STD_IndirectGateDecoder(Top,FakeIsland,gateBits_Del)
GateSwitches_Del = STD_IndirectGateSwitch(Top,FakeIsland,columns+1)
DelayLine_instances = [0]*columns
for i in range(columns):
    DelayLine_instances[i] = [0]*rows
for i in range(columns):
    for j in range(rows):
        DelayLine_instances[i][j] = "DelayLine_"+str(i)+"_"+str(j)
for i in range(columns):
    for j in range(rows):
        DelayLine_instances[i][j] = DelayLine(Top,DelayLineIsland)
        DelayLine_instances[i][j].place([j,i])
for i in range(columns):
    for j in range(rows):
        if i==columns-1:
            DelayLine_instances[i][j].V_NE += DelayLine_instances[i][j].V_SE
        else:
            DelayLine_instances[i][j].V_NE += DelayLine_instances[i+1][j].V_NW
            DelayLine_instances[i][j].V_SE += DelayLine_instances[i+1][j].V_SW
# FG Programming
# -------------------------------------------------------------------------------
if DrainDecoder==True:
    drainBits_Del = int(np.ceil(np.log2(rows*4)))
    print(drainBits_Del)
    DrainDecoder_Del = STD_DrainDecoder(Top,DelayLineIsland,bits=drainBits_Del)
    DrainSelect_Del = RunDrainSwitch(Top,DelayLineIsland,num=rows)
    DrainSwitch_Del = DrainCutoff(Top,DelayLineIsland,num=rows)
    for j in range(columns):
        for i in range(rows):
            DrainSwitch_Del.PR[4*i] += DelayLine_instances[j][i].VD_P[0]
            DrainSwitch_Del.PR[(4*i)+1] += DelayLine_instances[j][i].VD_P[1]
            DrainSwitch_Del.PR[(4*i)+2] += DelayLine_instances[j][i].VD_P[2]
            DrainSwitch_Del.PR[(4*i)+3] += DelayLine_instances[j][i].VD_P[3]
            DrainSwitch_Del.In[4*i] += DelayLine_instances[j][i].VD_R[0]
            DrainSwitch_Del.In[(4*i)+1] += DelayLine_instances[j][i].VD_R[1]
else:
    VD_P0=[0]*rows
    VD_P1=[0]*rows
    VD_P2=[0]*rows
    VD_P3=[0]*rows
    VD_R0=[0]*rows
    VD_R1=[0]*rows
    VD_R2=[0]*rows
    VD_R3=[0]*rows
    for j in range(columns-1):
        for i in range(rows):
            DelayLine_instances[j][i].VD_P[0] += DelayLine_instances[j+1][i].VD_P[0]
            DelayLine_instances[j][i].VD_P[1] += DelayLine_instances[j+1][i].VD_P[1]
            DelayLine_instances[j][i].VD_P[2] += DelayLine_instances[j+1][i].VD_P[2]
            DelayLine_instances[j][i].VD_P[3] += DelayLine_instances[j+1][i].VD_P[3]
            DelayLine_instances[j][i].VD_R[0] += DelayLine_instances[j+1][i].VD_R[0]
            DelayLine_instances[j][i].VD_R[1] += DelayLine_instances[j+1][i].VD_R[1]
    for i in range(rows):
        VD_P0[i] = DelayLine_instances[0][i].VD_P[0]
        VD_P1[i] = DelayLine_instances[0][i].VD_P[1]
        VD_P2[i] = DelayLine_instances[0][i].VD_P[2]
        VD_P3[i] = DelayLine_instances[0][i].VD_P[3]
        VD_R0[i] = DelayLine_instances[0][i].VD_R[0]
        VD_R1[i] = DelayLine_instances[0][i].VD_R[1]
for i in range(columns):
    GateSwitches_Del.Vg[i*2] += DelayLine_instances[i][0].Vg[0]
    GateSwitches_Del.Vg[i*2+1] += DelayLine_instances[i][0].Vg[1]
    GateSwitches_Del.CTRL_B[i*2] += DelayLine_instances[i][0].Vsel[0]
    GateSwitches_Del.CTRL_B[i*2+1] += DelayLine_instances[i][0].Vsel[1]
    GateSwitches_Del.VINJ[i] += DelayLine_instances[i][0].VINJ
    GateSwitches_Del.GND_B[i] += DelayLine_instances[i][0].GND
    GateSwitches_Del.VTUN[i] += DelayLine_instances[i][0].VTUN
    GateSwitches_Del.VDD[i] += DelayLine_instances[i][0].VDD
if V_NW==None:
    V_NW = [0]*rows
    for i in range(rows):
        V_NW[i] = DelayLine_instances[0][i].V_NW
else:
    for i in range(rows):
        V_NW[i] = DelayLine_instances[0][i].V_NW
ladder_out = [0]*(rows*columns)
pointer = 0
for i in range(columns):
    for j in range(rows):
        ladder_out[pointer] = DelayLine_instances[i][j].V_NE
        pointer += 1
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
# Connections
count = 0
for i in range(columns):
    if i == 0:
        for j in range(rows):
            DelayLine_instances[i][j].V_NW += GateDecoder_Mod.VGRUN[count]
            count += 1
        for j in range(rows):
            DelayLine_instances[i][j].V_NE += GateDecoder_Mod.VGRUN[count]
            count += 1
    else:
        for j in range(rows):
            DelayLine_instances[i][j].V_NE += GateDecoder_Mod.VGRUN[count]
            count += 1

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

WTA = TSMC350nm_4WTA_IndirectProg_noncab(Top,island=VMMWTAIsland,dim=[numRows2,1])
WTA.place([0,numCols+1])
        
if decoderPlace == True:
    # Add decoders
    gateBits_WTA = int(np.ceil(np.log2(dim2[1])))
    GateDecoder_WTA= STD_IndirectGateDecoder(Top,VMMWTAIsland,gateBits_WTA)
    GateSwitches_WTA = STD_IndirectGateSwitch(Top,VMMWTAIsland,numCols2-1)

    if inputs != None:
        inputs += GateDecoder_WTA.VGRUN[0:numCols2*2]

    drainBits_WTA = int(np.ceil(np.log2(dim2[0])))
    DrainDecoder_WTA = STD_DrainDecoder(Top,VMMWTAIsland,drainBits_WTA)
    DrainSel_WTA = STD_DrainSelect(Top,VMMWTAIsland,numRows2)
    DrainSwitches_WTA = STD_DrainSwitch(Top,VMMWTAIsland,numRows2)

#Connections
#for i in range(numRows):
    #Modulation.V4[4*i] += GateDecoder_WTA.VGRUN[4*i]
    #Modulation.V1[4*i+1] += GateDecoder_WTA.VGRUN[4*i+1]
    #Modulation.V2[4*i+2] += GateDecoder_WTA.VGRUN[4*i+2]
    #Modulation.V3[4*i+3] += GateDecoder_WTA.VGRUN[4*i+3]

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
# Delay Lines
# --------------------------------------------------------------------------------------
DrainlineP_Del = outerPins.createPort("W","Drainline_Prog_Del")
DrainlineR_Del= outerPins.createPort("W","Drainline_Run_Del")
GateEnable_Del = outerPins.createPort("N","GateEnable_Del")
GateB_Del = outerPins.createPort("N","GateB_Del",dimension=gateBits_Del)
DrainEnable_Del = outerPins.createPort("W","DrainEnable_Del")
DrainB_Del = outerPins.createPort("W","DrainB_Del",dimension=drainBits_Del)
# Delay Lines
# --------------------------------------------------------------------------------------
DrainlineP_Mod = outerPins.createPort("W","Drainline_Prog_Mod")
DrainlineR_Mod= outerPins.createPort("W","Drainline_Run_Mod")
GateEnable_Mod = outerPins.createPort("N","GateEnable_Mod")
GateB_Mod = outerPins.createPort("N","GateB_Mod",dimension=gateBits_Mod)
DrainEnable_Mod = outerPins.createPort("W","DrainEnable_Mod")
DrainB_Mod = outerPins.createPort("W","DrainB_Mod",dimension=drainBits_Mod)
#DemodOUT = outerPins.createPort("E","DemodOUT",dimension = dim[0])
VG_N = outerPins.createPort("N","VG_N")
VG_P = outerPins.createPort("N","VG_P")
VC = outerPins.createPort("N","VC")
# Pin Connections Delay Lines
# -------------------------------------------------------------------------------
for i in range(2*columns-1):
    GateSwitches_Del.RUN_IN[i] += VGRUN
GateSwitches_Del.Vgsel += VGPROG
GateSwitches_Del.PROG += PROG
GateSwitches_Del.RUN += RUN
GateSwitches_Del.vtun_l += VTUN
GateDecoder_Del.VINJV += VINJ_N
GateDecoder_Del.GNDV += GND_N
GateDecoder_Del.ENABLE += GateEnable_Del
#for i in range(gateBits_Del):
    #GateDecoder_Del.IN[i] += GateB_Del[i]
DrainSwitch_Del.VDD += VINJ_S
DrainSwitch_Del.GND += GND_S
DrainSwitch_Del.RUN += RUN
DrainSelect_Del.VINJ += VINJ_N
DrainSelect_Del.GND += GND_N
DrainSelect_Del.prog_drainrail += DrainlineP_Del
DrainSelect_Del.run_drainrail += DrainlineR_Del
DrainDecoder_Del.VINJ += VINJ_N
DrainDecoder_Del.GND += GND_N
#for i in range(drainBits_Del):
    #DrainDecoder_Del.IN[i] += DrainB_Del[i]
#DrainDecoder_Del.IN += DrainB_Del
DrainDecoder_Del.ENABLE += DrainEnable_Del
# Pin Connections Modulation
# -------------------------------------------------------------------------------
for i in range(2*columns-1):
    GateSwitches_Mod.RUN_IN[i] += VGRUN
GateSwitches_Mod.Vgsel += VGPROG
GateSwitches_Mod.PROG += PROG
GateSwitches_Mod.RUN += RUN
GateSwitches_Mod.vtun_l += VTUN
GateDecoder_Mod.VINJV += VINJ_N
GateDecoder_Mod.GNDV += GND_N
GateDecoder_Mod.ENABLE += GateEnable_Mod
#for i in range(gateBits_Mod):
    #GateDecoder_Mod.IN[i] += GateB_Mod[i]
DrainSwitches_Mod.VDD += VINJ_S
DrainSwitches_Mod.GND += GND_S
DrainSwitches_Mod.RUN += RUN
DrainSel_Mod.VINJ += VINJ_N
DrainSel_Mod.GND += GND_N
DrainSel_Mod.prog_drainrail += DrainlineP_Mod
DrainSel_Mod.run_drainrail += DrainlineR_Mod
DrainDecoder_Mod.VINJ += VINJ_N
DrainDecoder_Mod.GND += GND_N
#for i in range(drainBits_Mod):
    #DrainDecoder_Mod.IN[i] += DrainB_Mod[i]
#DrainDecoder_Del.IN += DrainB
DrainDecoder_Mod.ENABLE += DrainEnable_Mod
#for i in range(numRows):
#    Modulation.V4[i] += VMMWTA.VGRUN[4*i]
#    Modulation.V1[i] += DemodOUT[i*4+1]
#    Modulation.V2[i] += DemodOUT[i*4+2]
#    Modulation.V3[i] += DemodOUT[i*4+3]
Modulation.VC += VC
Modulation.GND += GND_N
Modulation.VPWR += AVDD
Modulation.VG_N += VG_N
Modulation.VG_P += VG_P

# Island Placement Offsets
# ------------------------------------------------------------------------
if numRows < 5:
    X_val = ((numCols-1)*27000) + 125000
    Y_val = numRows*23000
else:
    X_val = ((numCols-1)*3000) + 550000
    Y_val = (numRows*22000) + 250000 +750
offset = 100000
#offset = 50000
#mult = 1.2
mult = 4.4
#design_limits = [7e5, 8e5]
design_limits = [9e6, 8e6]
#location_islands = ((200000,offset),(240000,(22000*10)+10000+offset),(100000,320000),(mult*X_val,320000))
location_islands = ((400000,offset),(740000,(22000*32)+90000+offset),(400000,1500000),(4800000+mult*X_val,1500000),(1000000,offset))
#design_limits = [1e6, 3e6]
#location_islands = ((50000,25000),(240000,22000*130))
compile_asic(Top,process="TSMC350nm",fileName="CommBenchmark",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=10)