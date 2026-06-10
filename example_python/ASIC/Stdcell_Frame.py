import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
Top = Circuit()


# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
SmallPadFrame = SmallPadFrame(Top,FrameIsland,[1,1])
SmallPadFrame.place([0,0])
SmallPadFrame.markChipFrame()

#non-fg blocks

TGate_2nMirror_Island = Island(Top)
TGate_2nMirror = TSMC350nm_TGate_2nMirror(Top,TGate_2nMirror_Island,[1,1])
TGate_2nMirror.place([0,0])

TGate_2nMirror.IN_CM += SmallPadFrame.IO_W[0:2]
TGate_2nMirror.SelN += SmallPadFrame.IO_N[10]
TGate_2nMirror.IN_TG += SmallPadFrame.IO_N[11]
TGate_2nMirror.OUT_CM += SmallPadFrame.IO_W[2:4]
TGate_2nMirror.OUT_TG += SmallPadFrame.IO_W[8]
TGate_2nMirror.VPWR_b += SmallPadFrame.avdd_S[0]
TGate_2nMirror.GND_b += SmallPadFrame.gnd_S[0]

NandPfets_Island = Island(Top)
NandPfets = TSMC350nm_NandPfets(Top,NandPfets_Island,[1,1])
NandPfets.place([0,0])

NandPfets.GATE_N += SmallPadFrame.IO_N[10]
NandPfets.SOURCE_N += SmallPadFrame.IO_W[4]
NandPfets.GATE_P += SmallPadFrame.IO_N[11]
NandPfets.SOURCE_P += SmallPadFrame.IO_W[5]
NandPfets.DRAIN_N += SmallPadFrame.IO_W[6]
NandPfets.DRAIN_P += SmallPadFrame.IO_W[7]
NandPfets.VPWR_b += SmallPadFrame.avdd_S[0]
NandPfets.GND_b += SmallPadFrame.gnd_S[0] 

NeuralNetworkProgActFunc_Island = Island(Top)
NeuralNetworkProgActFunc = TSMC350nm_NeuralNetworkProgActFunc(Top,NeuralNetworkProgActFunc_Island,[1,1])
NeuralNetworkProgActFunc.place([0,0])

NeuralNetworkProgActFunc.I1_P += SmallPadFrame.IO_W[0]
NeuralNetworkProgActFunc.I1_N += SmallPadFrame.IO_W[1]
NeuralNetworkProgActFunc.I3_P += SmallPadFrame.IO_W[2]
NeuralNetworkProgActFunc.I3_N += SmallPadFrame.IO_W[3]
NeuralNetworkProgActFunc.V1 += SmallPadFrame.IO_N[0]
NeuralNetworkProgActFunc.V2 += SmallPadFrame.IO_N[1]
NeuralNetworkProgActFunc.V3 += SmallPadFrame.IO_N[2]
NeuralNetworkProgActFunc.V4 += SmallPadFrame.IO_N[3]
NeuralNetworkProgActFunc.VG_P += SmallPadFrame.IO_N[10]
NeuralNetworkProgActFunc.VG_N += SmallPadFrame.IO_N[11]
NeuralNetworkProgActFunc.VC += SmallPadFrame.IO_W[4]
NeuralNetworkProgActFunc.WTA += SmallPadFrame.IO_N[12]
NeuralNetworkProgActFunc.VG_PFET += SmallPadFrame.IO_N[13]
NeuralNetworkProgActFunc.WTA_ += SmallPadFrame.IO_N[14]
NeuralNetworkProgActFunc.GND_b += SmallPadFrame.gnd_S[0]
NeuralNetworkProgActFunc.VPWR_b += SmallPadFrame.avdd_S[0]

Modulation_Island = Island(Top)
Modulation = TSMC350nm_Modulation(Top,Modulation_Island,[1,1])
Modulation.place([0,0])

Modulation.I1_P += SmallPadFrame.IO_W[0]
Modulation.I1_N += SmallPadFrame.IO_W[1]
Modulation.I3_P += SmallPadFrame.IO_W[2]
Modulation.I3_N += SmallPadFrame.IO_W[3]
Modulation.V1 += SmallPadFrame.IO_N[4]
Modulation.V2 += SmallPadFrame.IO_N[5]
Modulation.V3 += SmallPadFrame.IO_N[6]
Modulation.V4 += SmallPadFrame.IO_N[7]
Modulation.VG_P += SmallPadFrame.IO_N[10]
Modulation.VG_N += SmallPadFrame.IO_N[11]
Modulation.VC += SmallPadFrame.IO_W[4]
Modulation.GND_b += SmallPadFrame.gnd_S[0]
Modulation.VPWR_b += SmallPadFrame.avdd_S[0]

