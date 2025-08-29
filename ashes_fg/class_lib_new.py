from ashes_fg.asic.asic_compile import *

class std_cell(StandardCell):
	def __init__(self, input, num_instances, cell_type):
		self.input = input
		self.num_instances = num_instances
		self.cell_type = cell_type

class inpad(StandardCell):
	def __init__(self,pad_number):
		self.pad_number=pad_number

class outpad(StandardCell):
	def __init__(self,input,pad_number):
		self.input=input
		self.pad_number=pad_number

class outpada(StandardCell):
	def __init__(self,input,pad_number):
		self.input=input
		self.pad_number=pad_number

class TSMC350nm_4x2_Direct(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),Vd=None,Vs=None,VINJ=None,Vg=None,GND=None,VTUN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_4x2_Direct'
		self.Vd = Port(circuit,self,'Vd','E',4*self.dim[0])
		self.Vs = Port(circuit,self,'Vs','N',2*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',2*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',2*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [Vd,Vs,VINJ,Vg,GND,VTUN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_4x2_Indirect(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),Vd_P=None,Vd_R=None,Vs=None,VINJ=None,Vsel=None,Vg=None,GND=None,VTUN=None,GND_b=None,Vs_b=None,VINJ_b=None,Vsel_b=None,Vg_b=None,VTUN_b=None,Vd_Rl=None,Vd_Pl=None):
		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim
		# Define cell information
		self.name = 'TSMC350nm_4x2_Indirect'
		self.Vd_P = Port(circuit,self,'Vd_P','E',4*self.dim[0])
		self.Vd_R = Port(circuit,self,'Vd_R','E',4*self.dim[0])
		self.Vs = Port(circuit,self,'Vs','N',2*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',2*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',2*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',2*self.dim[1])
		self.Vs_b = Port(circuit,self,'Vs_b','S',2*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',2*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.Vd_Rl = Port(circuit,self,'Vd_Rl','W',4*self.dim[0])
		self.Vd_Pl = Port(circuit,self,'Vd_Pl','W',4*self.dim[0])
		# Initialize ports with given values
		portsInit = [Vd_P,Vd_R,Vs,VINJ,Vsel,Vg,GND,VTUN,GND_b,Vs_b,VINJ_b,Vsel_b,Vg_b,VTUN_b,Vd_Rl,Vd_Pl]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1
		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_4WTA_IndirectProg(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,Iin=None,Vout=None,Vmid=None,Vbias=None,Vsel=None,Vs=None,VINJ=None,Vg=None,VTUN=None,GND=None,PROG=None,Vsel_b=None,Vs_b=None,VINJ_b=None,Vg_b=None,VTUN_b=None,GND_b=None,PROG_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_4WTA_IndirectProg'
		self.VD_P = Port(circuit,self,'VD_P','W',4*self.dim[0])
		self.Iin = Port(circuit,self,'Iin','W',4*self.dim[0])
		self.Vout = Port(circuit,self,'Vout','E',4*self.dim[0])
		self.Vmid = Port(circuit,self,'Vmid','E',1*self.dim[0])
		self.Vbias = Port(circuit,self,'Vbias','E',1*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
		self.Vs = Port(circuit,self,'Vs','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
		self.Vs_b = Port(circuit,self,'Vs_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,Iin,Vout,Vmid,Vbias,Vsel,Vs,VINJ,Vg,VTUN,GND,PROG,Vsel_b,Vs_b,VINJ_b,Vg_b,VTUN_b,GND_b,PROG_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Ampdet_NoFG(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,OUTPUT=None,VTUN=None,Vg=None,Vsel=None,VINJ=None,GND=None,VPWR=None,VTUN_b=None,Vg_b=None,Vsel_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Ampdet_NoFG'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN = Port(circuit,self,'VIN','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',1*self.dim[0])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN,OUTPUT,VTUN,Vg,Vsel,VINJ,GND,VPWR,VTUN_b,Vg_b,Vsel_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Ampdet_Strong(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Ampdet_Strong'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN = Port(circuit,self,'VIN','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',1*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN,OUTPUT,Vsel,RUN,Vg,PROG,VTUN,VINJ,GND,VPWR,Vsel_b,RUN_b,Vg_b,PROG_b,VTUN_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_C4(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,VREF=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_C4'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN = Port(circuit,self,'VIN','W',1*self.dim[0])
		self.VREF = Port(circuit,self,'VREF','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',1*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN,VREF,OUTPUT,Vsel,RUN,Vg,PROG,VTUN,VINJ,GND,VPWR,Vsel_b,RUN_b,Vg_b,PROG_b,VTUN_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_DelayBlock_3stage_new(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,VOUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,INJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,INJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_DelayBlock_3stage_new'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN = Port(circuit,self,'VIN','W',1*self.dim[0])
		self.VOUT = Port(circuit,self,'VOUT','E',3*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',12*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',6*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',12*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',6*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',6*self.dim[1])
		self.INJ = Port(circuit,self,'INJ','N',3*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',6*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',12*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',6*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',12*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',6*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',6*self.dim[1])
		self.INJ_b = Port(circuit,self,'INJ_b','S',3*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',6*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN,VOUT,Vsel,RUN,Vg,PROG,VTUN,INJ,GND,VPWR,Vsel_b,RUN_b,Vg_b,PROG_b,VTUN_b,INJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_TA2Cell_LongL_Cab(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN1_PLUS=None,VIN1_MINUS=None,VIN2_PLUS=None,VIN2_MINUS=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TA2Cell_LongL_Cab'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN1_PLUS = Port(circuit,self,'VIN1_PLUS','W',1*self.dim[0])
		self.VIN1_MINUS = Port(circuit,self,'VIN1_MINUS','W',1*self.dim[0])
		self.VIN2_PLUS = Port(circuit,self,'VIN2_PLUS','W',1*self.dim[0])
		self.VIN2_MINUS = Port(circuit,self,'VIN2_MINUS','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',2*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN1_PLUS,VIN1_MINUS,VIN2_PLUS,VIN2_MINUS,OUTPUT,Vsel,RUN,Vg,PROG,VTUN,VINJ,GND,VPWR,Vsel_b,RUN_b,Vg_b,PROG_b,VTUN_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_TA2Cell_NoFG(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN1_PLUS=None,VIN1_MINUS=None,VIN2_PLUS=None,VIN2_MINUS=None,OUTPUT=None,VTUN=None,Vg=None,Vsel=None,VINJ=None,GND=None,VPWR=None,VTUN_b=None,Vg_b=None,Vsel_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TA2Cell_NoFG'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN1_PLUS = Port(circuit,self,'VIN1_PLUS','W',1*self.dim[0])
		self.VIN1_MINUS = Port(circuit,self,'VIN1_MINUS','W',1*self.dim[0])
		self.VIN2_PLUS = Port(circuit,self,'VIN2_PLUS','W',1*self.dim[0])
		self.VIN2_MINUS = Port(circuit,self,'VIN2_MINUS','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',2*self.dim[0])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN1_PLUS,VIN1_MINUS,VIN2_PLUS,VIN2_MINUS,OUTPUT,VTUN,Vg,Vsel,VINJ,GND,VPWR,VTUN_b,Vg_b,Vsel_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_TA2Cell_Strong(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN1_PLUS=None,VIN1_MINUS=None,VIN2_PLUS=None,VIN2_MINUS=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TA2Cell_Strong'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN1_PLUS = Port(circuit,self,'VIN1_PLUS','W',1*self.dim[0])
		self.VIN1_MINUS = Port(circuit,self,'VIN1_MINUS','W',1*self.dim[0])
		self.VIN2_PLUS = Port(circuit,self,'VIN2_PLUS','W',1*self.dim[0])
		self.VIN2_MINUS = Port(circuit,self,'VIN2_MINUS','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',2*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN1_PLUS,VIN1_MINUS,VIN2_PLUS,VIN2_MINUS,OUTPUT,Vsel,RUN,Vg,PROG,VTUN,VINJ,GND,VPWR,Vsel_b,RUN_b,Vg_b,PROG_b,VTUN_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_TA2Cell_Weak(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN1_PLUS=None,VIN1_MINUS=None,VIN2_PLUS=None,VIN2_MINUS=None,OUTPUT=None,Vsel=None,RUN=None,Vg=None,PROG=None,VTUN=None,VINJ=None,GND=None,VPWR=None,Vsel_b=None,RUN_b=None,Vg_b=None,PROG_b=None,VTUN_b=None,VINJ_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TA2Cell_Weak'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN1_PLUS = Port(circuit,self,'VIN1_PLUS','W',1*self.dim[0])
		self.VIN1_MINUS = Port(circuit,self,'VIN1_MINUS','W',1*self.dim[0])
		self.VIN2_PLUS = Port(circuit,self,'VIN2_PLUS','W',1*self.dim[0])
		self.VIN2_MINUS = Port(circuit,self,'VIN2_MINUS','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',2*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN1_PLUS,VIN1_MINUS,VIN2_PLUS,VIN2_MINUS,OUTPUT,Vsel,RUN,Vg,PROG,VTUN,VINJ,GND,VPWR,Vsel_b,RUN_b,Vg_b,PROG_b,VTUN_b,VINJ_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Cab_Nfets(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),SOURCE_MED=None,GATE_MED=None,SOURCE_LARGE=None,GATE_LARGE=None,DRAIN_MED=None,DRAIN_LARGE=None,GND=None,GND_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Cab_Nfets'
		self.SOURCE_MED = Port(circuit,self,'SOURCE_MED','W',1*self.dim[0])
		self.GATE_MED = Port(circuit,self,'GATE_MED','W',1*self.dim[0])
		self.SOURCE_LARGE = Port(circuit,self,'SOURCE_LARGE','W',1*self.dim[0])
		self.GATE_LARGE = Port(circuit,self,'GATE_LARGE','W',1*self.dim[0])
		self.DRAIN_MED = Port(circuit,self,'DRAIN_MED','E',1*self.dim[0])
		self.DRAIN_LARGE = Port(circuit,self,'DRAIN_LARGE','E',1*self.dim[0])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [SOURCE_MED,GATE_MED,SOURCE_LARGE,GATE_LARGE,DRAIN_MED,DRAIN_LARGE,GND,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Cab_Pfets(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),SOURCE_MED=None,GATE_MED=None,SOURCE_LARGE=None,GATE_LARGE=None,DRAIN_MED=None,DRAIN_LARGE=None,VPWR=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Cab_Pfets'
		self.SOURCE_MED = Port(circuit,self,'SOURCE_MED','W',1*self.dim[0])
		self.GATE_MED = Port(circuit,self,'GATE_MED','W',1*self.dim[0])
		self.SOURCE_LARGE = Port(circuit,self,'SOURCE_LARGE','W',1*self.dim[0])
		self.GATE_LARGE = Port(circuit,self,'GATE_LARGE','W',1*self.dim[0])
		self.DRAIN_MED = Port(circuit,self,'DRAIN_MED','E',1*self.dim[0])
		self.DRAIN_LARGE = Port(circuit,self,'DRAIN_LARGE','E',1*self.dim[0])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [SOURCE_MED,GATE_MED,SOURCE_LARGE,GATE_LARGE,DRAIN_MED,DRAIN_LARGE,VPWR,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_TGate_2nMirror(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),IN_CM=None,SelN=None,IN_TG=None,OUT_CM=None,OUT_TG=None,VPWR=None,GND=None,VPWR_b=None,GND_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TGate_2nMirror'
		self.IN_CM = Port(circuit,self,'IN_CM','W',2*self.dim[0])
		self.SelN = Port(circuit,self,'SelN','W',1*self.dim[0])
		self.IN_TG = Port(circuit,self,'IN_TG','W',1*self.dim[0])
		self.OUT_CM = Port(circuit,self,'OUT_CM','E',2*self.dim[0])
		self.OUT_TG = Port(circuit,self,'OUT_TG','E',1*self.dim[0])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [IN_CM,SelN,IN_TG,OUT_CM,OUT_TG,VPWR,GND,VPWR_b,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Cap_Bank(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN=None,OUT=None,Vs=None,VINJ=None,Vsel=None,Vg=None,GND=None,VTUN=None,Vs_b=None,VINJ_b=None,Vsel_b=None,Vg_b=None,GND_b=None,VTUN_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Cap_Bank'
		self.VD_P = Port(circuit,self,'VD_P','W',4*self.dim[0])
		self.VIN = Port(circuit,self,'VIN','W',2*self.dim[0])
		self.OUT = Port(circuit,self,'OUT','E',2*self.dim[0])
		self.Vs = Port(circuit,self,'Vs','N',2*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.Vs_b = Port(circuit,self,'Vs_b','S',2*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN,OUT,Vs,VINJ,Vsel,Vg,GND,VTUN,Vs_b,VINJ_b,Vsel_b,Vg_b,GND_b,VTUN_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_HHNeuron(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),dummy1=None,dummy2=None,dummy3=None,dummy4=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_HHNeuron'
		self.dummy1 = Port(circuit,self,'dummy1','W',1*self.dim[0])
		self.dummy2 = Port(circuit,self,'dummy2','E',1*self.dim[0])
		self.dummy3 = Port(circuit,self,'dummy3','N',1*self.dim[1])
		self.dummy4 = Port(circuit,self,'dummy4','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [dummy1,dummy2,dummy3,dummy4]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_VMMWTA(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),Vd=None,Vout=None,VMM_Vs=None,VINJ=None,VMM_Vg=None,GND=None,VTUN=None,Ibias_Vs=None,Ibias_Vg=None,PROG=None,Vmid=None,VMM_Vs_b=None,VINJ_b=None,VMM_Vg_b=None,GND_b=None,VTUN_b=None,Ibias_Vs_b=None,Ibias_Vg_b=None,PROG_b=None,Vmid_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_VMMWTA'
		self.Vd = Port(circuit,self,'Vd','W',4*self.dim[0])
		self.Vout = Port(circuit,self,'Vout','E',4*self.dim[0])
		self.VMM_Vs = Port(circuit,self,'VMM_Vs','N',2*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.VMM_Vg = Port(circuit,self,'VMM_Vg','N',2*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',2*self.dim[1])
		self.Ibias_Vs = Port(circuit,self,'Ibias_Vs','N',1*self.dim[1])
		self.Ibias_Vg = Port(circuit,self,'Ibias_Vg','N',1*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.Vmid = Port(circuit,self,'Vmid','N',1*self.dim[1])
		self.VMM_Vs_b = Port(circuit,self,'VMM_Vs_b','S',2*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.VMM_Vg_b = Port(circuit,self,'VMM_Vg_b','S',2*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',2*self.dim[1])
		self.Ibias_Vs_b = Port(circuit,self,'Ibias_Vs_b','S',1*self.dim[1])
		self.Ibias_Vg_b = Port(circuit,self,'Ibias_Vg_b','S',1*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.Vmid_b = Port(circuit,self,'Vmid_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [Vd,Vout,VMM_Vs,VINJ,VMM_Vg,GND,VTUN,Ibias_Vs,Ibias_Vg,PROG,Vmid,VMM_Vs_b,VINJ_b,VMM_Vg_b,GND_b,VTUN_b,Ibias_Vs_b,Ibias_Vg_b,PROG_b,Vmid_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_NandPfets(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),GATE_N=None,SOURCE_N=None,GATE_P=None,SOURCE_P=None,DRAIN_N=None,DRAIN_P=None,VPWR=None,GND=None,VPWR_b=None,GND_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_NandPfets'
		self.GATE_N = Port(circuit,self,'GATE_N','W',1*self.dim[0])
		self.SOURCE_N = Port(circuit,self,'SOURCE_N','W',1*self.dim[0])
		self.GATE_P = Port(circuit,self,'GATE_P','W',1*self.dim[0])
		self.SOURCE_P = Port(circuit,self,'SOURCE_P','W',1*self.dim[0])
		self.DRAIN_N = Port(circuit,self,'DRAIN_N','E',1*self.dim[0])
		self.DRAIN_P = Port(circuit,self,'DRAIN_P','E',1*self.dim[0])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [GATE_N,SOURCE_N,GATE_P,SOURCE_P,DRAIN_N,DRAIN_P,VPWR,GND,VPWR_b,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class TSMC350nm_TA2Cell_Direct(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VIN1_PLUS=None,VIN1_MINUS=None,VIN2_PLUS=None,VIN2_MINUS=None,OUTPUT=None,VTUN=None,VG=None,Vsel=None,VINJ=None,RUN=None,PROG=None,GND=None,VPWR=None,VTUN_b=None,VG_b=None,Vsel_b=None,VINJ_b=None,RUN_b=None,PROG_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TA2Cell_Direct'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.VIN1_PLUS = Port(circuit,self,'VIN1_PLUS','W',1*self.dim[0])
		self.VIN1_MINUS = Port(circuit,self,'VIN1_MINUS','W',1*self.dim[0])
		self.VIN2_PLUS = Port(circuit,self,'VIN2_PLUS','W',1*self.dim[0])
		self.VIN2_MINUS = Port(circuit,self,'VIN2_MINUS','W',1*self.dim[0])
		self.OUTPUT = Port(circuit,self,'OUTPUT','E',2*self.dim[0])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VG = Port(circuit,self,'VG','N',1*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.RUN = Port(circuit,self,'RUN','N',1*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VG_b = Port(circuit,self,'VG_b','S',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.RUN_b = Port(circuit,self,'RUN_b','S',1*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VIN1_PLUS,VIN1_MINUS,VIN2_PLUS,VIN2_MINUS,OUTPUT,VTUN,VG,Vsel,VINJ,RUN,PROG,GND,VPWR,VTUN_b,VG_b,Vsel_b,VINJ_b,RUN_b,PROG_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		

class TSMC350nm_Amplifier9T_FGBias(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,VD_R=None,VIN_MINUS=None,VIN_PLUS=None,Vout=None,Vsel=None,VTUN=None,PROG=None,Vg=None,VINJ=None,VPWR=None,GND=None,Vsel_b=None,VTUN_b=None,PROG_b=None,Vg_b=None,VINJ_b=None,VPWR_b=None,GND_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Amplifier9T_FGBias'
		self.VD_P = Port(circuit,self,'VD_P','W',1*self.dim[0])
		self.VD_R = Port(circuit,self,'VD_R','W',1*self.dim[0])
		self.VIN_MINUS = Port(circuit,self,'VIN_MINUS','W',1*self.dim[0])
		self.VIN_PLUS = Port(circuit,self,'VIN_PLUS','W',1*self.dim[0])
		self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])
		self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,VD_R,VIN_MINUS,VIN_PLUS,Vout,Vsel,VTUN,PROG,Vg,VINJ,VPWR,GND,Vsel_b,VTUN_b,PROG_b,Vg_b,VINJ_b,VPWR_b,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Amplifier9T_FGInputs_Bias(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,Vin_PLUS=None,Vin_MINUS=None,Vout=None,VINJ=None,Vsel=None,Vg=None,VTUN=None,PROG=None,VPWR=None,GND=None,VINJ_b=None,Vsel_b=None,Vg_b=None,VTUN_b=None,PROG_b=None,VPWR_b=None,GND_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Amplifier9T_FGInputs_Bias'
		self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])
		self.Vin_PLUS = Port(circuit,self,'Vin_PLUS','W',1*self.dim[0])
		self.Vin_MINUS = Port(circuit,self,'Vin_MINUS','W',1*self.dim[0])
		self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [VD_P,Vin_PLUS,Vin_MINUS,Vout,VINJ,Vsel,Vg,VTUN,PROG,VPWR,GND,VINJ_b,Vsel_b,Vg_b,VTUN_b,PROG_b,VPWR_b,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Capacitor_400ff_x4(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),A=None,B=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Capacitor_400ff_x4'
		self.A = Port(circuit,self,'A','W',4*self.dim[0])
		self.B = Port(circuit,self,'B','E',4*self.dim[0])


		# Initialize ports with given values
		portsInit = [A,B]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_Resistors_x4(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),A=None,B=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Resistors_x4'
		self.A = Port(circuit,self,'A','W',4*self.dim[0])
		self.B = Port(circuit,self,'B','E',4*self.dim[0])


		# Initialize ports with given values
		portsInit = [A,B]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TSMC350nm_TobiElement_x4(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),A=None,B=None,GND=None,VPWR=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_TobiElement_x4'
		self.A = Port(circuit,self,'A','W',4*self.dim[0])
		self.B = Port(circuit,self,'B','E',4*self.dim[0])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [A,B,GND,VPWR,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class TSMC350nm_NeuralNetworkProgActFunc(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),I1_P=None,I1_N=None,I3_P=None,I3_N=None,V4=None,V1=None,V2=None,V3=None,VG_P=None,VG_N=None,VC=None,WTA=None,VG_PFET=None,WTA_=None,GND=None,VPWR=None,VG_P_b=None,VG_N_b=None,VC_b=None,WTA_b=None,VG_PFET_b=None,WTA__b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_NeuralNetworkProgActFunc'
		self.I1_P = Port(circuit,self,'I1_P','W',1*self.dim[0])
		self.I1_N = Port(circuit,self,'I1_N','W',1*self.dim[0])
		self.I3_P = Port(circuit,self,'I3_P','W',1*self.dim[0])
		self.I3_N = Port(circuit,self,'I3_N','W',1*self.dim[0])
		self.V4 = Port(circuit,self,'V4','E',1*self.dim[0])
		self.V1 = Port(circuit,self,'V1','E',1*self.dim[0])
		self.V2 = Port(circuit,self,'V2','E',1*self.dim[0])
		self.V3 = Port(circuit,self,'V3','E',1*self.dim[0])
		self.VG_P = Port(circuit,self,'VG_P','N',1*self.dim[1])
		self.VG_N = Port(circuit,self,'VG_N','N',1*self.dim[1])
		self.VC = Port(circuit,self,'VC','N',1*self.dim[1])
		self.WTA = Port(circuit,self,'WTA','N',1*self.dim[1])
		self.VG_PFET = Port(circuit,self,'VG_PFET','N',1*self.dim[1])
		self.WTA_ = Port(circuit,self,'WTA_','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.VG_P_b = Port(circuit,self,'VG_P_b','S',1*self.dim[1])
		self.VG_N_b = Port(circuit,self,'VG_N_b','S',1*self.dim[1])
		self.VC_b = Port(circuit,self,'VC_b','S',1*self.dim[1])
		self.WTA_b = Port(circuit,self,'WTA_b','S',1*self.dim[1])
		self.VG_PFET_b = Port(circuit,self,'VG_PFET_b','S',1*self.dim[1])
		self.WTA__b = Port(circuit,self,'WTA__b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [I1_P,I1_N,I3_P,I3_N,V4,V1,V2,V3,VG_P,VG_N,VC,WTA,VG_PFET,WTA_,GND,VPWR,VG_P_b,VG_N_b,VC_b,WTA_b,VG_PFET_b,WTA__b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class TSMC350nm_Modulation(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),I1_P=None,I1_N=None,I3_P=None,I3_N=None,V4=None,V1=None,V2=None,V3=None,VG_P=None,VG_N=None,VC=None,GND=None,VPWR=None,VG_P_b=None,VG_N_b=None,VC_b=None,GND_b=None,VPWR_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Modulation'
		self.I1_P = Port(circuit,self,'I1_P','W',1*self.dim[0])
		self.I1_N = Port(circuit,self,'I1_N','W',1*self.dim[0])
		self.I3_P = Port(circuit,self,'I3_P','W',1*self.dim[0])
		self.I3_N = Port(circuit,self,'I3_N','W',1*self.dim[0])
		self.V4 = Port(circuit,self,'V4','E',1*self.dim[0])
		self.V1 = Port(circuit,self,'V1','E',1*self.dim[0])
		self.V2 = Port(circuit,self,'V2','E',1*self.dim[0])
		self.V3 = Port(circuit,self,'V3','E',1*self.dim[0])
		self.VG_P = Port(circuit,self,'VG_P','N',1*self.dim[1])
		self.VG_N = Port(circuit,self,'VG_N','N',1*self.dim[1])
		self.VC = Port(circuit,self,'VC','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VPWR = Port(circuit,self,'VPWR','N',1*self.dim[1])
		self.VG_P_b = Port(circuit,self,'VG_P_b','S',1*self.dim[1])
		self.VG_N_b = Port(circuit,self,'VG_N_b','S',1*self.dim[1])
		self.VC_b = Port(circuit,self,'VC_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.VPWR_b = Port(circuit,self,'VPWR_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [I1_P,I1_N,I3_P,I3_N,V4,V1,V2,V3,VG_P,VG_N,VC,GND,VPWR,VG_P_b,VG_N_b,VC_b,GND_b,VPWR_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)


class TSMC350nm_Termination_bot(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),GATE=None,IREF=None,IOUT=None,GND=None,GND_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_Termination_bot'
		self.GATE = Port(circuit,self,'GATE','W',1*self.dim[0])
		self.IREF = Port(circuit,self,'IREF','W',1*self.dim[0])
		self.IOUT = Port(circuit,self,'IOUT','E',1*self.dim[0])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])


		# Initialize ports with given values
		portsInit = [GATE,IREF,IOUT,GND,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)		

class DelayLine(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),Vsel=None, Vg=None, VTUN=None, VINJ=None, PROG=None, VDD=None, GND=None, VD_P=None, V_NW=None, VD_R=None, V_SW=None, V_NE=None, V_SE=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'DelayLine'
		self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
		self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])

		self.VD_P = Port(circuit,self,'VD_P','W',4*self.dim[0])
		self.V_NW = Port(circuit,self,'V_NW','W',1*self.dim[0])
		self.VD_R = Port(circuit,self,'VD_R','W',2*self.dim[0])
		self.V_SW = Port(circuit,self,'V_SW','W',1*self.dim[0])

		self.V_NE = Port(circuit,self,'V_NE','E',1*self.dim[0])
		self.V_SE = Port(circuit,self,'V_SE','E',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [Vsel, Vg, VTUN, VINJ, PROG, VDD, GND, VD_P, V_NW, VD_R, V_SW, V_NE, V_SE]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

		
class SHblock1:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],SHblock1_ls='0',SHblock1_Ibias='3e-06',SHblock1_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.SHblock1_ls=SHblock1_ls
		self.SHblock1_Ibias=SHblock1_Ibias
		self.SHblock1_cap0_1x_cs=SHblock1_cap0_1x_cs

class switchint1:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],switchint1_ls='0',switchint1_Ibias1='3e-06',switchint1_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.switchint1_ls=switchint1_ls
		self.switchint1_Ibias1=switchint1_Ibias1
		self.switchint1_cap0_1x_cs=switchint1_cap0_1x_cs

class lpfota:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],cut_off_freq='21.7'):
		self.input=input
		self.num_instances=num_instances
		self.cut_off_freq=cut_off_freq


class hhn_debug:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],hhn_debug_ls='0',hhn_debug_fgswc_ibias='5.000D-08',hhn_debug_fgota1_ibias='2e-06',hhn_debug_fgota1_pbias='2e-06',hhn_debug_fgota1_nbias='2e-06',hhn_debug_fgota0_ibias='2e-06',hhn_debug_fgota0_pbias='2e-06',hhn_debug_fgota0_nbias='2e-06',hhn_debug_ota0_ibias='2e-06',hhn_debug_ota1_ibias='2e-06',hhn_debug_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.hhn_debug_ls=hhn_debug_ls
		self.hhn_debug_fgswc_ibias=hhn_debug_fgswc_ibias
		self.hhn_debug_fgota1_ibias=hhn_debug_fgota1_ibias
		self.hhn_debug_fgota1_pbias=hhn_debug_fgota1_pbias
		self.hhn_debug_fgota1_nbias=hhn_debug_fgota1_nbias
		self.hhn_debug_fgota0_ibias=hhn_debug_fgota0_ibias
		self.hhn_debug_fgota0_pbias=hhn_debug_fgota0_pbias
		self.hhn_debug_fgota0_nbias=hhn_debug_fgota0_nbias
		self.hhn_debug_ota0_ibias=hhn_debug_ota0_ibias
		self.hhn_debug_ota1_ibias=hhn_debug_ota1_ibias
		self.hhn_debug_cap0_1x_cs=hhn_debug_cap0_1x_cs

class HH_RG_2s:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],HH_RG_2s_ls='0',HH_RG_2s_Nafb_ibias='5.000D-08',HH_RG_2s_syn0_ibias='5.000D-08',HH_RG_2s_syn1_ibias='5.000D-08',HH_RG_2s_pfet_ibias='5.000D-08',HH_RG_2s_nmr_ibias='5.000D-08',HH_RG_2s_Na_ibias='2e-06',HH_RG_2s_Na_pbias='2e-06',HH_RG_2s_Na_nbias='2e-06',HH_RG_2s_K_ibias='2e-06',HH_RG_2s_K_pbias='2e-06',HH_RG_2s_K_nbias='2e-06',HH_RG_2s_buf_ibias='2e-06',HH_RG_2s_comp_ibias='2e-06',HH_RG_2s_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.HH_RG_2s_ls=HH_RG_2s_ls
		self.HH_RG_2s_Nafb_ibias=HH_RG_2s_Nafb_ibias
		self.HH_RG_2s_syn0_ibias=HH_RG_2s_syn0_ibias
		self.HH_RG_2s_syn1_ibias=HH_RG_2s_syn1_ibias
		self.HH_RG_2s_pfet_ibias=HH_RG_2s_pfet_ibias
		self.HH_RG_2s_nmr_ibias=HH_RG_2s_nmr_ibias
		self.HH_RG_2s_Na_ibias=HH_RG_2s_Na_ibias
		self.HH_RG_2s_Na_pbias=HH_RG_2s_Na_pbias
		self.HH_RG_2s_Na_nbias=HH_RG_2s_Na_nbias
		self.HH_RG_2s_K_ibias=HH_RG_2s_K_ibias
		self.HH_RG_2s_K_pbias=HH_RG_2s_K_pbias
		self.HH_RG_2s_K_nbias=HH_RG_2s_K_nbias
		self.HH_RG_2s_buf_ibias=HH_RG_2s_buf_ibias
		self.HH_RG_2s_comp_ibias=HH_RG_2s_comp_ibias
		self.HH_RG_2s_cap0_1x_cs=HH_RG_2s_cap0_1x_cs

class subbandArray:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],SubbandArray_ls='0',SubbandArray_FBbias='5.000D-10',SubbandArray_FBpbias='5.000D-08',SubbandArray_FBnbias='5.000D-08',SubbandArray_FFbias='5.000D-08',SubbandArray_FFpbias='5.000D-08',SubbandArray_FFnbias='5.000D-08',SubbandArray_Maxota='5.000D-08',SubbandArray_LPF='3.000D-09',SubbandArray_FFcap_1x_cs='1',SubbandArray_FBcap_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.SubbandArray_ls=SubbandArray_ls
		self.SubbandArray_FBbias=SubbandArray_FBbias
		self.SubbandArray_FBpbias=SubbandArray_FBpbias
		self.SubbandArray_FBnbias=SubbandArray_FBnbias
		self.SubbandArray_FFbias=SubbandArray_FFbias
		self.SubbandArray_FFpbias=SubbandArray_FFpbias
		self.SubbandArray_FFnbias=SubbandArray_FFnbias
		self.SubbandArray_Maxota=SubbandArray_Maxota
		self.SubbandArray_LPF=SubbandArray_LPF
		self.SubbandArray_FFcap_1x_cs=SubbandArray_FFcap_1x_cs
		self.SubbandArray_FBcap_1x_cs=SubbandArray_FBcap_1x_cs

class common_drain:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],common_drain_ls='0',common_drain_fgswc_ibias='5.000D-08'):
		self.input=input
		self.num_instances=num_instances
		self.common_drain_ls=common_drain_ls
		self.common_drain_fgswc_ibias=common_drain_fgswc_ibias

class Senseamp1:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],Senseamp1_ls='0',Senseamp1_fgota0_ibias='5e-07',Senseamp1_fgota0_pbias='2e-07',Senseamp1_fgota0_nbias='2e-07',Senseamp1_ota0_ibias='3e-06'):
		self.input=input
		self.num_instances=num_instances
		self.Senseamp1_ls=Senseamp1_ls
		self.Senseamp1_fgota0_ibias=Senseamp1_fgota0_ibias
		self.Senseamp1_fgota0_pbias=Senseamp1_fgota0_pbias
		self.Senseamp1_fgota0_nbias=Senseamp1_fgota0_nbias
		self.Senseamp1_ota0_ibias=Senseamp1_ota0_ibias

class Hyst_diff:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],Hyst_diff_ls='0',Hyst_diff_ota1_ibias='2e-06'):
		self.input=input
		self.num_instances=num_instances
		self.Hyst_diff_ls=Hyst_diff_ls
		self.Hyst_diff_ota1_ibias=Hyst_diff_ota1_ibias

class common_drain_nfet:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],common_drain_nfet_ls='0',common_drain_nfet_ibias='5.000D-08'):
		self.input=input
		self.num_instances=num_instances
		self.common_drain_nfet_ls=common_drain_nfet_ls
		self.common_drain_nfet_ibias=common_drain_nfet_ibias

class ota_buf:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],ota_buf_bias='1e-05'):
		self.input=input
		self.num_instances=num_instances
		self.ota_buf_bias=ota_buf_bias

class hhn:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],hhn_ls='0',hhn_fgswc_ibias='5.000D-08',hhn_fgota1_ibias='2e-06',hhn_fgota1_pbias='2e-06',hhn_fgota1_nbias='2e-06',hhn_fgota0_ibias='2e-06',hhn_fgota0_pbias='2e-06',hhn_fgota0_nbias='2e-06',hhn_ota0_ibias='2e-06',hhn_ota1_ibias='2e-06',hhn_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.hhn_ls=hhn_ls
		self.hhn_fgswc_ibias=hhn_fgswc_ibias
		self.hhn_fgota1_ibias=hhn_fgota1_ibias
		self.hhn_fgota1_pbias=hhn_fgota1_pbias
		self.hhn_fgota1_nbias=hhn_fgota1_nbias
		self.hhn_fgota0_ibias=hhn_fgota0_ibias
		self.hhn_fgota0_pbias=hhn_fgota0_pbias
		self.hhn_fgota0_nbias=hhn_fgota0_nbias
		self.hhn_ota0_ibias=hhn_ota0_ibias
		self.hhn_ota1_ibias=hhn_ota1_ibias
		self.hhn_cap0_1x_cs=hhn_cap0_1x_cs

class Min_detect:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],Min_detect_ls='0',Min_detect_fgswc_ibias='5.000D-08',Min_detect_ota0_ibias='2e-06'):
		self.input=input
		self.num_instances=num_instances
		self.Min_detect_ls=Min_detect_ls
		self.Min_detect_fgswc_ibias=Min_detect_fgswc_ibias
		self.Min_detect_ota0_ibias=Min_detect_ota0_ibias

class signalmult:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],signalmult_fg='1e-06',signalmult_v1p='5e-08',signalmult_v1n='5e-08'):
		self.input=input
		self.num_instances=num_instances
		self.signalmult_fg=signalmult_fg
		self.signalmult_v1p=signalmult_v1p
		self.signalmult_v1n=signalmult_v1n

class common_source:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],common_source_ls='0',common_source_ibias='5.000D-08'):
		self.input=input
		self.num_instances=num_instances
		self.common_source_ls=common_source_ls
		self.common_source_ibias=common_source_ibias

class VolDivide1:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],VolDivide1_ls='0',VolDivide1_fgota0_ibias='2e-06',VolDivide1_fgota0_pbias='2e-06',VolDivide1_fgota0_nbias='2e-06',VolDivide1_ota0_ibias='2e-06'):
		self.input=input
		self.num_instances=num_instances
		self.VolDivide1_ls=VolDivide1_ls
		self.VolDivide1_fgota0_ibias=VolDivide1_fgota0_ibias
		self.VolDivide1_fgota0_pbias=VolDivide1_fgota0_pbias
		self.VolDivide1_fgota0_nbias=VolDivide1_fgota0_nbias
		self.VolDivide1_ota0_ibias=VolDivide1_ota0_ibias

class HH_RG_3s:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],HH_RG_3s_ls='0',HH_RG_3s_Nafb_ibias='5.000D-08',HH_RG_3s_syn0_ibias='5.000D-08',HH_RG_3s_syn1_ibias='5.000D-08',HH_RG_3s_syn2_ibias='5.000D-08',HH_RG_3s_pfet_ibias='5.000D-08',HH_RG_3s_nmr_ibias='5.000D-08',HH_RG_3s_Na_ibias='2e-06',HH_RG_3s_Na_pbias='2e-06',HH_RG_3s_Na_nbias='2e-06',HH_RG_3s_K_ibias='2e-06',HH_RG_3s_K_pbias='2e-06',HH_RG_3s_K_nbias='2e-06',HH_RG_3s_buf_ibias='2e-06',HH_RG_3s_comp_ibias='2e-06',HH_RG_3s_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.HH_RG_3s_ls=HH_RG_3s_ls
		self.HH_RG_3s_Nafb_ibias=HH_RG_3s_Nafb_ibias
		self.HH_RG_3s_syn0_ibias=HH_RG_3s_syn0_ibias
		self.HH_RG_3s_syn1_ibias=HH_RG_3s_syn1_ibias
		self.HH_RG_3s_syn2_ibias=HH_RG_3s_syn2_ibias
		self.HH_RG_3s_pfet_ibias=HH_RG_3s_pfet_ibias
		self.HH_RG_3s_nmr_ibias=HH_RG_3s_nmr_ibias
		self.HH_RG_3s_Na_ibias=HH_RG_3s_Na_ibias
		self.HH_RG_3s_Na_pbias=HH_RG_3s_Na_pbias
		self.HH_RG_3s_Na_nbias=HH_RG_3s_Na_nbias
		self.HH_RG_3s_K_ibias=HH_RG_3s_K_ibias
		self.HH_RG_3s_K_pbias=HH_RG_3s_K_pbias
		self.HH_RG_3s_K_nbias=HH_RG_3s_K_nbias
		self.HH_RG_3s_buf_ibias=HH_RG_3s_buf_ibias
		self.HH_RG_3s_comp_ibias=HH_RG_3s_comp_ibias
		self.HH_RG_3s_cap0_1x_cs=HH_RG_3s_cap0_1x_cs

class switchcapint1:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],switchcapint1_Bias='3e-06',switchcapint1_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.switchcapint1_Bias=switchcapint1_Bias
		self.switchcapint1_cap0_1x_cs=switchcapint1_cap0_1x_cs

class switchAmplifier1:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],switchAmplifier1_ls='0',switchAmplifier1_ota0_ibias='3e-06',switchAmplifier1_cap0_1x_cs='1',switchAmplifier1_cap1_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.switchAmplifier1_ls=switchAmplifier1_ls
		self.switchAmplifier1_ota0_ibias=switchAmplifier1_ota0_ibias
		self.switchAmplifier1_cap0_1x_cs=switchAmplifier1_cap0_1x_cs
		self.switchAmplifier1_cap1_1x_cs=switchAmplifier1_cap1_1x_cs

class SOSLPF:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],SOSLPF_ls='0',SOSLPF_Ibias2='2e-07',SOSLPF_FG2p='1e-06',SOSLPF_FG2n='1e-06',SOSLPF_Ibias1='2e-07',SOSLPF_FG1p='1e-06',SOSLPF_FG1n='1e-06',SOSLPF_Feedback='4.000D-09',SOSLPF_Buffer='1e-06'):
		self.input=input
		self.num_instances=num_instances
		self.SOSLPF_ls=SOSLPF_ls
		self.SOSLPF_Ibias2=SOSLPF_Ibias2
		self.SOSLPF_FG2p=SOSLPF_FG2p
		self.SOSLPF_FG2n=SOSLPF_FG2n
		self.SOSLPF_Ibias1=SOSLPF_Ibias1
		self.SOSLPF_FG1p=SOSLPF_FG1p
		self.SOSLPF_FG1n=SOSLPF_FG1n
		self.SOSLPF_Feedback=SOSLPF_Feedback
		self.SOSLPF_Buffer=SOSLPF_Buffer

class Max_detect:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],Max_detect_ls='0',Max_detect_fgswc_ibias='5.000D-08',Max_detect_ota0_ibias='2e-06'):
		self.input=input
		self.num_instances=num_instances
		self.Max_detect_ls=Max_detect_ls
		self.Max_detect_fgswc_ibias=Max_detect_fgswc_ibias
		self.Max_detect_ota0_ibias=Max_detect_ota0_ibias

class MSOS02:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],MSOS02_ls='0',MSOS02_Ibias2='2e-07',MSOS02_Wbp='1e-06',MSOS02_Wbn='1e-06',MSOS02_Ibias1='2e-07',MSOS02_Wap='1e-06',MSOS02_Wan='1e-06',MSOS02_Feedback='4.000D-09',MSOS02_Buffer='3e-06'):
		self.input=input
		self.num_instances=num_instances
		self.MSOS02_ls=MSOS02_ls
		self.MSOS02_Ibias2=MSOS02_Ibias2
		self.MSOS02_Wbp=MSOS02_Wbp
		self.MSOS02_Wbn=MSOS02_Wbn
		self.MSOS02_Ibias1=MSOS02_Ibias1
		self.MSOS02_Wap=MSOS02_Wap
		self.MSOS02_Wan=MSOS02_Wan
		self.MSOS02_Feedback=MSOS02_Feedback
		self.MSOS02_Buffer=MSOS02_Buffer


class c4_sp:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],Gain_Bias='3e-06',Gain_Bias_n='1e-06',Gain_Bias_p='1e-06',Feedback_bias='3.000D-09',Feedback_bias_n='1.000D-09',Feedback_bias_p='1.000D-09',num_caps='6'):
		self.input=input
		self.num_instances=num_instances
		self.Gain_Bias=Gain_Bias
		self.Gain_Bias_n=Gain_Bias_n
		self.Gain_Bias_p=Gain_Bias_p
		self.Feedback_bias=Feedback_bias
		self.Feedback_bias_n=Feedback_bias_n
		self.Feedback_bias_p=Feedback_bias_p
		self.num_caps=num_caps

class HH_RG:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],HH_RG_ls='0',HH_RG_Nafb_ibias='5.000D-08',HH_RG_in0_ibias='5.000D-08',HH_RG_pfet_ibias='5.000D-08',HH_RG_nmr_ibias='5.000D-08',HH_RG_Na_ibias='2e-06',HH_RG_Na_pbias='2e-06',HH_RG_Na_nbias='2e-06',HH_RG_K_ibias='2e-06',HH_RG_K_pbias='2e-06',HH_RG_K_nbias='2e-06',HH_RG_buf_ibias='2e-06',HH_RG_comp_ibias='2e-06',HH_RG_cap0_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.HH_RG_ls=HH_RG_ls
		self.HH_RG_Nafb_ibias=HH_RG_Nafb_ibias
		self.HH_RG_in0_ibias=HH_RG_in0_ibias
		self.HH_RG_pfet_ibias=HH_RG_pfet_ibias
		self.HH_RG_nmr_ibias=HH_RG_nmr_ibias
		self.HH_RG_Na_ibias=HH_RG_Na_ibias
		self.HH_RG_Na_pbias=HH_RG_Na_pbias
		self.HH_RG_Na_nbias=HH_RG_Na_nbias
		self.HH_RG_K_ibias=HH_RG_K_ibias
		self.HH_RG_K_pbias=HH_RG_K_pbias
		self.HH_RG_K_nbias=HH_RG_K_nbias
		self.HH_RG_buf_ibias=HH_RG_buf_ibias
		self.HH_RG_comp_ibias=HH_RG_comp_ibias
		self.HH_RG_cap0_1x_cs=HH_RG_cap0_1x_cs

class gpio_in:
	def __init__(self):
		pass



class dc_in:
	def __init__(self,DC_value):
		self.DC_value=DC_value


class GENARB_f:
	def __init__(self,input):
		self.input=input



class meas_volt:
	def __init__(self,input):
		self.input=input



class cap:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],cap_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.cap_1x_cs=cap_1x_cs

