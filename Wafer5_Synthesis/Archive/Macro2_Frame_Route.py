import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
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

# Compilation
#-------------------------------------------------------------------------------
design_limits = [7e6, 6.21e6]
location_islands = ((250600, 4500000), (20600, 20000))
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="Macro2_Frame",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
