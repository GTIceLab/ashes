import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
from ashes_fg.class_lib_LLM import *
import json as json
Top = Circuit()

MacroIsland = Island(Top)
macro = Macro_abs(Top,MacroIsland,[1,1])
macro.place([0,0])

# TODO Fix the instances pin names:[0] to <0> or add another parsing method

# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
chipframe = ChipFrame(Top,FrameIsland,[1,1])
chipframe.place([0,0])
chipframe.markChipFrame()

# Macro <--> Frame Connections
# --------------------------------------------------------------------------------
# ___ IO Pins ___
# North IO Pins
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

# East IO Pins
# bottom right macro pins to east frame pins
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
macro.irq[0] += chipframe.gnd_N[2]#####################could change
macro.irq[1] += chipframe.gnd_N[2]#######################could change
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

#ALICE Left
DiscTimeSaliencyIsland = Island(Top)
DiscTimeSaliency = DiscTimeSaliency(Top,DiscTimeSaliencyIsland,[1,1])
DiscTimeSaliency.place([0,0])

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

#PROG/Run buffer

DigBufferIsland = Island(Top)
DigBuffer = TSMC350nm_DigBuffer_x2(Top,DigBufferIsland,[1,1])
DigBuffer.place([0,0])

DigBuffer.GND += chipframe.gnd_W[2]
DigBuffer.VINJ += chipframe.VINJ_W
DigBuffer.In[0] += macro.PROG_HV
DigBuffer.In[1] += macro.RUN_HV

#Analog buffer

AnalogBufferIsland = Island(Top)
AnalogBuffer = AnalogBuffer(Top,AnalogBufferIsland,[4,1])
AnalogBuffer.place([0,0])

DrainDecoder_buf = STD_DrainDecoder(Top,AnalogBufferIsland,bits=2)
DrainSelect_buf = RunDrainSwitch(Top,AnalogBufferIsland,num=1)
DrainSwitch_buf = DrainCutoff(Top,AnalogBufferIsland,num=1)    

GateSwitch_buf = STD_IndirectGateSwitch(Top,AnalogBufferIsland,1)

AnalogBuffer.VTUN += GateSwitch_buf.VTUN
AnalogBuffer.VDD += GateSwitch_buf.VDD[0]
GateSwitch_buf.VPWR[0] += chipframe.avdd_E
GateSwitch_buf.VPWR[1] += chipframe.avdd_E
AnalogBuffer.GND += GateSwitch_buf.GND[0]
AnalogBuffer.VINJ += GateSwitch_buf.VINJ
AnalogBuffer.Vg += GateSwitch_buf.Vg[0]
AnalogBuffer.Vsel += GateSwitch_buf.CTRL_B[0]
AnalogBuffer.Vd_P += DrainSwitch_buf.PR

GateSwitch_buf.VTUN_T += chipframe.IO_W_RES[0]
GateSwitch_buf.Vgsel += macro.VGPROG
GateSwitch_buf.PROG += DigBuffer.Out[0]
GateSwitch_buf.RUN += DigBuffer.Out[1]
GateSwitch_buf.VINJ_T += chipframe.VINJ_E
GateSwitch_buf.GND_T += chipframe.gnd_E[2]
GateSwitch_buf.RUN_IN[0] += macro.VGRUN
GateSwitch_buf.RUN_IN[1] += macro.VGRUN
GateSwitch_buf.decode[0] += LVLShifter2.OUT[15]

DrainSwitch_buf.VDD += chipframe.VINJ_E
DrainSwitch_buf.GND += chipframe.gnd_E[2]
DrainSwitch_buf.RUN += DigBuffer.Out[1]

DrainSelect_buf.VINJ += chipframe.VINJ_E
DrainSelect_buf.GND += chipframe.gnd_E[2]
DrainSelect_buf.prog_drainrail += macro.SystemDrainline[0]
DrainSelect_buf.run_drainrail += macro.SystemDrainline[1]

#DrainDecoder_buf.VINJ += chipframe.VINJ_N[2]
#DrainDecoder_buf.GND += chipframe.gnd_N[8]
DrainDecoder_buf.ENABLE += LVLShifter2.OUT[14]
DrainDecoder_buf.IN += LVLShifter2.OUT[12:14]

