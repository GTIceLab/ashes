from ashes_fg.asic.asic_compile import *

class AveragerDAC(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),AVDD_N=None,AVDD_S=None,VINJ_N=None,VINJ_S=None,GND_N=None,GND_S=None,VTUN=None,DrainB=None,DrainEnable=None,GateEnable=None,GateB=None,Prog=None,Run=None,Code=None,DEBUG=None,Vout=None,Drainline_Prog=None,Drainline_Run=None,VGRUN=None,VGPROG=None):

        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'AveragerDAC_synth'
        self.AVDD_N = Port(circuit,self,"n_avdd",'N',1)
        self.AVDD_S = Port(circuit,self,"s_avdd",'S',1)
        self.VINJ_N = Port(circuit,self,"n_vinj",'N',1)
        self.VINJ_S = Port(circuit,self,"s_vinj",'S',1)
        self.GND_N = Port(circuit,self,"n_gnd",'N',1)
        self.GND_S = Port(circuit,self,"s_gnd",'S',1)
        self.VTUN = Port(circuit,self,"n_VTUN",'N',1)

        self.DrainB = Port(circuit,self,"w_DrainB",'W',4)
        self.DrainEnable = Port(circuit,self,"w_DrainEnable",'W',1)
        self.GateEnable = Port(circuit,self,"n_GateEnable",'N',1)
        self.GateB = Port(circuit,self,"w_GateB",'W',2)

        self.Prog= Port(circuit,self,"n_Prog",'N',1)
        self.Run = Port(circuit,self,"n_Run",'N',1)
        
        self.Code = Port(circuit,self,"e_Code",'E',5)

        self.DEBUG = Port(circuit,self,"s_DEBUG",'S',2)

        self.Vout = Port(circuit,self,"s_Vout",'S',1)
        self.Drainline_Prog = Port(circuit,self,"s_Prog_Drainline",'S',1)
        self.Drainline_Run = Port(circuit,self,"s_Run_Drainline",'S',1)

        self.VGRUN  = Port(circuit,self,"n_VGRUN",'N',1)
        self.VGPROG = Port(circuit,self,"n_VGPROG",'N',1)
        # Initialize ports with given values
        portsInit = [AVDD_N,AVDD_S,VINJ_N,VINJ_S,GND_N,GND_S,VTUN,DrainB,DrainEnable,GateEnable,GateB,Prog,Run,Code,DEBUG,Vout,Drainline_Prog,Drainline_Run,VGRUN,VGPROG]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class AlgorithmicADC(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),AVDD_N=None,AVDD_S=None,VINJ_N=None,VINJ_S=None,GND_N=None,GND_S=None,VTUN=None,DrainB=None,DrainEnable=None,GateEnable=None,GateB=None,Prog=None,Run=None,Vin=None,Code=None,CLK_Sample=None,CLK_Amp=None,CLK_Load=None,CLK_RST=None,VRES=None,DEBUG=None,Drainline_Prog=None,Drainline_Run=None,VGRUN=None,VGPROG=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'AlgorithmicADC_synth'
        self.AVDD_N = Port(circuit,self,"n_avdd",'N',1)
        self.AVDD_S = Port(circuit,self,"s_avdd",'S',1)
        self.VINJ_N = Port(circuit,self,"n_vinj",'N',1)
        self.VINJ_S = Port(circuit,self,"s_vinj",'S',1)
        self.GND_N = Port(circuit,self,"n_gnd",'N',1)
        self.GND_S = Port(circuit,self,"s_gnd",'S',1)
        self.VTUN = Port(circuit,self,"n_VTUN",'N',1)

        self.DrainB = Port(circuit,self,"w_DrainB",'W',4)
        self.DrainEnable = Port(circuit,self,"w_DrainEnable",'W',1)
        self.GateEnable = Port(circuit,self,"n_GateEnable",'N',1)
        self.GateB = Port(circuit,self,"w_GateB",'W',2)

        self.Prog= Port(circuit,self,"n_PROG",'N',1)
        self.Run = Port(circuit,self,"n_RUN",'N',1)
        
        self.Vin = Port(circuit,self,"w_Vin",'W',1)
        self.Code = Port(circuit,self,"s_Code",'S',1)

        self.CLK_Sample = Port(circuit,self,"e_CLK_Sample",'E',1)
        self.CLK_Amp = Port(circuit,self,"e_CLK_Amp",'E',1)
        self.CLK_Load = Port(circuit,self,"e_CLK_Load",'E',1)
        self.CLK_RST = Port(circuit,self,"s_CLK_RST",'S',1)

        self.VRES = Port(circuit,self,"s_VRES",'S',1)
        self.DEBUG = Port(circuit,self,"e_DEBUG",'E',3)

        self.Drainline_Prog = Port(circuit,self,"s_Prog_Drainline",'S',1)
        self.Drainline_Run = Port(circuit,self,"s_Run_Drainline",'S',1)

        self.VGRUN  = Port(circuit,self,"n_VGRUN",'N',1)
        self.VGPROG = Port(circuit,self,"n_VGPROG",'N',1)

        # Initialize ports with given values
        portsInit = [AVDD_N,AVDD_S,VINJ_N,VINJ_S,GND_N,GND_S,VTUN,DrainB,DrainEnable,GateEnable,GateB,Prog,Run,Vin,Code,CLK_Sample,CLK_Amp,CLK_Load,CLK_RST,VRES,DEBUG,Drainline_Prog,Drainline_Run,VGRUN,VGPROG]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1


        # Add cell to circuit
        circuit.addInstance(self,self.island)

