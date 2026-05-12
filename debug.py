import ashes_fg.fpaa.blif_to_switches as bs
import os

project_name = 'test'
system_name = 'test'
board_type = '3.0a'
out_path = os.path.abspath(f'./{project_name}')
sys_path = os.path.join(out_path, system_name)

bs.blif2swcs(sys_path, project_name, board_type, out_path)
