import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

import json
import numpy as np

Top = Circuit()

# Placement
DelayLineIsland = Island(Top)

DrainDecoder = True
V_NW=None

# Delay Line Sizing
rows = 40
columns = 9

FakeIsland=Island(Top)
FakeCells = [0]*(columns+1)
for i in range(columns+1):
    FakeCells[i]=FakeCellGateDecoder(Top,FakeIsland)
for i in range(columns+1):
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
    GateSwitches_Del.GND[i] += DelayLine_instances[i][0].GND
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

Gate_Route_Del = Island(Top)
GR_Del = Gate_Routing_NoVGRUN(Top,dim=(1,int((columns+1)/2)-1),island=Gate_Route_Del)
GR_Del.place([0,0])

Gate_Route_Half = Island(Top)
GR_Half = Gate_Routing_Half(Top,dim=(1,1),island=Gate_Route_Half)
GR_Half.place([0,0])

Scanner_Island = Island(Top)
Scanner = [0]*3
for i in range(3):
    Scanner[i] = "Scanner_"+str(i)
for i in range(3):
    Scanner[i] = TSMC350nm_VerticalScanner(Top, Scanner_Island)
    Scanner[i].place([i,0])

DelayLine_instances[0][rows-1].V_NW += Scanner[0].In[0]
DelayLine_instances[0][rows-1].V_NE += Scanner[0].In[1]
DelayLine_instances[1][rows-1].V_NE += Scanner[0].In[2]
DelayLine_instances[2][rows-1].V_NE += Scanner[0].In[3]
DelayLine_instances[3][rows-1].V_NE += Scanner[1].In[0]
DelayLine_instances[4][rows-1].V_NE += Scanner[1].In[1]
DelayLine_instances[5][rows-1].V_NE += Scanner[1].In[2]
DelayLine_instances[6][rows-1].V_NE += Scanner[1].In[3]
DelayLine_instances[7][rows-1].V_NE += Scanner[2].In[0]
DelayLine_instances[8][rows-1].V_NE += Scanner[2].In[1]

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
GateB = outerPins.createPort("N","GateB",dimension=gateBits_Del)
DrainB = outerPins.createPort("W","DrainB",dimension=drainBits_Del)
DrainlineP = outerPins.createPort("W","Drainline_Prog")
DrainlineR = outerPins.createPort("W","Drainline_Run")
Input = outerPins.createPort("W","Input",dimension=rows)
OUTS = outerPins.createPort("N","OUTS",dimension=(rows*columns)+rows)

Scan_out = outerPins.createPort("S","WTA_out")
Din = outerPins.createPort("S","Din")
CLK = outerPins.createPort("S","CLK")
RSTBar = outerPins.createPort("S","RSTBar")
# Delay Lines
# --------------------------------------------------------------------------------------
GateEnable_Del = outerPins.createPort("N","GateEnable_Del")
DrainEnable_Del = outerPins.createPort("W","DrainEnable_Del")

WTA_CTRL_B = outerPins.createPort("E","WTA_CTRL_B",dimension=2)
WTA_Vg = outerPins.createPort("E","WTA_Vg",dimension=2)
WTA_Prog = outerPins.createPort("E","WTA_Prog")
# Pin Connections Delay Lines
# -------------------------------------------------------------------------------
for i in range(rows):
    DelayLine_instances[0][i].V_NW += Input[i]
#for i in range(2*columns-1):
    #GateSwitches_Del.RUN_IN[i] += VGRUN
GR_Del.VGRUN += VGRUN
GR_Half.AVDD += AVDD
GateSwitches_Del.Vgsel += VGPROG
GateSwitches_Del.PROG += PROG
GateSwitches_Del.RUN += RUN
GateSwitches_Del.vtun_l += VTUN
GateDecoder_Del.VINJV += VINJ_N
GateDecoder_Del.GNDV += GND_N
for i in range((columns+1)*2):
    GateDecoder_Del.VGRUN[i] += AVDD
GateDecoder_Del.ENABLE += GateEnable_Del
for i in range(gateBits_Del):
    GateDecoder_Del.IN[i] += GateB[i]
DrainSwitch_Del.VDD += VINJ_S
DrainSwitch_Del.GND += GND_S
DrainSwitch_Del.RUN += RUN
DrainSelect_Del.VINJ += VINJ_N
DrainSelect_Del.GND += GND_N
DrainSelect_Del.prog_drainrail += DrainlineP
DrainSelect_Del.run_drainrail += DrainlineR
DrainDecoder_Del.VINJ += VINJ_N
DrainDecoder_Del.GND += GND_N
for i in range(drainBits_Del):
    DrainDecoder_Del.IN[i] += DrainB[i]
#DrainDecoder_Del.IN += DrainB_Del
DrainDecoder_Del.ENABLE += DrainEnable_Del

GateSwitches_Del.VDD[18] += AVDD
GateSwitches_Del.VDD[19] += GateSwitches_Del.VDD[18]
GateSwitches_Del.CTRL_B[18] += WTA_CTRL_B[0]
GateSwitches_Del.CTRL_B[19] += WTA_CTRL_B[1]
GateSwitches_Del.Vg[18] += WTA_Vg[0]
GateSwitches_Del.Vg[19] += WTA_Vg[1]

Scanner[0].Out += Scan_out
Scanner[0].Din += Din
Scanner[0].CLK += CLK
Scanner[0].RSTBar += RSTBar
Scanner[0].VDD += AVDD
Scanner[0].GND += GND_S

count = 0
for i in range(columns):
    if i == 0:
        for j in range(rows):
            DelayLine_instances[i][j].V_NW += OUTS[count]
            count += 1
        for j in range(rows):
            DelayLine_instances[i][j].V_NE += OUTS[count]
            count += 1
    else:
        for j in range(rows):
            DelayLine_instances[i][j].V_NE += OUTS[count]
            count += 1

with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 50
qparams["via"] = 10
qparams["jog"] = 35
qparams["conflict"] = 40
qparams["stage1"] = "mask auto force"
qparams["stage2"] = "mask bbox force effort 500"
qparams["stage3"] = "mask bbox force effort 500"

offset = 120000
mult = 1.2
#mult = 4.4
#design_limits = [7e5, 8e5]
design_limits = [5e6, 5e6]
#location_islands = ((200000,offset),(240000,(22000*10)+10000+offset),(100000,320000),(mult*X_val,320000))
location_islands = ((70000,offset),(490000,(22000*rows)+90000+offset),(490000,1112001), (689180,1112001), (500000, 20000))
#design_limits = [1e6, 3e6]
#location_islands = ((50000,25000),(240000,22000*130))
compile_asic(Top,process="TSMC350nm",fileName="Delaylines",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=10)