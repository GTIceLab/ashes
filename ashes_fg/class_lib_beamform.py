from ashes_fg.asic.asic_compile import *

class DelayLinesAlgFlip(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_OUTS=None,w_Input=None,w_Drainline_Prog=None,w_Drainline_Run=None,w_DrainB=None,w_DrainEnable_Del=None,n_Prog=None,n_Run=None,n_VGPROG=None,n_GateB=None,n_GateEnable_Del=None,n_VTUN=None,n_AVDD=None,n_vinj=None,n_gnd=None,e_Din=None,e_Out=None,e_CLK=None,e_RSTBar=None,e_WTA_Vg=None,e_WTA_Prog=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'Delaylines_Flip'
		self.w_Input = Port(circuit,self,'w_Input','E',40*self.dim[0])	
		self.n_OUTS = Port(circuit,self,'n_OUTS','N',400*self.dim[1])	
		self.w_Drainline_Prog = Port(circuit,self,'w_Drainline_Prog','E',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'w_Drainline_Run','E',self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','E',8*self.dim[0])
		self.w_DrainEnable_Del = Port(circuit,self,'w_DrainEnable_Del','E',self.dim[0])
		self.n_Prog = Port(circuit,self,'n_Prog','N',self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','N',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','N',self.dim[1])
		self.n_VGRUN = Port(circuit,self,'n_VGRUN','N',self.dim[1])
		self.n_GateB = Port(circuit,self,'n_GateB','N',5*self.dim[1])
		self.n_GateEnable_Del = Port(circuit,self,'n_GateEnable_Del','N',self.dim[1])
		self.n_VTUN = Port(circuit,self,'n_VTUN','N',self.dim[1])	

		self.n_AVDD = Port(circuit,self,'n_AVDD','N',self.dim[1])
		self.n_vinj = Port(circuit,self,'n_vinj','N',self.dim[1])	
		self.n_gnd = Port(circuit,self,'n_gnd','N',self.dim[1])	

		self.e_Din = Port(circuit,self,'e_Din','W',self.dim[0])		
		self.e_WTA_out = Port(circuit,self,'e_WTA_out','W',self.dim[0])	
		self.e_CLK = Port(circuit,self,'e_CLK','W',self.dim[0])	
		self.e_RSTBar = Port(circuit,self,'e_RSTBar','W',self.dim[0])
		self.e_WTA_Vg = Port(circuit,self,'e_WTA_Vg','W',2*self.dim[0])	
		self.e_WTA_CTRL_B = Port(circuit,self,'e_WTA_CTRL_B','W',2*self.dim[0])	
		# Initialize ports with given values
		portsInit = [n_OUTS,w_Input,w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_Del,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_Del,n_VTUN,n_vinj,n_gnd,e_Din,e_Out,e_CLK,e_RSTBar,e_WTA_Vg,e_WTA_Prog]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class VMMWTAAlgFullRoute(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_AVDD=None,w_Drainline_Prog=None,w_Drainline_Run=None,w_DrainB=None,w_DrainEnable_WTA=None,n_Prog=None,n_Run=None,n_VGPROG=None,n_GateB=None,n_GateEnable_WTA=None,n_VTUN=None,RUNO=None,VOUT=None,n_vinj=None,n_gnd=None,Vmid=None,Vbias=None,Vsel_WTA=None,Vs_WTA=None,Vg_WTA=None,Prog_WTA=None,e_Din=None,e_Out=None,e_CLK=None,e_RSTBar=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim
		##self.w_Input = []

		# Define cell information
		self.name = 'VMMWTA_FullRoute'
		self.w_Drainline_Prog = Port(circuit,self,'w_Drainline_Prog','W',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'w_Drainline_Run','W',self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','W',8*self.dim[0])
		self.w_DrainEnable_WTA = Port(circuit,self,'w_DrainEnable_WTA','W',self.dim[0])
		self.n_Prog = Port(circuit,self,'n_Prog','N',self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','N',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','N',self.dim[1])
		self.n_GateB = Port(circuit,self,'n_GateB','N',9*self.dim[1])
		self.n_GateEnable_WTA = Port(circuit,self,'n_GateEnable_WTA','N',self.dim[1])
		self.n_VTUN = Port(circuit,self,'n_VTUN','N',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','N',280*self.dim[1])  
		self.n_AVDD = Port(circuit,self,'n_AVDD','N',self.dim[1])
		self.n_vinj = Port(circuit,self,'n_vinj','N',self.dim[1])	
		self.n_gnd = Port(circuit,self,'n_gnd','N',self.dim[1])	
		self.Vmid = Port(circuit,self,'Vmid','N',self.dim[1])	
		self.Vbias = Port(circuit,self,'Vbias','N',self.dim[1])
		self.Vsel_WTA = Port(circuit,self,'Vsel_WTA','N',self.dim[1])	
		self.Vs_WTA = Port(circuit,self,'Vs_WTA','N',self.dim[1])	
		self.Vg_WTA = Port(circuit,self,'Vg_WTA','N',self.dim[1])
		self.Prog_WTA = Port(circuit,self,'Prog_WTA','N',self.dim[1])
		self.e_Din = Port(circuit,self,'e_Din','E',self.dim[0])		
		self.e_Out = Port(circuit,self,'e_Out','E',self.dim[0])	
		self.e_CLK = Port(circuit,self,'e_CLK','E',self.dim[0])	
		self.e_RSTBar = Port(circuit,self,'e_RSTBar','E',self.dim[0])	

		# Initialize ports with given values
		portsInit = [w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_WTA,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_WTA,n_VTUN,RUNO,n_vinj,n_gnd,Vmid,Vbias,Vsel_WTA,Vs_WTA,Vg_WTA,Prog_WTA,e_Din,e_Out,e_CLK,e_RSTBar]
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
		self.w_Drainline_Prog = Port(circuit,self,'w_Drainline_Prog','E',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'w_Drainline_Run','E',self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','E',9*self.dim[0])
		self.w_DrainEnable_Mod = Port(circuit,self,'w_DrainEnable_Mod','E',self.dim[0])
		self.n_Prog = Port(circuit,self,'n_Prog','S',self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','S',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','S',self.dim[1])
		self.n_GateB = Port(circuit,self,'n_GateB','S',9*self.dim[1])
		self.n_GateEnable_Mod = Port(circuit,self,'n_GateEnable_Mod','S',self.dim[0])
		self.n_VTUN = Port(circuit,self,'n_VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',400*self.dim[1]) 
		self.VOUT = Port(circuit,self,'VOUT','W',280*self.dim[1]) 
		self.n_AVDD = Port(circuit,self,'n_AVDD','S',self.dim[1])
		self.e_VG_N = Port(circuit,self,'e_VG_N','W',self.dim[0])
		self.e_VG_P = Port(circuit,self,'e_VG_P','W',self.dim[0])
		self.e_VC = Port(circuit,self,'e_VC','W',self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','S',self.dim[1])	
		self.n_gnd = Port(circuit,self,'n_gnd','S',self.dim[1])			
		# Initialize ports with given values
		portsInit = [w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_Mod,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_Mod,n_VTUN,RUNO,VOUT,e_VG_N,e_VG_P,e_VC,n_vinj,n_gnd]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class ModulationAlgFlipRight(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_AVDD=None,w_Drainline_Prog=None,w_Drainline_Run=None,w_DrainB=None,w_DrainEnable_Mod=None,n_Prog=None,n_Run=None,n_VGPROG=None,n_GateB=None,n_GateEnable_Mod=None,n_VTUN=None,RUNO=None,VOUT=None,e_VG_N=None,e_VG_P=None,e_VC=None,n_vinj=None,n_gnd=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'Modulation_Flip_Right'
		self.w_Drainline_Prog = Port(circuit,self,'w_Drainline_Prog','E',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'w_Drainline_Run','E',self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','E',9*self.dim[0])
		self.w_DrainEnable_Mod = Port(circuit,self,'w_DrainEnable_Mod','E',self.dim[0])
		self.n_Prog = Port(circuit,self,'n_Prog','S',self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','S',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','S',self.dim[1])
		self.n_GateB = Port(circuit,self,'n_GateB','S',9*self.dim[1])
		self.n_GateEnable_Mod = Port(circuit,self,'n_GateEnable_Mod','S',self.dim[0])
		self.n_VTUN = Port(circuit,self,'n_VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',400*self.dim[1]) 
		self.VOUT = Port(circuit,self,'VOUT','W',280*self.dim[1]) 
		self.n_AVDD = Port(circuit,self,'n_AVDD','S',self.dim[1])
		self.e_VG_N = Port(circuit,self,'e_VG_N','W',self.dim[0])
		self.e_VG_P = Port(circuit,self,'e_VG_P','W',self.dim[0])
		self.e_VC = Port(circuit,self,'e_VC','W',self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','S',self.dim[1])	
		self.n_gnd = Port(circuit,self,'n_gnd','S',self.dim[1])			
		# Initialize ports with given values
		portsInit = [w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_Mod,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_Mod,n_VTUN,RUNO,VOUT,e_VG_N,e_VG_P,e_VC,n_vinj,n_gnd]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class ModulationAlgFlipBot(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_AVDD=None,w_Drainline_Prog=None,w_Drainline_Run=None,w_DrainB=None,w_DrainEnable_Mod=None,n_Prog=None,n_Run=None,n_VGPROG=None,n_GateB=None,n_GateEnable_Mod=None,n_VTUN=None,RUNO=None,VOUT=None,e_VG_N=None,e_VG_P=None,e_VC=None,n_vinj=None,n_gnd=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'Modulation_Flip_Bot'
		self.w_Drainline_Prog = Port(circuit,self,'w_Drainline_Prog','E',self.dim[0])
		self.w_Drainline_Run = Port(circuit,self,'w_Drainline_Run','E',self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','E',9*self.dim[0])
		self.w_DrainEnable_Mod = Port(circuit,self,'w_DrainEnable_Mod','E',self.dim[0])
		self.n_Prog = Port(circuit,self,'n_Prog','S',self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','S',self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','S',self.dim[1])
		self.n_GateB = Port(circuit,self,'n_GateB','S',9*self.dim[1])
		self.n_GateEnable_Mod = Port(circuit,self,'n_GateEnable_Mod','S',self.dim[0])
		self.n_VTUN = Port(circuit,self,'n_VTUN','S',self.dim[1])
		self.RUNO = Port(circuit,self,'RUNO','S',400*self.dim[1]) 
		self.VOUT = Port(circuit,self,'VOUT','S',280*self.dim[1]) 
		self.n_AVDD = Port(circuit,self,'n_AVDD','S',self.dim[1])
		self.e_VG_N = Port(circuit,self,'e_VG_N','W',self.dim[0])
		self.e_VG_P = Port(circuit,self,'e_VG_P','W',self.dim[0])
		self.e_VC = Port(circuit,self,'e_VC','W',self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','S',self.dim[1])	
		self.n_gnd = Port(circuit,self,'n_gnd','S',self.dim[1])			
		# Initialize ports with given values
		portsInit = [w_Drainline_Prog, w_Drainline_Run,n_AVDD,w_DrainB,w_DrainEnable_Mod,n_Prog,n_Run,n_VGPROG,n_GateB,n_GateEnable_Mod,n_VTUN,RUNO,VOUT,e_VG_N,e_VG_P,e_VC,n_vinj,n_gnd]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
