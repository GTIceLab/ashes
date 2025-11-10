import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
import json as json


Top = Circuit()

###########---------------- Pins to connect to macro
outerPins = frame(Top)

M_VGPROG = outerPins.createPort("N","M_VGPROG")
M_VGRUN = outerPins.createPort("N","M_VGRUN")
M_mmio_rg_5_vinj = outerPins.createPort("N","M_mmio_rg_5_vinj",dimension=6) 
M_Sys_Drln = outerPins.createPort("N","M_Sys_Drln", dimension=2)
M_Sig_RampADC_in = outerPins.createPort("N","M_Sig_RampADC_in",dimension=4)
M_mmio_rg_7 = outerPins.createPort("N","M_mmio_rg_7", dimension=11) 
M_mmio_rg_9 = outerPins.createPort("N","M_mmio_rg_9",dimension=16)
M_mmio_rg_10 = outerPins.createPort("N","M_mmio_rg_10",dimension=16)
M_prog_hv = outerPins.createPort("N","M_prog_hv")
M_run_hv = outerPins.createPort("N","M_run_hv")

CP_DVDD_W = outerPins.createPort("W","CP_DVDD_W")
CP_VINJ_W = outerPins.createPort("W","CP_VINJ_W")
CP_gnd_W_2 = outerPins.createPort("W","CP_gnd_W_2")
CP_IO_W_RES_0= outerPins.createPort("W","CP_IO_W_RES_0")
CP_AVDD_W= outerPins.createPort("W","CP_AVDD_W")
CP_IO_W = outerPins.createPort("W","CP_IO_W", dimension=17)

CP_AVDD_E= outerPins.createPort("E","CP_AVDD_E")
CP_VINJ_E = outerPins.createPort("E","CP_VINJ_E")
CP_GND_E_2 = outerPins.createPort("E","CP_GND_E_2")
CP_IO_E = outerPins.createPort("E","CP_IO_E", dimension=30)
CP_DVDD_E = outerPins.createPort("E","CP_DVDD_E")

CP_IO_S = outerPins.createPort("E","CP_IO_S", dimension=13)


##########################################add more system islands if needed, Praveen should have 3############################

## Define and place ConvNN layers
Conv_Layer1_Island = Island(Top)
Conv_Layer1 = ConvNN_AvgPool(Top,Conv_Layer1_Island,[1,1])
Conv_Layer1.place([0,0])

Conv_Layer2_Island = Island(Top)
Conv_Layer2 = ConvNN(Top,Conv_Layer2_Island,[1,1])
Conv_Layer2.place([0,0])

## Define and place FNN layers
FNN_Island = Island(Top)
FNN_layers = FullyCon_NN(Top,FNN_Island,[1,1])
FNN_layers.place([0,0])

#LVL shifter
LVLShifter1Island = Island(Top)
LVLShifter1 = TSMC350nm_LVLShift_x16(Top,LVLShifter1Island,[1,1])
LVLShifter1.place([0,0])

LVLShifter1.DVDD += CP_DVDD_W
LVLShifter1.GND += CP_gnd_W_2
LVLShifter1.VINJ += CP_VINJ_W

LVLShifter2Island = Island(Top)
LVLShifter2 = TSMC350nm_LVLShift_x16(Top,LVLShifter2Island,[1,1])
LVLShifter2.place([0,0])

LVLShifter2.DVDD += CP_DVDD_W
LVLShifter2.GND += CP_gnd_W_2
LVLShifter2.VINJ += CP_VINJ_W

LVLShifter1.Vin += M_mmio_rg_9[0:16]
LVLShifter2.Vin += M_mmio_rg_10[0:16]

#PROG/Run buffer

DigBufferIsland = Island(Top)
DigBuffer = TSMC350nm_DigBuffer_x2(Top,DigBufferIsland,[1,1])
DigBuffer.place([0,0])

