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

DelayLineIsland = Island(Top)

DrainDecoder = True
V_NW=None

decoderPlace = True

# VMMDemod Sizing
dim = [280,400]

# VMMWTA Sizing
dim2 = [256,280]

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

if DrainDecoder==True:
    drainBits_Del = int(np.ceil(np.log2(rows*4)))
    print(drainBits_Del)
    DrainDecoder_Del = STD_DrainDecoder(Top,DelayLineIsland,bits=drainBits_Del)
    DrainSelect_Del = RunDrainSwitch(Top,DelayLineIsland,num=rows)
    DrainSwitch_Del = DrainCutoff(Top,DelayLineIsland,num=rows)

Scanner_Island = Island(Top)
Scanner = [0]*3
for i in range(3):
    Scanner[i] = "Scanner_"+str(i)
for i in range(3):
    Scanner[i] = TSMC350nm_VerticalScanner(Top, Scanner_Island)
    Scanner[i].place([i,0])

numRows = int(dim[0]/4)
numCols = int(dim[1]/2)

VMMIsland = Island(Top)

# Create VMM and place in an island

VMM = TSMC350nm_4x2_Indirect(Top,dim=(numRows,numCols),island=VMMIsland)
VMM.place([0,0])
#VMM.markAbut()

Tgate_4 = ST_BMatrix(Top,dim=(numRows,1),island=VMMIsland)
Tgate_4.place([0,numCols+1])

if decoderPlace == True:

    gateBits = int(np.ceil(np.log2(dim[1])))
    GateDecoder = STD_IndirectGateDecoder(Top,VMMIsland,gateBits)
    GateSwitches = STD_IndirectGateSwitch(Top,VMMIsland,numCols)

    drainBits = int(np.ceil(np.log2(dim[0])))
    DrainDecoder = STD_DrainDecoder(Top,VMMIsland,drainBits)
    DrainSel = RunDrainSwitch(Top,VMMIsland,num=numRows)
    DrainSwitches = DrainCutoff(Top,VMMIsland,num=numRows)

Mod = Island(Top)

Modualtion = TSMC350nm_Modulation(Top,dim=(numRows,1),island=Mod)
Modualtion.place([0,numCols+3]) 

# VMMWTA
if (dim2[0] % 4) != 0:
    raise Exception("Error: VMM rows must be divisible by 4")
if (dim2[1] % 2) != 0:
    raise Exception("Error: VMM columns must be divisible by 2")

numRows2 = int(dim2[0]/4)
numCols2 = int(dim2[1]/2)

loc = [0,0]

VMMWTAIsland = Island(Top)

VMM2 = TSMC350nm_4x2_Indirect(Top,dim=(numRows2,numCols2),island=VMMWTAIsland)
VMM2.place([0,0])

WTA = TSMC350nm_4WTA_IndirectProg_noncab(Top,island=VMMWTAIsland,dim=[numRows2,1])
WTA.place([0,numCols+1])
        
if decoderPlace == True:
    # Add decoders
    gateBits_WTA = int(np.ceil(np.log2(dim2[1])))
    GateDecoder_WTA= STD_IndirectGateDecoder(Top,VMMWTAIsland,gateBits_WTA)
    GateSwitches_WTA = STD_IndirectGateSwitch(Top,VMMWTAIsland,numCols2)

    drainBits_WTA = int(np.ceil(np.log2(dim2[0])))
    DrainDecoder_WTA = STD_DrainDecoder(Top,VMMWTAIsland,drainBits_WTA)
    DrainSel_WTA = RunDrainSwitch(Top,VMMWTAIsland,numRows2)
    DrainSwitches_WTA = DrainCutoff(Top,VMMWTAIsland,numRows2)

#Connections

Scanner_Island = Island(Top)
Scanner = [0]*numRows2
for i in range(numRows2):
    Scanner[i] = "Scanner_"+str(i)
for i in range(numRows2):
    Scanner[i] = TSMC350nm_VerticalScanner(Top, Scanner_Island)
    Scanner[i].place([i,0])

# Frame
# -------------------------------------------------------------------------------
FrameIsland = Island(Top)
chipframe = ChipFrame(Top,FrameIsland,[1,1])
chipframe.place([0,0])
chipframe.markChipFrame()

# Macro <--> Frame Connections
# --------------------------------------------------------------------------------
# ___ IO Pins ___

'''macro.peri_spi_slave_RX_DV += chipframe.IO_N[0]
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

# west pins
macro.peri_spi_mstr_TX_Ready += chipframe.IO_W[0]
macro.peri_spi_mstr_cs_n_3 += chipframe.IO_W[1]
macro.peri_spi_mstr_cs_n_2 += chipframe.IO_W[2]
macro.peri_spi_mstr_cs_n_1 += chipframe.IO_W[3]
macro.peri_spi_mstr_cs_n_0 += chipframe.IO_W[4]
macro.peri_spi_mstr_mosi += chipframe.IO_W[5]
macro.peri_spi_mstr_miso += chipframe.IO_W[6]
macro.peri_spi_slave_cs_n += chipframe.IO_W[7]
macro.peri_spi_slave_mosi += chipframe.IO_W[8]

macro.peri_spi_slave_miso += chipframe.IO_W[9]
macro.peri_spi_rst += chipframe.IO_W[10]
macro.peri_use_uP += chipframe.IO_W[11]
macro.sram_CS_VBIAS += chipframe.IO_W[12]
macro.irq[13] += chipframe.IO_W[13]
macro.irq[12] += chipframe.IO_W[14]
macro.irq[11] += chipframe.IO_W[15]
macro.irq[10] += chipframe.IO_W[16]
macro.irq_acc[13] += chipframe.IO_W[17]
macro.irq_acc[12] += chipframe.IO_W[18]

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

# ___ clk lines ___
macro.peri_spi_cpu_clk += chipframe.IO_N_CLK[0]
macro.peri_spi_slave_clk += chipframe.IO_N_CLK[1]
macro.peri_spi_mstr_spiclk += chipframe.IO_N_CLK[2]
macro.fast_ADC_clk += chipframe.IO_N_CLK[3]

# ___ Macro power/gnd pins ___
macro.GND += chipframe.gnd_N[8]
macro.AVDD_AM += chipframe.avdd_N[2]
macro.VINJ += chipframe.VINJ_N[2]
macro.DVDD += chipframe.DVDD_N[2]'''

# Compilation
#-------------------------------------------------------------------------------
design_limits = [7e6, 6.21e6]

offset = 420000
mult = 1.2
location_islands = ((350600, 4500000), (400000,offset+100000),(790000,(22000*40)+90000+100000+offset), (400000, offset),(500000,2300000),(6200000,2300000), (2200000,offset),(6300000,offset),(20600, 20000))
# location_islands = ((250600, 4600000), (20600, 20000), (300000, 250600))
# location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="Macro_Frame",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
