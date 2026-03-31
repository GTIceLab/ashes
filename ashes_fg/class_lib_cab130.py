from ashes_fg.asic.asic_compile import *

class alexpmos(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VS_w=None,D1_e=None,VG_n=None,VDD_e=None,D2_s=None,D3_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'alexpmos'
        self.VS_w = Port(circuit,self,'VS_w','W',1*self.dim[0])
        self.D1_e = Port(circuit,self,'D1_e','E',1*self.dim[0])
        self.VG_n = Port(circuit,self,'VG_n','N',1*self.dim[1])
        self.VDD_e = Port(circuit,self,'VDD_e','S',1*self.dim[1])
        self.D2_s = Port(circuit,self,'D2_s','S',1*self.dim[1])
        self.D3_s = Port(circuit,self,'D3_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [VS_w,D1_e,VG_n,VDD_e,D2_s,D3_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

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
    def __init__(self,circuit,island=None,dim=(1,1),Vgrun_w=None,prog_w=None,run_w=None,AVDD_w=None,Vgrun_e=None,prog_e=None,run_e=None,AVDD_e=None,Vsel_n=None,VINJ_n=None,GND_n=None,fg_pu_n=None,VTUN_n=None,Vs_global_n=None,Vg_global_n=None,Vs_out_mtrx_s=None,Vsel_s=None,VINJ_s=None,GND_s=None,Vg_out_mtrx_s=None,VTUN_s=None,fg_pu_s=None):
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
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.fg_pu_n = Port(circuit,self,'fg_pu_n','N',1*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.Vs_global_n = Port(circuit,self,'Vs_global_n','N',2*self.dim[1])
        self.Vg_global_n = Port(circuit,self,'Vg_global_n','N',2*self.dim[1])
        self.Vs_out_mtrx_s = Port(circuit,self,'Vs_out_mtrx_s','S',2*self.dim[1])
        self.Vsel_s = Port(circuit,self,'Vsel_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Vg_out_mtrx_s = Port(circuit,self,'Vg_out_mtrx_s','S',2*self.dim[1])
        self.VTUN_s = Port(circuit,self,'VTUN_s','S',1*self.dim[1])
        self.fg_pu_s = Port(circuit,self,'fg_pu_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Vgrun_w,prog_w,run_w,AVDD_w,Vgrun_e,prog_e,run_e,AVDD_e,Vsel_n,VINJ_n,GND_n,fg_pu_n,VTUN_n,Vs_global_n,Vg_global_n,Vs_out_mtrx_s,Vsel_s,VINJ_s,GND_s,Vg_out_mtrx_s,VTUN_s,fg_pu_s]
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

class IndirectVMM_DrainSwcs(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Sel_w=None,N_Sel_w=None,GND_w=None,VINJ_w=None,VD_P_e=None,VD_R_e=None,GND_n=None,Prog_DrLn_n=None,Sel_n=None,VD_P_n=None,VINJ_n=None,Run_DrLn_n=None,N_Sel_n=None,GND_s=None,Prog_DrLn_s=None,VD_P_s=None,Sel_s=None,VINJ_s=None,Run_DrLn_s=None,VD_R_s=None,N_Sel_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'IndirectVMM_DrainSwcs'
        self.Sel_w = Port(circuit,self,'Sel_w','W',4*self.dim[0])
        self.N_Sel_w = Port(circuit,self,'N_Sel_w','W',2*self.dim[0])
        self.GND_w = Port(circuit,self,'GND_w','W',1*self.dim[0])
        self.VINJ_w = Port(circuit,self,'VINJ_w','W',1*self.dim[0])
        self.VD_P_e = Port(circuit,self,'VD_P_e','E',4*self.dim[0])
        self.VD_R_e = Port(circuit,self,'VD_R_e','E',4*self.dim[0])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Prog_DrLn_n = Port(circuit,self,'Prog_DrLn_n','N',1*self.dim[1])
        self.Sel_n = Port(circuit,self,'Sel_n','N',2*self.dim[1])
        self.VD_P_n = Port(circuit,self,'VD_P_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Run_DrLn_n = Port(circuit,self,'Run_DrLn_n','N',1*self.dim[1])
        self.N_Sel_n = Port(circuit,self,'N_Sel_n','N',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Prog_DrLn_s = Port(circuit,self,'Prog_DrLn_s','S',1*self.dim[1])
        self.VD_P_s = Port(circuit,self,'VD_P_s','S',2*self.dim[1])
        self.Sel_s = Port(circuit,self,'Sel_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.Run_DrLn_s = Port(circuit,self,'Run_DrLn_s','S',1*self.dim[1])
        self.VD_R_s = Port(circuit,self,'VD_R_s','S',2*self.dim[1])
        self.N_Sel_s = Port(circuit,self,'N_Sel_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Sel_w,N_Sel_w,GND_w,VINJ_w,VD_P_e,VD_R_e,GND_n,Prog_DrLn_n,Sel_n,VD_P_n,VINJ_n,Run_DrLn_n,N_Sel_n,GND_s,Prog_DrLn_s,VD_P_s,Sel_s,VINJ_s,Run_DrLn_s,VD_R_s,N_Sel_s]
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

class Volatile_Swcs(StandardCell):
    # NOTE: I have manually removed pins from internal nets (those with dots. in their names). This needs to be fixed later
    def __init__(self,circuit,island=None,dim=(1,1),RST_b_w=None,D_w=None,GND_w=None,VDD_w=None,Vd_P_w=None,CLK_w=None,Scan_Vout_w=None,Q_e=None,Vin_n=None,Vsel_n=None,Vg_n=None,VTUN_n=None,VINJ_n=None,Scan_VOut_s=None,GND_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        # Define cell information
        self.name = 'Volatile_Swcs'
        self.RST_b_w = Port(circuit,self,'RST_b_w','W',1*self.dim[0])
        self.D_w = Port(circuit,self,'D_w','W',1*self.dim[0])
        self.GND_w = Port(circuit,self,'GND_w','W',1*self.dim[0])
        self.VDD_w = Port(circuit,self,'VDD_w','W',1*self.dim[0])
        self.Vd_P_w = Port(circuit,self,'Vd_P_w','W',1*self.dim[0])
        self.CLK_w = Port(circuit,self,'CLK_w','W',1*self.dim[0])
        self.Scan_Vout_w = Port(circuit,self,'Scan_Vout_w','W',1*self.dim[0])
        self.Q_e = Port(circuit,self,'Q_e','E',1*self.dim[0])
        self.Vin_n = Port(circuit,self,'Vin_n','N',2*self.dim[1])
        self.Vsel_n = Port(circuit,self,'Vsel_n','N',2*self.dim[1])
        self.Vg_n = Port(circuit,self,'Vg_n','N',2*self.dim[1])
        self.VTUN_n = Port(circuit,self,'VTUN_n','N',1*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Scan_VOut_s = Port(circuit,self,'Scan_VOut_s','S',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [RST_b_w,D_w,GND_w,VDD_w,Vd_P_w,CLK_w,Scan_Vout_w,Q_e,Vin_n,Vsel_n,Vg_n,VTUN_n,VINJ_n,Scan_VOut_s,GND_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)


# This part of the file is added instead of ashes/ashes_fg/asic/asic_systems.py
# so that the correct 130nm cells can be used.
# Some of these should override standard cells definitions generated above

import math

import ashes_fg.asic.asic_compile as ac
from ashes_fg.asic.asic_compile import *


def IndirectVMM(circuit,dim=[4,2], island=None,decoderPlace=True,loc=[0,0]):
    if (dim[0] % 4) != 0:
            raise Exception("Error: VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)

    VMMIsland = island
    if island == None:
          VMMIsland = Island(circuit)

    # Create VMM and place in an island
    VMM = IndirectVMM_4x2(circuit,dim=(numRows,numCols),island=VMMIsland)
    circuit.placeInstance(VMM,loc)

    if decoderPlace == True: # TODO
        raise NotImplementedError
        # # Add decoders
        # gateBits = int(np.ceil(np.log2(dim[1])))
        # GateDecoder = STD_IndirectGateDecoder(circuit,VMMIsland,gateBits)
        # GateSwitches = STD_IndirectGateSwitch(circuit,VMMIsland,numCols)

        # drainBits = int(np.ceil(np.log2(dim[0])))
        # DrainDecoder = STD_DrainDecoder(circuit,VMMIsland,drainBits)
        # DrainSel = STD_DrainSelect(circuit,VMMIsland,numRows)
        # DrainSwitches = STD_DrainSwitch(circuit,VMMIsland,numRows)

    return VMM

def generate_sblocks(top: ac.Circuit, island: ac.Island,
                     num_sblocks: int = 18, base_loc: list = [0, 0],
                     return_horizontal_lines: bool = True):
    # One 4x2 VMM has 8 floating gates
    # One S-block needs 6 floating gates
    # Therefore, we use 3 4x2 VMMs in one row to get 4 S-blocks (8 * 3 / 6 = 4)
    
    # top = ac.Circuit()
    # vmm_island = ac.Island(top)
    # num_sblocks = 18
    # return_horizontal_lines = True

    if (num_sblocks % 4 != 0): 
        print("Warning: Some floating gates may be left unused")
        
    number_of_rows = math.ceil(num_sblocks / 4)
    print("Number of S Block rows:", number_of_rows)


    ########### Place Cells ###########
    WestVMMs = S_Block_west(top,island,dim=[number_of_rows,1])
    EastVMMs = S_Block_east(top,island,dim=[number_of_rows,1])

    # (0,0) is upper left corner
    print("Placing west at", base_loc)##
    WestVMMs.place(base_loc)
    print("Placing east at", [base_loc[0], base_loc[1] + number_of_rows + 1])##
    EastVMMs.place([base_loc[0], base_loc[1] + number_of_rows + 1])

    # Place the middle routing blocks
    routing_block_row_index = 0
    S_Block_middle_blocks = [[None for _ in range(number_of_rows)] for _ in range(number_of_rows)]

    for x in range(number_of_rows):
        for y in range(number_of_rows):
            if (y == routing_block_row_index):
                S_Block_middle_blocks[x][y] = S_Block_NS_routing_diagonal(top, island, dim=[1,1])
            else:
                S_Block_middle_blocks[x][y] = S_Block_filler_off_diagonal(top, island, dim=[1,1])
            
            ## added a + 1 at the end, just to get rid of error
            ## need to look at gds to see if this turned out right
            print("Placing at", [base_loc[0] + y, base_loc[1] + x + 1])##
            S_Block_middle_blocks[x][y].place([base_loc[0] + y, base_loc[1] + x + 1])
            S_Block_middle_blocks[x][y].markAbut()
        routing_block_row_index += 1
        
    ########### Wire/Net Definition ###########
    # One VMM block has the following nets: 4 W, 4 Vd_P, 2 Vsel, 2 VINJ, 2 Vg, 1 VTUN, 1 GND
    # One S_Block_NS_routing and one S_Block_filler both have the following nets: 4 N, 4 W

    VINJ = ac.Wire(top)
    GND = ac.Wire(top)
    VTUN = ac.Wire(top)

    Vg_lines = [ac.Wire(top) for _ in range(6)]
    Vsel_lines = [ac.Wire(top) for _ in range(6)]
    Vd_P_lines = [ac.Wire(top) for _ in range(6)]

    N_lines = [ac.Wire(top) for _ in range(4 * number_of_rows)]
    S_lines = [ac.Wire(top) for _ in range(4 * number_of_rows)]
    E_lines = [ac.Wire(top) for _ in range(4 * number_of_rows)]
    W_lines = [ac.Wire(top) for _ in range(4 * number_of_rows)]


    ########### Define Connections ###########
    # # West VMM vertical lines
    # for i in range(2):
    #     Vsel_lines[i] += WestVMMs.Vsel_n[i]
    #     Vg_lines[i] += WestVMMs.Vg_n[i]
    #     VINJ += WestVMMs.VINJ_n[i]

    # # East VMM vertical lines
    # for i in range(4):
    #     Vsel_lines[2 + i] += EastVMMs.Vsel_n[i]
    #     Vg_lines[2 + i] += EastVMMs.Vg_n[i]
    #     VINJ += EastVMMs.VINJ_n[i]
        
    # # Both VMM horizontal lines
    # for i in range(4 * number_of_rows):
    #     Vd_P_lines[i] += WestVMMs.Vd_P_e[i]
    #     W_lines[i] += WestVMMs.W[i]
        
    # # Middle routing/filler blocks
    # for x in range(number_of_rows):
    #     for y in range(number_of_rows):
    #         N_lines[i] += S_Block_middle_blocks[x][y].N[i]
    #         S_lines[i] += S_Block_middle_blocks[x][y].S[i]
    
    return WestVMMs, EastVMMs # TODO what else?

######### Overridden cells below #########

class G_or_S_IndrctSwcs(MUX):
    def __init__(self,circuit,island=None,num=0,Vgrun_w=None,run_w=None,prog_w=None,AVDD_w=None,Vgrun_e=None,run_e=None,prog_e=None,AVDD_e=None,VINJ_n=None,Vg_n=None,GND_n=None,VTUN_n=None,Input_n=None,Vsel_n=None,Vsel_s=None,Vs_s=None,VINJ_s=None,GND_s=None,Vg_s=None,fgmem_s=None,VTUN_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (0, self.num)

        self.type = "switch"

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

class IndirectVMM_DrainSwcs(MUX):
    def __init__(self,circuit,island=None,num=1,col=-1,Sel_w=None,N_Sel_w=None,GND_w=None,VINJ_w=None,VD_P_e=None,VD_R_e=None,GND_n=None,Prog_DrLn_n=None,Sel_n=None,VD_P_n=None,VINJ_n=None,Run_DrLn_n=None,N_Sel_n=None,GND_s=None,Prog_DrLn_s=None,VD_P_s=None,Sel_s=None,VINJ_s=None,Run_DrLn_s=None,VD_R_s=None,N_Sel_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.col = col
        # self.dim = dim
        
        self.dim = (self.num, 0)
        self.decoder = True
        self.type = "switch"
        self.switchType = "drain_select"

        # Define cell information
        self.name = 'IndirectVMM_DrainSwcs'
        self.Sel_w = Port(circuit,self,'Sel_w','W',4*self.dim[0])
        self.N_Sel_w = Port(circuit,self,'N_Sel_w','W',2*self.dim[0])
        self.GND_w = Port(circuit,self,'GND_w','W',1*self.dim[0])
        self.VINJ_w = Port(circuit,self,'VINJ_w','W',1*self.dim[0])
        self.VD_P_e = Port(circuit,self,'VD_P_e','E',4*self.dim[0])
        self.VD_R_e = Port(circuit,self,'VD_R_e','E',4*self.dim[0])
        self.GND_n = Port(circuit,self,'GND_n','N',1*self.dim[1])
        self.Prog_DrLn_n = Port(circuit,self,'Prog_DrLn_n','N',1*self.dim[1])
        self.Sel_n = Port(circuit,self,'Sel_n','N',2*self.dim[1])
        self.VD_P_n = Port(circuit,self,'VD_P_n','N',2*self.dim[1])
        self.VINJ_n = Port(circuit,self,'VINJ_n','N',1*self.dim[1])
        self.Run_DrLn_n = Port(circuit,self,'Run_DrLn_n','N',1*self.dim[1])
        self.N_Sel_n = Port(circuit,self,'N_Sel_n','N',1*self.dim[1])
        self.GND_s = Port(circuit,self,'GND_s','S',1*self.dim[1])
        self.Prog_DrLn_s = Port(circuit,self,'Prog_DrLn_s','S',1*self.dim[1])
        self.VD_P_s = Port(circuit,self,'VD_P_s','S',2*self.dim[1])
        self.Sel_s = Port(circuit,self,'Sel_s','S',2*self.dim[1])
        self.VINJ_s = Port(circuit,self,'VINJ_s','S',1*self.dim[1])
        self.Run_DrLn_s = Port(circuit,self,'Run_DrLn_s','S',1*self.dim[1])
        self.VD_R_s = Port(circuit,self,'VD_R_s','S',2*self.dim[1])
        self.N_Sel_s = Port(circuit,self,'N_Sel_s','S',1*self.dim[1])

        # Initialize ports with given values
        portsInit = [Sel_w,N_Sel_w,GND_w,VINJ_w,VD_P_e,VD_R_e,GND_n,Prog_DrLn_n,Sel_n,VD_P_n,VINJ_n,Run_DrLn_n,N_Sel_n,GND_s,Prog_DrLn_s,VD_P_s,Sel_s,VINJ_s,Run_DrLn_s,VD_R_s,N_Sel_s]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class IndirectVMM_GSwcs_1x2(MUX):
    def __init__(self,circuit,island=None,num=1,col=-1,PROG_w=None,RUN_w=None,Vgsel_w=None,GND_n=None,Vgrun_n=None,VINJ_n=None,Vsel_n=None,VTUN_n=None,Vg_s=None,Vs_s=None,Vsel_B_s=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.col = col
        # self.dim = dim
        self.dim = (0, self.num)
        
        self.type = "switch_ind"
        if self.col < 0: # col < 0
            self.type = "switch"

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

class ERASE_IndirectVMM_GSwcs_1x2(MUX):
    def __init__(self,circuit,island=None,num=0,col=-1,PROG_w=None,RUN_w=None,Vgsel_w=None,GND_n=None,Vgrun_n=None,VINJ_n=None,Vsel_n=None,VTUN_n=None,Vg_s=None,Vs_s=None,Vsel_B_s=None):
        # TODO num=0,col=-1; dim=(num,col)?
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        # self.dim = dim
        self.num = num
        self.col = col
        self.dim = (0, self.num)
        
        self.type = "switch_ind"
        if self.col < 0: # col < 0
            raise Exception("Specify column to erase gate switch")

        # Define cell information
        self.name = "none" # instead of 'IndirectVMM_GSwcs_1x2'
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