DigBuffer.GND += CP_gnd_W_2
DigBuffer.VINJ += CP_VINJ_W
DigBuffer.In[0] += M_prog_hv
DigBuffer.In[1] += M_run_hv

#Dig Scanner for debug Island
Dig_Scanner_dbg_Island = Island(Top)

Dig_Scanner_dbg = TSMC350nm_VerticalScanner(Top,Dig_Scanner_dbg_Island,dim=[10,1])
Dig_Scanner_dbg.place([0,0])

Dig_Scanner_dbg.GND[0] += CP_gnd_W_2
Dig_Scanner_dbg.VDD[0] += CP_DVDD_E
Dig_Scanner_dbg.Din[0] += M_mmio_rg_7[8]
Dig_Scanner_dbg.RSTBar[0] += M_mmio_rg_7[9]
Dig_Scanner_dbg.CLK[0] += M_mmio_rg_7[10]
# Dig_Scanner_dbg.Qout[0] += Dig_Scanner_dbg.In[24]
# Dig_Scanner_dbg.Out_b[0] += CP_IO_S[12]

Tgts_fr_adc_meas = ST_BMatrix(Top,Dig_Scanner_dbg_Island,dim=[1,1])
Tgts_fr_adc_meas.place([20,0])

Tgts_fr_adc_meas1 = ST_BMatrix(Top,Dig_Scanner_dbg_Island,dim=[1,1])
Tgts_fr_adc_meas1.place([20,3])


#############################Analog buffer: change number if need more than 4, change decoder size accordingly######################

AnalogBufferIsland = Island(Top)
AnalogBuffer = AnalogBuffer(Top,AnalogBufferIsland,[14,1])
AnalogBuffer.place([0,0])

DrainDecoder_buf = STD_DrainDecoder(Top,AnalogBufferIsland,bits=4)
DrainSelect_buf = RunDrainSwitch(Top,AnalogBufferIsland,num=4)
DrainSwitch_buf = DrainCutoff(Top,AnalogBufferIsland,num=4)    

GateSwitch_buf = STD_IndirectGateSwitch(Top,AnalogBufferIsland,1)

AnalogBuffer.VTUN += GateSwitch_buf.VTUN
AnalogBuffer.VDD += GateSwitch_buf.VDD[0]
GateSwitch_buf.VPWR[0] += CP_AVDD_E
GateSwitch_buf.VPWR[1] += CP_AVDD_E
AnalogBuffer.GND += GateSwitch_buf.GND[0]
AnalogBuffer.VINJ += GateSwitch_buf.VINJ
AnalogBuffer.Vg += GateSwitch_buf.Vg[0]
AnalogBuffer.Vsel += GateSwitch_buf.CTRL_B[0]
AnalogBuffer.Vd_P += DrainSwitch_buf.PR[0:14]

GateSwitch_buf.VTUN_T += CP_IO_W_RES_0
GateSwitch_buf.Vgsel += M_VGPROG
GateSwitch_buf.PROG += DigBuffer.Out[0]
GateSwitch_buf.RUN += DigBuffer.Out[1]
GateSwitch_buf.VINJ_T += CP_VINJ_E
GateSwitch_buf.GND_T += CP_GND_E_2
GateSwitch_buf.RUN_IN[0] += M_VGRUN
GateSwitch_buf.RUN_IN[1] += M_VGRUN
GateSwitch_buf.decode[0] += M_mmio_rg_5_vinj[0]############################ gate decoder control for analog buffer####################

DrainSwitch_buf.VDD += CP_VINJ_E
DrainSwitch_buf.GND += CP_GND_E_2
DrainSwitch_buf.RUN += DigBuffer.Out[1]

DrainSelect_buf.VINJ += CP_VINJ_E
DrainSelect_buf.GND += CP_GND_E_2
DrainSelect_buf.prog_drainrail += M_Sys_Drln[0]
#DrainSelect_buf.run_drainrail += M_Sys_Drln[1]

