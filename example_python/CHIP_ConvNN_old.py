import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
import json as json


Top = Circuit()

MacroIsland = Island(Top)
macro = Macro_abs(Top,MacroIsland,[1,1])
macro.place([0,0])


# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
chipframe = ChipFrame(Top,FrameIsland,[1,1])
chipframe.place([0,0])
chipframe.markChipFrame()

# Macro <--> Frame Connections
# --------------------------------------------------------------------------------
# ___ IO Pins ___
#North IO Pins
macro.dco_enable_bout += chipframe.IO_N[0]
macro.dco_wkup_bout += chipframe.IO_N[1]
macro.lfxt_enable_bout += chipframe.IO_N[2]
macro.lfxt_wkup_bout += chipframe.IO_N[3]
macro.scan_out2_bout += chipframe.IO_N[4]
macro.scan_out1_bout += chipframe.IO_N[5]
macro.fgmem_CS_VBIAS += chipframe.IO_N[6]
macro.mmio_reg_in_5[1] += chipframe.IO_N[7] 
macro.mmio_reg_in_5[0] += chipframe.IO_N[8]

macro.cpu_en += chipframe.IO_N[9]
macro.dbg_en += chipframe.IO_N[10]
macro.dbg_uart_rxd += chipframe.IO_N[11]
macro.nmi += chipframe.IO_N[12]
macro.reset_n += chipframe.IO_N[13]
macro.scan_enable += chipframe.IO_N[14]
macro.dbg_uart_txd += chipframe.IO_N[15]
macro.scan_mode += chipframe.IO_N[16]
macro.wkup += chipframe.IO_N[17]
macro.scan_in1 += chipframe.IO_N[18]
macro.scan_in2 += chipframe.IO_N[19] 

# West IO pins
macro.dbg_freeze_bout += chipframe.IO_W[0]
macro.Macro_dbg_Scan_RST += chipframe.IO_W[1]
macro.Macro_dbg_Scan_Din += chipframe.IO_W[2]
macro.Macro_dbg_Scan_CLK += chipframe.IO_W[3]
macro.Macro_dbg_Scan_Vout += chipframe.IO_W[4]
macro.mmio_reg_7_bout[1] += chipframe.IO_W[5] 
macro.mmio_reg_7_bout[0] += chipframe.IO_W[6] 

macro.peri_spi_mstr_cs_n_3 += chipframe.IO_W[7]
macro.peri_spi_mstr_cs_n_2 += chipframe.IO_W[8]
macro.peri_spi_mstr_cs_n_1 += chipframe.IO_W[9]
macro.peri_spi_mstr_cs_n_0 += chipframe.IO_W[10]
macro.peri_spi_mstr_mosi += chipframe.IO_W[11]
macro.peri_spi_slave_miso += chipframe.IO_W[12]
macro.peri_spi_slave_cs_n += chipframe.IO_W[13]
macro.peri_spi_slave_mosi += chipframe.IO_W[14]
macro.peri_spi_mstr_miso += chipframe.IO_W[15]
macro.peri_spi_slave_clk += chipframe.IO_W[16]
macro.peri_use_uP += chipframe.IO_W[17]
macro.sram_CS_VBIAS += chipframe.IO_W[18]

#East IO Pins
#bottom right macro pins to east frame pins
macro.Cal_IO += chipframe.IO_E[0]
macro.Cal_Vin += chipframe.IO_E[1]
macro.Debug_IO += chipframe.IO_E[2]
macro.I_IO += chipframe.IO_E[3]
macro.VD_IO += chipframe.IO_E[4]
macro.VGPROG_IO += chipframe.IO_E[5]
macro.VG_IO += chipframe.IO_E[6]
macro.V_IO += chipframe.IO_E[7]
macro.pulse_fr_drain += chipframe.IO_E[8]

macro.puc_rst_bout += chipframe.IO_E[9]
macro.irq[0] += chipframe.gnd_N[2]
macro.irq[1] += chipframe.gnd_N[2]
macro.irq[2] += chipframe.IO_E[10]
macro.irq[3] += chipframe.IO_E[11]
macro.irq[4] += chipframe.IO_E[12]

