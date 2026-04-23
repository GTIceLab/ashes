import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *
Top = Circuit()

MacroIsland = Island(Top)
macro = Macro(Top,MacroIsland,[1,1])
macro.place([0,0])

# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
chipframe = SmallPadFrame(Top,FrameIsland,[1,1])
chipframe.place([0,0])
chipframe.markChipFrame()

# Macro <--> Frame Connections
# --------------------------------------------------------------------------------
# ___ IO Pins ___
# north
macro.peri_spi_slave_RX_DV += chipframe.IO_N[0]
macro.peri_spi_mstr_RX_DV += chipframe.IO_N[1]

macro.cpu_en += chipframe.IO_N[2]
macro.dbg_en += chipframe.IO_N[3]
macro.dbg_uart_rxd += chipframe.IO_N[4]
macro.dbg_uart_txd += chipframe.IO_N[5]
macro.dco_clk += chipframe.IO_N[6]
macro.lfxt_clk += chipframe.IO_N[7]
macro.nmi += chipframe.IO_N[8]
macro.reset_n += chipframe.IO_N[9]
macro.scan_enable += chipframe.IO_N[10]
macro.scan_mode += chipframe.IO_N[11]
macro.wkup += chipframe.IO_N[12]
macro.scan_in1 += chipframe.IO_N[13]
macro.scan_in2 += chipframe.IO_N[14]
macro.scan_out1 += chipframe.IO_N[15]
macro.scan_out2 += chipframe.IO_N[16]
macro.mclk += chipframe.IO_N[17]
# macro.puc_rst_dbg += chipframe.IO_N[18] # pin doesn't exist in the layout
macro.V_IO += chipframe.IO_N[19]

# bottom right macro pins to east frame pins
macro.VG_IO += chipframe.IO_E[0]
macro.VD_IO += chipframe.IO_E[1]
macro.I_IO += chipframe.IO_E[2]
macro.Debug_IO += chipframe.IO_E[3]
macro.Cal_Vin += chipframe.IO_E[4]
macro.Cal_IO += chipframe.IO_E[5]
macro.fgmem_CS_VBIAS += chipframe.IO_E[6]
macro.VGPROG_IO += chipframe.IO_E[7]
macro.drain_pulse_rst += chipframe.IO_E[8]

macro.ADC_Trim += chipframe.IO_Bare_E[0]
macro.Bias_Trim += chipframe.IO_Bare_E[1]
macro.VTUN_AM += chipframe.IO_E_RES[0]
macro.VTUN_fgmem += chipframe.IO_E_RES[1]

# west lines
macro.peri_spi_mstr_TX_Ready += chipframe.IO_W[0]
macro.peri_spi_mstr_cs_n_3 += chipframe.IO_W[1]
macro.peri_spi_mstr_cs_n_2 += chipframe.IO_W[2]
macro.peri_spi_mstr_cs_n_1 += chipframe.IO_W[3]
macro.peri_spi_mstr_cs_n_0 += chipframe.IO_W[4]
macro.peri_spi_mstr_mosi += chipframe.IO_W[5]
macro.peri_spi_mstr_miso += chipframe.IO_W[6]
macro.peri_spi_slave_cs_n += chipframe.IO_W[7]
macro.peri_spi_slave_mosi += chipframe.IO_W[8]

# south
macro.peri_spi_slave_miso += chipframe.IO_S[0]
macro.peri_spi_rst += chipframe.IO_S[1]
macro.peri_use_uP += chipframe.IO_S[2]
macro.sram_CS_VBIAS += chipframe.IO_S[3]
macro.irq[13] += chipframe.IO_S[4]
macro.irq[12] += chipframe.IO_S[5]
macro.irq[11] += chipframe.IO_S[6]
macro.irq[10] += chipframe.IO_S[7]
macro.irq_acc[13] += chipframe.IO_S[8]
macro.irq_acc[12] += chipframe.IO_S[9]

# ___ clk lines ___
macro.peri_spi_cpu_clk += chipframe.IO_N_CLK[0]
macro.peri_spi_slave_clk += chipframe.IO_N_CLK[1]
macro.peri_spi_mstr_spiclk += chipframe.IO_N_CLK[2]
macro.fast_ADC_clk += chipframe.IO_N_CLK[3]

# ___ Macro power/gnd pins ___
macro.GND += chipframe.gnd_N[8]
macro.AVDD_AM += chipframe.avdd_N[2]
macro.VINJ += chipframe.VINJ_N[2]
macro.DVDD += chipframe.DVDD_N[2]


# Compilation
#-------------------------------------------------------------------------------
design_limits = [7e6, 6.21e6]
location_islands = ((210600, 410000), (20600, 20000))
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="Macro_SmallFrame",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