class RampADC(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),AVDD_N=None,AVDD_S=None,VINJ_N=None,VINJ_S=None,GND_N=None,GND_S=None,VTUN=None,DrainB=None,DrainEnable=None,GateEnable=None,GateB=None,Prog=None,Run=None,RST=None,CLK=None,Vin=None,Code=None,DEBUG=None,Vout=None,Drainline_Prog=None,Drainline_Run=None,VGRUN=None,VGPROG=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'RampADC_synth'
        self.AVDD_N = Port(circuit,self,"n_avdd",'N',1)
        self.AVDD_S = Port(circuit,self,"s_avdd",'S',1)
        self.VINJ_N = Port(circuit,self,"n_vinj",'N',1)
        self.VINJ_S = Port(circuit,self,"s_vinj",'S',1)
        self.GND_N = Port(circuit,self,"n_gnd",'N',1)
        self.GND_S = Port(circuit,self,"s_gnd",'S',1)
        self.VTUN = Port(circuit,self,"n_VTUN",'N',1)

        self.DrainB = Port(circuit,self,"w_DrainB",'W',2)
        self.DrainEnable = Port(circuit,self,"w_DrainEnable",'W',1)
        self.GateEnable = Port(circuit,self,"n_GateEnable",'N',1)
        self.GateB = Port(circuit,self,"w_GateB",'W',2)

        self.Prog= Port(circuit,self,"n_Prog",'N',1)
        self.Run = Port(circuit,self,"n_Run",'N',1)
        
        self.RST = Port(circuit,self,"w_RST",'W',1)
        self.CLK = Port(circuit,self,"w_CLK",'W',1)
        self.Vin = Port(circuit,self,"w_Vin",'W',1)
        self.Code = Port(circuit,self,"s_Code",'S',8)

        self.DEBUG = Port(circuit,self,"e_DEBUG",'E',2)

        self.Vout = Port(circuit,self,"s_Vout",'S',1)
        self.Drainline_Prog = Port(circuit,self,"s_Prog_Drainline",'S',1)
        self.Drainline_Run = Port(circuit,self,"s_Run_Drainline",'S',1)

        self.VGRUN  = Port(circuit,self,"n_VGRUN",'N',1)
        self.VGPROG = Port(circuit,self,"n_VGPROG",'N',1)

        # Initialize ports with given values
        portsInit = [AVDD_N,AVDD_S,VINJ_N,VINJ_S,GND_N,GND_S,VTUN,DrainB,DrainEnable,GateEnable,GateB,Prog,Run,RST,CLK,Vin,Code,DEBUG,Vout,Drainline_Prog,Drainline_Run,VGRUN,VGPROG]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1


        # Add cell to circuit
        circuit.addInstance(self,self.island)

