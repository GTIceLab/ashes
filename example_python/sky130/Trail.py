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
VMMs = lib_new.IndirectVMM_4x2(Top,VMM_Island,dim=[4,4])
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
TAs = lib_new.TA_FGbias_1x2(Top,TA_Island,dim=[4,1])
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
Output_lines = outerPins.createPort("N","Output", dimension = 8)

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
    Vg_lines[i] += VMMs.Vg_n[i]
    Vsel_lines[i] += VMMs.Vsel_n[i]
    VINJ += VMMs.VINJ_n[i]
    AVDD += VMMs.Vs_n[i]

for i in range(4):
    VMMs.VTUN_n[i] += VTUN
    GND += VMMs.GND_n[i]

# for j in range(4):
#     for i in range(4):
#         print(np.shape(VMMs.Vd_P))
#         Vd_P_lines[i] += VMMs.Vd_P[i + 16*j]

for i in range(16):
    Vd_P_lines[i] += VMMs.Vd_P_e[i]

# for j in range(1,5):
#     for i in range(4):
#         TA_inp[i] += VMMs.Vd_R[i + 12*j]

for i in range(16):
    TA_inp[i] += VMMs.Vd_R_e[i]

# connections in TA array

VINJ += TAs.VINJ_n[0]
GND += TAs.GND_n[0]
#VTUN += TAs.VTUN_n[0]
AVDD += TAs.AVDD_n[0]

Vg_lines[8] += TAs.Vg_n[0]
Vsel_lines[8] += TAs.Vsel_n[0]

for i in range(8):
    Vd_P_lines[i] += TAs.Vd_P_w[i]

for i in range(0,8*2,2):
    TA_inp[i] += TAs.Vin_P_w[i//2]

for i in range(0,8*2,2):
    TA_inp[i+1] += TAs.Vin_M_w[i//2]

for i in range(8):
    Output_lines[i] += TAs.OUTPUT_e[i]
 
###########################



########### Island Placement Definition ###########

location_islands = ((30e3,42e3),
                    (30e3 + 80e3, 42e3))

# location_islands = ((160e3,120e3),
#                      (160e3 + 100e3, 120e3))

###########################



######################################## Compilation ########################################
design_limits = [200*1e3, 200*1e3]


with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 100
qparams["via"] = 80
qparams["jog"] = 30
qparams["conflict"] = 50
qparams["stage2"] = "mask none force effort 100"
qparams["stage3"] = "mask none force effort 100"



ac.compile_asic(Top,process="sky_130nm", fileName="Sky130_Trail", p_and_r = True, route=True, design_limits = design_limits, location_islands = location_islands, qparams=qparams)