#DrainDecoder_buf.VINJ += chipframe.VINJ_N[2]
#DrainDecoder_buf.GND += chipframe.gnd_N[8]
DrainDecoder_buf.ENABLE += M_mmio_rg_5_vinj[1]############################ drain decoder enable for analog buffer########################
DrainDecoder_buf.IN += M_mmio_rg_5_vinj[2:6]###########################drain decoder bits for analog buffer#########################

#System connections

# ############################################### Connections for Conv Layers ##########################

#### Wire for Global Connections ####
TEST_INP = Wire(Top)
DVDD_CONV = Wire(Top)
VTUN_chip = Wire(Top)
G_bits = [Wire(Top) for _ in range(8)]
Dr_bits = [Wire(Top) for _ in range(10)]
Global_rst_b = Wire(Top)
Prog_Drln = Wire(Top)
Run_Drln = Wire(Top)

FNN_Scanner_Din = Wire(Top)
FNN_Scanner_CLK = Wire(Top)

## ------------ Layer1 Connections------------##
Conv_Layer1.n_AP_col_ctrl_dbg[0] += Dig_Scanner_dbg.In[0]
Conv_Layer1.n_AP_col_ctrl_dbg[1] += Dig_Scanner_dbg.In[1]
Conv_Layer1.n_Final_rw_dbg += Dig_Scanner_dbg.In[2]
Conv_Layer1.n_Relu_en_b_dbg[0] += Dig_Scanner_dbg.In[3]
Conv_Layer1.n_Relu_en_b_dbg[1] += Dig_Scanner_dbg.In[4]
Conv_Layer1.n_SR_int_dbg_Q[0] += Dig_Scanner_dbg.In[5]
Conv_Layer1.n_SR_int_dbg_Q[1] += Dig_Scanner_dbg.In[6]
Conv_Layer1.n_SR_int_dbg_Q[2] += Dig_Scanner_dbg.In[7]
Conv_Layer1.n_SR_int_dbg_Q[3] += Dig_Scanner_dbg.In[8]
Conv_Layer1.n_int_rst_dbg[0] += Dig_Scanner_dbg.In[9]
Conv_Layer1.n_int_rst_dbg[1] += Dig_Scanner_dbg.In[10]
Conv_Layer1.n_intg_nxt_rw_dbg += Dig_Scanner_dbg.In[11]

# Connect the e_sub_img_out[0:35] in Layer2 Connections 
Conv_Layer1.e_sub_img_out[36] += AnalogBuffer.Vin[0]
AnalogBuffer.Vout[0] += CP_IO_E[0]
Conv_Layer1.e_sub_img_out[37] += AnalogBuffer.Vin[1]
AnalogBuffer.Vout[1] += CP_IO_E[1]

Conv_Layer1.n_AVDD +=CP_AVDD_W
Conv_Layer1.n_AVDD_by_2 += CP_IO_W[0]
Conv_Layer1.n_DVDD += DVDD_CONV
Conv_Layer1.n_GND += CP_gnd_W_2 # Make sure this is closest 

Conv_Layer1.n_VGPROG += M_VGPROG
Conv_Layer1.n_VINJ += CP_VINJ_W # Make sure this is closest 
VTUN_chip += Conv_Layer1.n_VTUN # Make sure this is closest 

Conv_Layer1.n_Vint_dbg[0] += AnalogBuffer.Vin[2]
AnalogBuffer.Vout[2] += CP_IO_E[2]
Conv_Layer1.n_Vint_dbg[1] += AnalogBuffer.Vin[3]
AnalogBuffer.Vout[3] += CP_IO_E[3]

Conv_Layer1.n_AP_G_En += LVLShifter1.OUT[0]

for _ in range(3):
    G_bits[_] += Conv_Layer1.n_AP_G_bit[_]
    
Conv_Layer1.n_AP_Relu_Vb += CP_IO_W[1]
Global_rst_b += Conv_Layer1.n_Global_rst_b
Conv_Layer1.n_Kvmm_AP_Dr_En += LVLShifter1.OUT[1]

