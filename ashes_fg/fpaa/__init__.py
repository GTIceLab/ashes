# ashes_fg/fpaa/__init__.py

# Expose Public API for IR and BLIF generation
from .ir import Module, Port, Net, Instance
from .py2blif import emit_py_to_blif, save_blif

# expose the function compile that pushes from python down to blif
from ashes_fg.fpaa.ir import Module
import ashes_fg.fpaa.gen_pads_30a
import ashes_fg.fpaa.gen_pads_30
import ashes_fg.fpaa.blif_to_switches as bs
import ashes_fg.fpaa.program_fpaa as pf
from ashes_fg.fpaa.Make_ProgramList_CompileAssembly import compile as ca
from ashes_fg.fpaa.py2blif import emit_py_to_blif, save_blif

import os

ASHESPATH = os.getenv("ASHESPATH", "/home/ubuntu/ashes")


def compile(system: Module, project_name: str, chip_num: int, board_type: str = "3.0a"):
    out_path = os.path.join(ASHESPATH, project_name)
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    blif_output = emit_py_to_blif(system, system.name)
    save_blif(blif_output, system.name, out_path)

    sys_name = os.path.join(out_path, system.name)
    if board_type == '3.0a':
    	gen_pads_30a.gen_pads_30a(sys_name, system, project_name)
    elif board_type == '3.0':
    	gen_pads_30.gen_pads_30(sys_name, project_name)
    bs.blif2swcs(sys_name, project_name, board_type, out_path)
    ca(project_name, board_type, chip_num)
    os.chdir(f'{out_path}')
    pf.main()