#System connections
AnalogBuffer.Vin[0] += DiscTimeSaliency.n_SoftWTA_Scanner_Out
AnalogBuffer.Vin[1] += DiscTimeSaliency.w_Q_Scanner_Out
AnalogBuffer.Vin[2] += DiscTimeSaliency.e_K_Scanner_Out
AnalogBuffer.Vin[3] += DiscTimeSaliency.n_Input_SoftWTA_Vmid
AnalogBuffer.Vout[0] += chipframe.IO_E[13]
AnalogBuffer.Vout[1] += chipframe.IO_E[14]
AnalogBuffer.Vout[2] += chipframe.IO_E[15]
AnalogBuffer.Vout[3] += chipframe.IO_E[16]

DiscTimeSaliency.n_Prog += DigBuffer.Out[0]
DiscTimeSaliency.n_RUN += DigBuffer.Out[1]
DiscTimeSaliency.n_VGPROG += macro.VGPROG
DiscTimeSaliency.n_Input_SoftWTA_Vg += macro.VGRUN

DiscTimeSaliency.n_VTUN += chipframe.IO_W_RES[0]

# Use the closest AVDD in east or west
DiscTimeSaliency.AVDD += chipframe.avdd_E

LVLShifter1.Vin += macro.mmio_reg_9_bout[0:16]
LVLShifter2.Vin += macro.mmio_reg_10_bout[0:16]

DiscTimeSaliency.n_InVMM_Drainline_Prog += macro.SystemDrainline[0]
DiscTimeSaliency.w_Q_Drainline_Prog += macro.SystemDrainline[0]
DiscTimeSaliency.e_K_Drainline_Prog += macro.SystemDrainline[0]

DiscTimeSaliency.n_InVMM_Drainline_Run += macro.SystemDrainline[1]
DiscTimeSaliency.w_Q_Drainline_Run += macro.SystemDrainline[1]
DiscTimeSaliency.e_K_Drainline_Run += macro.SystemDrainline[1]

DiscTimeSaliency.n_INPUT_D_ENABLE += LVLShifter2.OUT[0]
DiscTimeSaliency.n_INPUT_G_ENABLE += LVLShifter2.OUT[1]
DiscTimeSaliency.w_Q_D_enable += LVLShifter2.OUT[2]
DiscTimeSaliency.w_Q_G_enable += LVLShifter2.OUT[3]
DiscTimeSaliency.e_K_D_enable += LVLShifter2.OUT[4]
DiscTimeSaliency.e_K_G_enable += LVLShifter2.OUT[5]

DiscTimeSaliency.n_INPUT_DRAINBIT += LVLShifter1.OUT[0:7]
DiscTimeSaliency.w_Q_DRAINBIT += LVLShifter1.OUT[0:9]
DiscTimeSaliency.e_K_DRAINBIT += LVLShifter1.OUT[0:9]

DiscTimeSaliency.n_INPUT_GATEBIT += LVLShifter1.OUT[9:15]
DiscTimeSaliency.w_Q_GATEBIT += LVLShifter1.OUT[9:16]
DiscTimeSaliency.e_K_GATEBIT += LVLShifter1.OUT[9:16]

DiscTimeSaliency.n_SoftWTA_Scanner_Din += chipframe.IO_E[17]
DiscTimeSaliency.e_SoftWTA_Scanner_CLK += chipframe.IO_E[18]
DiscTimeSaliency.e_SoftWTA_Scanner_RSTBar += chipframe.IO_E[19]
DiscTimeSaliency.w_Q_Scanner_Din += chipframe.IO_W[19]
DiscTimeSaliency.w_Q_Scanner_CLK += chipframe.IO_W[20]
DiscTimeSaliency.w_Q_Scanner_RSTBar += chipframe.IO_W[21]
DiscTimeSaliency.e_K_Scanner_Din += chipframe.IO_E[20]
DiscTimeSaliency.e_K_Scanner_CLK += chipframe.IO_E[21]
DiscTimeSaliency.e_K_Scanner_RSTBar += chipframe.IO_E[22]

DiscTimeSaliency.n_Input_SoftWTA_Vbias += chipframe.IO_E[23]
DiscTimeSaliency.n_PBIAS += chipframe.IO_W[22]
DiscTimeSaliency.n_NBIAS += chipframe.IO_W[23]
DiscTimeSaliency.w_vbias += chipframe.IO_W[24]
DiscTimeSaliency.w_vdbias += chipframe.IO_W[25]
DiscTimeSaliency.w_vgbias += chipframe.IO_W[26]

DiscTimeSaliency.s_dvdd += chipframe.DVDD_S[0]
DiscTimeSaliency.s_CLK += chipframe.IO_S[0]
DiscTimeSaliency.s_Sample += chipframe.IO_S[1]
DiscTimeSaliency.s_Q += chipframe.IO_S[2]
DiscTimeSaliency.s_D += chipframe.IO_S[3]
DiscTimeSaliency.e_SoftWTA_Vs += chipframe.IO_E[24]
DiscTimeSaliency.s_vinj += chipframe.VINJ_S[2]
DiscTimeSaliency.GND += chipframe.gnd_E[2]


