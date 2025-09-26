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
		
class TSMC350nm_4WTA_IndirectProg_noncab(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),VD_P=None,Iin=None,Vout=None,Vmid=None,Vbias=None,Vsel=None,Vs=None,VINJ=None,Vg=None,VTUN=None,GND=None,PROG=None,Vsel_b=None,Vs_b=None,VINJ_b=None,Vg_b=None,VTUN_b=None,GND_b=None,PROG_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_4WTA_IndirectProg_noncab'
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
	def __init__(self,circuit,island=None,dim=(1,1),Vsel=None, Vg=None, VTUN=None, VINJ=None, PROG=None, VDD=None, GND=None, VD_P=None, V_NW=None, VD_R=None, V_SW=None, V_NE=None, V_SE=None, Vsel_b=None,Vg_b=None,VTUN_b=None,VINJ_b=None,PROG_b=None,VDD_b=None,GND_b=None):

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

		self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])
		self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])
		self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])
		self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
		self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])
		self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

		# Initialize ports with given values
		portsInit = [Vsel, Vg, VTUN, VINJ, PROG, VDD, GND, VD_P, V_NW, VD_R, V_SW, V_NE, V_SE, Vsel_b,Vg_b,VTUN_b,VINJ_b,PROG_b,VDD_b,GND_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		

class AnalogBuffer(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VTUN=None,VTUN_b=None,VDD=None,VDD_b=None,GND=None,GND_b=None,VINJ=None,VINJ_b=None,Vg=None,Vg_b=None,Vd_P=None,Vsel=None,Vsel_b=None,Vin=None,Vout=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'AnalogBuffer'
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
        self.Vd_P = Port(circuit,self,'Vd_P','W',1*self.dim[1])
        self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])
        self.Vin = Port(circuit,self,'Vin','W',1*self.dim[1])
        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [VTUN,VTUN_b,VDD,VDD_b,GND,GND_b,VINJ,VINJ_b,Vg,Vg_b,Vd_P,Vsel,Vsel_b,Vin,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)
        

class TSMC350nm_VerticalScanner(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),In=None,Out=None,Din=None,VDD=None,GND=None,CLK=None,RSTBar=None,Out_b=None,Qout=None,VDD_b=None,GND_b=None,CLK_b=None,RSTBar_b=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_VerticalScanner'
		self.In = Port(circuit,self,'In','W',4*self.dim[0])
		self.Out = Port(circuit,self,'Out','N',1*self.dim[1])
		self.Din = Port(circuit,self,'Din','N',1*self.dim[1])
		self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.CLK = Port(circuit,self,'CLK','N',1*self.dim[1])
		self.RSTBar = Port(circuit,self,'RSTBar','N',1*self.dim[1])
		self.Out_b = Port(circuit,self,'Out_b','S',1*self.dim[1])
		self.Qout = Port(circuit,self,'Qout','S',1*self.dim[1])
		self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
		self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])
		self.CLK_b = Port(circuit,self,'CLK_b','S',1*self.dim[1])
		self.RSTBar_b = Port(circuit,self,'RSTBar_b','S',1*self.dim[1])



		# Initialize ports with given values
		portsInit = [In,Out,Din,VDD,GND,CLK,RSTBar,Out_b,Qout,VDD_b,GND_b,CLK_b,RSTBar_b]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
			