# East special pads
macro.ADC_Trim += chipframe.IO_Bare_E[0]
macro.Bias_Trim += chipframe.IO_Bare_E[1]
macro.VTUN_AM += chipframe.IO_E_RES[0]
macro.VTUN_fgmem += chipframe.IO_E_RES[1]

# ___ clk lines ___
macro.peri_spi_mstr_spiclk += chipframe.IO_N_CLK[0] # TODO could change
macro.lfxt_clk += chipframe.IO_N_CLK[1]
macro.fast_clk += chipframe.IO_N_CLK[2]
macro.dco_clk += chipframe.IO_N_CLK[3]

# ___ Macro power/gnd pins ___
macro.GND += chipframe.gnd_N[8]
macro.AVDD += chipframe.avdd_N[2]
macro.VINJ += chipframe.VINJ_N[2]
macro.DVDD += chipframe.DVDD_N[2]

#System islands

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

LVLShifter1.DVDD += chipframe.DVDD_W
LVLShifter1.GND += chipframe.gnd_W[2]
LVLShifter1.VINJ += chipframe.VINJ_W

LVLShifter2Island = Island(Top)
LVLShifter2 = TSMC350nm_LVLShift_x16(Top,LVLShifter2Island,[1,1])
LVLShifter2.place([0,0])

LVLShifter2.DVDD += chipframe.DVDD_W
LVLShifter2.GND += chipframe.gnd_W[2]
LVLShifter2.VINJ += chipframe.VINJ_W

LVLShifter1.Vin += macro.mmio_reg_9_bout[0:16]
LVLShifter2.Vin += macro.mmio_reg_10_bout[0:16]

#PROG/Run buffer

DigBufferIsland = Island(Top)
DigBuffer = TSMC350nm_DigBuffer_x2(Top,DigBufferIsland,[1,1])
DigBuffer.place([0,0])

DigBuffer.GND += chipframe.gnd_W[2]
DigBuffer.VINJ += chipframe.VINJ_W
DigBuffer.In[0] += macro.PROG_HV
DigBuffer.In[1] += macro.RUN_HV

#Dig Scanner for debug Island
Dig_Scanner_dbg_Island = Island(Top)

Dig_Scanner_dbg = TSMC350nm_VerticalScanner(Top,Dig_Scanner_dbg_Island,dim=[10,1])
Dig_Scanner_dbg.place([0,0])

Tgts_fr_adc_meas = ST_BMatrix(Top,Dig_Scanner_dbg_Island,dim=[1,1])
Tgts_fr_adc_meas.place([0,4])

Tgts_fr_adc_meas1 = ST_BMatrix(Top,Dig_Scanner_dbg_Island,dim=[1,1])
Tgts_fr_adc_meas1.place([0,8])


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
GateSwitch_buf.VPWR[0] += chipframe.avdd_E
GateSwitch_buf.VPWR[1] += chipframe.avdd_E
AnalogBuffer.GND += GateSwitch_buf.GND[0]
AnalogBuffer.VINJ += GateSwitch_buf.VINJ
AnalogBuffer.Vg += GateSwitch_buf.Vg[0]
AnalogBuffer.Vsel += GateSwitch_buf.CTRL_B[0]
AnalogBuffer.Vd_P += DrainSwitch_buf.PR[0:14]

GateSwitch_buf.VTUN_T += chipframe.IO_W_RES[0]
GateSwitch_buf.Vgsel += macro.VGPROG
GateSwitch_buf.PROG += DigBuffer.Out[0]
GateSwitch_buf.RUN += DigBuffer.Out[1]
GateSwitch_buf.VINJ_T += chipframe.VINJ_E
GateSwitch_buf.GND_T += chipframe.gnd_E[2]
GateSwitch_buf.RUN_IN[0] += macro.VGRUN
GateSwitch_buf.RUN_IN[1] += macro.VGRUN
GateSwitch_buf.decode[0] += macro.mmio_reg_5_vinj[0]############################ gate decoder control for analog buffer####################

