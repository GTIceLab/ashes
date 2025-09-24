import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

rows = 16
delay_columns = 9
VMM_rows = 128

Top = Circuit()

#AFE
AFEIsland = Island(Top)
        
               
C4_instances = [0]*rows
Ampdet_instances = [0]*rows
for i in range(rows):
    C4_instances[i] = "C4_"+str(i)
for i in range(rows):
    Ampdet_instances[i] = "Ampdet_"+str(i)
        
for i in range(rows):
    C4_instances[i] = TSMC350nm_C4(Top,AFEIsland)
    Ampdet_instances[i] = TSMC350nm_Ampdet_NoFG(Top,AFEIsland)
    C4_instances[i].place([i,0])
    Ampdet_instances[i].place([i,1])
    C4_instances[i].OUTPUT += Ampdet_instances[i].VIN
    
      
DelayLine_instances = [0]*delay_columns
for i in range(delay_columns): 
    DelayLine_instances[i] = [0]*rows

for i in range(delay_columns):
    for j in range(rows):
        DelayLine_instances[i][j] = "DelayLine_"+str(i)+"_"+str(j)
        
for i in range(delay_columns):
    for j in range(rows):
        DelayLine_instances[i][j] = DelayLine(Top,AFEIsland)
        DelayLine_instances[i][j].place([j,i+2])
for i in range(delay_columns):
    for j in range(rows):
        if i==delay_columns-1:
                DelayLine_instances[i][j].V_NE += DelayLine_instances[i][j].V_SE
        else:
                DelayLine_instances[i][j].V_NE += DelayLine_instances[i+1][j].V_NW
                DelayLine_instances[i][j].V_SE += DelayLine_instances[i+1][j].V_SW
                
for i in range(rows):
    Ampdet_instances[i].OUTPUT += DelayLine_instances[0][i].V_NW
    
    
drainBits = int(np.ceil(np.log2(rows*4)))
DrainDecoder = STD_DrainDecoder(Top,AFEIsland,bits=drainBits)
DrainSelect = RunDrainSwitch(Top,AFEIsland,num=rows)
DrainSwitch = DrainCutoff(Top,AFEIsland,num=rows)            
                
for i in range(rows):
    DrainSwitch.PR[4*i] += C4_instances[i].VD_P[0]
    DrainSwitch.PR[(4*i)+1] += C4_instances[i].VD_P[1]
    DrainSwitch.PR[(4*i)+2] += Ampdet_instances[i].VD_P[0]
    DrainSwitch.PR[(4*i)+3] += Ampdet_instances[i].VD_P[1]
    C4_instances[i].VD_P[0] += DelayLine_instances[0][i].VD_P[0]
    C4_instances[i].VD_P[1] += DelayLine_instances[0][i].VD_P[1]
    Ampdet_instances[i].VD_P[0] += DelayLine_instances[0][i].VD_P[2]
    Ampdet_instances[i].VD_P[1] += DelayLine_instances[0][i].VD_P[3]
    DrainSwitch.In[4*i] += DelayLine_instances[0][i].VD_R[0]
    DrainSwitch.In[(4*i)+1] += DelayLine_instances[0][i].VD_R[1]
    
for j in range(delay_columns-1):
        for i in range(rows):
            DelayLine_instances[j][i].VD_P[0] += DelayLine_instances[j+1][i].VD_P[0]
            DelayLine_instances[j][i].VD_P[1] += DelayLine_instances[j+1][i].VD_P[1]
            DelayLine_instances[j][i].VD_P[2] += DelayLine_instances[j+1][i].VD_P[2]
            DelayLine_instances[j][i].VD_P[3] += DelayLine_instances[j+1][i].VD_P[3]
            DelayLine_instances[j][i].VD_R[0] += DelayLine_instances[j+1][i].VD_R[0]
            DelayLine_instances[j][i].VD_R[1] += DelayLine_instances[j+1][i].VD_R[1]
            
     
FakeIsland=Island(Top)
FakeCells = [0]*(delay_columns+2)
for i in range(delay_columns+2):
    FakeCells[i]=FakeCellGateDecoder(Top,FakeIsland)
for i in range(delay_columns+2):
    FakeCells[i].place([0,i])
    FakeCells[i].markAbut()


gateBits = int(np.ceil(np.log2((delay_columns+2)*2)))
GateDecoder = STD_IndirectGateDecoder(Top,FakeIsland,bits=gateBits)
GateSwitches = STD_IndirectGateSwitch(Top,FakeIsland,delay_columns+2)
        