class TSMC350nm_CS_RingOsc(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),AVDD=None, VINJ=None, Vsel=None, Vg=None, GND=None, VTUN=None, Vd_P=None, OUT=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_CS_RingOsc'
		self.AVDD = Port(circuit,self,'AVDD','N',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
		self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
		self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
		self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
		self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
		
		self.Vd_P = Port(circuit,self,'Vd_P','W',1*self.dim[0])
		
		self.OUT = Port(circuit,self,'OUT','E',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [AVDD, VINJ, Vsel, Vg, GND, VTUN, Vd_P, OUT]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)


class Top_DelayLPF(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_Prog=None, n_Run=None, n_VGRUN=None, n_VGPROG=None, n_VTUN=None, n_AVDD=None,n_gnd=None,n_vinj=None,n_GateEnable=None,s_gnd=None, s_vinj=None,s_Drainline_Prog=None,s_Drainline_Run=None,w_GateB=None,w_DrainB=None, w_Vin=None, e_Vout=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TOP_LPF_DelayBlock'
		self.n_Prog = Port(circuit,self,'n_Prog','N',1*self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','N',1*self.dim[1])
		self.n_VGRUN = Port(circuit,self,'n_VGRUN','N',1*self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','N',1*self.dim[1])
		self.n_VTUN = Port(circuit,self,'n_VTUN','N',1*self.dim[1])
		self.n_AVDD = Port(circuit,self,'n_AVDD','N',1*self.dim[1])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[1])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[1])
		self.n_GateEnable = Port(circuit,self,'n_GateEnable','N',1*self.dim[1])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[1])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[1])
		self.s_Drainline_Prog = Port(circuit,self,'s_Drainline_Prog','S',1*self.dim[1])
		self.s_Drainline_Run = Port(circuit,self,'s_Drainline_Run','S',1*self.dim[1])
		
		self.w_GateB = Port(circuit,self,'w_GateB','W',2*self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','W',6*self.dim[0])
		self.w_Vin = Port(circuit,self,'w_Vin','W',1*self.dim[0])
		
		self.e_Vout = Port(circuit,self,'e_Vout','E',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [n_Prog, n_Run, n_VGRUN, n_VGPROG, n_VTUN, n_AVDD,n_gnd,n_vinj,n_GateEnable,s_gnd,s_vinj,s_Drainline_Prog,s_Drainline_Run,w_GateB,w_DrainB, w_Vin,e_Vout]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class Top_MeadSOS(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),n_Prog=None, n_Run=None, n_VGRUN=None, n_VGPROG=None, n_VTUN=None, n_AVDD=None,n_gnd=None,n_vinj=None,n_GateEnable=None,s_gnd=None, s_vinj=None,s_Drainline_Prog=None,w_GateB=None,w_DrainB=None, w_Vin=None, e_Vout=None, e_Vout_buf=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TOP_Filter_MeadSOS'
		self.n_Prog = Port(circuit,self,'n_Prog','N',1*self.dim[1])
		self.n_Run = Port(circuit,self,'n_Run','N',1*self.dim[1])
		self.n_VGRUN = Port(circuit,self,'n_VGRUN','N',1*self.dim[1])
		self.n_VGPROG = Port(circuit,self,'n_VGPROG','N',1*self.dim[1])
		self.n_VTUN = Port(circuit,self,'n_VTUN','N',1*self.dim[1])
		self.n_AVDD = Port(circuit,self,'n_AVDD','N',1*self.dim[1])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[1])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[1])
		self.n_GateEnable = Port(circuit,self,'n_GateEnable','N',1*self.dim[1])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[1])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[1])
		self.s_Drainline_Prog = Port(circuit,self,'s_Drainline_Prog','S',1*self.dim[1])
		
		self.w_GateB = Port(circuit,self,'w_GateB','W',2*self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','W',5*self.dim[0])
		self.w_Vin = Port(circuit,self,'w_Vin','W',1*self.dim[0])
		
		self.e_Vout = Port(circuit,self,'e_Vout','E',1*self.dim[0])
		self.e_Vout_buf = Port(circuit,self,'e_Vout_buf','E',5*self.dim[0])

		# Initialize ports with given values
		portsInit = [n_Prog, n_Run, n_VGRUN, n_VGPROG, n_VTUN, n_AVDD,n_gnd,n_vinj,n_GateEnable,s_gnd,s_vinj,s_Drainline_Prog,w_GateB,w_DrainB, w_Vin,e_Vout, e_Vout_buf]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class ALICE(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),w_Prog=None,w_Run=None,w_VGRUN=None,w_VGPROG=None,w_VTUN=None,w_AVDD=None,w_Drainline_Prog_VMM=None, w_Drainline_Run_VMM=None,w_DrainEnable=None,w_DrainEnable_VMM=None,w_DrainB=None,e_WTA_out=None,e_Din=None,e_CLK=None,e_RSTBar=None,e_WTA_Vbias=None, e_AFE_out=None,n_Vin=None,n_Vref=None,n_Drainline_Prog_AFE=None,n_Drainline_Run_AFE=None,n_GateEnable=None,n_GateEnable_VMM=None,n_GateB=None,n_vinj=None, n_gnd=None,s_vinj=None,s_gnd=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'ALICE_separate'
		self.w_Prog = Port(circuit,self,'w_Prog','W',1*self.dim[0])
		self.w_Run = Port(circuit,self,'w_Run','W',1*self.dim[0])
		self.w_VGRUN = Port(circuit,self,'w_VGRUN','W',1*self.dim[0])
		self.w_VGPROG = Port(circuit,self,'w_VGPROG','W',1*self.dim[0])
		self.w_VTUN = Port(circuit,self,'w_VTUN','W',1*self.dim[0])
		self.w_AVDD = Port(circuit,self,'w_AVDD','W',1*self.dim[0])
		self.w_Drainline_Prog_VMM = Port(circuit,self,'w_Drainline_Prog_VMM','W',1*self.dim[0])
		self.w_Drainline_Run_VMM = Port(circuit,self,'w_Drainline_Run_VMM','W',1*self.dim[0])
		self.w_DrainEnable = Port(circuit,self,'w_DrainEnable','W',1*self.dim[0])
		self.w_DrainEnable_VMM = Port(circuit,self,'w_DrainEnable_VMM','W',1*self.dim[0])
		self.w_DrainB = Port(circuit,self,'w_DrainB','W',9*self.dim[0])
		self.e_WTA_out = Port(circuit,self,'e_WTA_out','E',1*self.dim[0])
		self.e_Din = Port(circuit,self,'e_Din','E',1*self.dim[0])
		self.e_CLK = Port(circuit,self,'e_CLK','E',1*self.dim[0])
		self.e_RSTBar = Port(circuit,self,'e_RSTBar','E',1*self.dim[0])
		self.e_WTA_Vbias = Port(circuit,self,'e_WTA_Vbias','E',1*self.dim[0])
		self.e_AFE_out = Port(circuit,self,'e_AFE_out','E',1*self.dim[0])
		self.n_Vin = Port(circuit,self,'n_Vin','N',1*self.dim[1])
		self.n_Vref = Port(circuit,self,'n_Vref','N',1*self.dim[1])
		self.n_Drainline_Prog_AFE = Port(circuit,self,'n_Drainline_Prog_AFE','N',1*self.dim[1])
		self.n_Drainline_Run_AFE = Port(circuit,self,'n_Drainline_Run_AFE','N',1*self.dim[1])
		self.n_GateEnable = Port(circuit,self,'n_GateEnable','N',1*self.dim[1])
		self.n_GateEnable_VMM = Port(circuit,self,'n_GateEnable_VMM','N',1*self.dim[1])
		self.n_GateB = Port(circuit,self,'n_GateB','N',8*self.dim[1])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[1])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[1])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[1])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[1])

		# Initialize ports with given values
		portsInit = [w_Prog,w_Run,w_VGRUN,w_VGPROG,w_VTUN,w_AVDD,w_Drainline_Prog_VMM,w_Drainline_Run_VMM,w_DrainEnable,w_DrainEnable_VMMw_DrainB,e_WTA_out,e_Din,e_CLK, e_RSTBar,e_WTA_Vbias,e_AFE_out,n_Vin,n_Vref,n_Drainline_Prog_AFE,n_Drainline_Run_AFE,n_GateEnable,n_GateEnable_VMM,n_GateB,n_vinj,n_gnds_vinj,s_gnd]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
		
