def Delayline_stages(circuit,rows=1,columns=1,V_NW=None,VD_P0=None,VD_P1=None,VD_P2=None,VD_P3=None,VD_R0=None, VD_R1=None,DrainDecoder=True,DelayLineIsland=None):

    Top = circuit
    # Placement
    if DelayLineIsland == None:
        DelayLineIsland = Island(Top)
        
    
    FakeIsland=Island(Top)
    FakeCells = [0]*columns
    for i in range(columns):
        FakeCells[i]=FakeCellGateDecoder(Top,FakeIsland)
    for i in range(columns):
        FakeCells[i].place([0,i])
        FakeCells[i].markAbut()
     
    GateDecoder = STD_IndirectGateDecoder(Top,FakeIsland,columns)
    GateSwitches = STD_IndirectGateSwitch(Top,FakeIsland,columns)
        
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
    for i in range(columns):
        for j in range(rows):
            if i==columns-1:
                DelayLine_instances[i][j].V_NE += DelayLine_instances[i][j].V_SE
            else:
                DelayLine_instances[i][j].V_NE += DelayLine_instances[i+1][j].V_NW
                DelayLine_instances[i][j].V_SE += DelayLine_instances[i+1][j].V_SW
                
                
        
    # FG Programming
    # -------------------------------------------------------------------------------
    if DrainDecoder==True:
        drainBits = int(np.ceil(np.log2(rows*4)))
        DrainDecoder = STD_DrainDecoder(Top,DelayLineIsland,bits=drainBits)
        DrainSelect = RunDrainSwitch(Top,DelayLineIsland,num=rows)
        DrainSwitch = DrainCutoff(Top,DelayLineIsland,num=rows)

        for j in range(columns):
            for i in range(rows):
                DrainSwitch.PR[4*i] += DelayLine_instances[j][i].VD_P[0]
                DrainSwitch.PR[(4*i)+1] += DelayLine_instances[j][i].VD_P[1]
                DrainSwitch.PR[(4*i)+2] += DelayLine_instances[j][i].VD_P[2]
                DrainSwitch.PR[(4*i)+3] += DelayLine_instances[j][i].VD_P[3]
                DrainSwitch.In[4*i] += DelayLine_instances[j][i].VD_R[0]
                DrainSwitch.In[(4*i)+1] += DelayLine_instances[j][i].VD_R[1]
    else:
        VD_P0=[0]*rows
        VD_P1=[0]*rows
        VD_P2=[0]*rows
        VD_P3=[0]*rows
        VD_R0=[0]*rows
        VD_R1=[0]*rows
        VD_R2=[0]*rows
        VD_R3=[0]*rows
        for j in range(columns-1):
            for i in range(rows):
                DelayLine_instances[j][i].VD_P[0] += DelayLine_instances[j+1][i].VD_P[0]
                DelayLine_instances[j][i].VD_P[1] += DelayLine_instances[j+1][i].VD_P[1]
                DelayLine_instances[j][i].VD_P[2] += DelayLine_instances[j+1][i].VD_P[2]
                DelayLine_instances[j][i].VD_P[3] += DelayLine_instances[j+1][i].VD_P[3]
                DelayLine_instances[j][i].VD_R[0] += DelayLine_instances[j+1][i].VD_R[0]
                DelayLine_instances[j][i].VD_R[1] += DelayLine_instances[j+1][i].VD_R[1]
        for i in range(rows):
            VD_P0[i] = DelayLine_instances[0][i].VD_P[0]
            VD_P1[i] = DelayLine_instances[0][i].VD_P[1]
            VD_P2[i] = DelayLine_instances[0][i].VD_P[2]
            VD_P3[i] = DelayLine_instances[0][i].VD_P[3]
            VD_R0[i] = DelayLine_instances[0][i].VD_R[0]
            VD_R1[i] = DelayLine_instances[0][i].VD_R[1]
    
 
    
    for i in range(columns):
        GateSwitches.Vg[i*2] += DelayLine_instances[i][0].Vg[0]
        GateSwitches.Vg[i*2+1] += DelayLine_instances[i][0].Vg[1]
        GateSwitches.CTRL_B[i*2] += DelayLine_instances[i][0].Vsel[0]
        GateSwitches.CTRL_B[i*2+1] += DelayLine_instances[i][0].Vsel[1]
    
        GateSwitches.VINJ[i] += DelayLine_instances[i][0].VINJ
        GateSwitches.GND[i] += DelayLine_instances[i][0].GND
        GateSwitches.VTUN[i] += DelayLine_instances[i][0].VTUN
        GateSwitches.VDD[i] += DelayLine_instances[i][0].VDD
    

    #Outerpins
    
    #outerPins = frame(Top)
    #Vin = outerPins.createPort("W","Vin")
    #Vref = outerPins.createPort("W","Vref")
    #for i in range(numStages):
    #    Vin += C4_instances[i].VIN
    #    Vref += C4_instances[i].VREF
        
    #PROG = outerPins.createPort("N","Prog")
    #RUN = outerPins.createPort("N","Run")
    #VGRUN = outerPins.createPort("N","VGRUN")
    #VGPROG = outerPins.createPort("N","VGPROG")

    #VTUN = outerPins.createPort("N","VTUN")
    #AVDD = outerPins.createPort("N","AVDD")
    #GND_N = outerPins.createPort("N","gnd")
    #GND_S = outerPins.createPort("S","gnd")
    #VINJ_N = outerPins.createPort("N","vinj")
    #VINJ_S = outerPins.createPort("S","vinj")

    #Drainline = outerPins.createPort("W","Drainline_Prog")

    #GateEnable = outerPins.createPort("N","GateEnable")
    #GateB = outerPins.createPort("N","GateB",dimension=2)

    #DrainEnable = outerPins.createPort("W","DrainEnable")
    #DrainB = outerPins.createPort("W","DrainB",dimension=drainBits)
    
    
    # Pin Connections
    # -------------------------------------------------------------------------------
    #GateSwitches.RUN_IN[0] += VGRUN
    #GateSwitches.RUN_IN[1] += VGRUN
    #GateSwitches.RUN_IN[2] += VGRUN
    #GateSwitches.RUN_IN[3] += VGRUN
    #GateSwitches.VINJ_T[0] += GateDecoder.VINJ_b[0]
    #GateSwitches.VINJ_T[1] += GateDecoder.VINJ_b[1]
    
    #GateSwitches.GND_T[0] += GND_N
    #GateSwitches.GND_T[1] += GND_N
    #GateSwitches.Vgsel += VGPROG
    #GateSwitches.PROG += PROG
    #GateSwitches.RUN += RUN

    #GateDecoder.VINJV += VINJ_N
    #GateDecoder.GNDV += GND_N
    #GateDecoder.ENABLE += GateEnable
    #GateDecoder.IN += GateB

    #DrainSwitch.VDD += VINJ_S
    #DrainSwitch.GND += GND_S
    #DrainSwitch.RUN += RUN

    #DrainSelect.VINJ_b += VINJ_S
    #DrainSelect.GND_b += GND_S
    #DrainSelect.prog_drainrail += Drainline

    #DrainDecoder.VINJ += VINJ_S
    #DrainDecoder.GND += GND_S
    #for i in range(drainBits):
    #    DrainDecoder.IN[i] += DrainB[i]
    #DrainDecoder.IN += DrainB
    #DrainDecoder.ENABLE += DrainEnable

    #C4_instances[0].PROG += PROG
    #C4_instances[0].RUN += RUN

    if V_NW==None:
	    V_NW = [0]*rows
	    for i in range(rows):
		    V_NW[i] = DelayLine_instances[0][i].V_NW
    else:
	    for i in range(rows):
		    V_NW[i] = DelayLine_instances[0][i].V_NW

    ladder_out = [0]*(rows*columns)
    pointer = 0
    for i in range(columns):
        for j in range(rows):
            ladder_out[pointer] = DelayLine_instances[i][j].V_NE
            pointer += 1
    
    return ladder_out

Top = Circuit()
#C4_Ampdet(Top,16)
Delayline_stages(Top,rows=128,columns=3)

design_limits = [1e6, 3e6]
location_islands = ((50000,25000),(240000,22000*130))


compile_asic(Top,process="TSMC350nm",fileName="Delayline_stages",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 0,gateSpaceIdx=0,gateSpace=10)