GateSwitches.Vg[0] += C4_instances[0].Vg[0]
GateSwitches.Vg[1] += C4_instances[0].Vg[1]
GateSwitches.Vg[2] += Ampdet_instances[0].Vg
GateSwitches.CTRL_B[0] += C4_instances[0].Vsel[0]
GateSwitches.CTRL_B[1] += C4_instances[0].Vsel[1]
GateSwitches.CTRL_B[2] += Ampdet_instances[0].Vsel
    
GateSwitches.VINJ[0] += C4_instances[0].VINJ
GateSwitches.GND[0] += C4_instances[0].GND
GateSwitches.VTUN[0] += C4_instances[0].VTUN
GateSwitches.VDD[0] += C4_instances[0].VPWR
    
GateSwitches.VINJ[1] += Ampdet_instances[0].VINJ
GateSwitches.GND[2] += Ampdet_instances[0].GND
GateSwitches.VTUN[1] += Ampdet_instances[0].VTUN
GateSwitches.VDD[2] += Ampdet_instances[0].VPWR

for i in range(delay_columns):
    GateSwitches.Vg[i*2+3] += DelayLine_instances[i][0].Vg[0]
    GateSwitches.Vg[i*2+1+3] += DelayLine_instances[i][0].Vg[1]
    GateSwitches.CTRL_B[i*2+3] += DelayLine_instances[i][0].Vsel[0]
    GateSwitches.CTRL_B[i*2+1+3] += DelayLine_instances[i][0].Vsel[1]
    
    GateSwitches.VINJ[i+2] += DelayLine_instances[i][0].VINJ
    GateSwitches.GND[i*2+4] += DelayLine_instances[i][0].GND
    GateSwitches.VTUN[i+2] += DelayLine_instances[i][0].VTUN
    GateSwitches.VDD[i*2+4] += DelayLine_instances[i][0].VDD
    


#VMM island 1
    
VMM_Island = Island(Top)


VMM_cols = int(rows*(delay_columns+1)/2)
VMM_matrix = TSMC350nm_4x2_Indirect(Top, VMM_Island, dim=(VMM_rows,VMM_cols))
VMM_matrix.place([0,0])

WTA_Island = Island(Top)
WTA = [0]*VMM_rows
for i in range(VMM_rows):
    WTA[i] = "WTA_"+str(i)
for i in range(VMM_rows):
    WTA[i] = TSMC350nm_4WTA_IndirectProg_noncab(Top, WTA_Island)
    WTA[i].place([i,0])
    
Scanner_Island = Island(Top)
Scanner = [0]*VMM_rows
for i in range(VMM_rows):
    Scanner[i] = "Scanner_"+str(i)
for i in range(VMM_rows):
    Scanner[i] = TSMC350nm_VerticalScanner(Top, Scanner_Island)
    Scanner[i].place([i,0])

for i in range(VMM_rows):
    #WTA[i].VD_P[0] += VMM_matrix.Vd_P[4*i]
    #WTA[i].VD_P[1] += VMM_matrix.Vd_P[4*i+1]
    #WTA[i].VD_P[2] += VMM_matrix.Vd_P[4*i+2]
    #WTA[i].VD_P[3] += VMM_matrix.Vd_P[4*i+3]
    #WTA[i].Iin[0] += VMM_matrix.Vd_R[4*i]
    #WTA[i].Iin[1] += VMM_matrix.Vd_R[4*i+1]
    #WTA[i].Iin[2] += VMM_matrix.Vd_R[4*i+2]
    #WTA[i].Iin[3] += VMM_matrix.Vd_R[4*i+3]
    WTA[i].Vout += Scanner[i].In
    
    
WTA[0].Vsel += GateSwitches.CTRL_B[delay_columns*2+3]
WTA[0].Vs += DelayLine_instances[delay_columns-1][rows-1].VDD_b
WTA[0].VINJ += DelayLine_instances[delay_columns-1][rows-1].VINJ_b
WTA[0].Vg += GateSwitches.Vg[delay_columns*2+3]
WTA[0].GND += DelayLine_instances[delay_columns-1][rows-1].GND_b
WTA[0].VTUN += DelayLine_instances[delay_columns-1][rows-1].VTUN_b

VMM_drainBits = int(np.ceil(np.log2(VMM_rows*4)))
DrainDecoder_VMM = STD_DrainDecoder(Top,VMM_Island,bits=VMM_drainBits)
DrainSelect_VMM = RunDrainSwitch(Top,VMM_Island,num=VMM_rows)
DrainSwitch_VMM = DrainCutoff(Top,VMM_Island,num=VMM_rows)  