DrainSwitch_buf.VDD += chipframe.VINJ_E
DrainSwitch_buf.GND += chipframe.gnd_E[2]
DrainSwitch_buf.RUN += DigBuffer.Out[1]

DrainSelect_buf.VINJ += chipframe.VINJ_E
DrainSelect_buf.GND += chipframe.gnd_E[2]
DrainSelect_buf.prog_drainrail += macro.SystemDrainline[0]
DrainSelect_buf.run_drainrail += macro.SystemDrainline[1]

#DrainDecoder_buf.VINJ += chipframe.VINJ_N[2]
#DrainDecoder_buf.GND += chipframe.gnd_N[8]
DrainDecoder_buf.ENABLE += macro.mmio_reg_5_vinj[1]############################ drain decoder enable for analog buffer########################
DrainDecoder_buf.IN += macro.mmio_reg_5_vinj[2:6]###########################drain decoder bits for analog buffer#########################

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
AnalogBuffer.Vout[0] += chipframe.IO_E[13]
Conv_Layer1.e_sub_img_out[37] += AnalogBuffer.Vin[1]
AnalogBuffer.Vout[1] += chipframe.IO_E[14]

Conv_Layer1.n_AVDD +=chipframe.avdd_W
Conv_Layer1.n_AVDD_by_2 += chipframe.IO_W[19]
Conv_Layer1.n_DVDD += DVDD_CONV
Conv_Layer1.n_GND += chipframe.gnd_W[2] # Make sure this is closest 

Conv_Layer1.n_VGPROG += macro.VGPROG
Conv_Layer1.n_VINJ += chipframe.VINJ_W # Make sure this is closest 
VTUN_chip += Conv_Layer1.n_VTUN # Make sure this is closest 

Conv_Layer1.n_Vint_dbg[0] += AnalogBuffer.Vin[2]
AnalogBuffer.Vout[2] += chipframe.IO_E[15]
Conv_Layer1.n_Vint_dbg[1] += AnalogBuffer.Vin[3]
AnalogBuffer.Vout[3] += chipframe.IO_E[16]

Conv_Layer1.n_AP_G_En += LVLShifter1.OUT[0]

for _ in range(3):
    G_bits[_] += Conv_Layer1.n_AP_G_bit[_]
    
Conv_Layer1.n_AP_Relu_Vb += chipframe.IO_W[20]
Global_rst_b += Conv_Layer1.n_Global_rst_b
Conv_Layer1.n_Kvmm_AP_Dr_En += LVLShifter1.OUT[1]

for _ in range(10):
    Dr_bits[_] += Conv_Layer1.n_Kvmm_AP_Dr_bit[_]

Prog_Drln += Conv_Layer1.n_Kvmm_AP_Prog_Drln
Run_Drln += Conv_Layer1.n_Kvmm_AP_Run_Drln

Conv_Layer1.n_Kvmm_G_En += LVLShifter1.OUT[2]

for _ in range(4):
    G_bits[_] += Conv_Layer1.n_Kvmm_G_bit[_]
    
Conv_Layer1.n_SR_Intg_CLK += chipframe.IO_W[21] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_Intg_RST_B += chipframe.IO_W[22] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_Intg_CLKB += chipframe.IO_W[23] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_Intg_Din += chipframe.IO_W[24] #### DIG IN BUF PAD ####

Conv_Layer1.n_SR_k_col_CLK += chipframe.IO_W[25] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_col_RST_B += chipframe.IO_W[26] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_col_CLKB += chipframe.IO_W[27] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_col_Din += chipframe.IO_W[28] #### DIG IN BUF PAD ####

Conv_Layer1.n_SR_k_rw_CLK += chipframe.IO_W[29] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_rw_RST_B += chipframe.IO_W[30] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_rw_CLKB += chipframe.IO_W[31] #### DIG IN BUF PAD ####
Conv_Layer1.n_SR_k_rw_Din += chipframe.IO_W[32] #### DIG IN BUF PAD ####