for _ in range(10):
    Dr_bits[_] += Conv_Layer1.n_Kvmm_AP_Dr_bit[_]

Prog_Drln += Conv_Layer1.n_Kvmm_AP_Prog_Drln
Run_Drln += Conv_Layer1.n_Kvmm_AP_Run_Drln

Conv_Layer1.n_Kvmm_G_En += LVLShifter1.OUT[2]

for _ in range(4):
    G_bits[_] += Conv_Layer1.n_Kvmm_G_bit[_]
    
Conv_Layer1.n_SR_Intg_CLK += CP_IO_W[2] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_Intg_RST_B += CP_IO_W[3] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_Intg_CLKB += CP_IO_W[4] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_Intg_Din += CP_IO_W[5] #### DIG IN BUF PAD ####

Conv_Layer1.n_SR_k_col_CLK += CP_IO_W[6] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_col_RST_B += CP_IO_W[7] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_col_CLKB += CP_IO_W[8] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_col_Din += CP_IO_W[9] #### DIG IN BUF PAD ####

Conv_Layer1.n_SR_k_rw_CLK += CP_IO_W[10] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_rw_RST_B += CP_IO_W[11] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_rw_CLKB += CP_IO_W[12] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_rw_Din += CP_IO_W[13] #### DIG IN BUF PAD ####

Conv_Layer1.n_Vin_inp_Ch[0] += CP_IO_W[14] #### DIG IN BUF PAD ####
Conv_Layer1.n_Vin_inp_Ch[1] += CP_IO_W[15] #### DIG IN BUF PAD ####
Conv_Layer1.n_Vin_inp_Ch[2] += CP_IO_W[16] #### DIG IN BUF PAD ####

Conv_Layer1.n_prog_hv += DigBuffer.Out[0]
Conv_Layer1.n_run_hv += DigBuffer.Out[1]


## ------------ Layer2 Connections------------##

Conv_Layer2.n_Out_En_dbg[0] += Dig_Scanner_dbg.In[12]
Conv_Layer2.n_Out_En_dbg[1] += Dig_Scanner_dbg.In[13]
Conv_Layer2.n_Rdout_flag_dbg += Dig_Scanner_dbg.In[14]
Conv_Layer2.n_SR_Intg_dbg_Q[0] += Dig_Scanner_dbg.In[15]
Conv_Layer2.n_SR_Intg_dbg_Q[1] += Dig_Scanner_dbg.In[16]
Conv_Layer2.n_SR_int_0_Q2_dbg += Dig_Scanner_dbg.In[17]
Conv_Layer2.n_int_rst_dbg[0] += Dig_Scanner_dbg.In[18]
Conv_Layer2.n_int_rst_dbg[1] += Dig_Scanner_dbg.In[19]
Conv_Layer2.n_sample_nxt_rw_dbg += Dig_Scanner_dbg.In[20]

Conv_Layer2.n_AVDD +=CP_AVDD_E
Conv_Layer2.n_AVDD_by_2 += CP_IO_W[0]
Conv_Layer2.n_DVDD += DVDD_CONV
Conv_Layer2.n_GND += CP_GND_E_2 # Make sure this is closest 

Conv_Layer2.n_VGPROG += M_VGPROG
Conv_Layer2.n_VINJ += CP_VINJ_E # Make sure this is closest 
VTUN_chip += Conv_Layer2.n_VTUN # Make sure this is closest 

Conv_Layer2.n_Vint_dbg[0] += AnalogBuffer.Vin[4]
AnalogBuffer.Vout[4] += CP_IO_E[4]
Conv_Layer2.n_Vint_dbg[1] += AnalogBuffer.Vin[5]
AnalogBuffer.Vout[5] += CP_IO_E[5]


