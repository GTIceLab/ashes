class IndirectVMM_4x2(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vsel_w=None,Vs_w=None,Vg_w=None,VTUN_w=None,GND_w=None,Vd_R_n=None,Vd_P_n=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_4x2'
        self.Vsel_w = Port(circuit,self,'Vsel_w','W',2*self.dim[0])
        self.Vs_w = Port(circuit,self,'Vs_w','W',2*self.dim[0])
        self.Vg_w = Port(circuit,self,'Vg_w','W',2*self.dim[0])
        self.VTUN_w = Port(circuit,self,'VTUN_w','W',1*self.dim[0])
        self.GND_w = Port(circuit,self,'GND_w','W',1*self.dim[0])
        self.Vd_R_n = Port(circuit,self,'Vd_R_n','N',4*self.dim[1])
        self.Vd_P_n = Port(circuit,self,'Vd_P_n','N',4*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vsel_w,Vs_w,Vg_w,VTUN_w,GND_w,Vd_R_n,Vd_P_n]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_4x2_TAP(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),GND_w=None,VTUN_w=None,Vg_w=None,Vs_w=None,Vsel_w=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_4x2_TAP'
        self.GND_w = Port(circuit,self,'GND_w','E',1*self.dim[0])
        self.VTUN_w = Port(circuit,self,'VTUN_w','E',1*self.dim[0])
        self.Vg_w = Port(circuit,self,'Vg_w','E',2*self.dim[0])
        self.Vs_w = Port(circuit,self,'Vs_w','E',2*self.dim[0])
        self.Vsel_w = Port(circuit,self,'Vsel_w','N',2*self.dim[1])

        # Initialize ports with given values
        portsInit = [GND_w,VTUN_w,Vg_w,Vs_w,Vsel_w]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class SWC_Drain(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Drainline_Direct_w=None,PROG_w=None,RUN_w=None,Drainline_Indirect_s=None,SelN_s=None,Vd_R_n=None,Vd_P_n=None,Sel_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'SWC_Drain'
        self.Drainline_Direct_w = Port(circuit,self,'Drainline_Direct_w','W',1*self.dim[0])
        self.PROG_w = Port(circuit,self,'PROG_w','W',1*self.dim[0])
        self.RUN_w = Port(circuit,self,'RUN_w','W',1*self.dim[0])
        self.Drainline_Indirect_s = Port(circuit,self,'Drainline_Indirect_s','S',1*self.dim[1])
        self.SelN_s = Port(circuit,self,'SelN_s','S',4*self.dim[1])
        self.Vd_R_n = Port(circuit,self,'Vd_R_n','N',4*self.dim[1])
        self.Vd_P_n = Port(circuit,self,'Vd_P_n','N',4*self.dim[1])
        self.Sel_s = Port(circuit,self,'Sel_s','S',4*self.dim[1])

        # Initialize ports with given values
        portsInit = [Drainline_Direct_w,PROG_w,RUN_w,Drainline_Indirect_s,SelN_s,Vd_R_n,Vd_P_n,Sel_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class SWC_Gate(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VG_RUN_w=None,SELN_w=None,SEL_w=None,GND_e=None,VG_e=None,VINJ_w=None,RUN_n=None,VGPROG_n=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'SWC_Gate'
        self.VG_RUN_w = Port(circuit,self,'VG_RUN_w','W',2*self.dim[0])
        self.SELN_w = Port(circuit,self,'SELN_w','W',2*self.dim[0])
        self.SEL_w = Port(circuit,self,'SEL_w','W',2*self.dim[0])
        self.GND_e = Port(circuit,self,'GND_e','E',1*self.dim[0])
        self.VG_e = Port(circuit,self,'VG_e','E',2*self.dim[0])
        self.VINJ_w = Port(circuit,self,'VINJ_w','W',1*self.dim[0])
        self.RUN_n = Port(circuit,self,'RUN_n','N',1*self.dim[1])
        self.VGPROG_n = Port(circuit,self,'VGPROG_n','N',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [VG_RUN_w,SELN_w,SEL_w,GND_e,VG_e,VINJ_w,RUN_n,VGPROG_n]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)