TobiElement_x4_Island = Island(Top)
TobiElement_x4 = TSMC350nm_TobiElement_x4(Top,TobiElement_x4_Island,[1,1])
TobiElement_x4.place([0,0])

TobiElement_x4.A += SmallPadFrame.IO_N[10:14]
TobiElement_x4.B += SmallPadFrame.IO_S[0:4]
TobiElement_x4.GND += SmallPadFrame.gnd_N[0]
TobiElement_x4.VPWR += SmallPadFrame.avdd_N[0]

#FG blocks

WTA_IndirectProg_Island = Island(Top)
WTA_IndirectProg = TSMC350nm_4WTA_IndirectProg(Top,WTA_IndirectProg_Island,[1,1])
WTA_IndirectProg.place([0,0])

WTA_IndirectProg.VD_P += SmallPadFrame.IO_N[10:14]
WTA_IndirectProg.Iin += SmallPadFrame.IO_W[0:4]
WTA_IndirectProg.Vout += SmallPadFrame.IO_S[4:8]
WTA_IndirectProg.Vmid += SmallPadFrame.IO_S[8]
WTA_IndirectProg.Vbias += SmallPadFrame.IO_S[9]
WTA_IndirectProg.Vsel_b += SmallPadFrame.IO_S[10]
WTA_IndirectProg.Vs_b += SmallPadFrame.IO_S[12]
WTA_IndirectProg.VINJ_b += SmallPadFrame.VINJ_S[1]
WTA_IndirectProg.Vg_b += SmallPadFrame.IO_S[14]
WTA_IndirectProg.VTUN_b += SmallPadFrame.IO_E_RES[0]
WTA_IndirectProg.GND_b += SmallPadFrame.gnd_S[1]
WTA_IndirectProg.PROG_b += SmallPadFrame.IO_S[16]

Ampdet_NoFG_Island = Island(Top)
Ampdet_NoFG = TSMC350nm_Ampdet_NoFG(Top,Ampdet_NoFG_Island,[1,1])
Ampdet_NoFG.place([0,0])

Ampdet_NoFG.VD_P += SmallPadFrame.IO_N[10:12]
Ampdet_NoFG.VIN += SmallPadFrame.IO_N[12]
Ampdet_NoFG.OUTPUT += SmallPadFrame.IO_N[8]
Ampdet_NoFG.VTUN += SmallPadFrame.IO_E_RES[0]
Ampdet_NoFG.Vg_b += SmallPadFrame.IO_S[14]
Ampdet_NoFG.Vsel_b += SmallPadFrame.IO_S[10]
Ampdet_NoFG.VINJ_b += SmallPadFrame.VINJ_S[1]
Ampdet_NoFG.GND_b += SmallPadFrame.gnd_S[1]
Ampdet_NoFG.VPWR_b += SmallPadFrame.avdd_S[1]

Ampdet_Strong_Island = Island(Top)
Ampdet_Strong = TSMC350nm_Ampdet_Strong(Top,Ampdet_Strong_Island,[1,1])
Ampdet_Strong.place([0,0])

Ampdet_Strong.VD_P += SmallPadFrame.IO_N[10:12]
Ampdet_Strong.VIN += SmallPadFrame.IO_N[12]
Ampdet_Strong.OUTPUT += SmallPadFrame.IO_N[9]
Ampdet_Strong.Vsel_b += SmallPadFrame.IO_S[10:12]
Ampdet_Strong.RUN_b += SmallPadFrame.IO_S[17]
Ampdet_Strong.Vg_b += SmallPadFrame.IO_S[14:16]
Ampdet_Strong.PROG_b += SmallPadFrame.IO_S[16]
Ampdet_Strong.VTUN += SmallPadFrame.IO_E_RES[0]
Ampdet_Strong.VINJ_b += SmallPadFrame.VINJ_S[1]
Ampdet_Strong.GND_b += SmallPadFrame.gnd_S[1]
Ampdet_Strong.VPWR_b += SmallPadFrame.avdd_S[1]

