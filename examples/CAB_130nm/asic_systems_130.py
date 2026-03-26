# This file is used instead of ashes/ashes_fg/asic/asic_systems.py
# so the correct 130nm cells can be used. In the future, we need
# a more flexible way to solve the problem: original asic_systems
# is hardcoded to use TSMC350 cells.

from ashes_fg.asic.asic_compile import *

import ashes.examples.mag2stdcells.library.lib as lib

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
    VMM = lib.IndirectVMM_4x2(circuit,dim=(numRows,numCols),island=VMMIsland)
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

