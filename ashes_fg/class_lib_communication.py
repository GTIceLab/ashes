from ashes_fg.asic.asic_compile import *

class TSMC350nm_DelayLines(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Prog=None, Run=None, VGRUN=None, VGPROG=None, VTUN=None, AVDD=None, GateB=None, OUTS=None,GateEnable_Del=None, VINJ_N=None, GND_N=None, WTA_CTRL_B=None, WTA_Vg=None, GND_S=None, VINJ_S=None, RSTBar=None, CLK=None, Din=None, WTA_out=None, DrainEnable_Del=None, Input=None, Drainline_Run=None, Drainline_Prog=None, DrainB=None):

		# Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

		# Define cell information
        self.name = 'TOP_DelayLines'
        self.Prog = Port(circuit,self, 'n_Prog' ,'N',1*self.dim[1])
        self.Run = Port(circuit,self, 'n_Run' ,'N',1*self.dim[1])
        self.VGRUN = Port(circuit,self, 'n_VGRUN' ,'N',1*self.dim[1])
        self.VGPROG = Port(circuit,self, 'n_VGPROG' ,'N',1*self.dim[1])
        self.VTUN = Port(circuit,self, 'n_VTUN' ,'N',1*self.dim[1])
        self.AVDD = Port(circuit,self, 'n_AVDD' ,'N',1*self.dim[1])
        self.GateB = Port(circuit,self, 'n_GateB' ,'N',5*self.dim[1])
        self.OUTS = Port(circuit,self, 'n_OUTS' ,'N',400*self.dim[1])
        self.GateEnable_Del = Port(circuit, self, 'n_GateEnable_Del' ,'N',1*self.dim[1])
        self.VINJ_N = Port(circuit,self, 'n_vinj' ,'N',1*self.dim[1])
        self.GND_N = Port(circuit,self, 'n_gnd' ,'N',1*self.dim[1])
        
        self.GND_S = Port(circuit,self, 's_gnd' ,'S',1*self.dim[1])        
        self.VINJ_S = Port(circuit,self, 's_vinj' ,'S',1*self.dim[1])
        self.RSTBar = Port(circuit,self, 's_RSTBar' ,'S',1*self.dim[1])
        self.CLK = Port(circuit,self, 's_CLK' ,'S',1*self.dim[1])
        self.Din = Port(circuit,self, 's_Din' ,'S',1*self.dim[1])
        self.WTA_out = Port(circuit,self, 's_WTA_out' ,'S',1*self.dim[1])
		
        self.WTA_CTRL_B = Port(circuit,self, 'e_WTA_CTRL_B' ,'E',2*self.dim[1])
        self.WTA_Vg = Port(circuit,self, 'e_WTA_Vg' ,'E',2*self.dim[1])
		
        self.DrainEnable_Del = Port(circuit,self, 'w_DrainEnable_Del' ,'W',1*self.dim[1])
        self.Input = Port(circuit,self, 'w_Input' ,'W',40*self.dim[1])
        self.Drainline_Run = Port(circuit,self, 'w_Drainline_Run' ,'W',1*self.dim[1])
        self.Drainline_Prog = Port(circuit,self, 'w_Drainline_Prog' ,'W',1*self.dim[1])
        self.DrainB = Port(circuit,self, 'w_DrainB' ,'W',8*self.dim[1])		
		
        # Initialize ports with given values
        portsInit = [Prog,Run,VGRUN,VGPROG,VTUN,AVDD,GateB,OUTS,GateEnable_Del,VINJ_N, VINJ_S,GND_N, GND_S,WTA_CTRL_B,WTA_Vg,RSTBar,CLK,Din,WTA_out,DrainEnable_Del,Input,Drainline_Run,Drainline_Prog,DrainB]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

		# Add cell to circuit
        circuit.addInstance(self,self.island)