class I_SenseAmp:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],I_SenseAmp_ls='0',I_SenseAmp_fgota0_ibias='2e-06',I_SenseAmp_fgota0_pbias='2e-06',I_SenseAmp_fgota0_nbias='2e-06',I_SenseAmp_ota0_ibias='2e-06',I_SenseAmp_cap0_1x_cs='1',I_SenseAmp_cap1_1x_cs='1'):
		self.input=input
		self.num_instances=num_instances
		self.I_SenseAmp_ls=I_SenseAmp_ls
		self.I_SenseAmp_fgota0_ibias=I_SenseAmp_fgota0_ibias
		self.I_SenseAmp_fgota0_pbias=I_SenseAmp_fgota0_pbias
		self.I_SenseAmp_fgota0_nbias=I_SenseAmp_fgota0_nbias
		self.I_SenseAmp_ota0_ibias=I_SenseAmp_ota0_ibias
		self.I_SenseAmp_cap0_1x_cs=I_SenseAmp_cap0_1x_cs
		self.I_SenseAmp_cap1_1x_cs=I_SenseAmp_cap1_1x_cs

class ota:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],ota_bias='1e-06'):
		self.input=input
		self.num_instances=num_instances
		self.ota_bias=ota_bias

class tgate2:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a']):
		self.input=input
		self.num_instances=num_instances