DiscTimeSaliency.n_InputVMM0 += chipframe.IO_W[27]
DiscTimeSaliency.n_InputVMM1 += chipframe.IO_W[28]
DiscTimeSaliency.n_InputVMM2 += chipframe.IO_W[29]
DiscTimeSaliency.n_InputVMM3 += chipframe.IO_W[30]
DiscTimeSaliency.n_InputVMM4 += chipframe.IO_W[31]
DiscTimeSaliency.n_InputVMM5 += chipframe.IO_W[32]
DiscTimeSaliency.n_InputVMM6 += chipframe.IO_W[33]
DiscTimeSaliency.n_InputVMM7 += chipframe.IO_W[34]
DiscTimeSaliency.n_InputVMM8 += chipframe.IO_W[35]
DiscTimeSaliency.n_InputVMM9 += chipframe.IO_W[36]
DiscTimeSaliency.n_InputVMM10 += chipframe.IO_W[37]
DiscTimeSaliency.n_InputVMM11 += chipframe.IO_W[38]
DiscTimeSaliency.n_InputVMM12 += chipframe.IO_W[39]
DiscTimeSaliency.n_InputVMM13 += chipframe.IO_W[40]
DiscTimeSaliency.n_InputVMM14 += chipframe.IO_W[41]
DiscTimeSaliency.n_InputVMM15 += chipframe.IO_W[42]
DiscTimeSaliency.n_InputVMM16 += chipframe.IO_S[4]
DiscTimeSaliency.n_InputVMM17 += chipframe.IO_S[5]
DiscTimeSaliency.n_InputVMM18 += chipframe.IO_S[6]
DiscTimeSaliency.n_InputVMM19 += chipframe.IO_S[7]
DiscTimeSaliency.n_InputVMM20 += chipframe.IO_S[8]
DiscTimeSaliency.n_InputVMM21 += chipframe.IO_S[9]
DiscTimeSaliency.n_InputVMM22 += chipframe.IO_S[10]
DiscTimeSaliency.n_InputVMM23 += chipframe.IO_S[11]
DiscTimeSaliency.n_InputVMM24 += chipframe.IO_S[12]
DiscTimeSaliency.n_InputVMM25 += chipframe.IO_S[13]
DiscTimeSaliency.n_InputVMM26 += chipframe.IO_S[14]
DiscTimeSaliency.n_InputVMM27 += chipframe.IO_S[15]
DiscTimeSaliency.n_InputVMM28 += chipframe.IO_S[16]
DiscTimeSaliency.n_InputVMM29 += chipframe.IO_S[17]
DiscTimeSaliency.n_InputVMM30 += chipframe.IO_S[18]
DiscTimeSaliency.n_InputVMM31 += chipframe.IO_S[19]
DiscTimeSaliency.n_InputVMM32 += chipframe.IO_S[20]
DiscTimeSaliency.n_InputVMM33 += chipframe.IO_S[21]
DiscTimeSaliency.n_InputVMM34 += chipframe.IO_S[22]
DiscTimeSaliency.n_InputVMM35 += chipframe.IO_S[23]
DiscTimeSaliency.n_InputVMM36 += chipframe.IO_S[24]
DiscTimeSaliency.n_InputVMM37 += chipframe.IO_S[25]
DiscTimeSaliency.n_InputVMM38 += chipframe.IO_S[26]
DiscTimeSaliency.n_InputVMM39 += chipframe.IO_S[27]




#Padframe buffer connections
for i in range(6):
	chipframe.buf_vdd_N[i] += chipframe.DVDD_N[2]
for i in range(11):
	chipframe.buf_vdd_W[i] += chipframe.DVDD_W
chipframe.buf_vdd_E += chipframe.DVDD_E

# Compilation
#-------------------------------------------------------------------------------
design_limits = [12e6, 12e6]
location_islands = ((250600, 4520000), #macro
                    (20600, 20000), #frame
                    (660000,400000), #Fabric
                    (3300000,4540000), #LVLShifter1
                    (4100000,4540000), #LVLShifter2
                    (1500000,4540000), #DigBuffer
                    (4700000,4450000)) #Analog Buffer
with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)
qparams["via"] = 20
qparams["jog"] = 40
compile_asic(Top,process="TSMC350nm",fileName="ConvChip_To_Frame",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=8,drainSpace=20,gateSpaceIdx=6,gateSpace=15)