VMM_gateBit = int(np.ceil(np.log2(VMM_cols*2)))
GateDecoder_VMM = STD_IndirectGateDecoder(Top,VMM_Island,VMM_gateBit)
GateSwitches_VMM = STD_IndirectGateSwitch(Top,VMM_Island,VMM_cols)

for i in range(VMM_cols*2):
    GateSwitches_VMM.RUN_IN[i] += GateDecoder_VMM.RUN_OUT[i]
    GateSwitches_VMM.decode[i] += GateDecoder_VMM.OUT[i]

for i in range(rows):
    GateDecoder_VMM.VGRUN[i] += Ampdet_instances[i].OUTPUT
    
for i in range(delay_columns):
    for j in range(rows):
        DelayLine_instances[i][j].V_NE += GateDecoder_VMM.VGRUN[16+16*i+j]
        
        
#nFET for WTA bias
nFET_Island = Island(Top)
nFET_WTA = TSMC350nm_Termination_bot(Top,nFET_Island)
nFET_WTA.place([0,0])

for i in range(VMM_rows):
    WTA[i].Vmid += nFET_WTA.IOUT

        
#scanner for AFE
Scanner_AFE_Island = Island(Top)

Scanner_AFE = TSMC350nm_VerticalScanner(Top, Scanner_AFE_Island,dim=(4,1))
Scanner_AFE.place([0,0])
    
Scanner_AFE.In[0] += C4_instances[0].OUTPUT
Scanner_AFE.In[1] += Ampdet_instances[0].OUTPUT
for i in range(delay_columns):
    Scanner_AFE.In[2+i] += DelayLine_instances[i][0].V_NE
Scanner_AFE.In[11] += nFET_WTA.IOUT
Scanner_AFE.In[12] += C4_instances[1].OUTPUT
Scanner_AFE.In[13] += C4_instances[2].OUTPUT
        
 
#Outerpins
    
outerPins = frame(Top)
Vin = outerPins.createPort("N","Vin")
Vref = outerPins.createPort("N","Vref")
for i in range(rows):
    Vin += C4_instances[i].VIN
    Vref += C4_instances[i].VREF
        
PROG = outerPins.createPort("W","Prog")
RUN = outerPins.createPort("W","Run")
VGRUN = outerPins.createPort("W","VGRUN")
VGPROG = outerPins.createPort("W","VGPROG")

VTUN = outerPins.createPort("W","VTUN")
AVDD = outerPins.createPort("W","AVDD")
GND_N = outerPins.createPort("N","gnd")
GND_S = outerPins.createPort("S","gnd")
VINJ_N = outerPins.createPort("N","vinj")
VINJ_S = outerPins.createPort("S","vinj")

Drainline_Prog_AFE = outerPins.createPort("N","Drainline_Prog_AFE")
Drainline_Prog_VMM = outerPins.createPort("W","Drainline_Prog_VMM")

Drainline_Run_AFE = outerPins.createPort("N","Drainline_Run_AFE")
Drainline_Run_VMM = outerPins.createPort("W","Drainline_Run_VMM")

GateEnable = outerPins.createPort("N","GateEnable")
GateEnable_VMM = outerPins.createPort("N","GateEnable_VMM")
GateB = outerPins.createPort("N","GateB",dimension=VMM_gateBit)

DrainEnable = outerPins.createPort("W","DrainEnable")
DrainEnable_VMM = outerPins.createPort("W","DrainEnable_VMM")
DrainB = outerPins.createPort("W","DrainB",dimension=VMM_drainBits)

WTA_out = outerPins.createPort("E","WTA_out")
Din = outerPins.createPort("E","Din")
CLK = outerPins.createPort("E","CLK")
RSTBar = outerPins.createPort("E","RSTBar")
    
WTA_Vbias = outerPins.createPort("E","WTA_Vbias")

AFE_out = outerPins.createPort("E","AFE_out")
    
# Pin Connections
# -------------------------------------------------------------------------------
GateSwitches.vtun_l += VTUN
GateSwitches.Vgsel += VGPROG
GateSwitches.PROG += PROG
GateSwitches.RUN += RUN
GateDecoder.VINJV += VINJ_N
GateDecoder.GNDV += GND_N
GateDecoder.ENABLE += GateEnable

for i in range((delay_columns+1)*16):
    VMM_matrix.Vs_b[i] += Scanner[VMM_rows-1].VDD_b
    
for i in range((delay_columns+2)*2):
    GateDecoder.VGRUN[i] += AVDD