C4_Island = Island(Top)
C4 = TSMC350nm_C4(Top,C4_Island,[1,1])
C4.place([0,0])

C4.VD_P += SmallPadFrame.IO_N[10:12]
C4.VIN += SmallPadFrame.IO_N[12]
C4.VREF += SmallPadFrame.IO_N[13]
C4.OUTPUT += SmallPadFrame.IO_N[18]
C4.Vsel_b += SmallPadFrame.IO_S[10:12]
C4.RUN_b += SmallPadFrame.IO_S[17]
C4.Vg_b += SmallPadFrame.IO_S[14:16]
C4.PROG_b += SmallPadFrame.IO_S[16]
C4.VTUN += SmallPadFrame.IO_E_RES[0]
C4.VINJ_b += SmallPadFrame.VINJ_S[1]
C4.GND_b += SmallPadFrame.gnd_S[1]
C4.VPWR_b += SmallPadFrame.avdd_S[1]

TA2Cell_LongL_Cab_Island = Island(Top)
TA2Cell_LongL_Cab = TSMC350nm_TA2Cell_LongL_Cab(Top,TA2Cell_LongL_Cab_Island,[1,1])
TA2Cell_LongL_Cab.place([0,0])

TA2Cell_LongL_Cab.VD_P += SmallPadFrame.IO_N[10:12]
TA2Cell_LongL_Cab.VIN1_PLUS += SmallPadFrame.IO_N[12]
TA2Cell_LongL_Cab.VIN1_MINUS += SmallPadFrame.IO_N[13]
TA2Cell_LongL_Cab.VIN2_PLUS += SmallPadFrame.IO_N[14]
TA2Cell_LongL_Cab.VIN2_MINUS += SmallPadFrame.IO_N[15]
TA2Cell_LongL_Cab.OUTPUT += SmallPadFrame.IO_N[19:21]
TA2Cell_LongL_Cab.Vsel_b += SmallPadFrame.IO_S[10:12]
TA2Cell_LongL_Cab.RUN_b += SmallPadFrame.IO_S[17]
TA2Cell_LongL_Cab.Vg_b += SmallPadFrame.IO_S[14:16]
TA2Cell_LongL_Cab.PROG_b += SmallPadFrame.IO_S[16]
TA2Cell_LongL_Cab.VTUN += SmallPadFrame.IO_E_RES[0]
TA2Cell_LongL_Cab.VINJ_b += SmallPadFrame.VINJ_S[1]
TA2Cell_LongL_Cab.GND_b += SmallPadFrame.gnd_S[1]
TA2Cell_LongL_Cab.VPWR_b += SmallPadFrame.avdd_S[1]

TA2Cell_NoFG_Island = Island(Top)
TA2Cell_NoFG = TSMC350nm_TA2Cell_NoFG(Top,TA2Cell_NoFG_Island,[1,1])
TA2Cell_NoFG.place([0,0])

TA2Cell_NoFG.VD_P += SmallPadFrame.IO_N[10:12]
TA2Cell_NoFG.VIN1_PLUS += SmallPadFrame.IO_N[12]
TA2Cell_NoFG.VIN1_MINUS += SmallPadFrame.IO_N[13]
TA2Cell_NoFG.VIN2_PLUS += SmallPadFrame.IO_N[14]
TA2Cell_NoFG.VIN2_MINUS += SmallPadFrame.IO_N[15]
TA2Cell_NoFG.OUTPUT += SmallPadFrame.IO_N[21:23]
TA2Cell_NoFG.VTUN += SmallPadFrame.IO_E_RES[0]
TA2Cell_NoFG.Vg_b += SmallPadFrame.IO_S[14]
TA2Cell_NoFG.Vsel_b += SmallPadFrame.IO_S[10]
TA2Cell_NoFG.VINJ_b += SmallPadFrame.VINJ_S[1]
TA2Cell_NoFG.GND_b += SmallPadFrame.gnd_S[1]
TA2Cell_NoFG.VPWR_b += SmallPadFrame.avdd_S[1]

TA2Cell_Strong_Island = Island(Top)
TA2Cell_Strong = TSMC350nm_TA2Cell_Strong(Top,TA2Cell_Strong_Island,[1,1])
TA2Cell_Strong.place([0,0])

