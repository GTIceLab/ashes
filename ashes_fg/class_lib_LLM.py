from ashes_fg.asic.asic_compile import *
class dotproduct_L(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,out1=None,out2=None,Q=None,K=None,GND=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'dotproduct_L'
        self.phi1 = Port(circuit,self,'phi1','N',1*self.dim[1])
        self.phi2 = Port(circuit,self,'phi2','N',1*self.dim[1])
        self.out1 = Port(circuit,self,'out1','N',1*self.dim[1])
        self.out2 = Port(circuit,self,'out2','N',1*self.dim[1])
        self.Q = Port(circuit,self,'Q','W',4*self.dim[1])
        self.K = Port(circuit,self,'K','E',4*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,out1,out2,Q,K,GND]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)

class dotproduct_R(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,out1=None,out2=None,Q=None,K=None,GND=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'dotproduct_R'
        self.phi1 = Port(circuit,self,'phi1','N',1*self.dim[1])
        self.phi2 = Port(circuit,self,'phi2','N',1*self.dim[1])
        self.out1 = Port(circuit,self,'out1','N',1*self.dim[1])
        self.out2 = Port(circuit,self,'out2','N',1*self.dim[1])
        self.Q = Port(circuit,self,'Q','W',4*self.dim[1])
        self.K = Port(circuit,self,'K','E',4*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,out1,out2,Q,K,GND]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)

class dotproduct_mid(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,out1=None,out2=None,Q=None,K=None,GND=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'dotproduct_mid'
        self.phi1 = Port(circuit,self,'phi1','N',1*self.dim[1])
        self.phi2 = Port(circuit,self,'phi2','N',1*self.dim[1])
        self.out1 = Port(circuit,self,'out1','N',1*self.dim[1])
        self.out2 = Port(circuit,self,'out2','N',1*self.dim[1])
        self.Q = Port(circuit,self,'Q','W',4*self.dim[1])
        self.K = Port(circuit,self,'K','E',4*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,out1,out2,Q,K,GND]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)



class K_layer_output(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),K=None,GND=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'K_layer_output'
        self.K = Port(circuit,self,'K','E',4*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [K,GND]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)