for i in range(gateBits):
    GateDecoder.IN[i] += GateB[i]
for i in range(delay_columns+2):
    GateSwitches.VINJ_T[i] += GateDecoder.VINJ_b[i]
    GateSwitches.GND_T[i] += GateDecoder.GND_b[i]
    GateSwitches.RUN_IN[2*i] += VGRUN
    GateSwitches.RUN_IN[2*i+1] += VGRUN
    
GateSwitches_VMM.vtun_l += VTUN
GateSwitches_VMM.Vgsel += VGPROG
GateSwitches_VMM.PROG += PROG
GateSwitches_VMM.RUN += RUN
GateDecoder_VMM.VINJV += VINJ_N
GateDecoder_VMM.GNDV += GND_N
GateDecoder_VMM.ENABLE += GateEnable_VMM
for i in range(VMM_gateBit):
    GateDecoder_VMM.IN[i] += GateB[i]
for i in range(VMM_cols):
    GateSwitches_VMM.VINJ_T[i] += GateDecoder_VMM.VINJ_b[i]
    GateSwitches_VMM.GND_T[i] += GateDecoder_VMM.GND_b[i]

DrainSwitch.VDD += VINJ_N
DrainSwitch.GND += GND_N
DrainSwitch.RUN += RUN

DrainSwitch_VMM.VDD_b += VINJ_S
DrainSwitch_VMM.GND_b += GND_S
DrainSwitch_VMM.RUN += RUN

DrainSelect.VINJ += VINJ_N
DrainSelect.GND += GND_N
DrainSelect.prog_drainrail += Drainline_Prog_AFE
DrainSelect.run_drainrail += Drainline_Run_AFE

DrainSelect_VMM.VINJ += VINJ_N
DrainSelect_VMM.GND += GND_N
DrainSelect_VMM.prog_drainrail += Drainline_Prog_VMM
DrainSelect_VMM.run_drainrail += Drainline_Run_VMM

DrainDecoder.VINJ += VINJ_N
DrainDecoder.GND += GND_N

DrainDecoder_VMM.VINJ += VINJ_S
DrainDecoder_VMM.GND += GND_S

DrainDecoder.ENABLE += DrainEnable
DrainDecoder_VMM.ENABLE += DrainEnable_VMM

for i in range(drainBits):
    DrainDecoder.IN[i] += DrainB[i]
for i in range(VMM_drainBits):
    DrainDecoder_VMM.IN[i] += DrainB[i]
    
C4_instances[0].PROG += PROG
C4_instances[0].RUN += RUN
WTA[0].PROG += PROG
        
for i in range(VMM_rows):
    WTA[i].Vbias += GND_S
    
Scanner[0].Out += WTA_out
Scanner[0].Din += Din
Scanner[0].CLK += CLK
Scanner[0].RSTBar += RSTBar
Scanner[0].VDD += AVDD
Scanner[VMM_rows-1].GND_b += GND_S

nFET_WTA.GATE += WTA_Vbias
nFET_WTA.GND += GND_N

Scanner_AFE.Out += AFE_out
Scanner_AFE.Din += Din
Scanner_AFE.CLK += CLK
Scanner_AFE.RSTBar += RSTBar
Scanner_AFE.VDD += AVDD
Scanner_AFE.GND += GND_N
Scanner_AFE.In[14] += Vin
Scanner_AFE.In[15] += Vref

#for i in range(VMM_rows):
#    WTA[i].Vmid += WTA_Vmid

x_start = 100000
y_start = 50000

design_limits = [10e6, 10e6]
location_islands = (
#AFE
(x_start,VMM_rows*22000+y_start+300000),
#AFE gate decoder
(x_start+1000000,(rows+VMM_rows)*22000+y_start+350000),
#VMM 1
(x_start,y_start),
#VMM 1 WTA
(12040+x_start+27460*(VMM_cols)+42460+20120+26270*(np.ceil(drainBits/2)-1),y_start),
#VMM 1 Scanner
(28000*VMM_cols+x_start+220000,y_start),
#VMM 2
#(28000*VMM_cols+x_start+570000,y_start),
#VMM 2 WTA
#(28000*VMM_cols*2+x_start+680000,y_start),
#VMM 2 Scanner
#(28000*VMM_cols*2+x_start+840000,y_start),
#nFET termination bot
(x_start+2200000,VMM_rows*22000+y_start+350000),
#AFE Scanner
(x_start+2200000,VMM_rows*22000+y_start+600000)
)

compile_asic(Top,process="TSMC350nm",fileName="ALICE_separate",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=10)
