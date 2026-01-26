import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np
import json


Top = ac.Circuit()

######### VMM Island #########

## Vectorized method (Abuts automatically)
VMM_Island = Island(Top)
VMMs = lib_new.TSMC350nm_4x2_Indirect(Top,VMM_Island,dim=[4,4])
VMMs.place([0,0])

## Non Vectorized method
# VMM_Island = Island(Top)
# VMMs = [[None for _ in range(4)] for _ in range(4)]

# for i in range(4):
#     for j in range(4):
#         VMMs[i][j] = lib_new.IndirectVMM_4x2(Top,VMM_Island,dim=[1,1])
#         VMMs[i][j].place([i,j])
#         VMMs[i][j].markAbut()

###########################


######### TA Island #########

## Vectorized method (Abuts automatically)
TA_Island = Island(Top)
TAs = lib_new.TSMC350nm_TA2Cell_NoFG(Top,TA_Island,dim=[4,1])
TAs.place([0,0])


## Non Vectorized method
# TA_Island = Island(Top)
# TAs = [[None for _ in range(1)] for _ in range(4)]

# for i in range(4):
#     for j in range(1):
#         TAs[i][j] = lib_new.TA_FGbias_1x2(Top,TA_Island,dim=[1,1])
#         TAs[i][j].place([i,0])
#         TAs[i][j].markAbut()

###########################

########### Frame Pins Definition ###########

outerPins = frame(Top)

Vg_lines = outerPins.createPort("N","Vg", dimension = 9)
Vsel_lines = outerPins.createPort("N","Vsel", dimension = 9)
Vd_P_lines = outerPins.createPort("W","Vd_P", dimension = 16)
Output_lines = outerPins.createPort("E","Output", dimension = 8)

###########################


########### Wire/Net Definition ###########

VINJ = Wire(Top)
GND = Wire(Top)
AVDD = Wire(Top)
VTUN = Wire(Top)
TA_inp = [Wire(Top) for _ in range(16)]


# Vg_lines = [Wire(Top) for _ in range(9)]
# Vsel_lines = [Wire(Top) for _ in range(9)]
# Vd_P_lines = [Wire(Top) for _ in range(16)]
# Output_lines = [Wire(Top) for _ in range(8)]

###########################  


########### Connection Definition ###########

# connections in VMM array

for i in range(8):
    Vg_lines[i] += VMMs.Vg[i]
    Vsel_lines[i] += VMMs.Vsel[i]
    VINJ += VMMs.VINJ[i]
    AVDD += VMMs.Vs[i]

for i in range(4):
    VTUN += VMMs.VTUN[i]
    GND += VMMs.GND[i]

# for j in range(4):
#     for i in range(4):
#         print(np.shape(VMMs.Vd_P))
#         Vd_P_lines[i] += VMMs.Vd_P[i + 16*j]

for i in range(16):
    Vd_P_lines[i] += VMMs.Vd_P[i]

# for j in range(1,5):
#     for i in range(4):
#         TA_inp[i] += VMMs.Vd_R[i + 12*j]

for i in range(16):
    TA_inp[i] += VMMs.Vd_R[i]

# connections in TA array

VINJ += TAs.VINJ[0]
GND += TAs.GND[0]
VTUN += TAs.VTUN[0]
AVDD += TAs.VPWR[0]

Vg_lines[8] += TAs.Vg[0]
Vsel_lines[8] += TAs.Vsel[0]

for i in range(8):
    Vd_P_lines[i] += TAs.VD_P[i]

for i in range(0,3,1):
    TA_inp[i] += TAs.VIN1_PLUS[i//2]
    TA_inp[i + 4] += TAs.VIN2_PLUS[i//2]
    TA_inp[i + 8] += TAs.VIN1_MINUS[i//2]
    TA_inp[i + 12] += TAs.VIN2_MINUS[i//2]

for i in range(8):
    Output_lines[i] += TAs.OUTPUT[i]
 
###########################



########### Island Placement Definition ###########

location_islands = ((50e3,70e3),
                    (50e3 + 200e3, 70e3))

###########################



######################################## Compilation ########################################
design_limits = [500*1e3, 500*1e3]


with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 10
qparams["via"] = 30
qparams["jog"] = 60
qparams["conflict"] = 50
qparams["stage2"] = "mask none force effort 50"
qparams["stage3"] = "mask none force effort 50"


ac.compile_asic(Top,process="tsmc_350nm", fileName="tsmc350_Trail", p_and_r = True, route=True, design_limits = design_limits, location_islands = location_islands, qparams=qparams)

