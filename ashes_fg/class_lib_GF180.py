from ashes_fg.asic.asic_compile import *

class TunnelingChargePump(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VDD_w=None,CLK_IN_w=None,GND_w=None,Vout_e=None,Vin_w=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'TunnelingChargePump'
        self.VDD_w = Port(circuit,self,'VDD_w','W',1*self.dim[0])
        self.CLK_IN_w = Port(circuit,self,'CLK_IN_w','W',1*self.dim[0])
        self.GND_w = Port(circuit,self,'GND_w','W',1*self.dim[0])
        self.Vout_e = Port(circuit,self,'Vout_e','E',1*self.dim[0])
        self.Vin_w = Port(circuit,self,'Vin_w','N',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [VDD_w,CLK_IN_w,GND_w,Vout_e,Vin_w]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class SchottkyDiode(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),GND_e=None,Anode_n=None,Cathode_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'SchottkyDiode'
        self.GND_e = Port(circuit,self,'GND_e','E',1*self.dim[0])
        self.Anode_n = Port(circuit,self,'Anode_n','N',1*self.dim[1])
        self.Cathode_s = Port(circuit,self,'Cathode_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [GND_e,Anode_n,Cathode_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)
