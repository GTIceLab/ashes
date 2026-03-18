class Cap_Bank(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vd_P_w=None,OUT_e=None,GND_n=None,Vg_n=None,VINJ_n=None,VIN_n=None,Vsel_n=None,VTUN_n=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'Cap_Bank'
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.OUT_e = Port(circuit,self,'OUT_e','E',1*self.dim[0])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.VIN_n = Port(circuit,self,'VIN_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vd_P_w,OUT_e,GND_n,Vg_n,VINJ_n,VIN_n,Vsel_n,VTUN_n]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class G_or_S_IndrctSwcs(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vgrun_w=None,run_w=None,prog_w=None,AVDD_w=None,Vgrun_e=None,run_e=None,prog_e=None,AVDD_e=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,Input_n=None,Vsel_n=None,Vsel_s=None,Vs_s=None,VINJ_s=None,GND_s=None,Vg_s=None,fgmem_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'G_or_S_IndrctSwcs'
        self.Vgrun_w = Port(circuit,self,'Vgrun_w','W',1*self.dim[0])
        self.run_w = Port(circuit,self,'run_w','W',1*self.dim[0])
        self.prog_w = Port(circuit,self,'prog_w','W',1*self.dim[0])
        self.AVDD_w = Port(circuit,self,'AVDD_w','W',1*self.dim[0])
        self.Vgrun_e = Port(circuit,self,'Vgrun_e','E',1*self.dim[0])
        self.run_e = Port(circuit,self,'run_e','E',1*self.dim[0])
        self.prog_e = Port(circuit,self,'prog_e','E',1*self.dim[0])
        self.AVDD_e = Port(circuit,self,'AVDD_e','E',1*self.dim[0])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',2*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.Input_n = Port(circuit,self,'Input_n','N',2*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',2*self.dim[1])
        self.Vs_s = Port(circuit,self,'Vs_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',2*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.fgmem_s = Port(circuit,self,'fgmem_s','S',2*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vgrun_w,run_w,prog_w,AVDD_w,Vgrun_e,run_e,prog_e,AVDD_e,VINJ_n,Vg_n,GND_n,VTUN_n,Input_n,Vsel_n,Vsel_s,Vs_s,VINJ_s,GND_s,Vg_s,fgmem_s,VTUN_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectGswc_OutMat(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vgrun_w=None,prog_w=None,run_w=None,AVDD_w=None,Vgrun_e=None,prog_e=None,run_e=None,AVDD_e=None,Vsel(0)_n=None,VINJ_n=None,GND_n=None,fg_pu(0)_n=None,VTUN_n=None,Vsel(1)_n=None,Vs_global(0)_n=None,Vg_global(0)_n=None,Vg_global(1)_n=None,Vs_global(1)_n=None,Vs_out_mtrx(0)_s=None,Vsel(0)_s=None,VINJ_s=None,GND_s=None,Vg_out_mtrx(0)_s=None,VTUN_s=None,fg_pu(1)_s=None,Vg_out_mtrx(1)_s=None,Vsel(1)_s=None,Vs_out_mtrx(1)_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectGswc_OutMat'
        self.Vgrun_w = Port(circuit,self,'Vgrun_w','W',1*self.dim[0])
        self.prog_w = Port(circuit,self,'prog_w','W',1*self.dim[0])
        self.run_w = Port(circuit,self,'run_w','W',1*self.dim[0])
        self.AVDD_w = Port(circuit,self,'AVDD_w','W',1*self.dim[0])
        self.Vgrun_e = Port(circuit,self,'Vgrun_e','E',1*self.dim[0])
        self.prog_e = Port(circuit,self,'prog_e','E',1*self.dim[0])
        self.run_e = Port(circuit,self,'run_e','E',1*self.dim[0])
        self.AVDD_e = Port(circuit,self,'AVDD_e','E',1*self.dim[0])
        self.Vsel(0)_n = Port(circuit,self,'Vsel(0)_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.fg_pu(0)_n = Port(circuit,self,'fg_pu(0)_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.Vsel(1)_n = Port(circuit,self,'Vsel(1)_n','N',1*self.dim[1])
        self.Vs_global(0)_n = Port(circuit,self,'Vs_global(0)_n','N',1*self.dim[1])
        self.Vg_global(0)_n = Port(circuit,self,'Vg_global(0)_n','N',1*self.dim[1])
        self.Vg_global(1)_n = Port(circuit,self,'Vg_global(1)_n','N',1*self.dim[1])
        self.Vs_global(1)_n = Port(circuit,self,'Vs_global(1)_n','N',1*self.dim[1])
        self.Vs_out_mtrx(0)_s = Port(circuit,self,'Vs_out_mtrx(0)_s','S',1*self.dim[1])
        self.Vsel(0)_s = Port(circuit,self,'Vsel(0)_s','S',1*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vg_out_mtrx(0)_s = Port(circuit,self,'Vg_out_mtrx(0)_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])
        self.fg_pu(1)_s = Port(circuit,self,'fg_pu(1)_s','S',1*self.dim[1])
        self.Vg_out_mtrx(1)_s = Port(circuit,self,'Vg_out_mtrx(1)_s','S',1*self.dim[1])
        self.Vsel(1)_s = Port(circuit,self,'Vsel(1)_s','S',1*self.dim[1])
        self.Vs_out_mtrx(1)_s = Port(circuit,self,'Vs_out_mtrx(1)_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vgrun_w,prog_w,run_w,AVDD_w,Vgrun_e,prog_e,run_e,AVDD_e,Vsel(0)_n,VINJ_n,GND_n,fg_pu(0)_n,VTUN_n,Vsel(1)_n,Vs_global(0)_n,Vg_global(0)_n,Vg_global(1)_n,Vs_global(1)_n,Vs_out_mtrx(0)_s,Vsel(0)_s,VINJ_s,GND_s,Vg_out_mtrx(0)_s,VTUN_s,fg_pu(1)_s,Vg_out_mtrx(1)_s,Vsel(1)_s,Vs_out_mtrx(1)_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_4x1(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vmid_w=None,Vd_P_w=None,Vd_R_w=None,FG_n=None,FG_s=None,Vmid_n=None,Vs_n=None,GND_n=None,Vg_n=None,VTUN_n=None,VINJ_n=None,Vsel_n=None,Vmid_s=None,Vs_s=None,GND_s=None,Vg_s=None,VTUN_s=None,VINJ_s=None,Vsel_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_4x1'
        self.Vmid_w = Port(circuit,self,'Vmid_w','W',2*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.Vd_R_w = Port(circuit,self,'Vd_R_w','W',4*self.dim[0])
        self.FG_n = Port(circuit,self,'FG_n','E',2*self.dim[0])
        self.FG_s = Port(circuit,self,'FG_s','E',2*self.dim[0])
        self.Vmid_n = Port(circuit,self,'Vmid_n','N',1*self.dim[1])
        self.Vs_n = Port(circuit,self,'Vs_n','N',1*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',1*self.dim[1])
        self.Vmid_s = Port(circuit,self,'Vmid_s','S',1*self.dim[1])
        self.Vs_s = Port(circuit,self,'Vs_s','S',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vmid_w,Vd_P_w,Vd_R_w,FG_n,FG_s,Vmid_n,Vs_n,GND_n,Vg_n,VTUN_n,VINJ_n,Vsel_n,Vmid_s,Vs_s,GND_s,Vg_s,VTUN_s,VINJ_s,Vsel_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_4x2(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vd_P_w=None,Vd_R_w=None,Vd_R_e=None,Vd_P_e=None,Vsel_n=None,Vs_n=None,VINJ_n=None,GND_n=None,Vg_n=None,VTUN_n=None,Vsel_s=None,Vs_s=None,VINJ_s=None,GND_s=None,Vg_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_4x2'
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.Vd_R_w = Port(circuit,self,'Vd_R_w','W',4*self.dim[0])
        self.Vd_R_e = Port(circuit,self,'Vd_R_e','E',4*self.dim[0])
        self.Vd_P_e = Port(circuit,self,'Vd_P_e','E',4*self.dim[0])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.Vs_n = Port(circuit,self,'Vs_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',2*self.dim[1])
        self.Vs_s = Port(circuit,self,'Vs_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',2*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vd_P_w,Vd_R_w,Vd_R_e,Vd_P_e,Vsel_n,Vs_n,VINJ_n,GND_n,Vg_n,VTUN_n,Vsel_s,Vs_s,VINJ_s,GND_s,Vg_s,VTUN_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_Bot_Bmat_4x2(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vmid_w=None,Vd_P_w=None,Vd_R_w=None,Vmid_e=None,Vd_P_e=None,Vd_R_e=None,FG_n=None,Vmid_n=None,Vsel_n=None,Vs_n=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,FG_s=None,Vmid_s=None,Vsel_s=None,Vs_s=None,VINJ_s=None,Vg_s=None,GND_s=None,VTUN_s=None,fg_mem_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_Bot_Bmat_4x2'
        self.Vmid_w = Port(circuit,self,'Vmid_w','W',2*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.Vd_R_w = Port(circuit,self,'Vd_R_w','W',3*self.dim[0])
        self.Vmid_e = Port(circuit,self,'Vmid_e','E',2*self.dim[0])
        self.Vd_P_e = Port(circuit,self,'Vd_P_e','E',4*self.dim[0])
        self.Vd_R_e = Port(circuit,self,'Vd_R_e','E',3*self.dim[0])
        self.FG_n = Port(circuit,self,'FG_n','N',2*self.dim[1])
        self.Vmid_n = Port(circuit,self,'Vmid_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.Vs_n = Port(circuit,self,'Vs_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',2*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.FG_s = Port(circuit,self,'FG_s','S',2*self.dim[1])
        self.Vmid_s = Port(circuit,self,'Vmid_s','S',1*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',2*self.dim[1])
        self.Vs_s = Port(circuit,self,'Vs_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',2*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])
        self.fg_mem_s = Port(circuit,self,'fg_mem_s','S',2*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vmid_w,Vd_P_w,Vd_R_w,Vmid_e,Vd_P_e,Vd_R_e,FG_n,Vmid_n,Vsel_n,Vs_n,VINJ_n,Vg_n,GND_n,VTUN_n,FG_s,Vmid_s,Vsel_s,Vs_s,VINJ_s,Vg_s,GND_s,VTUN_s,fg_mem_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_GSwcs_1x2(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),PROG_w=None,RUN_w=None,Vgsel_w=None,GND_n=None,Vgrun_n=None,VINJ_n=None,Vsel_n=None,VTUN_n=None,Vg_s=None,Vs_s=None,Vsel_B_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_GSwcs_1x2'
        self.PROG_w = Port(circuit,self,'PROG_w','W',1*self.dim[0])
        self.RUN_w = Port(circuit,self,'RUN_w','W',1*self.dim[0])
        self.Vgsel_w = Port(circuit,self,'Vgsel_w','W',1*self.dim[0])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Vgrun_n = Port(circuit,self,'Vgrun_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.Vs_s = Port(circuit,self,'Vs_s','S',2*self.dim[1])
        self.Vsel_B_s = Port(circuit,self,'Vsel_B_s','S',2*self.dim[1])

        # Initialize ports with given values
        portsInit = [PROG_w,RUN_w,Vgsel_w,GND_n,Vgrun_n,VINJ_n,Vsel_n,VTUN_n,Vg_s,Vs_s,Vsel_B_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_Top_AorBmat_4x2(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vmid_w=None,Vd_P_w=None,Vd_R_w=None,Vmid_e=None,Vd_P_e=None,Vd_R_e=None,FG_n=None,Vmid_n=None,Vsel_n=None,Vs_n=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,fgmem_n=None,FG_s=None,Vmid_s=None,Vsel_s=None,Vs_s=None,VINJ_s=None,Vg_s=None,GND_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_Top_AorBmat_4x2'
        self.Vmid_w = Port(circuit,self,'Vmid_w','W',2*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.Vd_R_w = Port(circuit,self,'Vd_R_w','W',3*self.dim[0])
        self.Vmid_e = Port(circuit,self,'Vmid_e','E',2*self.dim[0])
        self.Vd_P_e = Port(circuit,self,'Vd_P_e','E',4*self.dim[0])
        self.Vd_R_e = Port(circuit,self,'Vd_R_e','E',3*self.dim[0])
        self.FG_n = Port(circuit,self,'FG_n','N',2*self.dim[1])
        self.Vmid_n = Port(circuit,self,'Vmid_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.Vs_n = Port(circuit,self,'Vs_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',2*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.fgmem_n = Port(circuit,self,'fgmem_n','N',2*self.dim[1])
        self.FG_s = Port(circuit,self,'FG_s','S',2*self.dim[1])
        self.Vmid_s = Port(circuit,self,'Vmid_s','S',1*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',2*self.dim[1])
        self.Vs_s = Port(circuit,self,'Vs_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',2*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vmid_w,Vd_P_w,Vd_R_w,Vmid_e,Vd_P_e,Vd_R_e,FG_n,Vmid_n,Vsel_n,Vs_n,VINJ_n,Vg_n,GND_n,VTUN_n,fgmem_n,FG_s,Vmid_s,Vsel_s,Vs_s,VINJ_s,Vg_s,GND_s,VTUN_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class level_shifter_horizontal(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),GND_e=None,Vhi_e=None,Vout_e=None,Vout_B_e=None,Vin_n=None,Vlow_n=None,Vout_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'level_shifter_horizontal'
        self.GND_e = Port(circuit,self,'GND_e','E',1*self.dim[0])
        self.Vhi_e = Port(circuit,self,'Vhi_e','E',1*self.dim[0])
        self.Vout_e = Port(circuit,self,'Vout_e','E',2*self.dim[0])
        self.Vout_B_e = Port(circuit,self,'Vout_B_e','E',4*self.dim[0])
        self.Vin_n = Port(circuit,self,'Vin_n','N',4*self.dim[1])
        self.Vlow_n = Port(circuit,self,'Vlow_n','N',1*self.dim[1])
        self.Vout_s = Port(circuit,self,'Vout_s','S',2*self.dim[1])

        # Initialize ports with given values
        portsInit = [GND_e,Vhi_e,Vout_e,Vout_B_e,Vin_n,Vlow_n,Vout_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class level_shifter_vertical(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vlow_w=None,Vin_n=None,GND_s=None,Vgrun_s=None,Vhi_s=None,Vout_s=None,Vout_B_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'level_shifter_vertical'
        self.Vlow_w = Port(circuit,self,'Vlow_w','W',1*self.dim[0])
        self.Vin_n = Port(circuit,self,'Vin_n','N',2*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vgrun_s = Port(circuit,self,'Vgrun_s','S',2*self.dim[1])
        self.Vhi_s = Port(circuit,self,'Vhi_s','S',1*self.dim[1])
        self.Vout_s = Port(circuit,self,'Vout_s','S',2*self.dim[1])
        self.Vout_B_s = Port(circuit,self,'Vout_B_s','S',2*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vlow_w,Vin_n,GND_s,Vgrun_s,Vhi_s,Vout_s,Vout_B_s,VTUN_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_Block_east(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vmid_s=None,Vmid_e=None,Vd_P_e=None,Vd_R_e=None,E_e=None,FG_n=None,Vmid_n=None,Vsel_n=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,FG_s=None,Vsel_s=None,VINJ_s=None,Vg_s=None,Vd_R_s=None,GND_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'S_Block_east'
        self.Vmid_s = Port(circuit,self,'Vmid_s','W',2*self.dim[0])
        self.Vmid_e = Port(circuit,self,'Vmid_e','E',2*self.dim[0])
        self.Vd_P_e = Port(circuit,self,'Vd_P_e','E',4*self.dim[0])
        self.Vd_R_e = Port(circuit,self,'Vd_R_e','E',1*self.dim[0])
        self.E_e = Port(circuit,self,'E_e','E',4*self.dim[0])
        self.FG_n = Port(circuit,self,'FG_n','N',2*self.dim[1])
        self.Vmid_n = Port(circuit,self,'Vmid_n','N',2*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.FG_s = Port(circuit,self,'FG_s','S',2*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',1*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.Vd_R_s = Port(circuit,self,'Vd_R_s','S',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vmid_s,Vmid_e,Vd_P_e,Vd_R_e,E_e,FG_n,Vmid_n,Vsel_n,VINJ_n,Vg_n,GND_n,VTUN_n,FG_s,Vsel_s,VINJ_s,Vg_s,Vd_R_s,GND_s,VTUN_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_Block_filler_off_diagonal(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),N_n=None,S_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'S_Block_filler_off_diagonal'
        self.N_n = Port(circuit,self,'N_n','N',4*self.dim[1])
        self.S_s = Port(circuit,self,'S_s','S',4*self.dim[1])

        # Initialize ports with given values
        portsInit = [N_n,S_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_Block(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vmid_w=None,Vd_P_w=None,W_w=None,Vmid_e=None,Vd_P_e=None,Vd_R_e=None,E_e=None,FG_n=None,Vmid_n=None,Vsel_n=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,N_n=None,FG_s=None,Vmid_s=None,Vsel_s=None,VINJ_s=None,Vg_s=None,Vd_R_s=None,GND_s=None,VTUN_s=None,S_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'S_Block'
        self.Vmid_w = Port(circuit,self,'Vmid_w','W',2*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.W_w = Port(circuit,self,'W_w','W',4*self.dim[0])
        self.Vmid_e = Port(circuit,self,'Vmid_e','E',2*self.dim[0])
        self.Vd_P_e = Port(circuit,self,'Vd_P_e','E',4*self.dim[0])
        self.Vd_R_e = Port(circuit,self,'Vd_R_e','E',1*self.dim[0])
        self.E_e = Port(circuit,self,'E_e','E',4*self.dim[0])
        self.FG_n = Port(circuit,self,'FG_n','N',2*self.dim[1])
        self.Vmid_n = Port(circuit,self,'Vmid_n','N',2*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.N_n = Port(circuit,self,'N_n','N',4*self.dim[1])
        self.FG_s = Port(circuit,self,'FG_s','S',2*self.dim[1])
        self.Vmid_s = Port(circuit,self,'Vmid_s','S',2*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',1*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.Vd_R_s = Port(circuit,self,'Vd_R_s','S',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])
        self.S_s = Port(circuit,self,'S_s','S',4*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vmid_w,Vd_P_w,W_w,Vmid_e,Vd_P_e,Vd_R_e,E_e,FG_n,Vmid_n,Vsel_n,VINJ_n,Vg_n,GND_n,VTUN_n,N_n,FG_s,Vmid_s,Vsel_s,VINJ_s,Vg_s,Vd_R_s,GND_s,VTUN_s,S_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_Block_NS_routing_diagonal(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),N_n=None,S_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'S_Block_NS_routing_diagonal'
        self.N_n = Port(circuit,self,'N_n','N',4*self.dim[1])
        self.S_s = Port(circuit,self,'S_s','S',4*self.dim[1])

        # Initialize ports with given values
        portsInit = [N_n,S_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_Block_west(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vmid_w=None,Vd_P_w=None,W_w=None,Vmid_e=None,Vd_R_e=None,FG_n=None,Vmid_n=None,Vsel_n=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,FG_s=None,Vmid_s=None,Vsel_s=None,VINJ_s=None,Vg_s=None,GND_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'S_Block_west'
        self.Vmid_w = Port(circuit,self,'Vmid_w','W',2*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',4*self.dim[0])
        self.W_w = Port(circuit,self,'W_w','W',4*self.dim[0])
        self.Vmid_e = Port(circuit,self,'Vmid_e','E',2*self.dim[0])
        self.Vd_R_e = Port(circuit,self,'Vd_R_e','E',1*self.dim[0])
        self.FG_n = Port(circuit,self,'FG_n','N',2*self.dim[1])
        self.Vmid_n = Port(circuit,self,'Vmid_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.FG_s = Port(circuit,self,'FG_s','S',2*self.dim[1])
        self.Vmid_s = Port(circuit,self,'Vmid_s','S',1*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',1*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',2*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vmid_w,Vd_P_w,W_w,Vmid_e,Vd_R_e,FG_n,Vmid_n,Vsel_n,VINJ_n,Vg_n,GND_n,VTUN_n,FG_s,Vmid_s,Vsel_s,VINJ_s,Vg_s,GND_s,VTUN_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TA_FGbias_1x2(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Vin_P_w=None,Vin_M_w=None,Vd_P_w=None,GND_w=None,OUTPUT_e=None,GND_n=None,Vg_n=None,Vsel_n=None,AVDD_n=None,VTUN_n=None,VINJ_n=None,GND_s=None,Vg_s=None,Vsel_s=None,AVDD_s=None,VTUN_s=None,VINJ_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'TA_FGbias_1x2'
        self.Vin_P_w = Port(circuit,self,'Vin_P_w','W',2*self.dim[0])
        self.Vin_M_w = Port(circuit,self,'Vin_M_w','W',2*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',2*self.dim[0])
        self.GND_w = Port(circuit,self,'GND_w','W',1*self.dim[0])
        self.OUTPUT_e = Port(circuit,self,'OUTPUT_e','E',2*self.dim[0])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',1*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',1*self.dim[1])
        self.AVDD_n = Port(circuit,self,'AVDD_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vg_s = Port(circuit,self,'Vg_s','S',1*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',1*self.dim[1])
        self.AVDD_s = Port(circuit,self,'AVDD_s','S',1*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vin_P_w,Vin_M_w,Vd_P_w,GND_w,OUTPUT_e,GND_n,Vg_n,Vsel_n,AVDD_n,VTUN_n,VINJ_n,GND_s,Vg_s,Vsel_s,AVDD_s,VTUN_s,VINJ_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TGate_2nMirror(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),IN_CM_w=None,IN_TG_w=None,SelN_w=None,OUT_CM_e=None,OUT_TG_e=None,GND_n=None,AVDD_n=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'TGate_2nMirror'
        self.IN_CM_w = Port(circuit,self,'IN_CM_w','W',2*self.dim[0])
        self.IN_TG_w = Port(circuit,self,'IN_TG_w','W',1*self.dim[0])
        self.SelN_w = Port(circuit,self,'SelN_w','W',1*self.dim[0])
        self.OUT_CM_e = Port(circuit,self,'OUT_CM_e','E',2*self.dim[0])
        self.OUT_TG_e = Port(circuit,self,'OUT_TG_e','E',1*self.dim[0])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.AVDD_n = Port(circuit,self,'AVDD_n','N',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [IN_CM_w,IN_TG_w,SelN_w,OUT_CM_e,OUT_TG_e,GND_n,AVDD_n]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)