Conv_Layer1.n_Vin_inp_Ch[0] += chipframe.IO_W[33] #### DIG IN BUF PAD ####
Conv_Layer1.n_Vin_inp_Ch[1] += chipframe.IO_W[34] #### DIG IN BUF PAD ####
Conv_Layer1.n_Vin_inp_Ch[2] += chipframe.IO_W[35] #### DIG IN BUF PAD ####

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

Conv_Layer2.n_AVDD +=chipframe.avdd_E
Conv_Layer2.n_AVDD_by_2 += chipframe.IO_W[19]
Conv_Layer2.n_DVDD += DVDD_CONV
Conv_Layer2.n_GND += chipframe.gnd_E[2] # Make sure this is closest 

Conv_Layer2.n_VGPROG += macro.VGPROG
Conv_Layer2.n_VINJ += chipframe.VINJ_E # Make sure this is closest 
VTUN_chip += Conv_Layer2.n_VTUN # Make sure this is closest 

Conv_Layer2.n_Vint_dbg[0] += AnalogBuffer.Vin[4]
AnalogBuffer.Vout[4] += chipframe.IO_E[17]
Conv_Layer2.n_Vint_dbg[1] += AnalogBuffer.Vin[5]
AnalogBuffer.Vout[5] += chipframe.IO_E[18]


# Connect the s_sub_img_out[0:153], w_sub_img_out[0:21] in FNN Connections 
for _ in range(8):
    Conv_Layer2.w_sub_img_out[22+_] += chipframe.IO_E[19+_]

Global_rst_b += Conv_Layer2.n_Global_rst_b
Conv_Layer2.n_Kvmm_Dr_En += LVLShifter1.OUT[3]

for _ in range(8):
    Dr_bits[_] += Conv_Layer2.n_Kvmm_Dr_bit[_]
    
Conv_Layer2.n_Kvmm_G_En += LVLShifter1.OUT[4]

for _ in range(7):
    G_bits[_] += Conv_Layer2.n_Kvmm_G_bit[_]

Prog_Drln += Conv_Layer2.n_Kvmm_Prog_Drln
Run_Drln += Conv_Layer2.n_Kvmm_Run_Drln

Conv_Layer2.n_Relu_Vb += chipframe.IO_E[27]


Conv_Layer2.n_SR_Intg_CLK += chipframe.IO_E[28] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_Intg_RST_B += chipframe.IO_E[29] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_Intg_CLKB += chipframe.IO_E[30] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_Intg_Din += chipframe.IO_E[31] #### DIG IN BUF PAD ####

Conv_Layer2.n_SR_k_col_CLK += chipframe.IO_E[32] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_col_RST_B += chipframe.IO_E[33] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_col_CLKB += chipframe.IO_E[34] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_col_Din += chipframe.IO_E[35] #### DIG IN BUF PAD ####

Conv_Layer2.n_SR_k_rw_CLK += chipframe.IO_E[36] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_rw_RST_B += chipframe.IO_E[37] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_rw_CLKB += chipframe.IO_E[38] #### DIG IN BUF PAD ####
Conv_Layer2.n_SR_k_rw_Din += chipframe.IO_E[39] #### DIG IN BUF PAD ####

Conv_Layer2.n_prog_hv += DigBuffer.Out[0]
Conv_Layer2.n_run_hv += DigBuffer.Out[1]

Conv_Layer2.n_sample_buf_Vb += chipframe.IO_E[40] #### DIG IN BUF PAD ####

for i in range(36):
    Conv_Layer2.w_Vin_inp_Ch[i] += Conv_Layer1.e_sub_img_out[i]

## ------------ FNN Layer Connections------------##

FNN_layers.n_Act_ly0_scan_Qout += Dig_Scanner_dbg.In[21]
FNN_layers.n_Act_ly1_scan_Qout += Dig_Scanner_dbg.In[22]
FNN_layers.n_FNN_Vsel_dbg += chipframe.IO_S[45]
FNN_layers.n_WTA_final_scan_Qout += Dig_Scanner_dbg.In[23]

FNN_layers.n_AVDD += chipframe.avdd_E
FNN_layers.n_ActF_Vg_bias += chipframe.IO_S[44]