TA2Cell_Strong.VD_P += SmallPadFrame.IO_N[10:12]
TA2Cell_Strong.VIN1_PLUS += SmallPadFrame.IO_N[12]
TA2Cell_Strong.VIN1_MINUS += SmallPadFrame.IO_N[13]
TA2Cell_Strong.VIN2_PLUS += SmallPadFrame.IO_N[14]
TA2Cell_Strong.VIN2_MINUS += SmallPadFrame.IO_N[15]
TA2Cell_Strong.OUTPUT += SmallPadFrame.IO_S[18:20]
TA2Cell_Strong.Vsel_b += SmallPadFrame.IO_S[10:12]
TA2Cell_Strong.RUN_b += SmallPadFrame.IO_S[17]
TA2Cell_Strong.Vg_b += SmallPadFrame.IO_S[14:16]
TA2Cell_Strong.PROG_b += SmallPadFrame.IO_S[16]
TA2Cell_Strong.VTUN += SmallPadFrame.IO_E_RES[0]
TA2Cell_Strong.VINJ_b += SmallPadFrame.VINJ_S[1]
TA2Cell_Strong.GND_b += SmallPadFrame.gnd_S[1]
TA2Cell_Strong.VPWR_b += SmallPadFrame.avdd_S[1]

TA2Cell_Weak_Island = Island(Top)
TA2Cell_Weak = TSMC350nm_TA2Cell_Weak(Top,TA2Cell_Weak_Island,[1,1])
TA2Cell_Weak.place([0,0])

TA2Cell_Weak.VD_P += SmallPadFrame.IO_N[10:12]
TA2Cell_Weak.VIN1_PLUS += SmallPadFrame.IO_N[12]
TA2Cell_Weak.VIN1_MINUS += SmallPadFrame.IO_N[13]
TA2Cell_Weak.VIN2_PLUS += SmallPadFrame.IO_N[14]
TA2Cell_Weak.VIN2_MINUS += SmallPadFrame.IO_N[15]
TA2Cell_Weak.OUTPUT += SmallPadFrame.IO_S[20:22]
TA2Cell_Weak.Vsel_b += SmallPadFrame.IO_S[10:12]
TA2Cell_Weak.RUN_b += SmallPadFrame.IO_S[17]
TA2Cell_Weak.Vg_b += SmallPadFrame.IO_S[14:16]
TA2Cell_Weak.PROG_b += SmallPadFrame.IO_S[16]
TA2Cell_Weak.VTUN += SmallPadFrame.IO_E_RES[0]
TA2Cell_Weak.VINJ_b += SmallPadFrame.VINJ_S[1]
TA2Cell_Weak.GND_b += SmallPadFrame.gnd_S[1]
TA2Cell_Weak.VPWR_b += SmallPadFrame.avdd_S[1]

Cap_Bank_Island = Island(Top)
Cap_Bank = TSMC350nm_Cap_Bank(Top,Cap_Bank_Island,[1,1])
Cap_Bank.place([0,0])

Cap_Bank.VD_P += SmallPadFrame.IO_N[10:14]
Cap_Bank.VIN += SmallPadFrame.IO_N[14:16]
Cap_Bank.OUT += SmallPadFrame.IO_N[23:25]
Cap_Bank.Vs_b += SmallPadFrame.IO_S[12:14]
Cap_Bank.VINJ_b += SmallPadFrame.VINJ_S[1]
Cap_Bank.Vsel_b += SmallPadFrame.IO_S[10:12]
Cap_Bank.Vg_b += SmallPadFrame.IO_S[14:16]
Cap_Bank.GND_b += SmallPadFrame.gnd_S[1]
Cap_Bank.VTUN += SmallPadFrame.IO_E_RES[0]

Amplifier9T_FGBias_Island = Island(Top)
Amplifier9T_FGBias = TSMC350nm_Amplifier9T_FGBias(Top,Amplifier9T_FGBias_Island,[1,1])
Amplifier9T_FGBias.place([0,0])

