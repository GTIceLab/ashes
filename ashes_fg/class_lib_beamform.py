from ashes_fg.asic.asic_compile import *

class TOP_DelayLines_flipped(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),PROG=None,RUN=None,VGRUN=None,VGPROG=None,VTUN=None,AVDD=None,GATE_BITS=None,OUTS=None,G_ENABLE=None,VINJ_N=None,GND_N=None,D_ENABLE=None,INPUT=None,DRAIN_RUN=None,DRAIN_PROG=None,DRAIN_BITS=None,GND_S=None,VINJ_S=None,RSTBar=None,CLK=None,Din=None,WTA_OUT=None,WTA_CTRL_B=None,WTA_VG=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'TOP_DelayLines'

		self.PROG = Port(circuit,self, 'n_Prog' ,'N',1*self.dim[1])
		self.RUN = Port(circuit,self, 'n_Run' ,'N',1*self.dim[1])
		self.VGRUN = Port(circuit,self, 'n_VGRUN' ,'N',1*self.dim[1])
		self.VGPROG = Port(circuit,self, 'n_VGPROG' ,'N',1*self.dim[1])
		self.VTUN = Port(circuit,self, 'n_VTUN' ,'N',1*self.dim[1])
		self.AVDD = Port(circuit,self, 'n_AVDD' ,'N',1*self.dim[1])
		self.GATE_BITS = Port(circuit,self, 'n_GateB' ,'N',5*self.dim[1])
		self.OUTS = Port(circuit,self, 'n_OUTS' ,'N',400*self.dim[1])
		self.G_ENABLE = Port(circuit, self, 'n_GateEnable_Del' ,'N',1*self.dim[1])
		self.VINJ_N = Port(circuit,self, 'n_vinj' ,'N',1*self.dim[1])
		self.GND_N = Port(circuit,self, 'n_gnd' ,'N',1*self.dim[1])

		self.GND_S = Port(circuit,self, 's_gnd' ,'S',1*self.dim[1])        
		self.VINJ_S = Port(circuit,self, 's_vinj' ,'S',1*self.dim[1])
		self.RSTBar = Port(circuit,self, 's_RSTBar' ,'S',1*self.dim[1])
		self.CLK = Port(circuit,self, 's_CLK' ,'S',1*self.dim[1])
		self.Din = Port(circuit,self, 's_Din' ,'S',1*self.dim[1])
		self.WTA_OUT = Port(circuit,self, 's_WTA_out' ,'S',1*self.dim[1])

		self.WTA_CTRL_B = Port(circuit,self, 'e_WTA_CTRL_B' ,'W',2*self.dim[1])
		self.WTA_VG = Port(circuit,self, 'e_WTA_Vg' ,'W',2*self.dim[1])

		self.D_ENABLE = Port(circuit,self, 'w_DrainEnable_Del' ,'E',1*self.dim[1])
		self.INPUT = Port(circuit,self, 'w_Input' ,'E',40*self.dim[1])
		self.DRAIN_RUN = Port(circuit,self, 'w_Drainline_Run' ,'E',1*self.dim[1])
		self.DRAIN_PROG = Port(circuit,self, 'w_Drainline_Prog' ,'E',1*self.dim[1])
		self.DRAIN_BITS = Port(circuit,self, 'w_DrainB' ,'E',8*self.dim[1])		
		
		# Initialize ports with given values
		portsInit = [PROG,RUN,VGRUN,VGPROG,VTUN,AVDD,GATE_BITS,OUTS,G_ENABLE,VINJ_N,GND_N,D_ENABLE,INPUT,DRAIN_RUN,DRAIN_PROG,DRAIN_BITS,GND_S,VINJ_S,RSTBar,CLK,Din,WTA_OUT,WTA_CTRL_B,WTA_VG]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class VMMWTAAlgFullRoute(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VMID=None,VBIAS=None,VSEL_WTA=None,VS_WTA=None,VG_WTA=None,PROG_WTA=None,DRAIN_PROG=None,DRAIN_RUN=None,DRAIN_BITS=None,D_ENABLE=None,PROG=None,RUN=None,VGPROG=None,GATE_BITS=None,G_ENABLE=None,VTUN=None,RUNO=None,AVDD=None,VINJ_N=None,GND_N=None,Din=None,Out=None,CLK=None,RSTBar=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'VMMWTA_FullRoute'
		
		self.DRAIN_PROG = Port(circuit,self,'w_Drainline_Prog','E',self.dim[0])
		self.DRAIN_RUN = Port(circuit,self,'w_Drainline_Run','E',self.dim[0])
		self.DRAIN_BITS = Port(circuit,self,'w_DrainB','E',8*self.dim[0])
		self.D_ENABLE = Port(circuit,self,'w_DrainEnable_Mod','E',self.dim[0])
		
		self.PROG = Port(circuit,self,'n_Prog','S',self.dim[1])
		self.RUN = Port(circuit,self,'n_Run','S',self.dim[1])
		self.VGPROG = Port(circuit,self,'n_VGPROG','S',self.dim[1])
		self.GATE_BITS = Port(circuit,self,'n_GateB','S',9*self.dim[1])
		self.G_ENABLE = Port(circuit,self,'w_GateEnable_Mod','S',self.dim[1])
		self.VTUN = Port(circuit,self,'n_VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',280*self.dim[1])  
		self.AVDD = Port(circuit,self,'n_AVDD','S',self.dim[1])
		self.VINJ_N = Port(circuit,self,'n_vinj','S',self.dim[1])	
		self.GND_N = Port(circuit,self,'n_gnd','S',self.dim[1])	
		
		self.VMID = Port(circuit,self,'Vmid','N',self.dim[1])	
		self.VBIAS = Port(circuit,self,'Vbias','N',self.dim[1])
		self.VSEL_WTA = Port(circuit,self,'Vsel_WTA','N',self.dim[1])	
		self.VS_WTA = Port(circuit,self,'Vs_WTA','N',self.dim[1])	
		self.VG_WTA = Port(circuit,self,'Vg_WTA','N',self.dim[1])
		self.PROG_WTA = Port(circuit,self,'Prog_WTA','N',self.dim[1])
		
		self.Din = Port(circuit,self,'e_Din','W',self.dim[0])		
		self.Out = Port(circuit,self,'e_Out','W',self.dim[0])	
		self.CLK = Port(circuit,self,'e_CLK','W',self.dim[0])	
		self.RSTBar = Port(circuit,self,'e_RSTBar','W',self.dim[0])	

		# Initialize ports with given values
		portsInit = [VMID,VBIAS,VSEL_WTA,VS_WTA,VG_WTA,PROG_WTA,DRAIN_PROG,DRAIN_RUN,DRAIN_BITS,D_ENABLE,PROG,RUN,VGPROG,GATE_BITS,G_ENABLE,VTUN,RUNO,AVDD,VINJ_N,GND_N,Din,Out,CLK,RSTBar]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class ModulationAlgFlip(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VINJ_S=None,GND_S=None,DRAIN_PROG=None,DRAIN_RUN=None,DRAIN_BITS=None,D_ENABLE=None,PROG=None,RUN=None,VGPROG=None,GATE_BITS=None,G_ENABLE=None,VTUN=None,RUNO=None,VOUT=None,AVDD=None,VINJ_N=None,GND_N=None,VG_N=None,VG_P=None,VC=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'Modulation_Flip'
		self.DRAIN_PROG = Port(circuit,self,'w_Drainline_Prog','E',self.dim[0])
		self.DRAIN_RUN = Port(circuit,self,'w_Drainline_Run','E',self.dim[0])
		self.DRAIN_BITS = Port(circuit,self,'w_DrainB','E',9*self.dim[0])
		self.D_ENABLE = Port(circuit,self,'w_DrainEnable_Mod','E',self.dim[0])
		
		self.PROG = Port(circuit,self,'n_Prog','S',self.dim[1])
		self.RUN = Port(circuit,self,'n_Run','S',self.dim[1])
		self.VGPROG = Port(circuit,self,'n_VGPROG','S',self.dim[1])
		self.GATE_BITS = Port(circuit,self,'n_GateB','S',9*self.dim[1])
		self.G_ENABLE = Port(circuit,self,'w_GateEnable_Mod','S',self.dim[1])
		self.VTUN = Port(circuit,self,'n_VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',400*self.dim[1]) 
		self.VOUT = Port(circuit,self,'VOUT','S',280*self.dim[1]) 
		self.AVDD = Port(circuit,self,'n_AVDD','S',self.dim[1])
		self.VINJ_N = Port(circuit,self,'n_vinj','S',self.dim[1])	
		self.GND_N = Port(circuit,self,'n_gnd','S',self.dim[1])		
		
		self.VG_N = Port(circuit,self,'e_VG_N','W',self.dim[0])
		self.VG_P = Port(circuit,self,'e_VG_P','W',self.dim[0])
		self.VC = Port(circuit,self,'e_VC','W',self.dim[0])
		
		self.VINJ_S = Port(circuit,self,'s_vinj','N',self.dim[1])	
		self.VINJ_S = Port(circuit,self,'s_gnd','N',self.dim[1])	

		# Initialize ports with given values
		portsInit = [VINJ_S,GND_S,DRAIN_PROG,DRAIN_RUN,DRAIN_BITS,D_ENABLE,PROG,RUN,VGPROG,GATE_BITS,G_ENABLE,VTUN,RUNO,VOUT,AVDD,VINJ_N,GND_N,VG_N,VG_P,VC]
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