### Tgates for directing outputs to either ADC or to PAD thru analog buf
FNN_layers.n_Act_ly0_scan_out += Tgts_fr_adc_meas.In[0]
FNN_layers.n_Act_ly0_scan_out += Tgts_fr_adc_meas.In[2]
Tgts_fr_adc_meas.A[0] += macro.Signal_RampADC_inp[0]
Tgts_fr_adc_meas.A[2] += AnalogBuffer.Vin[6]
AnalogBuffer.Vout[6] +=  chipframe.IO_E[41]

FNN_layers.n_Act_ly0_scan_out += Tgts_fr_adc_meas.In[1]
FNN_layers.n_Act_ly0_scan_out += Tgts_fr_adc_meas.In[3]
Tgts_fr_adc_meas.A[1] += macro.Signal_RampADC_inp[1]
Tgts_fr_adc_meas.A[3] += AnalogBuffer.Vin[7]
AnalogBuffer.Vout[7] +=  chipframe.IO_E[42]

Tgts_fr_adc_meas.Prog += macro.mmio_reg_7_bout[2]
Tgts_fr_adc_meas.VDD += chipframe.DVDD_E
Tgts_fr_adc_meas.GND += chipframe.gnd_E[2]

FNN_layers.n_DVDD += DVDD_CONV

for i in range(176):
    if (i<154):
        FNN_layers.n_FNN_input[i] += Conv_Layer2.s_sub_img_out[153-i]
    else:
        FNN_layers.n_FNN_input[i] += Conv_Layer2.w_sub_img_out[i-154]

# for i in range(154,176,1):
#     FNN_layers.n_FNN_input[i] += Conv_Layer2.w_sub_img_out[(i-154)]

FNN_layers.n_FNN_ly0_out_95 += AnalogBuffer.Vin[8]
FNN_layers.n_GND += chipframe.gnd_E[1] # Make sure this is closest 

Prog_Drln += FNN_layers.n_Prog_Drainline
Run_Drln += FNN_layers.n_Run_Drainline
FNN_layers.n_VGPROG += macro.VGPROG
FNN_layers.n_VGRUN += macro.VGRUN
FNN_layers.n_VINJ += chipframe.VINJ_E
VTUN_chip += FNN_layers.n_VTUN

FNN_layers.n_WTA_final_Vbias += chipframe.IO_S[43]
#Im not going to measure the Vmid of WTA

### Tgates for directing outputs to either ADC or to PAD thru analog buf
FNN_layers.n_WTA_final_scan_out += Tgts_fr_adc_meas1.In[0]
FNN_layers.n_WTA_final_scan_out += Tgts_fr_adc_meas1.In[2]
Tgts_fr_adc_meas1.A[0] += macro.Signal_RampADC_inp[2]
Tgts_fr_adc_meas1.A[2] += AnalogBuffer.Vin[8]
AnalogBuffer.Vout[8] +=  chipframe.IO_S[42]

TEST_INP += Tgts_fr_adc_meas1.In[1]
TEST_INP += Tgts_fr_adc_meas1.In[3]
Tgts_fr_adc_meas1.A[1] += macro.Signal_RampADC_inp[3]
Tgts_fr_adc_meas1.A[3] += AnalogBuffer.Vin[9]
AnalogBuffer.Vout[9] +=  chipframe.IO_S[41]

Tgts_fr_adc_meas1.Prog += macro.mmio_reg_7_bout[3]
Tgts_fr_adc_meas1.VDD += chipframe.DVDD_E
Tgts_fr_adc_meas1.GND += chipframe.gnd_E[2]

FNN_layers.s_FNN_diocon_dbg += AnalogBuffer.Vin[10]
AnalogBuffer.Vout[10] += chipframe.IO_S[40]
FNN_layers.s_FNN_ly1_out_63 += AnalogBuffer.Vin[11]
AnalogBuffer.Vout[11] += chipframe.IO_S[39]
FNN_layers.s_VMM_WTA_out_10 += AnalogBuffer.Vin[12]
AnalogBuffer.Vout[12] += chipframe.IO_S[38]
FNN_layers.s_VMM_WTA_out_11 += AnalogBuffer.Vin[13]
AnalogBuffer.Vout[13] += chipframe.IO_S[37]