Amplifier9T_FGBias.VD_P += SmallPadFrame.IO_N[10]
Amplifier9T_FGBias.VD_R += SmallPadFrame.IO_N[11]
Amplifier9T_FGBias.VIN_PLUS += SmallPadFrame.IO_N[12]
Amplifier9T_FGBias.VIN_MINUS += SmallPadFrame.IO_N[13]
Amplifier9T_FGBias.Vout += SmallPadFrame.IO_S[22]
Amplifier9T_FGBias.Vsel_b += SmallPadFrame.IO_S[10]
Amplifier9T_FGBias.VTUN += SmallPadFrame.IO_E_RES[0]
Amplifier9T_FGBias.PROG_b += SmallPadFrame.IO_S[16]
Amplifier9T_FGBias.Vg_b += SmallPadFrame.IO_S[14]
Amplifier9T_FGBias.VINJ_b += SmallPadFrame.VINJ_S[1]
Amplifier9T_FGBias.VPWR_b += SmallPadFrame.avdd_S[1]
Amplifier9T_FGBias.GND_b += SmallPadFrame.gnd_S[1]

Amplifier9T_FGInputs_Bias_Island = Island(Top)
Amplifier9T_FGInputs_Bias = TSMC350nm_Amplifier9T_FGInputs_Bias(Top,Amplifier9T_FGInputs_Bias_Island,[1,1])
Amplifier9T_FGInputs_Bias.place([0,0])

Amplifier9T_FGInputs_Bias.VD_P += SmallPadFrame.IO_N[10:12]
Amplifier9T_FGInputs_Bias.Vin_PLUS += SmallPadFrame.IO_N[12]
Amplifier9T_FGInputs_Bias.Vin_MINUS += SmallPadFrame.IO_N[13]
Amplifier9T_FGInputs_Bias.Vout += SmallPadFrame.IO_S[23]
Amplifier9T_FGInputs_Bias.VINJ_b += SmallPadFrame.VINJ_S[1]
Amplifier9T_FGInputs_Bias.Vsel_b += SmallPadFrame.IO_S[10:12]
Amplifier9T_FGInputs_Bias.Vg_b += SmallPadFrame.IO_S[14:16]
Amplifier9T_FGInputs_Bias.VTUN += SmallPadFrame.IO_E_RES[0]
Amplifier9T_FGInputs_Bias.PROG_b += SmallPadFrame.IO_S[16]
Amplifier9T_FGInputs_Bias.VPWR_b += SmallPadFrame.avdd_S[1]
Amplifier9T_FGInputs_Bias.GND_b += SmallPadFrame.gnd_S[1]

#4x2 isolated

indirect_4x2_Island = Island(Top)
indirect_4x2 = TSMC350nm_4x2_Indirect(Top,indirect_4x2_Island,[1,1])
indirect_4x2.place([0,0])

indirect_4x2.Vd_P += SmallPadFrame.IO_S[32:36]
indirect_4x2.Vd_R += SmallPadFrame.IO_S[36:40]
indirect_4x2.Vs_b += SmallPadFrame.IO_S[40:42]
indirect_4x2.VINJ_b += SmallPadFrame.VINJ_S[1:3]
indirect_4x2.Vsel_b += SmallPadFrame.IO_S[42:44]
indirect_4x2.Vg_b += SmallPadFrame.IO_S[44:46]
indirect_4x2.GND_b += SmallPadFrame.gnd_S[1:3]
indirect_4x2.VTUN += SmallPadFrame.IO_E_RES[0]

Direct_4x2_Island = Island(Top)
Direct_4x2 = TSMC350nm_4x2_Direct(Top,Direct_4x2_Island,[1,1])
Direct_4x2.place([0,0])

Direct_4x2.Vd += SmallPadFrame.IO_E[0:4]
Direct_4x2.Vs += SmallPadFrame.IO_E[4:6]
Direct_4x2.VINJ += SmallPadFrame.VINJ_N[1:3]
Direct_4x2.Vg += SmallPadFrame.IO_E[6:8]
Direct_4x2.GND += SmallPadFrame.gnd_N[1:3]
Direct_4x2.VTUN += SmallPadFrame.IO_E_RES[0]

# Compilation
#-------------------------------------------------------------------------------
design_limits = [7e6, 6.21e6]
location_islands = ((20600, 20000),(300000,1000600),(500000,1000600),(700000,1000600),(900000,1000600),(1100000,1000600),(1300000,1000600),(1600000,1000600),(1900000,1000600),(2200000,1000600),(2500000,1000600),(2800000,1000600),(3100000,1000600),(3400000,1000600),(3700000,1000600),(4000000,1000600),(4300000,1000600),(4600000,1000600),(4900000,1000600))
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="Stdcell_Frame",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