class pfet:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a']):
		self.input=input
		self.num_instances=num_instances

class nfet:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a']):
		self.input=input
		self.num_instances=num_instances


class mite_FG:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],mite_fg0='1.000D-07'):
		self.input=input
		self.num_instances=num_instances
		self.mite_fg0=mite_fg0

class wta_new:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],wta_new_ls='0',wta_new_wta_bias='1.000D-08',wta_new_buf_bias='2e-06'):
		self.input=input
		self.num_instances=num_instances
		self.wta_new_ls=wta_new_ls
		self.wta_new_wta_bias=wta_new_wta_bias
		self.wta_new_buf_bias=wta_new_buf_bias

class vmm12x1_wowta:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],vmm12x1_wowta_fg='0',vmm12x1_target=['1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09'],vmm12x1_offsetbias='5.000D-09'):
		self.input=input
		self.num_instances=num_instances
		self.vmm12x1_wowta_fg=vmm12x1_wowta_fg
		self.vmm12x1_target=vmm12x1_target
		self.vmm12x1_offsetbias=vmm12x1_offsetbias

class fgswitch:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],fgswitch_ls='0',fgswitch_fgswc_ibias='5.000D-08'):
		self.input=input
		self.num_instances=num_instances
		self.fgswitch_ls=fgswitch_ls
		self.fgswitch_fgswc_ibias=fgswitch_fgswc_ibias