class TSMC350nm_LVLShift_x16(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),Vin=None,DVDD=None,GND=None,VINJ=None,OUT=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_LVLShift_x16'
		self.Vin = Port(circuit,self,'Vin','N',16*self.dim[1])
		self.DVDD = Port(circuit,self,'DVDD','W',1*self.dim[0])
		self.GND = Port(circuit,self,'GND','W',1*self.dim[0])
		self.VINJ = Port(circuit,self,'VINJ','W',1*self.dim[0])
		self.OUT = Port(circuit,self,'OUT','S',16*self.dim[1])
		
		
		# Initialize ports with given values
		portsInit = [Vin,DVDD,GND,VINJ,OUT]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
class TSMC350nm_DigBuffer_x2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),Vin=None,GND=None,VINJ=None,OUT=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TSMC350nm_DigBuffer_x2'
		self.In = Port(circuit,self,'In','N',2*self.dim[1])
		self.GND = Port(circuit,self,'GND','S',1*self.dim[1])
		self.VINJ = Port(circuit,self,'VINJ','S',1*self.dim[1])
		self.OUT = Port(circuit,self,'Out','S',2*self.dim[1])
		
		
		# Initialize ports with given values
		portsInit = [Vin,GND,VINJ,OUT]
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
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0,e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7, e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN,w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd, w_avdd,w_drainbit2,w_drainbit1,w_drainbit0,w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4, w_drainbit3,w_drainEN]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class TILE_analog(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit5=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit5=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'TILE_analog' # this matches the gds name
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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit5 = Port(circuit,self,'n_gatebit5','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit5 = Port(circuit,self,'s_gatebit5','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class sensor_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit5=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit5=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit5 = Port(circuit,self,'n_gatebit5','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit5 = Port(circuit,self,'s_gatebit5','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class sensor_cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit5=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit5=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit5 = Port(circuit,self,'n_gatebit5','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit5 = Port(circuit,self,'s_gatebit5','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class optimized_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit5=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit5=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit5 = Port(circuit,self,'n_gatebit5','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit5 = Port(circuit,self,'s_gatebit5','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class optimized_cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit5=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit5=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit5 = Port(circuit,self,'n_gatebit5','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit5 = Port(circuit,self,'s_gatebit5','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class PDE_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None, e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None,  s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

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
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class NN_cab1(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'NN_cab1' # this matches the gds name
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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
		
class NN_cab2(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1),e_cns0=None,e_cns1=None,e_cns2=None,e_cns3=None,e_vgrun=None,e_vtun=None,e_vinj=None,e_gnd=None,e_avdd=None, e_drainbit2=None,e_drainbit1=None,e_drainbit0=None,e_s0=None,e_s1=None,e_s2=None,e_s3=None,e_s4=None,e_s5=None,e_s6=None,e_s7=None,e_s8=None, e_s9=None,e_s10=None,e_s11=None,e_s12=None,e_s13=None,e_s14=None,e_s15=None,e_s16=None,e_s17=None,e_s18=None,e_s19=None, e_drainbit10=None,e_drainbit9=None,e_drainbit8=None,e_drainbit7=None,e_drainbit6=None,e_drainbit5=None,e_drainbit4=None,e_drainbit3=None,e_drainEN=None, w_cns0=None,w_cns1=None,w_cns2=None,w_cns3=None,w_vgrun=None,w_vtun=None,w_vinj=None,w_gnd=None,w_avdd=None,w_drainbit2=None,w_drainbit1=None,w_drainbit0=None, w_s0=None,w_s1=None,w_s2=None,w_s3=None,w_s4=None,w_s5=None,w_s6=None,w_s7=None,w_s8=None,w_s9=None,w_s10=None,w_s11=None,w_s12=None,w_s13=None,w_s14=None, w_s15=None,w_s16=None,w_s17=None,w_s18=None,w_s19=None,w_drainbit10=None,w_drainbit9=None,w_drainbit8=None,w_drainbit7=None,w_drainbit6=None,w_drainbit5=None, w_drainbit4=None,w_drainbit3=None,w_drainEN=None,n_gateEN=None,n_gatebit5=None,n_gatebit4=None,n_gatebit3=None,n_gatebit2=None,n_gatebit1=None,n_gatebit0=None, n_progdrain=None,n_rundrain=None,n_cew0=None,n_cew1=None,n_cew2=None,n_cew3=None,n_s0=None,n_s1=None,n_s2=None,n_s3=None,n_s4=None,n_s5=None,n_s6=None,n_s7=None, n_s8=None,n_s9=None,n_s10=None,n_s11=None,n_s12=None,n_s13=None,n_s14=None,n_s15=None,n_s16=None,n_s17=None,n_s18=None,n_s19=None,n_prog=None,n_run=None,n_vgsel=None, n_avdd=None,n_gnd=None,n_vinj=None,n_vtun=None,s_gateEN=None,s_gatebit5=None,s_gatebit4=None,s_gatebit3=None,s_gatebit2=None,s_gatebit1=None,s_gatebit0=None, s_progdrain=None,s_rundrain=None,s_cew0=None,s_cew1=None,s_cew2=None,s_cew3=None,s_s0=None,s_s1=None,s_s2=None,s_s3=None,s_s4=None,s_s5=None,s_s6=None,s_s7=None, s_s8=None,s_s9=None,s_s10=None,s_s11=None,s_s12=None,s_s13=None,s_s14=None,s_s15=None,s_s16=None,s_s17=None,s_s18=None,s_s19=None, s_prog=None,s_run=None,s_vgsel=None,s_avdd=None,s_gnd=None,s_vinj=None,s_vtun=None):

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
		self.e_s8 = Port(circuit,self,'e_s8','E',1*self.dim[0])
		self.e_s9 = Port(circuit,self,'e_s9','E',1*self.dim[0])
		self.e_s10 = Port(circuit,self,'e_s10','E',1*self.dim[0])
		self.e_s11 = Port(circuit,self,'e_s11','E',1*self.dim[0])
		self.e_s12 = Port(circuit,self,'e_s12','E',1*self.dim[0])
		self.e_s13 = Port(circuit,self,'e_s13','E',1*self.dim[0])
		self.e_s14 = Port(circuit,self,'e_s14','E',1*self.dim[0])
		self.e_s15 = Port(circuit,self,'e_s15','E',1*self.dim[0])
		self.e_s16 = Port(circuit,self,'e_s16','E',1*self.dim[0])
		self.e_s17 = Port(circuit,self,'e_s17','E',1*self.dim[0])
		self.e_s18 = Port(circuit,self,'e_s18','E',1*self.dim[0])
		self.e_s19 = Port(circuit,self,'e_s19','E',1*self.dim[0])
		self.e_drainbit10 = Port(circuit,self,'e_drainbit10','E',1*self.dim[0])
		self.e_drainbit9 = Port(circuit,self,'e_drainbit9','E',1*self.dim[0])
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
		self.w_s8 = Port(circuit,self,'w_s8','W',1*self.dim[0])
		self.w_s9 = Port(circuit,self,'w_s9','W',1*self.dim[0])
		self.w_s10 = Port(circuit,self,'w_s10','W',1*self.dim[0])
		self.w_s11 = Port(circuit,self,'w_s11','W',1*self.dim[0])
		self.w_s12 = Port(circuit,self,'w_s12','W',1*self.dim[0])
		self.w_s13 = Port(circuit,self,'w_s13','W',1*self.dim[0])
		self.w_s14 = Port(circuit,self,'w_s14','W',1*self.dim[0])
		self.w_s15 = Port(circuit,self,'w_s15','W',1*self.dim[0])
		self.w_s16 = Port(circuit,self,'w_s16','W',1*self.dim[0])
		self.w_s17 = Port(circuit,self,'w_s17','W',1*self.dim[0])
		self.w_s18 = Port(circuit,self,'w_s18','W',1*self.dim[0])
		self.w_s19 = Port(circuit,self,'w_s19','W',1*self.dim[0])
		self.w_drainbit10 = Port(circuit,self,'w_drainbit10','W',1*self.dim[0])
		self.w_drainbit9 = Port(circuit,self,'w_drainbit9','W',1*self.dim[0])
		self.w_drainbit8 = Port(circuit,self,'w_drainbit8','W',1*self.dim[0])
		self.w_drainbit7 = Port(circuit,self,'w_drainbit7','W',1*self.dim[0])
		self.w_drainbit6 = Port(circuit,self,'w_drainbit6','W',1*self.dim[0])
		self.w_drainbit5 = Port(circuit,self,'w_drainbit5','W',1*self.dim[0])
		self.w_drainbit4 = Port(circuit,self,'w_drainbit4','W',1*self.dim[0])
		self.w_drainbit3 = Port(circuit,self,'w_drainbit3','W',1*self.dim[0])
		self.w_drainEN = Port(circuit,self,'w_drainEN','W',1*self.dim[0])
		
		self.n_gateEN = Port(circuit,self,'n_gateEN','N',1*self.dim[1])
		self.n_gatebit5 = Port(circuit,self,'n_gatebit5','N',1*self.dim[1])
		self.n_gatebit4 = Port(circuit,self,'n_gatebit4','N',1*self.dim[1])
		self.n_gatebit3 = Port(circuit,self,'n_gatebit3','N',1*self.dim[1])
		self.n_gatebit2 = Port(circuit,self,'n_gatebit2','N',1*self.dim[1])
		self.n_gatebit1 = Port(circuit,self,'n_gatebit1','N',1*self.dim[1])
		self.n_gatebit0 = Port(circuit,self,'n_gatebit0','N',1*self.dim[1])
		self.n_progdrain = Port(circuit,self,'n_progdrain','N',1*self.dim[1])
		self.n_rundrain = Port(circuit,self,'n_rundrain','N',1*self.dim[1])
		self.n_cew0 = Port(circuit,self,'n_cew0','N',1*self.dim[1])
		self.n_cew1 = Port(circuit,self,'n_cew1','N',1*self.dim[1])
		self.n_cew2 = Port(circuit,self,'n_cew2','N',1*self.dim[1])
		self.n_cew3 = Port(circuit,self,'n_cew3','N',1*self.dim[1])
		self.n_s0 = Port(circuit,self,'n_s0','N',1*self.dim[0])
		self.n_s1 = Port(circuit,self,'n_s1','N',1*self.dim[0])
		self.n_s2 = Port(circuit,self,'n_s2','N',1*self.dim[0])
		self.n_s3 = Port(circuit,self,'n_s3','N',1*self.dim[0])
		self.n_s4 = Port(circuit,self,'n_s4','N',1*self.dim[0])
		self.n_s5 = Port(circuit,self,'n_s5','N',1*self.dim[0])
		self.n_s6 = Port(circuit,self,'n_s6','N',1*self.dim[0])
		self.n_s7 = Port(circuit,self,'n_s7','N',1*self.dim[0])
		self.n_s8 = Port(circuit,self,'n_s8','N',1*self.dim[0])
		self.n_s9 = Port(circuit,self,'n_s9','N',1*self.dim[0])
		self.n_s10 = Port(circuit,self,'n_s10','N',1*self.dim[0])
		self.n_s11 = Port(circuit,self,'n_s11','N',1*self.dim[0])
		self.n_s12 = Port(circuit,self,'n_s12','N',1*self.dim[0])
		self.n_s13 = Port(circuit,self,'n_s13','N',1*self.dim[0])
		self.n_s14 = Port(circuit,self,'n_s14','N',1*self.dim[0])
		self.n_s15 = Port(circuit,self,'n_s15','N',1*self.dim[0])
		self.n_s16 = Port(circuit,self,'n_s16','N',1*self.dim[0])
		self.n_s17 = Port(circuit,self,'n_s17','N',1*self.dim[0])
		self.n_s18 = Port(circuit,self,'n_s18','N',1*self.dim[0])
		self.n_s19 = Port(circuit,self,'n_s19','N',1*self.dim[0])
		self.n_prog = Port(circuit,self,'n_prog','N',1*self.dim[0])
		self.n_run = Port(circuit,self,'n_run','N',1*self.dim[0])
		self.n_vgsel = Port(circuit,self,'n_vgsel','N',1*self.dim[0])
		self.n_avdd = Port(circuit,self,'n_avdd','N',1*self.dim[0])
		self.n_gnd = Port(circuit,self,'n_gnd','N',1*self.dim[0])
		self.n_vinj = Port(circuit,self,'n_vinj','N',1*self.dim[0])
		self.n_vtun = Port(circuit,self,'n_vtun','N',1*self.dim[0])
		
		self.s_gateEN = Port(circuit,self,'s_gateEN','S',1*self.dim[1])
		self.s_gatebit5 = Port(circuit,self,'s_gatebit5','S',1*self.dim[1])
		self.s_gatebit4 = Port(circuit,self,'s_gatebit4','S',1*self.dim[1])
		self.s_gatebit3 = Port(circuit,self,'s_gatebit3','S',1*self.dim[1])
		self.s_gatebit2 = Port(circuit,self,'s_gatebit2','S',1*self.dim[1])
		self.s_gatebit1 = Port(circuit,self,'s_gatebit1','S',1*self.dim[1])
		self.s_gatebit0 = Port(circuit,self,'s_gatebit0','S',1*self.dim[1])
		self.s_progdrain = Port(circuit,self,'s_progdrain','S',1*self.dim[1])
		self.s_rundrain = Port(circuit,self,'s_rundrain','S',1*self.dim[1])
		self.s_cew0 = Port(circuit,self,'s_cew0','S',1*self.dim[1])
		self.s_cew1 = Port(circuit,self,'s_cew1','S',1*self.dim[1])
		self.s_cew2 = Port(circuit,self,'s_cew2','S',1*self.dim[1])
		self.s_cew3 = Port(circuit,self,'s_cew3','S',1*self.dim[1])
		self.s_s0 = Port(circuit,self,'s_s0','S',1*self.dim[0])
		self.s_s1 = Port(circuit,self,'s_s1','S',1*self.dim[0])
		self.s_s2 = Port(circuit,self,'s_s2','S',1*self.dim[0])
		self.s_s3 = Port(circuit,self,'s_s3','S',1*self.dim[0])
		self.s_s4 = Port(circuit,self,'s_s4','S',1*self.dim[0])
		self.s_s5 = Port(circuit,self,'s_s5','S',1*self.dim[0])
		self.s_s6 = Port(circuit,self,'s_s6','S',1*self.dim[0])
		self.s_s7 = Port(circuit,self,'s_s7','S',1*self.dim[0])
		self.s_s8 = Port(circuit,self,'s_s8','S',1*self.dim[0])
		self.s_s9 = Port(circuit,self,'s_s9','S',1*self.dim[0])
		self.s_s10 = Port(circuit,self,'s_s10','S',1*self.dim[0])
		self.s_s11 = Port(circuit,self,'s_s11','S',1*self.dim[0])
		self.s_s12 = Port(circuit,self,'s_s12','S',1*self.dim[0])
		self.s_s13 = Port(circuit,self,'s_s13','S',1*self.dim[0])
		self.s_s14 = Port(circuit,self,'s_s14','S',1*self.dim[0])
		self.s_s15 = Port(circuit,self,'s_s15','S',1*self.dim[0])
		self.s_s16 = Port(circuit,self,'s_s16','S',1*self.dim[0])
		self.s_s17 = Port(circuit,self,'s_s17','S',1*self.dim[0])
		self.s_s18 = Port(circuit,self,'s_s18','S',1*self.dim[0])
		self.s_s19 = Port(circuit,self,'s_s19','S',1*self.dim[0])
		self.s_prog = Port(circuit,self,'s_prog','S',1*self.dim[0])
		self.s_run = Port(circuit,self,'s_run','S',1*self.dim[0])
		self.s_vgsel = Port(circuit,self,'s_vgsel','S',1*self.dim[0])
		self.s_avdd = Port(circuit,self,'s_avdd','S',1*self.dim[0])
		self.s_gnd = Port(circuit,self,'s_gnd','S',1*self.dim[0])
		self.s_vinj = Port(circuit,self,'s_vinj','S',1*self.dim[0])
		self.s_vtun = Port(circuit,self,'s_vtun','S',1*self.dim[0])

		# Initialize ports with given values
		portsInit = [e_cns0,e_cns1,e_cns2,e_cns3,e_vgrun,e_vtun,e_vinj,e_gnd,e_avdd,e_drainbit2,e_drainbit1,e_drainbit0, e_s0,e_s1,e_s2,e_s3,e_s4,e_s5,e_s6,e_s7,e_s8,e_s9,e_s10,e_s11,e_s12,e_s13,e_s14,e_s15,e_s16,e_s17,e_s18,e_s19, e_drainbit10,e_drainbit9,e_drainbit8,e_drainbit7,e_drainbit6,e_drainbit5,e_drainbit4,e_drainbit3,e_drainEN, w_cns0,w_cns1,w_cns2,w_cns3,w_vgrun,w_vtun,w_vinj,w_gnd,w_avdd,w_drainbit2,w_drainbit1,w_drainbit0, w_s0,w_s1,w_s2,w_s3,w_s4,w_s5,w_s6,w_s7,w_s8,w_s9,w_s10,w_s11,w_s12,w_s13,w_s14,w_s15,w_s16,w_s17,w_s18,w_s19, w_drainbit10,w_drainbit9,w_drainbit8,w_drainbit7,w_drainbit6,w_drainbit5,w_drainbit4,w_drainbit3,w_drainEN, n_gateEN,n_gatebit5,n_gatebit4,n_gatebit3,n_gatebit2,n_gatebit1,n_gatebit0,n_progdrain,n_rundrain,n_cew0,n_cew1,n_cew2,n_cew3, n_s0,n_s1,n_s2,n_s3,n_s4,n_s5,n_s6,n_s7,n_s8,n_s9,n_s10,n_s11,n_s12,n_s13,n_s14,n_s15,n_s16,n_s17,n_s18,n_s19,n_prog,n_run,n_vgsel,n_avdd,n_gnd,n_vinj,n_vtun, s_gateEN,s_gatebit5,s_gatebit4,s_gatebit3,s_gatebit2,s_gatebit1,s_gatebit0,s_progdrain,s_rundrain,s_cew0,s_cew1,s_cew2,s_cew3, s_s0,s_s1,s_s2,s_s3,s_s4,s_s5,s_s6,s_s7,s_s8,s_s9,s_s10,s_s11,s_s12,s_s13,s_s14,s_s15,s_s16,s_s17,s_s18,s_s19,s_prog,s_run,s_vgsel,s_avdd,s_gnd,s_vinj,s_vtun]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class Macro(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1), AVDD=None, Cal_IO=None, VINJ=None, ADC_Trim=None, Bias_Trim=None, Cal_Vin=None, Debug_IO=None, I_IO=None, VD_IO=None, VGPROG=None, VGPROG_IO=None, VGRUN=None, VG_IO=None, VTUN_AM=None, V_IO=None, SystemDrainline=None, pulse_fr_drain=None, Signal_DAC_out=None, Signal_RampADC_inp=None, GND=None, VTUN_fgmem=None, DVDD=None, mmio_reg_5_vinj=None, unused_AN_MUX=None, smclk_per_ext=None, mmio_reg_9_bout=None, mmio_reg_10_bout=None, puc_rst_bout=None, per_en_bout=None, per_we_bout=None, per_din_bout=None, per_addr_bout=None, per_dout_ext=None, irq=None, prog_lv=None, PROG_HV=None, RUN_HV=None, sram_CS_VBIAS=None, peri_use_uP=None, peri_spi_cpu_clk=None, peri_spi_slave_clk=None, peri_spi_mstr_miso=None, peri_spi_slave_mosi=None, peri_spi_slave_cs_n=None, peri_spi_mstr_spiclk=None, peri_spi_slave_miso=None, peri_spi_mstr_mosi=None, peri_spi_mstr_cs_n_0=None, peri_spi_mstr_cs_n_1=None, peri_spi_mstr_cs_n_2=None, peri_spi_mstr_cs_n_3=None, mmio_reg_7_bout=None, Macro_dbg_Scan_Vout=None, Macro_dbg_Scan_CLK=None, Macro_dbg_Scan_Din=None, Macro_dbg_Scan_RST=None, dbg_freeze_bout=None, dco_enable_bout=None, dco_wkup_bout=None, lfxt_enable_bout=None, lfxt_wkup_bout=None, scan_out2_bout=None, scan_out1_bout=None, fgmem_CS_VBIAS=None, mmio_reg_in_5=None, mmio_reg_3_vinj_b0=None, lfxt_clk=None, fast_clk=None, cpu_en=None, dbg_en=None, dbg_uart_rxd=None, nmi=None, reset_n=None, scan_enable=None, dbg_uart_txd=None, scan_mode=None, wkup=None, scan_in1=None, scan_in2=None, dco_clk=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'Full_Macro_2p0'
		
		self.lfxt_clk = Port(circuit,self, 'lfxt_clk' ,'N',1*self.dim[1])
		self.fast_clk = Port(circuit,self, 'fast_clk' ,'N',1*self.dim[1])
		# self.irq = Port(circuit,self, 'irq' ,'N',2*self.dim[1]) # Combined with south listing
		self.cpu_en = Port(circuit,self, 'cpu_en' ,'N',1*self.dim[1])
		self.dbg_en = Port(circuit,self, 'dbg_en' ,'N',1*self.dim[1])
		self.dbg_uart_rxd = Port(circuit,self, 'dbg_uart_rxd' ,'N',1*self.dim[1])
		self.nmi = Port(circuit,self, 'nmi' ,'N',1*self.dim[1])
		self.reset_n = Port(circuit,self, 'reset_n' ,'N',1*self.dim[1])
		self.scan_enable = Port(circuit,self, 'scan_enable' ,'N',1*self.dim[1])
		self.dbg_uart_txd = Port(circuit,self, 'dbg_uart_txd' ,'N',1*self.dim[1])
		self.scan_mode = Port(circuit,self, 'scan_mode' ,'N',1*self.dim[1])
		self.wkup = Port(circuit,self, 'wkup' ,'N',1*self.dim[1])
		self.scan_in1 = Port(circuit,self, 'scan_in1' ,'N',1*self.dim[1])
		self.scan_in2 = Port(circuit,self, 'scan_in2' ,'N',1*self.dim[1])
		self.dco_clk = Port(circuit,self, 'dco_clk' ,'N',1*self.dim[1])


		self.AVDD = Port(circuit,self, 'AVDD' ,'S',1*self.dim[1])
		self.Cal_IO = Port(circuit,self, 'Cal_IO' ,'S',1*self.dim[1])
		self.VINJ = Port(circuit,self, 'VINJ' ,'S',1*self.dim[1])
		self.ADC_Trim = Port(circuit,self, 'ADC_Trim' ,'S',1*self.dim[1])
		self.Bias_Trim = Port(circuit,self, 'Bias_Trim' ,'S',1*self.dim[1])
		self.Cal_Vin = Port(circuit,self, 'Cal_Vin' ,'S',1*self.dim[1])
		self.Debug_IO = Port(circuit,self, 'Debug_IO' ,'S',1*self.dim[1])
		self.I_IO = Port(circuit,self, 'I_IO' ,'S',1*self.dim[1])
		self.VD_IO = Port(circuit,self, 'VD_IO' ,'S',1*self.dim[1])
		self.VGPROG = Port(circuit,self, 'VGPROG' ,'S',1*self.dim[1])
		self.VGPROG_IO = Port(circuit,self, 'VGPROG_IO' ,'S',1*self.dim[1])
		self.VGRUN = Port(circuit,self, 'VGRUN' ,'S',1*self.dim[1])
		self.VG_IO = Port(circuit,self, 'VG_IO' ,'S',1*self.dim[1])
		self.VTUN_AM = Port(circuit,self, 'VTUN_AM' ,'S',1*self.dim[1])
		self.V_IO = Port(circuit,self, 'V_IO' ,'S',1*self.dim[1])
		self.SystemDrainline = Port(circuit,self, 'SystemDrainline' ,'S',3*self.dim[1])
		self.pulse_fr_drain = Port(circuit,self, 'pulse_fr_drain' ,'S',1*self.dim[1])
		self.Signal_DAC_out = Port(circuit,self, 'Signal_DAC_out' ,'S',3*self.dim[1])
		self.Signal_RampADC_inp = Port(circuit,self, 'Signal_RampADC_inp' ,'S',6*self.dim[1])
		self.GND = Port(circuit,self, 'GND' ,'S',1*self.dim[1])
		self.VTUN_fgmem = Port(circuit,self, 'VTUN_fgmem' ,'S',1*self.dim[1])
		self.DVDD = Port(circuit,self, 'DVDD' ,'S',1*self.dim[1])
		self.mmio_reg_5_vinj = Port(circuit,self, 'mmio_reg_5_vinj' ,'S',10*self.dim[1]) # all are along the south edge
		self.unused_AN_MUX = Port(circuit,self, 'unused_AN_MUX' ,'S',1*self.dim[1])
		self.smclk_per_ext = Port(circuit,self, 'smclk_per_ext' ,'S',1*self.dim[1])
		self.mmio_reg_9_bout = Port(circuit,self, 'mmio_reg_9_bout' ,'S',16*self.dim[1])
		self.mmio_reg_10_bout = Port(circuit,self, 'mmio_reg_10_bout' ,'S',16*self.dim[1])
		self.puc_rst_bout = Port(circuit,self, 'puc_rst_bout' ,'S',1*self.dim[1])
		self.per_en_bout = Port(circuit,self, 'per_en_bout' ,'S',1*self.dim[1])
		self.per_we_bout = Port(circuit,self, 'per_we_bout' ,'S',2*self.dim[1])
		self.per_din_bout = Port(circuit,self, 'per_din_bout' ,'S',16*self.dim[1])
		self.per_addr_bout = Port(circuit,self, 'per_addr_bout' ,'S',14*self.dim[1]) # all along south edge
		self.per_dout_ext = Port(circuit,self, 'per_dout_ext' ,'S',16*self.dim[1])
		self.irq = Port(circuit,self, 'irq' ,'S',5*self.dim[1]) # combined with north listing
		self.prog_lv = Port(circuit,self, 'prog_lv' ,'S',1*self.dim[1])
		self.PROG_HV = Port(circuit,self, 'PROG_HV' ,'S',1*self.dim[1])
		self.RUN_HV = Port(circuit,self, 'RUN_HV' ,'S',1*self.dim[1])


		self.sram_CS_VBIAS = Port(circuit,self, 'sram_CS_VBIAS' ,'W',1*self.dim[0])
		self.peri_use_uP = Port(circuit,self, 'peri_use_uP' ,'W',1*self.dim[0])
		self.peri_spi_cpu_clk = Port(circuit,self, 'peri_spi_cpu_clk' ,'W',1*self.dim[0])
		self.peri_spi_slave_clk = Port(circuit,self, 'peri_spi_slave_clk' ,'W',1*self.dim[0])
		self.peri_spi_mstr_miso = Port(circuit,self, 'peri_spi_mstr_miso' ,'W',1*self.dim[0])
		self.peri_spi_slave_mosi = Port(circuit,self, 'peri_spi_slave_mosi' ,'W',1*self.dim[0])
		self.peri_spi_slave_cs_n = Port(circuit,self, 'peri_spi_slave_cs_n' ,'W',1*self.dim[0])
		self.peri_spi_mstr_spiclk = Port(circuit,self, 'peri_spi_mstr_spiclk' ,'W',1*self.dim[0])
		self.peri_spi_slave_miso = Port(circuit,self, 'peri_spi_slave_miso' ,'W',1*self.dim[0])
		self.peri_spi_mstr_mosi = Port(circuit,self, 'peri_spi_mstr_mosi' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_0 = Port(circuit,self, 'peri_spi_mstr_cs_n_0' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_1 = Port(circuit,self, 'peri_spi_mstr_cs_n_1' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_2 = Port(circuit,self, 'peri_spi_mstr_cs_n_2' ,'W',1*self.dim[0])
		self.peri_spi_mstr_cs_n_3 = Port(circuit,self, 'peri_spi_mstr_cs_n_3' ,'W',1*self.dim[0])
		self.mmio_reg_7_bout = Port(circuit,self, 'mmio_reg_7_bout' ,'W',15*self.dim[0])
		self.Macro_dbg_Scan_Vout = Port(circuit,self, 'Macro_dbg_Scan_Vout' ,'W',1*self.dim[0])
		self.Macro_dbg_Scan_CLK = Port(circuit,self, 'Macro_dbg_Scan_CLK' ,'W',1*self.dim[0])
		self.Macro_dbg_Scan_Din = Port(circuit,self, 'Macro_dbg_Scan_Din' ,'W',1*self.dim[0])
		self.Macro_dbg_Scan_RST = Port(circuit,self, 'Macro_dbg_Scan_RST' ,'W',1*self.dim[0])
		self.dbg_freeze_bout = Port(circuit,self, 'dbg_freeze_bout' ,'W',1*self.dim[0])
		self.dco_enable_bout = Port(circuit,self, 'dco_enable_bout' ,'W',1*self.dim[0])
		self.dco_wkup_bout = Port(circuit,self, 'dco_wkup_bout' ,'W',1*self.dim[0])
		self.lfxt_enable_bout = Port(circuit,self, 'lfxt_enable_bout' ,'W',1*self.dim[0])
		self.lfxt_wkup_bout = Port(circuit,self, 'lfxt_wkup_bout' ,'W',1*self.dim[0])
		self.scan_out2_bout = Port(circuit,self, 'scan_out2_bout' ,'W',1*self.dim[0])
		self.scan_out1_bout = Port(circuit,self, 'scan_out1_bout' ,'W',1*self.dim[0])
		self.fgmem_CS_VBIAS = Port(circuit,self, 'fgmem_CS_VBIAS' ,'W',1*self.dim[0])
		self.mmio_reg_in_5 = Port(circuit,self, 'mmio_reg_in_5' ,'W',16*self.dim[0])
		self.mmio_reg_3_vinj_b0 = Port(circuit,self, 'mmio_reg_3_vinj_b0' ,'W',1*self.dim[0])


		# Initialize ports with given values
		portsInit = [AVDD,Cal_IO,VINJ,ADC_Trim,Bias_Trim,Cal_Vin,Debug_IO,I_IO,VD_IO,VGPROG,VGPROG_IO,VGRUN,VG_IO,VTUN_AM,V_IO,SystemDrainline,pulse_fr_drain,Signal_DAC_out,Signal_RampADC_inp,GND,VTUN_fgmem,DVDD,mmio_reg_5_vinj,unused_AN_MUX,smclk_per_ext,mmio_reg_9_bout,mmio_reg_10_bout,puc_rst_bout,per_en_bout,per_we_bout,per_din_bout,per_addr_bout,per_addr_bout,per_dout_ext,irq,prog_lv,PROG_HV,RUN_HV,sram_CS_VBIAS,peri_use_uP,peri_spi_cpu_clk,peri_spi_slave_clk,peri_spi_mstr_miso,peri_spi_slave_mosi,peri_spi_slave_cs_n,peri_spi_mstr_spiclk,peri_spi_slave_miso,peri_spi_mstr_mosi,peri_spi_mstr_cs_n_0,peri_spi_mstr_cs_n_1,peri_spi_mstr_cs_n_2,peri_spi_mstr_cs_n_3,mmio_reg_7_bout,Macro_dbg_Scan_Vout,Macro_dbg_Scan_CLK,Macro_dbg_Scan_Din,Macro_dbg_Scan_RST,dbg_freeze_bout,dco_enable_bout,dco_wkup_bout,lfxt_enable_bout,lfxt_wkup_bout,scan_out2_bout,scan_out1_bout,fgmem_CS_VBIAS,mmio_reg_in_5,mmio_reg_3_vinj_b0,lfxt_clk,fast_clk,cpu_en,dbg_en,dbg_uart_rxd,nmi,reset_n,scan_enable,dbg_uart_txd,scan_mode,wkup,scan_in1,scan_in2,dco_clk]
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)

class Macro_test(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1), cpu_en=None, dbg_en=None, dbg_uart_rxd=None, dbg_uart_txd=None, dco_clk=None, lfxt_clk=None, nmi=None, reset_n=None, scan_enable=None, scan_mode=None, wkup=None, scan_in1=None, scan_in2=None, scan_out1=None, scan_out2=None, aclk=None, aclk_en=None, dbg_freeze=None, dco_enable=None, dco_wkup=None, lfxt_enable=None, lfxt_wkup=None, mclk=None, smclk=None, smclk_en=None, DVDD=None, GND=None, AVDD_AM=None, VINJ=None, VTUN_AM=None, VTUN_fgmem=None, VGPROG_IO=None, fgmem_CS_VBIAS=None, prog=None, run=None, Signal_ADC_inp=None, Signal_DAC_out=None, ADC_Trim=None, Bias_Trim=None, Cal_IO=None, Cal_Vin=None, Debug_IO=None, I_IO=None, VD_IO=None, VGRUN=None, VG_IO=None, V_IO=None, mmio_reg_10=None, mmio_reg_in_5=None, mmio_reg_1_out=None, mmio_reg_9_out_b15=None, mmio_reg_2_out_b15=None, mmio_reg_3_vinj_out=None, mmio_reg_4_vinj_out=None, irq_acc=None, irq=None, puc_rst_dbg=None, sram_CS_VBIAS=None, peri_use_uP=None, peri_spi_rst=None, peri_spi_cpu_clk=None, peri_spi_slave_clk=None, peri_spi_slave_miso=None, peri_spi_slave_mosi=None, peri_spi_slave_cs_n=None, peri_spi_mstr_spiclk=None, peri_spi_mstr_miso=None, peri_spi_mstr_mosi=None, peri_spi_mstr_cs_n_0=None, peri_spi_mstr_cs_n_1=None, peri_spi_mstr_cs_n_2=None, peri_spi_mstr_cs_n_3=None, peri_spi_mstr_TX_Ready=None, peri_spi_mstr_RX_DV=None, peri_spi_slave_RX_DV=None, SystemDrainline=None, fast_ADC_clk=None, drain_pulse_rst=None):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'Full_Macro_Edit'
		#self.name = 'Full_Macro_Corner'
		
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
		
		'''		self.mmio_reg_3_vinj_out = Port(circuit,self, 'mmio_reg_3_vinj_out' ,'S',1*self.dim[1]) # mmio_reg_3_vinj_out[15:10]
		self.mmio_reg_3_vinj_out = Port(circuit,self, 'mmio_reg_3_vinj_out' ,'S',1*self.dim[1]) # mmio_reg_3_vinj_out[15:10]
		self.mmio_reg_3_vinj_out = Port(circuit,self, 'mmio_reg_3_vinj_out' ,'S',1*self.dim[1]) # mmio_reg_3_vinj_out[15:10]
		self.mmio_reg_3_vinj_out = Port(circuit,self, 'mmio_reg_3_vinj_out' ,'S',1*self.dim[1]) # mmio_reg_3_vinj_out[15:10]
		self.mmio_reg_3_vinj_out = Port(circuit,self, 'mmio_reg_3_vinj_out' ,'S',1*self.dim[1]) # mmio_reg_3_vinj_out[15:10]	'''							
		
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

class FakeCellGateDecoder(StandardCell):
	def __init__(self,circuit,island=None,dim=(1,1)):

		# Define variables
		self.circuit = circuit
		self.pins = []
		self.ports = []
		self.island = island
		self.dim = dim


		# Define cell information
		self.name = 'FakeCellGateDecoder'

		# Initialize ports with given values
		portsInit = []
		i=0
		for p in self.ports:
			self.assignPort(p,portsInit[i])
			i+=1

		# Add cell to circuit
		circuit.addInstance(self,self.island)