class QDAC(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),AVDD_N=None,AVDD_S=None,VINJ_N=None,VINJ_S=None,GND_N=None,GND_S=None,VTUN=None,DrainB=None,DrainEnable=None,GateEnable=None,GateB=None,Prog=None,Run=None,RST=None,Code=None,DEBUG=None,Vout=None,Drainline_Prog=None,Drainline_Run=None,VGRUN=None,VGPROG=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'QDAC_synth'
        self.AVDD_N = Port(circuit,self,"n_avdd",'N',1)
        self.AVDD_S = Port(circuit,self,"s_avdd",'S',1)
        self.VINJ_N = Port(circuit,self,"n_vinj",'N',1)
        self.VINJ_S = Port(circuit,self,"s_vinj",'S',1)
        self.GND_N = Port(circuit,self,"n_gnd",'N',1)
        self.GND_S = Port(circuit,self,"s_gnd",'S',1)
        self.VTUN = Port(circuit,self,"n_VTUN",'N',1)

        self.DrainB = Port(circuit,self,"w_DrainB",'W',4)
        self.DrainEnable = Port(circuit,self,"w_DrainEnable",'W',1)
        self.GateEnable = Port(circuit,self,"n_GateEnable",'N',1)
        self.GateB = Port(circuit,self,"w_GateB",'W',2)

        self.Prog= Port(circuit,self,"n_Prog",'N',1)
        self.Run = Port(circuit,self,"n_Run",'N',1)
        
        self.RST = Port(circuit,self,"n_RST",'N',1)
        self.Code = Port(circuit,self,"n_Code",'N',5)

        self.DEBUG = Port(circuit,self,"e_DEBUG",'E',5)

        self.Vout = Port(circuit,self,"s_Vout",'S',1)
        self.Drainline_Prog = Port(circuit,self,"s_Prog_Drainline",'S',1)
        self.Drainline_Run = Port(circuit,self,"s_Run_Drainline",'S',1)

        self.VGRUN  = Port(circuit,self,"n_VGRUN",'N',1)
        self.VGPROG = Port(circuit,self,"n_VGPROG",'N',1)

        # Initialize ports with given values
        portsInit = [AVDD_N,AVDD_S,VINJ_N,VINJ_S,GND_N,GND_S,VTUN,DrainB,DrainEnable,GateEnable,GateB,Prog,Run,RST,Code,DEBUG,Vout,Drainline_Prog,Drainline_Run,VGRUN,VGPROG]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class TSMC350nm_RippleCounter(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Count=None,Count_B=None,RST=None,RST_L=None,CLK=None,GND=None,GND_L = None,VDD=None,VDD_L=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'RippleCounter'
        self.Count = Port(circuit,self,"Count",'N',1*self.dim[1])
        self.Count_B = Port(circuit,self,"Count",'S',1*self.dim[1])
        self.RST = Port(circuit,self,"RST",'E',1)
        self.RST_L = Port(circuit,self,"RST_L",'W',1)
        self.CLK = Port(circuit,self,"CLK",'W',1)
        self.GND = Port(circuit,self,"GND",'E',1)
        self.GND_L = Port(circuit,self,"GND_L",'W',1)
        self.VDD = Port(circuit,self,"VDD",'E',1)
        self.VDD_L = Port(circuit,self,"VDD_L",'W',1)

        # Initialize ports with given values
        portsInit = [Count,Count_B,RST,RST_L,CLK,GND,GND_L,VDD,VDD_L]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class TSMC350nm_AnalogBuffer(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VTUN=None,VTUN_b=None,VDD=None,VDD_b=None,GND=None,GND_b=None,VINJ=None,VINJ_b=None,Vg=None,Vg_b=None,Vd_P=None,Vsel=None,Vsel_b=None,Vin=None,Vout=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'TSMC350nm_AnalogBuffer'
        self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
        self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
        self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
        self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
        self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
        self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
        self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])
        self.Vd_P = Port(circuit,self,'Vd_P','W',1*self.dim[0])
        self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
        self.Vin = Port(circuit,self,'Vin','W',1*self.dim[0])
        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])

        # Initialize ports with given values
        portsInit = [VTUN,VTUN_b,VDD,VDD_b,GND,GND_b,VINJ,VINJ_b,Vg,Vg_b,Vd_P,Vsel,Vsel_b,Vin,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_EPOT(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VDD=None,VDD_b=None,VINJ=None,VINJ_b=None,GND=None,GND_b=None,VTUN=None,VTUN_b=None,Prog=None,Prog_b=None,Vg=None,Vg_b=None,Vsel=None,Vsel_b=None,VD_P=None,VINPLUS=None,Vout=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'EPOT'
        self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
        self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
        self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])

        self.Prog = Port(circuit,self,'Prog','N',1*self.dim[1])
        self.Prog_b = Port(circuit,self,'Prog_b','S',1*self.dim[1])

        self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
        self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])

        self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])

        self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])

        self.VIN_PLUS = Port(circuit,self,'VIN_PLUS','W',1*self.dim[0])
        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])

		
        # Initialize ports with given values
        portsInit = [VDD,VDD_b,VINJ,VINJ_b,GND,GND_b,VTUN,VTUN_b,Prog,Prog_b,Vg,Vg_b,Vsel,Vsel_b,VD_P,VINPLUS,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class  TSMC350nm_Amplifier9T_FGInputs_Bias(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VDD=None,VDD_b=None,VINJ=None,VINJ_b=None,GND=None,GND_b=None,VTUN=None,VTUN_b=None,Vg=None,Vg_b=None,Vd_P=None,Vd_R=None,Vsel=None,Vsel_b=None,Prog=None,Prog_b=None,VIN_PLUS=None,VIN_MINUS=None,Vout=None):

        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'TSMC350nm_Amplifier9T_FGInputs_Bias'
        self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
        self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
        self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
        
        self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
        self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])

        self.Vd_P = Port(circuit,self,'Vd_P','W',2*self.dim[0])
        self.Vd_R = Port(circuit,self,'Vd_R','W',1*self.dim[0])

        self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])

        self.Prog= Port(circuit,self,'Prog','N',1*self.dim[1])
        self.Prog_b= Port(circuit,self,'Prog_b','S',1*self.dim[1])

        self.VIN_PLUS = Port(circuit,self,'VIN_PLUS','W',1*self.dim[0])
        self.VIN_MINUS = Port(circuit,self,'VIN_MINUS','W',1*self.dim[0])

        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])

        # Initialize ports with given values
        portsInit = [VDD,VDD_b,VINJ,VINJ_b,GND,GND_b,VTUN,VTUN_b,Vg,Vg_b,Vd_P,Vd_R,Vsel,Vsel_b,Prog,Prog_b,VIN_PLUS,VIN_MINUS,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_Amplifier9T_FGBias(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VPWR=None,VPWR_b=None,VINJ=None,VINJ_b=None,GND=None,GND_b=None,VTUN=None,VTUN_b=None,Vg=None,Vg_b=None,VD_P=None,VD_R=None,Vsel=None,Vsel_b=None,PROG=None,PROG_b=None,VIN_PLUS=None,VIN_MINUS=None,Vout=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'TSMC350nm_Amplifier9T_FGBias'
        self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
        self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])
        self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
        self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
        self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])

        self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
        self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])

        self.VD_P = Port(circuit,self,'VD_P','W',1*self.dim[0])
        self.VD_R = Port(circuit,self,'VD_R','W',1*self.dim[0])

        self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])

        self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
        self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])

        self.VIN_PLUS = Port(circuit,self,'VIN_PLUS','W',1*self.dim[0])
        self.VIN_MINUS = Port(circuit,self,'VIN_MINUS','W',1*self.dim[0])

        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])


        # Initialize ports with given values
        portsInit = [VPWR,VPWR_b,VINJ,VINJ_b,GND,GND_b,VTUN,VTUN_b,Vg,Vg_b,VD_P,VD_R,Vsel,Vsel_b,PROG,PROG_b,VIN_PLUS,VIN_MINUS,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_Capacitor_80ff(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Top=None,Bot=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'Capacitor_80ff'
        self.Top = Port(circuit,self,'Top','W',1*self.dim[0])
        self.Bot = Port(circuit,self,'Bot','E',1*self.dim[0])
      

        # Initialize ports with given values
        portsInit = [Top,Bot]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_TGate_DT(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VDD=None,VDD_b=None,GND=None,GND_b=None,SELA=None,C=None,A=None,B=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'TGate_DT'
        self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.SELA = Port(circuit,self,'SELA','W',1*self.dim[0])
        self.C = Port(circuit,self,'C','W',1*self.dim[0])

        self.A = Port(circuit,self,'A','E',1*self.dim[0])
        self.B = Port(circuit,self,'B','E',1*self.dim[0])

        # Initialize ports with given values
        portsInit = [VDD,VDD_b,GND,GND_b,SELA,C,A,B]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)