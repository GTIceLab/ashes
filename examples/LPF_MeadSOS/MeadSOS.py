import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.asic.asic_systems as algs


def MeadSOS(circuit,LPFIsland=None,loc=[0,0],Vin=None):
    Top = circuit
    # Placement
    if LPFIsland == None:
        LPFIsland = ac.Island(Top)

    TAWeak0 = lib_new.TSMC350nm_TA2Cell_Weak(Top,LPFIsland)
    TAWeak1 = lib_new.TSMC350nm_TA2Cell_Weak(Top,LPFIsland)

    TAWeak0.markAbut()
    TAWeak1.markAbut()

    TAWeak0.place([loc[0],loc[1]])
    TAWeak1.place([loc[0]+1,loc[1]])
    # Connections
	# V1 = TA Weak
    # -------------------------------------------------------------------------------
    if Vin != None:
        TAWeak0.VIN1_PLUS += Vin
    # Feedback Buffer Connections
    Vmid = ac.Wire(Top)
    # TA1
    TAWeak0.OUTPUT[0] += Vmid
    TAWeak0.VIN1_MINUS += Vmid
    # TA2
    TAWeak1.VIN1_PLUS += Vmid
    # TA3
    TAWeak0.VIN2_PLUS += Vmid
    TAWeak0.OUTPUT[1] += Vmid
    # Output Connections
    Vout = ac.Wire(Top)
    # TA2
    TAWeak1.OUTPUT[0] += Vout
    TAWeak1.VIN1_MINUS += Vout
    # TA3
    TAWeak0.VIN2_MINUS += Vout
    #Buffer
    TAWeak1.VIN2_PLUS += Vout
    # Buffer Feedback
    Vout_Buf = ac.Wire(Top)
    TAWeak1.VIN2_MINUS += Vout_Buf
    TAWeak1.OUTPUT[1] += Vout_Buf

    return Vout,Vout_Buf,[TAWeak0,TAWeak1]