# Connect the s_sub_img_out[0:153], w_sub_img_out[0:21] in FNN Connections 
for _ in range(8):
    Conv_Layer2.w_sub_img_out[22+_] += CP_IO_E[6+_]

Global_rst_b += Conv_Layer2.n_Global_rst_b
Conv_Layer2.n_Kvmm_Dr_En += LVLShifter1.OUT[3]

for _ in range(8):
    Dr_bits[_] += Conv_Layer2.n_Kvmm_Dr_bit[_]
    
Conv_Layer2.n_Kvmm_G_En += LVLShifter1.OUT[4]

for _ in range(7):
    G_bits[_] += Conv_Layer2.n_Kvmm_G_bit[_]

Prog_Drln += Conv_Layer2.n_Kvmm_Prog_Drln
Run_Drln += Conv_Layer2.n_Kvmm_Run_Drln

Conv_Layer2.n_Relu_Vb += CP_IO_E[14]


Conv_Layer2.n_SR_Intg_CLK += CP_IO_E[15] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_Intg_RST_B += CP_IO_E[16] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_Intg_CLKB += CP_IO_E[17] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_Intg_Din += CP_IO_E[18] #### DIG IN BUF PAD ####

Conv_Layer2.n_SR_k_col_CLK += CP_IO_E[19] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_col_RST_B += CP_IO_E[20] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_col_CLKB += CP_IO_E[21] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_col_Din += CP_IO_E[22] #### DIG IN BUF PAD ####

Conv_Layer2.n_SR_k_rw_CLK += CP_IO_E[23] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_rw_RST_B += CP_IO_E[24] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_rw_CLKB += CP_IO_E[25] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_rw_Din += CP_IO_E[26] #### DIG IN BUF PAD ####

Conv_Layer2.n_prog_hv += DigBuffer.Out[0]
Conv_Layer2.n_run_hv += DigBuffer.Out[1]

Conv_Layer2.n_sample_buf_Vb += CP_IO_E[27] #### DIG IN BUF PAD ####

for i in range(36):
    Conv_Layer2.w_Vin_inp_Ch[i] += Conv_Layer1.e_sub_img_out[i]

## ------------ FNN Layer Connections------------##

FNN_layers.n_Act_ly0_scan_Qout += Dig_Scanner_dbg.In[21]
FNN_layers.n_Act_ly1_scan_Qout += Dig_Scanner_dbg.In[22]
FNN_layers.n_FNN_Vsel_dbg += CP_IO_S[11]
FNN_layers.n_WTA_final_scan_Qout += Dig_Scanner_dbg.In[23]

FNN_layers.n_AVDD += CP_AVDD_E
FNN_layers.n_ActF_Vg_bias += CP_IO_S[10]

### Tgates for directing outputs to either ADC or to PAD thru analog buf
FNN_layers.n_Act_ly0_scan_out += Tgts_fr_adc_meas.In[0]
FNN_layers.n_Act_ly0_scan_out += Tgts_fr_adc_meas.In[2]
Tgts_fr_adc_meas.A[0] += M_Sig_RampADC_in[0]
Tgts_fr_adc_meas.A[2] += AnalogBuffer.Vin[6]
AnalogBuffer.Vout[6] +=  CP_IO_E[28]

FNN_layers.n_Act_ly1_scan_out += Tgts_fr_adc_meas.In[1]
FNN_layers.n_Act_ly1_scan_out += Tgts_fr_adc_meas.In[3]
Tgts_fr_adc_meas.A[1] += M_Sig_RampADC_in[1]
Tgts_fr_adc_meas.A[3] += AnalogBuffer.Vin[7]
AnalogBuffer.Vout[7] +=  CP_IO_E[29]

Tgts_fr_adc_meas.Prog += M_mmio_rg_7[0] # Wrong tie it to LV
Tgts_fr_adc_meas.VDD += CP_DVDD_W
Tgts_fr_adc_meas.GND += CP_GND_E_2