FNN_layers.n_ActF_sel += macro.mmio_reg_7_bout[4]
# Add an inverter manually after synthesis for n_ActF_selb
FNN_Scanner_CLK += FNN_layers.n_Act_ly0_scan_CLK
FNN_Scanner_Din += FNN_layers.n_Act_ly0_scan_Din
FNN_layers.n_Act_ly0_scan_RSTB += macro.mmio_reg_7_bout[5]
FNN_Scanner_CLK += FNN_layers.n_Act_ly1_scan_CLK
FNN_Scanner_Din += FNN_layers.n_Act_ly1_scan_Din
FNN_layers.n_Act_ly1_scan_RSTB += macro.mmio_reg_7_bout[6]

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
FNN_layers.n_WTA_final_scan_RSTB += macro.mmio_reg_7_bout[7]

FNN_layers.n_prog_hv += DigBuffer.Out[0]
FNN_layers.n_run_hv += DigBuffer.Out[1]

## ------------ Final Connections for Global Wires ------------##

TEST_INP += chipframe.IO_S[36]

#Need Multiple PADs for splitting the power supply currents
DVDD_CONV += chipframe.IO_S[35]
DVDD_CONV += chipframe.IO_S[34]
DVDD_CONV += chipframe.IO_S[33]

VTUN_chip += chipframe.IO_W_RES[0]

for _ in range(8):
    G_bits[_] += LVLShifter2.OUT[_]

for _ in range(10):
    if _ < 8:
        Dr_bits[_] += LVLShifter2.OUT[8+_]
    else:
        Dr_bits[_] += LVLShifter1.OUT[13+(_ - 8)]

Global_rst_b += chipframe.IO_S[32]

Prog_Drln += macro.SystemDrainline[0]
Run_Drln += macro.SystemDrainline[1]

FNN_Scanner_Din += macro.mmio_reg_7_bout[8]
FNN_Scanner_CLK += macro.mmio_reg_7_bout[9]


#Padframe buffer connections
for i in range(6):
    chipframe.buf_vdd_N[i] += chipframe.DVDD_N[2]
for i in range(11):
    chipframe.buf_vdd_W[i] += chipframe.DVDD_W
chipframe.buf_vdd_E += chipframe.DVDD_E

# Compilation
#-------------------------------------------------------------------------------
design_limits = [8e6, 8e6]
location_islands = ((250.6*1e3, 4520*1e3), #macro
                    (20.6*1e3, 20*1e3), #frame
                    (3859*1e3,2336*1e3), #ConvLy1
                    (1020*1e3,2550*1e3), #ConvLy2
                    (660*1e3,200*1e3), #FNN
                    (3300*1e3,4440*1e3), #LVLShifter1
                    (4100*1e3,4440*1e3), #LVLShifter2
                    (6000*1e3,4500*1e3), #DigBuffer
                    (6000*1e3,3400*1e3), #DigScanner, Tgates					
                    (6000*1e3,3900*1e3)) #Analog Buffer

with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["passes"] = 80
qparams["via"] = 20
qparams["jog"] = 50
qparams["conflict"] = 50
qparams["stage2"] = "mask none force effort 100  limit 60 break"
qparams["stage3"] = "mask none force effort 100"

# qparams["via"] = 20
# qparams["jog"] = 10
# qparams["conflict"] = 5

# # GIVE STAGE 1 A LARGER MASK
# qparams["stage1"] = "mask 6" # Use a mask value of 4 for stage1 (default for 'auto' in stage2)

# # Stage 2 for remaining failed nets with bbox and controlled rip-up
# qparams["stage2"] = "mask bbox force effort 15 limit 45 break"

# # Stage 3 as the most aggressive fallback
# qparams["stage3"] = "mask none force effort 30"

compile_asic(Top,process="TSMC350nm",fileName="CHIP_CONV",p_and_r = True,route=True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=9,drainSpace=20,gateSpaceIdx=9,gateSpace=15, qparams=qparams)