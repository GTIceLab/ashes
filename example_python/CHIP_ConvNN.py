import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
import json as json

###################### Note ################
# The indices when assigning buses should +1.
# For example to assign a 2 bit net to a bit pin: example_pin += example_net[0:2]
###################### Note ################

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


# Toplevel ConvNN
# -------------------------------------------------------------------------------
Top_CNN_Island = Island(Top)
Top_CNN = Top_ConvNN(Top,Top_CNN_Island,[1,1])
Top_CNN.place([0,0])


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

###################### Connections between Top_ConvNN ######################

Top_CNN.M_VGPROG += macro.VGPROG
Top_CNN.M_VGRUN += macro.VGRUN
Top_CNN.M_mmio_rg_5_vinj += macro.mmio_reg_in_5[2:8]
Top_CNN.M_Sys_Drln += macro.SystemDrainline[0:2]
Top_CNN.M_Sig_RampADC_in += macro.Signal_RampADC_inp[0:4]
Top_CNN.M_mmio_rg_7 += macro.mmio_reg_7_bout[2:13]
Top_CNN.M_mmio_rg_9 += macro.mmio_reg_9_bout[0:16]
Top_CNN.M_mmio_rg_10 += macro.mmio_reg_10_bout[0:16]
Top_CNN.M_prog_hv += macro.PROG_HV
Top_CNN.M_run_hv += macro.RUN_HV


Top_CNN.CP_DVDD_W += chipframe.DVDD_W
Top_CNN.CP_VINJ_W += chipframe.VINJ_W
Top_CNN.CP_gnd_W_2 += chipframe.gnd_W[2]
Top_CNN.CP_IO_W_RES_0 += chipframe.IO_W_RES_0
Top_CNN.CP_AVDD_W += chipframe.ADD_w
Top_CNN.CP_IO_W += chipframe.IO_W[20:37]

Top_CNN.CP_AVDD_E += chipframe.ADD_E
Top_CNN.CP_VINJ_E += chipframe.VINJ_E
Top_CNN.CP_GND_E_2 += chipframe.gnd_E[2]
Top_CNN.CP_DVDD_E += chipframe.DVDD_E

Top_CNN.CP_IO_S += chipframe.IO_S[33:46]


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
                    (200*1e3,200*1e3)) #Top_CNN

with open('./ashes_fg/asic/qrouter_default.json') as file:
    qparams = json.load(file)

qparams["via"] = 60
qparams["jog"] = 30

# GIVE STAGE 1 A LARGER MASK
qparams["stage1"] = "mask none force" # Use a mask value of 4 for stage1 (default for 'auto' in stage2)

# Stage 2 for remaining failed nets with bbox and controlled rip-up
qparams["stage2"] = "mask none force"

# Stage 3 as the most aggressive fallback
qparams["stage3"] = "mask none force"


compile_asic(Top,process="TSMC350nm",fileName="CHIP_CONV",p_and_r = True,route=True,design_limits = design_limits, location_islands = location_islands, qparams=qparams)