class fgota:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],fgota_bias='1.000D-08',fgota_p_bias='1.9',fgota_n_bias='1.9',fgota_small_cap='1'):
		self.input=input
		self.num_instances=num_instances
		self.fgota_bias=fgota_bias
		self.fgota_p_bias=fgota_p_bias
		self.fgota_n_bias=fgota_n_bias
		self.fgota_small_cap=fgota_small_cap

class tgate:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a']):
		self.input=input
		self.num_instances=num_instances

class nmirror_w_bias:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],nmirror_w_bias_ls='0',nmirror_w_bias_ibias='5.000D-08'):
		self.input=input
		self.num_instances=num_instances
		self.nmirror_w_bias_ls=nmirror_w_bias_ls
		self.nmirror_w_bias_ibias=nmirror_w_bias_ibias

class ota2:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],ota2_bias='1e-06'):
		self.input=input
		self.num_instances=num_instances
		self.ota2_bias=ota2_bias

class nmirror:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a']):
		self.input=input
		self.num_instances=num_instances


class vdd:
	def __init__(self):
		pass



class output_f:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a']):
		self.input=input
		self.num_instances=num_instances

class gnd:
	def __init__(self):
		pass











class sr_1i_16o:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],output_num='16'):
		self.input=input
		self.num_instances=num_instances
		self.output_num=output_num





