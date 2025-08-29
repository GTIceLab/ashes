import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.class_lib_LLM as lib_LLM
import ashes_fg.asic.asic_systems as algs

import numpy as np

def DotprodArray(circuit,numStages=1,p=0,q=0,m=0,island=None,islandLoc = [0,0], edgeCells=False):
    DotprodIsland = island
    if island == None:
        DotprodIsland = ac.Island(circuit)
    dotprod_L = lib_LLM.dotproduct_L(circuit,DotprodIsland,dim=[p,1])
    dotprod_L.place([islandLoc[0],islandLoc[1]])

    dotprod_mid = lib_LLM.dotproduct_mid(circuit,DotprodIsland,dim=[p,m-2])
    dotprod_mid.place([islandLoc[0],islandLoc[1]+1])

    dotprod_R = lib_LLM.dotproduct_R(circuit, DotprodIsland,dim=[p,1])
    dotprod_R.place([islandLoc[0],islandLoc[1]+m-1])

    if edgeCells == True:
        K_layer_output=lib_LLM.K_layer_output(circuit,DotprodIsland,dim=[p,1])
        K_layer_output.place([islandLoc[0],islandLoc[1]+m])
    return DotprodIsland

#keep m>=3 for now
def DiscTimeSaliency(circuit,numStages=1,p=0,q=0,m=0,island=None,islandLoc = [0,0],edgeCells=True):
    
    SaliencyIsland = island
    if island == None:
        SaliencyIsland = ac.Island(circuit)
    
    Q_layer = lib_new.TSMC350nm_4x2_Indirect(Top,SaliencyIsland,dim=[p,q])
    print(islandLoc[0])
    Q_layer.place([islandLoc[0],islandLoc[1]])
    Dotproduct = DotprodArray(circuit,p=p,q=q,m=m,island=SaliencyIsland,islandLoc = [islandLoc[0],islandLoc[1]+q],edgeCells=edgeCells)
    K_layer = lib_new.TSMC350nm_4x2_Indirect(Top,SaliencyIsland,dim=[p,q])
    K_layer.place([islandLoc[0],islandLoc[1]+q+m+1])

    #Island0 = ac.Island(Top)
    #dotprod_L=lib_LLM.dotproduct_L(Top,Island0,dim=[p,1])
    #dotprod_L.place([0,0])

    #Island1 = ac.Island(Top)
    #dotprod_mid1=lib_LLM.dotproduct_mid(Top,Island1,dim=[p,m-2])
    #dotprod_mid1.place([0,0])

    #Island2 = ac.Island(Top)
    #dotprod_R=lib_LLM.dotproduct_R(Top,Island2,dim=[p,1])
    #dotprod_R.place([0,0])

    #Island3 = ac.Island(Top)
    #K_layer_output = lib_LLM.K_layer_output(Top,Island3,dim=[p,1])
    #K_layer_output.place([0,0])
    
    #Island4 = ac.Island(Top)
    #K_input = lib_new.TSMC350nm_4x2_Indirect(Top,Island4,dim=[p,q])
    #K_input.place([0,0])

    # Pins
    # -------------------------------------------------------------------------------
    #outerPins = lib_mux.frame(Top)

    #PROG = outerPins.createPort("N","Prog")
    #RUN = outerPins.createPort("N","Run")
    #VGRUN = outerPins.createPort("N","VGRUN")
    #VGPROG = outerPins.createPort("N","VGPROG")
    #VTUN = outerPins.createPort("N","VTUN")
    #AVDD = outerPins.createPort("N","AVDD")
    #GND_N = outerPins.createPort("N","gnd")
    #GND_S = outerPins.createPort("S","gnd")
    #VINJ_N = outerPins.createPort("N","vinj")
    #VINJ_S = outerPins.createPort("S","vinj")
    #VOUT = outerPins.createPort("E","Vout")
    # Pin Connections
    # -------------------------------------------------------------------------------

    
    
    # Island Placement
    # -------------------------------------------------------------------------------
    #Pitch = 22000
    X = islandLoc[0]
    Y = islandLoc[1]
    K_output_width = 9550
    #location_islands = ((X,Y),(X+Pitch,Y),(X+(m-1)*Pitch,Y),(X+m*Pitch,Y),(X+m*Pitch+K_output_width,Y))
    location_islands = ((X,Y))
    return location_islands


Top = ac.Circuit()

#location_islands = Transformer(Top,1,islandLoc=[50000,25000])
design_limits = [5e5, 5e5]
DiscTimeSaliencyCircuit = DiscTimeSaliency(Top,p=4,q=3,m=7)
location_islands=None
ac.compile_asic(Top,process="TSMC350nm",fileName="DiscTimeSaliency",p_and_r = True,design_limits = design_limits, location_islands = location_islands)