FNN_layers.n_DVDD += DVDD_CONV

# for i in range(176):
#     if (i<154):
#         FNN_layers.n_FNN_input[i] += Conv_Layer2.s_sub_img_out[i]
#     else:
#         FNN_layers.n_FNN_input[i] += Conv_Layer2.w_sub_img_out[i-154]

for i in range(154,176,1):
    FNN_layers.n_FNN_input[i] += Conv_Layer2.w_sub_img_out[(i-154)]

FNN_layers.n_FNN_ly0_out_95 += AnalogBuffer.Vin[8] # Used this buffer multiple times
FNN_layers.n_GND += CP_GND_E_2 # Make sure this is closest 

Prog_Drln += FNN_layers.n_Prog_Drainline
Run_Drln += FNN_layers.n_Run_Drainline
FNN_layers.n_VGPROG += M_VGPROG
FNN_layers.n_VGRUN += M_VGRUN
FNN_layers.n_VINJ += CP_VINJ_E
VTUN_chip += FNN_layers.n_VTUN

FNN_layers.n_WTA_final_Vbias += CP_IO_S[9]
#Im not going to measure the Vmid of WTA

### Tgates for directing outputs to either ADC or to PAD thru analog buf
FNN_layers.n_WTA_final_scan_out += Tgts_fr_adc_meas1.In[0]
FNN_layers.n_WTA_final_scan_out += Tgts_fr_adc_meas1.In[2]
Tgts_fr_adc_meas1.A[0] += M_Sig_RampADC_in[2]
Tgts_fr_adc_meas1.A[2] += AnalogBuffer.Vin[8]
AnalogBuffer.Vout[8] +=  CP_IO_S[8]

TEST_INP += Tgts_fr_adc_meas1.In[1]
TEST_INP += Tgts_fr_adc_meas1.In[3]
Tgts_fr_adc_meas1.A[1] += M_Sig_RampADC_in[3]
Tgts_fr_adc_meas1.A[3] += AnalogBuffer.Vin[9]
AnalogBuffer.Vout[9] +=  CP_IO_S[7]

Tgts_fr_adc_meas1.Prog += M_mmio_rg_7[1]
Tgts_fr_adc_meas1.VDD += CP_DVDD_E
Tgts_fr_adc_meas1.GND += CP_GND_E_2

FNN_layers.s_FNN_diocon_dbg += AnalogBuffer.Vin[10]
AnalogBuffer.Vout[10] += CP_IO_S[6]
FNN_layers.s_FNN_ly1_out_63 += AnalogBuffer.Vin[11]
AnalogBuffer.Vout[11] += CP_IO_S[5]
FNN_layers.s_VMM_WTA_out_10 += AnalogBuffer.Vin[12]
AnalogBuffer.Vout[12] += CP_IO_S[4]
FNN_layers.s_VMM_WTA_out_11 += AnalogBuffer.Vin[13]
AnalogBuffer.Vout[13] += CP_IO_S[3]

FNN_layers.n_ActF_sel += M_mmio_rg_7[2]
# Add an inverter manually after synthesis for n_ActF_selb
FNN_Scanner_CLK += FNN_layers.n_Act_ly0_scan_CLK
FNN_Scanner_Din += FNN_layers.n_Act_ly0_scan_Din
FNN_layers.n_Act_ly0_scan_RSTB += M_mmio_rg_7[3]
FNN_Scanner_CLK += FNN_layers.n_Act_ly1_scan_CLK
FNN_Scanner_Din += FNN_layers.n_Act_ly1_scan_Din
FNN_layers.n_Act_ly1_scan_RSTB += M_mmio_rg_7[4]