class VMMWTAAlgFullRoute(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_AVDD=None,w_Drainline_Prog=None,w_Drainline_Run=None,w_DrainB=None,w_DrainEnable_Mod=None,n_Prog=None,n_Run=None,n_VGPROG=None,n_GateB=None,n_GateEnable_Mod=None,n_VTUN=None,RUNO=None,VOUT=None,n_vinj=None,n_gnd=None,Vmid=None,Vbias=None,Vsel_WTA=None,Vs_WTA=None,Vg_WTA=None,Prog_WTA=None,e_Din=None,e_Out=None,e_CLK=None,e_RSTBar=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'VMMWTA_FullRoute'
		self.w_Drainline_Prog = Port(circuit,self,'DRAIN_PROG','E',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'DRAIN_RUN','E',self.dim[0])
		self.w_DrainB = Port(circuit,self,'DRAIN_BITS','E',8*self.dim[0])
		self.w_DrainEnable_Mod = Port(circuit,self,'D_ENABLE','E',self.dim[0])
		self.n_Prog = Port(circuit,self,'PROG','S',self.dim[1])
		self.n_Run = Port(circuit,self,'RUN','S',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'VGPROG','S',self.dim[1])
		self.n_GateB = Port(circuit,self,'GATE_BITS','S',9*self.dim[1])
		self.w_GateEnable_Mod = Port(circuit,self,'G_ENABLE','S',self.dim[1])
		self.n_VTUN = Port(circuit,self,'VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',280*self.dim[1])  
		self.n_AVDD = Port(circuit,self,'AVDD','S',self.dim[1])
		self.n_vinj = Port(circuit,self,'VINJ_N','S',self.dim[1])	
		self.n_gnd = Port(circuit,self,'GND_N','S',self.dim[1])	
		self.Vmid = Port(circuit,self,'VMID','N',self.dim[1])	
		self.Vbias = Port(circuit,self,'VBIAS','N',self.dim[1])
		self.Vsel_WTA = Port(circuit,self,'VSEL_WTA','N',self.dim[1])	
		self.Vs_WTA = Port(circuit,self,'VS_WTA','N',self.dim[1])	
		self.Vg_WTA = Port(circuit,self,'VG_WTA','N',self.dim[1])
		self.Prog_WTA = Port(circuit,self,'PROG_WTA','N',self.dim[1])
		self.e_Din = Port(circuit,self,'e_Din','E',self.dim[0])		
		self.e_Out = Port(circuit,self,'e_Out','E',self.dim[0])	
		self.e_CLK = Port(circuit,self,'e_CLK','E',self.dim[0])	
		self.e_RSTBar = Port(circuit,self,'e_RSTBar','E',self.dim[0])	

		# Initialize ports with given values
		portsInit = [w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_Mod,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_Mod,n_VTUN,RUNO,n_vinj,n_gnd,Vmid,Vbias,Vsel_WTA,Vs_WTA,Vg_WTA,Prog_WTA,e_Din,e_Out,e_CLK,e_RSTBar]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class ModulationAlgFlip(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_AVDD=None,w_Drainline_Prog=None,w_Drainline_Run=None,w_DrainB=None,w_DrainEnable_Mod=None,n_Prog=None,n_Run=None,n_VGPROG=None,n_GateB=None,n_GateEnable_Mod=None,n_VTUN=None,RUNO=None,VOUT=None,e_VG_N=None,e_VG_P=None,e_VC=None,n_vinj=None,n_gnd=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'Modulation_Flip'
		self.w_Drainline_Prog = Port(circuit,self,'DRAIN_PROG','E',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'DRAIN_RUN','E',self.dim[0])
		self.w_DrainB = Port(circuit,self,'DRAIN_BITS','E',9*self.dim[0])
		self.w_DrainEnable_Mod = Port(circuit,self,'D_ENABLE','E',self.dim[0])
		self.n_Prog = Port(circuit,self,'PROG','S',self.dim[1])
		self.n_Run = Port(circuit,self,'RUN','S',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'VGPROG','S',self.dim[1])
		self.n_GateB = Port(circuit,self,'GATE_BITS','S',9*self.dim[1])
		self.w_GateEnable_Mod = Port(circuit,self,'G_ENABLE','S',self.dim[1])
		self.n_VTUN = Port(circuit,self,'VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',400*self.dim[1]) 
		self.VOUT = Port(circuit,self,'VOUT','S',280*self.dim[1]) 
		self.n_AVDD = Port(circuit,self,'AVDD','S',self.dim[1])
		self.e_VG_N = Port(circuit,self,'e_VG_N','W',self.dim[0])
		self.e_VG_P = Port(circuit,self,'e_VG_P','W',self.dim[0])
		self.e_VC = Port(circuit,self,'e_VC','W',self.dim[0])
		self.n_vinj = Port(circuit,self,'VINJ_N','S',self.dim[1])	
		self.n_gnd = Port(circuit,self,'GND_N','S',self.dim[1])			
		# Initialize ports with given values
		portsInit = [w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_Mod,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_Mod,n_VTUN,RUNO,VOUT,e_VG_N,e_VG_P,e_VC,n_vinj,n_gnd]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class FakeCell(FakeStandardCell):
	def __init__(self,circuit,island=None,dim=(2,2),FakePort=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'FakeCell'
		self.FakePort = Port(circuit,self,'FakePort','E',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [FakePort]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)