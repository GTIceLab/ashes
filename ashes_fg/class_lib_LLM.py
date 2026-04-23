from ashes_fg.asic.asic_compile import *

class dotproduct_L(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,out1=None,out2=None,Q=None,K=None,GND=None,phi1_B=None,phi2_B=None,GND_B=None):
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
        self.Q = Port(circuit,self,'Q','W',4*self.dim[0])
        self.K = Port(circuit,self,'K','E',4*self.dim[0])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.phi1_B = Port(circuit,self,'phi1_B','S',1*self.dim[1])
        self.phi2_B = Port(circuit,self,'phi2_B','S',1*self.dim[1])
        self.GND_B = Port(circuit,self,'GND_B','S',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,out1,out2,Q,K,GND,phi1_B,phi2_B,GND_B]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)

class dotproduct_R(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,out1=None,out2=None,Q=None,K=None,GND=None,phi1_B=None,phi2_B=None,GND_B=None):
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
        self.Q = Port(circuit,self,'Q','W',4*self.dim[0])
        self.K = Port(circuit,self,'K','E',4*self.dim[0])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.phi1_B = Port(circuit,self,'phi1_B','S',1*self.dim[1])
        self.phi2_B = Port(circuit,self,'phi2_B','S',1*self.dim[1])
        self.GND_B = Port(circuit,self,'GND_B','S',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,out1,out2,Q,K,GND,phi1_B,phi2_B,GND_B]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)

class dotproduct_mid(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,out1=None,out2=None,Q=None,K=None,GND=None,phi1_B=None,phi2_B=None,GND_B=None):
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
        self.Q = Port(circuit,self,'Q','W',4*self.dim[0])
        self.K = Port(circuit,self,'K','E',4*self.dim[0])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.phi1_B = Port(circuit,self,'phi1_B','S',1*self.dim[1])
        self.phi2_B = Port(circuit,self,'phi2_B','S',1*self.dim[1])
        self.GND_B = Port(circuit,self,'GND_B','S',1*self.dim[1])

        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,out1,out2,Q,K,GND,phi1_B,phi2_B,GND_B]
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
        self.K = Port(circuit,self,'K','E',4*self.dim[0])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [K,GND]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)
        
class Q_layer_output(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VPWR=None,Vdbias=None,Vbias=None,Vgbias=None,Q_in=None,Q_out=None,GND=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'Q_layer_output'
        self.VPWR = Port(circuit,self,'VPWR','N',2*self.dim[1])
        self.Vdbias = Port(circuit,self,'Vdbias','N',2*self.dim[1])
        self.Vbias = Port(circuit,self,'Vbias','N',2*self.dim[1])
        self.Vgbias = Port(circuit,self,'Vgbias','N',1*self.dim[1])
        self.Q_in = Port(circuit,self,'Q_in','W',4*self.dim[0])
        self.Q_out = Port(circuit,self,'Q_out','E',4*self.dim[0])
        self.GND = Port(circuit,self,'GND','N',2*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [VPWR,Vdbias,Vbias,Vgbias,Q_in,Q_out,GND]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
            
        # Add cell to circuit
        circuit.addInstance(self,self.island)
        
class SampleControl(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),phi1=None,phi2=None,GND=None,VDD=None,Sample=None,D=None,CLK=None,Q=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'SampleControl'
        self.phi1 = Port(circuit,self,'phi1','N',1*self.dim[1])
        self.phi2 = Port(circuit,self,'phi2','N',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.VDD = Port(circuit,self,'VDD','W',1*self.dim[0])
        self.Sample = Port(circuit,self,'Sample','W',1*self.dim[0])
        self.D = Port(circuit,self,'D','W',1*self.dim[0])
        self.CLK = Port(circuit,self,'CLK','W',1*self.dim[0])
        self.Q = Port(circuit,self,'Q','E',1*self.dim[0])
        
        
        
        # Initialize ports with given values
        portsInit = [phi1,phi2,GND,VDD,Sample,D,CLK,Q]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
            
        # Add cell to circuit
        circuit.addInstance(self,self.island)

class HorizontalScanner(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),RSTBar=None,CLK=None,VSS=None,VDD=None,Din=None,Qout=None,Out=None,In=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        
        # Define cell information
        self.name = 'TSMC350nm_HorizontalScanner'
        self.RSTBar = Port(circuit,self,'RSTBar','E',1*self.dim[0])
        self.CLK = Port(circuit,self,'CLK','E',1*self.dim[0])
        self.VSS = Port(circuit,self,'VSS','W',1*self.dim[0])
        self.VDD = Port(circuit,self,'VDD','E',1*self.dim[0])
        self.Din = Port(circuit,self,'Din','E',1*self.dim[0])
        self.Qout = Port(circuit,self,'Qout','W',1*self.dim[0])
        self.Out = Port(circuit,self,'Out','W',1*self.dim[0])
        self.In = Port(circuit,self,'In','S',4*self.dim[1])
        
        
        
        # Initialize ports with given values
        portsInit = [RSTBar,CLK,VSS,VDD,Din,Qout,Out,In]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1
            
        # Add cell to circuit
        circuit.addInstance(self,self.island)
