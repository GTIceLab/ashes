import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes.examples.mag2stdcells.library.lib as lib # standard cell library

import math

# One 4x2 VMM has 8 floating gates
# One S-block needs 6 floating gates
# Therefore, we use 3 4x2 VMMs in one row to get 4 S-blocks (8 * 3 / 6 = 4)

def generate_sblocks(top: ac.Circuit, vmm_island: ac.Island,
                     num_sblocks: int = 18, return_horizontal_lines: bool = True):
  
  # top = ac.Circuit()
  # vmm_island = ac.Island(top)
  # num_sblocks = 18
  # return_horizontal_lines = True

  if (num_sblocks % 4 != 0): 
    print("Warning: Some floating gates may be left unused")
    
  number_of_rows = math.ceil(num_sblocks / 4)


  ########### Place Cells ###########
  WestVMMs = lib.S_Block_west(top,vmm_island,dim=[number_of_rows,1])
  EastVMMs = lib.S_Block_east(top,vmm_island,dim=[number_of_rows,1])

  # (0,0) is upper left corner
  WestVMMs.place([0,0])
  EastVMMs.place([number_of_rows + 1, 0])

  # Place the middle routing blocks
  routing_block_row_index = 0
  S_Block_middle_blocks = [[None for _ in range(number_of_rows)] for _ in range(number_of_rows)]

  for x in range(number_of_rows):
    for y in range(number_of_rows):
      if (y == routing_block_row_index):
        S_Block_middle_blocks[x][y] = lib.S_Block_NS_routing_diagonal(top, vmm_island, dim=[1,1])
      else:
        S_Block_middle_blocks[x][y] = lib.S_Block_filler_off_diagonal(top, vmm_island, dim=[1,1])
      
      S_Block_middle_blocks[x][y].place([x + 1, y])
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
  # West VMM vertical lines
  for i in range(2):
    Vsel_lines[i] += WestVMMs.Vsel_n[i]
    Vg_lines[i] += WestVMMs.Vg_n[i]
    VINJ += WestVMMs.VINJ_n[i]

  # East VMM vertical lines
  for i in range(4):
    Vsel_lines[2 + i] += EastVMMs.Vsel_n[i]
    Vg_lines[2 + i] += EastVMMs.Vg_n[i]
    VINJ += EastVMMs.VINJ_n[i]
    
  # Both VMM horizontal lines
  for i in range(4 * number_of_rows):
    Vd_P_lines[i] += WestVMMs.Vd_P_e[i]
    W_lines[i] += WestVMMs.W[i]
    
  # Middle routing/filler blocks
  for x in range(number_of_rows):
    for y in range(number_of_rows):
      N_lines[i] += S_Block_middle_blocks[x][y].N[i]
      S_lines[i] += S_Block_middle_blocks[x][y].S[i]