class delay_block:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],delay_block_ls='0',delay_block_ota0_ibias='2e-06',delay_block_ota1_ibias='2e-06'):
		self.input=input
		self.num_instances=num_instances
		self.delay_block_ls=delay_block_ls
		self.delay_block_ota0_ibias=delay_block_ota0_ibias
		self.delay_block_ota1_ibias=delay_block_ota1_ibias

class vmm_12x4:
	def __init__(self,input,num_instances='1',type='FPAA',board=['3.0', '3.0a'],vmm_12x4_ls='0',vmm_12x4_in1=[5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08],vmm_12x4_in2=[5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08],vmm_12x4_in3=[5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08],vmm_12x4_in4=[5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08]):
		self.input=input
		self.num_instances=num_instances
		self.vmm_12x4_ls=vmm_12x4_ls
		self.vmm_12x4_in1=vmm_12x4_in1
		self.vmm_12x4_in2=vmm_12x4_in2
		self.vmm_12x4_in3=vmm_12x4_in3
		self.vmm_12x4_in4=vmm_12x4_in4
	
class cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'cab1' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
	
class cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'cab2'

		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class general_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'general_cab1' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class sensor_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'sensor_cab1' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class sensor_cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'sensor_cab2' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class optimized_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'optimized_cab1' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class optimized_cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'optimized_cab2' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class PDE_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'PDE_cab1' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class NN_cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None,e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None,w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None,w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None,w_drainbit4=None,w_drainbit3=None,w_drainEN=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'NN_cab2' # this matches the gds name
		self.e_cns0 = Port(circuit,self,'e_cns0','E',1*self.dim[0])
		self.e_cns1 = Port(circuit,self,'e_cns1','E',1*self.dim[0])
		self.e_cns2 = Port(circuit,self,'e_cns2','E',1*self.dim[0])
		self.e_cns3 = Port(circuit,self,'e_cns3','E',1*self.dim[0])
		self.e_vgrun = Port(circuit,self,'e_vgrun','E',1*self.dim[0])
		self.e_vtun = Port(circuit,self,'e_vtun','E',1*self.dim[0])
		self.e_vinj = Port(circuit,self,'e_vinj','E',1*self.dim[0])
		self.e_gnd = Port(circuit,self,'e_gnd','E',1*self.dim[0])
		self.e_avdd = Port(circuit,self,'e_avdd','E',1*self.dim[0])
		self.e_drainbit2 = Port(circuit,self,'e_drainbit2','E',1*self.dim[0])
		self.e_drainbit1 = Port(circuit,self,'e_drainbit1','E',1*self.dim[0])
		self.e_drainbit0 = Port(circuit,self,'e_drainbit0','E',1*self.dim[0])
		self.e_s0 = Port(circuit,self,'e_s0','E',1*self.dim[0])
		self.e_s1 = Port(circuit,self,'e_s1','E',1*self.dim[0])
		self.e_s2 = Port(circuit,self,'e_s2','E',1*self.dim[0])
		self.e_s3 = Port(circuit,self,'e_s3','E',1*self.dim[0])
		self.e_s4 = Port(circuit,self,'e_s4','E',1*self.dim[0])
		self.e_s5 = Port(circuit,self,'e_s5','E',1*self.dim[0])
		self.e_s6 = Port(circuit,self,'e_s6','E',1*self.dim[0])
		self.e_s7 = Port(circuit,self,'e_s7','E',1*self.dim[0])
		self.e_drainbit8 = Port(circuit,self,'e_drainbit8','E',1*self.dim[0])
		self.e_drainbit7 = Port(circuit,self,'e_drainbit7','E',1*self.dim[0])
		self.e_drainbit6 = Port(circuit,self,'e_drainbit6','E',1*self.dim[0])
		self.e_drainbit5 = Port(circuit,self,'e_drainbit5','E',1*self.dim[0])
		self.e_drainbit4 = Port(circuit,self,'e_drainbit4','E',1*self.dim[0])
		self.e_drainbit3 = Port(circuit,self,'e_drainbit3','E',1*self.dim[0])
		self.e_drainEN = Port(circuit,self,'e_drainEN','E',1*self.dim[0])
		
		self.w_cns0 = Port(circuit,self,'w_cns0','W',1*self.dim[0])
		self.w_cns1 = Port(circuit,self,'w_cns1','W',1*self.dim[0])
		self.w_cns2 = Port(circuit,self,'w_cns2','W',1*self.dim[0])
		self.w_cns3 = Port(circuit,self,'w_cns3','W',1*self.dim[0])
		self.w_vgrun = Port(circuit,self,'w_vgrun','W',1*self.dim[0])
		self.w_vtun = Port(circuit,self,'w_vtun','W',1*self.dim[0])
		self.w_vinj = Port(circuit,self,'w_vinj','W',1*self.dim[0])
		self.w_gnd = Port(circuit,self,'w_gnd','W',1*self.dim[0])
		self.w_avdd = Port(circuit,self,'w_avdd','W',1*self.dim[0])
		self.w_drainbit2 = Port(circuit,self,'w_drainbit2','W',1*self.dim[0])
		self.w_drainbit1 = Port(circuit,self,'w_drainbit1','W',1*self.dim[0])
		self.w_drainbit0 = Port(circuit,self,'w_drainbit0','W',1*self.dim[0])
		self.w_s0 = Port(circuit,self,'w_s0','W',1*self.dim[0])
		self.w_s1 = Port(circuit,self,'w_s1','W',1*self.dim[0])
		self.w_s2 = Port(circuit,self,'w_s2','W',1*self.dim[0])
		self.w_s3 = Port(circuit,self,'w_s3','W',1*self.dim[0])
		self.w_s4 = Port(circuit,self,'w_s4','W',1*self.dim[0])
		self.w_s5 = Port(circuit,self,'w_s5','W',1*self.dim[0])
		self.w_s6 = Port(circuit,self,'w_s6','W',1*self.dim[0])
		self.w_s7 = Port(circuit,self,'w_s7','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class Macro(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1), cpu_en=None, dbg_en=None, dbg_uart_rxd=None, dbg_uart_txd=None, dco_clk=None, lfxt_clk=None, nmi=None, reset_n=None, scan_enable=None, scan_mode=None, wkup=None, scan_in1=None, scan_in2=None, scan_out1=None, scan_out2=None, aclk=None, aclk_en=None, dbg_freeze=None, dco_enable=None, dco_wkup=None, lfxt_enable=None, lfxt_wkup=None, mclk=None, smclk=None, smclk_en=None, DVDD=None, GND=None, AVDD_AM=None, VINJ=None, VTUN_AM=None, VTUN_fgmem=None, VGPROG_IO=None, fgmem_CS_VBIAS=None, prog=None, run=None, Signal_ADC_inp=None, Signal_DAC_out=None, ADC_Trim=None, Bias_Trim=None, Cal_IO=None, Cal_Vin=None, Debug_IO=None, I_IO=None, VD_IO=None, VGRUN=None, VG_IO=None, V_IO=None, mmio_reg_10=None, mmio_reg_in_5=None, mmio_reg_1_out=None, mmio_reg_9_out_b15=None, mmio_reg_2_out_b15=None, mmio_reg_3_vinj_out=None, mmio_reg_4_vinj_out=None, irq_acc=None, irq=None, puc_rst_dbg=None, sram_CS_VBIAS=None, peri_use_uP=None, peri_spi_rst=None, peri_spi_cpu_clk=None, peri_spi_slave_clk=None, peri_spi_slave_miso=None, peri_spi_slave_mosi=None, peri_spi_slave_cs_n=None, peri_spi_mstr_spiclk=None, peri_spi_mstr_miso=None, peri_spi_mstr_mosi=None, peri_spi_mstr_cs_n_0=None, peri_spi_mstr_cs_n_1=None, peri_spi_mstr_cs_n_2=None, peri_spi_mstr_cs_n_3=None, peri_spi_mstr_TX_Ready=None, peri_spi_mstr_RX_DV=None, peri_spi_slave_RX_DV=None, SystemDrainline=None, fast_ADC_clk=None, drain_pulse_rst=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'Full_Macro_Edit'
		
		self.cpu_en = Port(circuit,self, 'cpu_en' ,'N',1*self.dim[1])
		self.dbg_en = Port(circuit,self, 'dbg_en' ,'N',1*self.dim[1])
		self.dbg_uart_rxd = Port(circuit,self, 'dbg_uart_rxd' ,'N',1*self.dim[1])
		self.dbg_uart_txd = Port(circuit,self, 'dbg_uart_txd' ,'N',1*self.dim[1])
		self.dco_clk = Port(circuit,self, 'dco_clk' ,'N',1*self.dim[1])
		self.lfxt_clk = Port(circuit,self, 'lfxt_clk' ,'N',1*self.dim[1])
		self.nmi = Port(circuit,self, 'nmi' ,'N',1*self.dim[1])
		self.reset_n = Port(circuit,self, 'reset_n' ,'N',1*self.dim[1])
		self.scan_enable = Port(circuit,self, 'scan_enable' ,'N',1*self.dim[1])
		self.scan_mode = Port(circuit,self, 'scan_mode' ,'N',1*self.dim[1])
		self.wkup = Port(circuit,self, 'wkup' ,'N',1*self.dim[1])
		self.scan_in1 = Port(circuit,self, 'scan_in1' ,'N',1*self.dim[1])
		self.scan_in2 = Port(circuit,self, 'scan_in2' ,'N',1*self.dim[1])
		self.scan_out1 = Port(circuit,self, 'scan_out1' ,'N',1*self.dim[1])
		self.scan_out2 = Port(circuit,self, 'scan_out2' ,'N',1*self.dim[1])
		self.aclk = Port(circuit,self, 'aclk' ,'N',1*self.dim[1])
		self.aclk_en = Port(circuit,self, 'aclk_en' ,'N',1*self.dim[1])
		self.dbg_freeze = Port(circuit,self, 'dbg_freeze' ,'N',1*self.dim[1])
		self.dco_enable = Port(circuit,self, 'dco_enable' ,'N',1*self.dim[1])
		self.dco_wkup = Port(circuit,self, 'dco_wkup' ,'N',1*self.dim[1])
		self.lfxt_enable = Port(circuit,self, 'lfxt_enable' ,'N',1*self.dim[1])
		self.lfxt_wkup = Port(circuit,self, 'lfxt_wkup' ,'N',1*self.dim[1])
		self.mclk = Port(circuit,self, 'mclk' ,'N',1*self.dim[1])
		self.smclk = Port(circuit,self, 'smclk' ,'N',1*self.dim[1])
		self.smclk_en = Port(circuit,self, 'smclk_en' ,'N',1*self.dim[1])


		self.DVDD = Port(circuit,self, 'DVDD' ,'S',1*self.dim[1])
		self.GND = Port(circuit,self, 'GND' ,'S',1*self.dim[1])
		self.AVDD_AM = Port(circuit,self, 'AVDD_AM' ,'S',1*self.dim[1])
		self.VINJ = Port(circuit,self, 'VINJ' ,'S',1*self.dim[1])
		self.VTUN_AM = Port(circuit,self, 'VTUN_AM' ,'S',1*self.dim[1])
		self.VTUN_fgmem = Port(circuit,self, 'VTUN_fgmem' ,'S',1*self.dim[1])
		self.VGPROG_IO = Port(circuit,self, 'VGPROG_IO' ,'S',1*self.dim[1])
		self.fgmem_CS_VBIAS = Port(circuit,self, 'fgmem_CS_VBIAS' ,'S',1*self.dim[1])
		self.prog = Port(circuit,self, 'prog' ,'S',1*self.dim[1])
		self.run = Port(circuit,self, 'run' ,'S',1*self.dim[1])
		self.Signal_ADC_inp = Port(circuit,self, 'Signal_ADC_inp' ,'S',6*self.dim[1]) # Signal_ADC_inp[5:0]
		self.Signal_DAC_out = Port(circuit,self, 'Signal_DAC_out' ,'S',5*self.dim[1]) # Signal_DAC_out[4:0]
		self.ADC_Trim = Port(circuit,self, 'ADC_Trim' ,'S',1*self.dim[1])
		self.Bias_Trim = Port(circuit,self, 'Bias_Trim' ,'S',1*self.dim[1])
		self.Cal_IO = Port(circuit,self, 'Cal_IO' ,'S',1*self.dim[1])
		self.Cal_Vin = Port(circuit,self, 'Cal_Vin' ,'S',1*self.dim[1])
		self.Debug_IO = Port(circuit,self, 'Debug_IO' ,'S',1*self.dim[1])
		self.I_IO = Port(circuit,self, 'I_IO' ,'S',1*self.dim[1])
		self.VD_IO = Port(circuit,self, 'VD_IO' ,'S',1*self.dim[1])
		self.VGRUN = Port(circuit,self, 'VGRUN' ,'S',1*self.dim[1])
		self.VG_IO = Port(circuit,self, 'VG_IO' ,'S',1*self.dim[1])
		self.V_IO = Port(circuit,self, 'V_IO' ,'S',1*self.dim[1])
		self.mmio_reg_10 = Port(circuit,self, 'mmio_reg_10' ,'S',16*self.dim[1]) # mmio_reg_10[15:0]
		self.mmio_reg_in_5 = Port(circuit,self, 'mmio_reg_in_5' ,'S',16*self.dim[1]) # mmio_reg_in_5[15:0]
		self.mmio_reg_1_out = Port(circuit,self, 'mmio_reg_1_out' ,'S',2*self.dim[1]) # mmio_reg_1_out[1:0]
		self.mmio_reg_9_out_b15 = Port(circuit,self, 'mmio_reg_9_out_b15' ,'S',1*self.dim[1])
		self.mmio_reg_2_out_b15 = Port(circuit,self, 'mmio_reg_2_out_b15' ,'S',1*self.dim[1])
		self.mmio_reg_3_vinj_out = Port(circuit,self, 'mmio_reg_3_vinj_out' ,'S',6*self.dim[1]) # mmio_reg_3_vinj_out[15:10]
		self.mmio_reg_4_vinj_out = Port(circuit,self, 'mmio_reg_4_vinj_out' ,'S',6*self.dim[1]) # mmio_reg_4_vinj_out[5:0]
		self.irq_acc = Port(circuit,self, 'irq_acc' ,'S',14*self.dim[1]) # irq_acc[13:0]
		self.irq = Port(circuit,self, 'irq' ,'S',14*self.dim[1]) # irq[13:0]
		self.puc_rst_dbg = Port(circuit,self, 'puc_rst_dbg' ,'S',1*self.dim[1])


		self.SystemDrainline = Port(circuit,self, 'SystemDrainline' ,'E',2*self.dim[0]) # SystemDrainline[2:1]
		self.fast_ADC_clk = Port(circuit,self, 'fast_ADC_clk' ,'E',1*self.dim[0])
		self.drain_pulse_rst = Port(circuit,self, 'drain_pulse_rst' ,'E',1*self.dim[0])


		self.sram_CS_VBIAS = Port(circuit,self, 'sram_CS_VBIAS' ,'W',1*self.dim[0])
		self.peri_use_uP = Port(circuit,self, 'peri_use_uP' ,'W',1*self.dim[0])
		self.peri_spi_rst = Port(circuit,self, 'peri_spi_rst' ,'W',1*self.dim[0])
		self.peri_spi_cpu_clk = Port(circuit,self, 'peri_spi_cpu_clk' ,'W',1*self.dim[0])
		self.peri_spi_slave_clk = Port(circuit,self, 'peri_spi_slave_clk' ,'W',1*self.dim[0])
		self.peri_spi_slave_miso = Port(circuit,self, 'peri_spi_slave_miso' ,'W',1*self.dim[0])
		self.peri_spi_slave_mosi = Port(circuit,self, 'peri_spi_slave_mosi' ,'W',1*self.dim[0])
		self.peri_spi_slave_cs_n = Port(circuit,self, 'peri_spi_slave_cs_n' ,'W',1*self.dim[0])
		self.peri_spi_mstr_spiclk = Port(circuit,self, 'peri_spi_mstr_spiclk' ,'W',1*self.dim[0])
		self.peri_spi_mstr_miso = Port(circuit,self, 'peri_spi_mstr_miso' ,'W',1*self.dim[0])
		self.peri_spi_mstr_mosi = Port(circuit,self, 'peri_spi_mstr_mosi' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_0 = Port(circuit,self, 'peri_spi_mstr_cs_n_0' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_1 = Port(circuit,self, 'peri_spi_mstr_cs_n_1' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_2 = Port(circuit,self, 'peri_spi_mstr_cs_n_2' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_3 = Port(circuit,self, 'peri_spi_mstr_cs_n_3' ,'W',1*self.dim[0])
		self.peri_spi_mstr_TX_Ready = Port(circuit,self, 'peri_spi_mstr_TX_Ready' ,'W',1*self.dim[0])
		self.peri_spi_mstr_RX_DV = Port(circuit,self, 'peri_spi_mstr_RX_DV' ,'W',1*self.dim[0])
		self.peri_spi_slave_RX_DV = Port(circuit,self, 'peri_spi_slave_RX_DV' ,'W',1*self.dim[0])


		# Initialize ports with given values
		portsInit = [cpu_en,dbg_en,dbg_uart_rxd,dbg_uart_txd,dco_clk,lfxt_clk,nmi,reset_n,scan_enable,scan_mode,wkup,scan_in1,scan_in2,scan_out1,scan_out2,aclk,aclk_en,dbg_freeze,dco_enable,dco_wkup,lfxt_enable,lfxt_wkup,mclk,smclk,smclk_en,DVDD,GND,AVDD_AM,VINJ,VTUN_AM,VTUN_fgmem,VGPROG_IO,fgmem_CS_VBIAS,prog,run,Signal_ADC_inp,Signal_DAC_out,ADC_Trim,Bias_Trim,Cal_IO,Cal_Vin,Debug_IO,I_IO,VD_IO,VGRUN,VG_IO,V_IO,mmio_reg_10,mmio_reg_in_5,mmio_reg_1_out,mmio_reg_9_out_b15,mmio_reg_2_out_b15,mmio_reg_3_vinj_out,mmio_reg_4_vinj_out,irq_acc,irq,puc_rst_dbg,sram_CS_VBIAS,peri_use_uP,peri_spi_rst,peri_spi_cpu_clk,peri_spi_slave_clk,peri_spi_slave_miso,peri_spi_slave_mosi,peri_spi_slave_cs_n,peri_spi_mstr_spiclk,peri_spi_mstr_miso,peri_spi_mstr_mosi,peri_spi_mstr_cs_n_0,peri_spi_mstr_cs_n_1,peri_spi_mstr_cs_n_2,peri_spi_mstr_cs_n_3,peri_spi_mstr_TX_Ready,peri_spi_mstr_RX_DV,peri_spi_slave_RX_DV,SystemDrainline,fast_ADC_clk,drain_pulse_rst]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class ChipFrame(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),gnd_N=None, esd_vdd_N=None, avdd_N=None, VINJ_N=None, DVDD_N=None, IO_N_CLK=None, IO_N=None, gnd_S=None, esd_vdd_S=None, avdd_S=None, VINJ_S=None, DVDD_S=None, IO_S=None, IO_Bare_W=None, IO_W_RES=None, IO_W=None, gnd_W=None, esd_vdd_W=None, avdd_W=None, VINJ_W=None, DVDD_W=None, IO_Bare_E=None, IO_E_RES=None, IO_E=None, gnd_E=None, esd_vdd_E=None, avdd_E=None, VINJ_E=None, DVDD_E=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'frame_6p9mm_6p2mm_edit'
		
		self.gnd_N = Port(circuit,self, 'gnd_N' ,'N',9*self.dim[1])
		self.esd_vdd_N = Port(circuit,self, 'esd_vdd_N' ,'N',3*self.dim[1])
		self.avdd_N = Port(circuit,self, 'avdd_N' ,'N',3*self.dim[1])
		self.VINJ_N = Port(circuit,self, 'VINJ_N' ,'N',3*self.dim[1])
		self.DVDD_N = Port(circuit,self, 'DVDD_N' ,'N',3*self.dim[1])
		self.IO_N_CLK = Port(circuit,self, 'IO_N_CLK' ,'N',4*self.dim[1])
		self.IO_N = Port(circuit,self, 'IO_N' ,'N',36*self.dim[1])


		self.gnd_S = Port(circuit,self, 'gnd_S' ,'S',3*self.dim[1])
		self.esd_vdd_S = Port(circuit,self, 'esd_vdd_S' ,'S',3*self.dim[1])
		self.avdd_S = Port(circuit,self, 'avdd_S' ,'S',3*self.dim[1])
		self.VINJ_S = Port(circuit,self, 'VINJ_S' ,'S',3*self.dim[1])
		self.DVDD_S = Port(circuit,self, 'DVDD_S' ,'S',3*self.dim[1])
		self.IO_S = Port(circuit,self, 'IO_S' ,'S',46*self.dim[1])


		self.IO_Bare_E = Port(circuit,self, 'IO_Bare_E' ,'E',2*self.dim[0])
		self.gnd_E = Port(circuit,self, 'gnd_E' ,'E',3*self.dim[0])
		self.IO_E_RES = Port(circuit,self, 'IO_E_RES' ,'E',2*self.dim[0])
		self.IO_E = Port(circuit,self, 'IO_E' ,'E',43*self.dim[0])
		self.esd_vdd_E = Port(circuit,self, 'esd_vdd_E' ,'E',1*self.dim[0])
		self.avdd_E = Port(circuit,self, 'avdd_E' ,'E',1*self.dim[0])
		self.VINJ_E = Port(circuit,self, 'VINJ_E' ,'E',1*self.dim[0])
		self.DVDD_E = Port(circuit,self, 'DVDD_E' ,'E',1*self.dim[0])


		self.IO_Bare_W = Port(circuit,self, 'IO_Bare_W' ,'W',2*self.dim[0])
		self.gnd_W = Port(circuit,self, 'gnd_W' ,'W',3*self.dim[0])
		self.IO_W_RES = Port(circuit,self, 'IO_W_RES' ,'W',2*self.dim[0])
		self.IO_W = Port(circuit,self, 'IO_W' ,'W',43*self.dim[0])
		self.esd_vdd_W = Port(circuit,self, 'esd_vdd_W' ,'W',1*self.dim[0])
		self.avdd_W = Port(circuit,self, 'avdd_W' ,'W',1*self.dim[0])
		self.VINJ_W = Port(circuit,self, 'VINJ_W' ,'W',1*self.dim[0])
		self.DVDD_W = Port(circuit,self, 'DVDD_W' ,'W',1*self.dim[0])


		# Initialize ports with given values
		portsInit = [gnd_N,esd_vdd_N,avdd_N,VINJ_N,DVDD_N,IO_N_CLK,IO_N,gnd_S,esd_vdd_S,avdd_S,VINJ_S,DVDD_S,IO_S,IO_Bare_W,IO_W_RES,IO_W,gnd_W,esd_vdd_W,avdd_W,VINJ_N,DVDD_W,IO_Bare_E,IO_E_RES,IO_E,gnd_E,esd_vdd_E,avdd_E,VINJ_N,DVDD_E]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self, self.island)

class SmallPadFrame(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),gnd_N=None,esd_vdd_N=None,avdd_N=None,VINJ_N=None,DVDD_N=None,IO_N_CLK=None,IO_N=None,gnd_S=None,esd_vdd_S=None,avdd_S=None,VINJ_S=None,DVDD_S=None,IO_S=None,IO_Bare_E=None,gnd_E=None,IO_E_RES=None,IO_E=None,IO_Bare_W=None,gnd_W=None,IO_W_RES=None,IO_W=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim

		# Define cell information
		self.name = 'frame_6p9mm_2mm_edit'

		self.gnd_N = Port(circuit,self,'gnd_N','N',9*self.dim[1])
		self.esd_vdd_N = Port(circuit,self,'esd_vdd_N','N',3*self.dim[1])
		self.avdd_N = Port(circuit,self,'avdd_N','N',3*self.dim[1])
		self.VINJ_N = Port(circuit,self,'VINJ_N','N',3*self.dim[1])
		self.DVDD_N = Port(circuit,self,'DVDD_N','N',3*self.dim[1])
		self.IO_N_CLK = Port(circuit,self,'IO_N_CLK','N',4*self.dim[1])
		self.IO_N = Port(circuit,self,'IO_N','N',36*self.dim[1])

		self.gnd_S = Port(circuit,self, 'gnd_S' ,'S',3*self.dim[1])
		self.esd_vdd_S = Port(circuit,self, 'esd_vdd_S' ,'S',3*self.dim[1])
		self.avdd_S = Port(circuit,self, 'avdd_S' ,'S',3*self.dim[1])
		self.VINJ_S = Port(circuit,self, 'VINJ_S' ,'S',3*self.dim[1])
		self.DVDD_S = Port(circuit,self, 'DVDD_S' ,'S',3*self.dim[1])
		self.IO_S = Port(circuit,self, 'IO_S' ,'S',46*self.dim[1])

		self.IO_Bare_E = Port(circuit,self, 'IO_Bare_E' ,'E',2*self.dim[0])
		self.gnd_E = Port(circuit,self, 'gnd_E' ,'E',2*self.dim[0])
		self.IO_E_RES = Port(circuit,self, 'IO_E_RES' ,'E',2*self.dim[0])
		self.IO_E = Port(circuit,self, 'IO_E' ,'E',9*self.dim[0])

		self.IO_Bare_W = Port(circuit,self, 'IO_Bare_W' ,'W',2*self.dim[0])
		self.gnd_W = Port(circuit,self, 'gnd_W' ,'W',2*self.dim[0])
		self.IO_W_RES = Port(circuit,self, 'IO_W_RES' ,'W',2*self.dim[0])
		self.IO_W = Port(circuit,self, 'IO_W' ,'W',9*self.dim[0])

		# Initialize ports with given values
		portsInit = [gnd_N,esd_vdd_N,avdd_N,VINJ_N,DVDD_N,IO_N_CLK,IO_N,gnd_S,esd_vdd_S,avdd_S,VINJ_S,DVDD_S,IO_S,IO_Bare_E,gnd_E,IO_E_RES,IO_E,IO_Bare_W,gnd_W,IO_W_RES,IO_W]
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