FNN_layers.n_FNN_final_Dr_En += LVLShifter1.OUT[5]
FNN_layers.n_FNN_final_G_En += LVLShifter1.OUT[6]
FNN_layers.n_FNN_ly0_ActF_G_En += LVLShifter1.OUT[7]
FNN_layers.n_FNN_ly0_Dr_En += LVLShifter1.OUT[8]
FNN_layers.n_FNN_ly0_G_En += LVLShifter1.OUT[9]
FNN_layers.n_FNN_ly1_ActF_G_En += LVLShifter1.OUT[10]
FNN_layers.n_FNN_ly1_Dr_En += LVLShifter1.OUT[11]
FNN_layers.n_FNN_ly1_G_En += LVLShifter1.OUT[12]

for _ in range(8):
    Dr_bits[_] += FNN_layers.n_FNN_shr_Dr_bit[_]
    
for _ in range(8):
    G_bits[_] += FNN_layers.n_FNN_shr_G_bit[_]
    
FNN_Scanner_CLK += FNN_layers.n_WTA_final_scan_CLK
FNN_Scanner_Din += FNN_layers.n_WTA_final_scan_Din
FNN_layers.n_WTA_final_scan_RSTB +=M_mmio_rg_7[5]

FNN_layers.n_prog_hv += DigBuffer.Out[0]
FNN_layers.n_run_hv += DigBuffer.Out[1]

## ------------ Final Connections for Global Wires ------------##

TEST_INP += CP_IO_S[2]

#Need Multiple PADs for splitting the power supply currents
DVDD_CONV += CP_IO_S[1]

VTUN_chip += CP_IO_W_RES_0

for _ in range(8):
    G_bits[_] += LVLShifter2.OUT[_]

for _ in range(10):
    if _ < 8:
        Dr_bits[_] += LVLShifter2.OUT[8+_]
    else:
        Dr_bits[_] += LVLShifter1.OUT[13+(_ - 8)]

Global_rst_b += CP_IO_S[0]

Prog_Drln += M_Sys_Drln[0]
Run_Drln += M_Sys_Drln[1]

FNN_Scanner_Din += M_mmio_rg_7[6]
FNN_Scanner_CLK +=M_mmio_rg_7[7]



# Compilation
#-------------------------------------------------------------------------------
design_limits = [7e6, 5e6]
location_islands = ((320*1e3,1650*1e3),#ConvLy1
                    (3158.6*1e3,1632.23*1e3),#ConvLy2
                    (230*1e3,20*1e3), #FNN
                    (2800*1e3,3600*1e3), #LVLShifter1
                    (3600*1e3,3600*1e3), #LVLShifter2
                    (5500*1e3,3900*1e3), #DigBuffer
                    (4350*1e3,3400*1e3), #DigScanner, Tgates					
                    (4850*1e3,3500*1e3)) #Analog Buffer

with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

# qparams["passes"] = 100
# qparams["via"] = 50
# qparams["jog"] = 30
# qparams["conflict"] = 10
# qparams["stage2"] = "mask none force effort 100"
# qparams["stage3"] = "mask none force effort 100"

qparams["via"] = 50
qparams["jog"] = 30
#qparams["conflict"] = 10

# # GIVE STAGE 1 A LARGER MASK
# qparams["stage1"] = "mask 40" # Use a mask value of 4 for stage1 (default for 'auto' in stage2)

# # Stage 2 for remaining failed nets with bbox and controlled rip-up
# qparams["stage2"] = "mask none force effort 30 limit 100"

# # Stage 3 as the most aggressive fallback
# qparams["stage3"] = "mask none force effort 50"

# GIVE STAGE 1 A LARGER MASK
qparams["stage1"] = "mask none force" # Use a mask value of 4 for stage1 (default for 'auto' in stage2)

# Stage 2 for remaining failed nets with bbox and controlled rip-up
qparams["stage2"] = "mask none limit 100 force"

# Stage 3 as the most aggressive fallback
qparams["stage3"] = "mask none force"

compile_asic(Top,process="TSMC350nm",fileName="Top_Conv",p_and_r = True,route=True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=7,drainSpace=20,gateSpaceIdx=7,gateSpace=15, qparams=qparams)