from ashes_fg.asic.py_to_verilog import asic_compiler
from ashes_fg.asic.verilog_to_gds import gds_synthesis
from ashes_fg.asic import pd_tcl_gen as pd_cadence_tcl_gen

import os
import subprocess
import re
import time
import json
from pathlib import Path

def compile(circuit,process="Process",project_path = ".",project_name = "project",lib_path = None, place=True, route=True, location_islands=None, design_limits = [1e6, 6.1e5],drainSpaceIdx=None,drainSpace=10,gateSpaceIdx=None,gateSpace=10,qparams=None,pd_args=None,prBoundary_layer = None,run_fr_cadence=0):

        """
        Main ASIC compilation function
        - Makes Verilog netlist for a given Circuit
        - Creates directory for physical design
        - Calls P&R tools
        """

        # 1. Path Definitions
        syn_path = os.path.join(project_path, 'syn')
        cadence_base = os.path.join(project_path, 'cadence')
        cadence_proj_dir = os.path.join(cadence_base, project_name)
        cadence_tcl = os.path.join(cadence_proj_dir, 'tcl')
        cadence_inputs = os.path.join(cadence_proj_dir, 'inputs')
        cadence_outputs = os.path.join(cadence_proj_dir, 'outputs')
        cadence_run= os.path.join(cadence_proj_dir, 'run')

        # 2. Directory Creation
        dirs_to_create = [syn_path]
        if run_fr_cadence == 1:
                dirs_to_create += [cadence_proj_dir, cadence_tcl, cadence_inputs, cadence_outputs, cadence_run]
        
        for folder in dirs_to_create:
                if not os.path.exists(folder):
                        os.makedirs(folder)

        # 3. Generate Standard Verilog (Synthesis)
        verilog_path = os.path.join(syn_path, project_name + '.v')
        with open(verilog_path, "w") as f:
                f.write(circuit.print(process))



        # Variables to set space between IO edge and Core edge
        x_IO, y_IO = 0, 0 

        # Variables to pass mux info
        drainmux_space_isle_idx=drainSpaceIdx
        drainmux_space = drainSpace
        gatemux_space_isle_idx=gateSpaceIdx
        gatemux_space = gateSpace

        # Find the process node and define tech parameters
        if (process.split('_')[0].lower() == "tsmc" and process.split('_')[1].lower() == "350nm"):
                # All units in nanometers
                tech_process = 'vis350'
                cell_pitch = 22000
                dbu = 1000
                track_spacing = 1400
                # placement offset to make space for pin routing
                x_offset, y_offset = 400*track_spacing, 2000*track_spacing

        elif (process.split('_')[0].lower() == "sky" and process.split('_')[1].lower() == "130nm"):
                # All units in nanometers
                tech_process = 'sky130'
                cell_pitch = 6500
                dbu = 1000
                track_spacing = 1600 # M5 metal spacing
                # placement offset to make space for pin routing
                x_offset, y_offset = 400*track_spacing, 2000*track_spacing
                
        elif (process.split('_')[0].lower() == "tsmc" and process.split('_')[1].lower() == "16nm"):
                # All units in nanometers
                tech_process = 'tsmcN16'
                cell_pitch = 1632
                dbu = 2000
                track_spacing = 160 # M5 metal spacing
                # placement offset to make space for pin routing
                x_offset, y_offset = 400*track_spacing, 2000*track_spacing
                
                if(run_fr_cadence):
                        #x_IO, y_IO = 9990, 9984
                        x_IO, y_IO = 1980, 1728

                        
                ## Account for IO area so, location islands in python code can start from 0,0
                location_islands = tuple((x + x_IO, y + y_IO) for x, y in location_islands)


        design_area = (x_IO, y_IO, design_limits[0], design_limits[1], x_offset, y_offset)



       # 4. Cadence Physical Design Setup
        if run_fr_cadence == 1:
                if pd_args is None:
                        raise ValueError("pd_args (JSON settings) must be provided for Cadence flow.")

                # Generate flattened verilog for Cadence
                flat_verilog, pin_info, ndr_info = circuit.print_cadence(process)
                verilog_cadence_path = os.path.join(cadence_inputs, project_name + '.v')

                with open(verilog_cadence_path, "w") as f:
                        f.write(flat_verilog)

                # Generate individual TCL scripts inside cadence/inputs/
                pd_cadence_tcl_gen.generate_init_tcl( pd_args, os.path.join(cadence_tcl, "init.tcl"), top_level=project_name)
                pd_cadence_tcl_gen.generate_pins_tcl(pd_args, design_area, pin_info, os.path.join(cadence_tcl, "pins.tcl"))
                pd_cadence_tcl_gen.generate_power_tcl(pd_args, os.path.join(cadence_tcl, "power.tcl"))
                pd_cadence_tcl_gen.generate_route_tcl(pd_args, ndr_info, os.path.join(cadence_tcl, "route.tcl"))
                pd_cadence_tcl_gen.generate_signoff_tcl(pd_args, os.path.join(cadence_tcl, "signoff.tcl"),top_level=project_name)

                pd_cadence_tcl_gen.generate_main_tcl(os.path.join(cadence_proj_dir, "main.tcl"), subdir="../tcl")
                
                print(f"--- Cadence PD Scripts generated in {cadence_proj_dir} ---")



        if place == True:
                pdPath = os.path.join(project_path,'pd')
                #drainmux_space_isle_idx = 0
                process_params = (tech_process, dbu, track_spacing, x_offset, y_offset, cell_pitch, drainmux_space_isle_idx, drainmux_space, gatemux_space_isle_idx, gatemux_space,lib_path,prBoundary_layer,run_fr_cadence)
                pl_start = time.time()
                gds_synthesis(process_params, design_area, project_name,project_path,isle_loc=location_islands)
                pl_end = time.time()

                if route == True:

                        if qparams == None:
                                qdefpath = os.path.join(Path(__file__).parent,'qrouter_default.json')
                                with open(qdefpath) as file:
                                        qrouterParams = json.load(file)
                        else:
                                qrouterParams = qparams


                        # Pick the detailed router and default to qrouter. If not available, check for Triton.
                        qrouter = True if os.system('command -v qrouter') == 0 else False
                        triton_route = os.path.exists(os.path.join('TritonRoute','build','TritonRoute'))
                        lef_file = os.path.join(pdPath , project_name + '.lef')
                        def_file = os.path.join(pdPath , project_name + '.def')
                        report_file = os.path.join(pdPath , project_name + '_report.txt')
                        if qrouter and route==True:
                                base_cost = 10
                                out_file = os.path.join(pdPath , project_name + '_qroute.def')
                                param_file = os.path.join(pdPath, "qrouter_params.tcl")
                                info_file = os.path.join(pdPath , "layers_info.lef") ##Added
                                q_params = open(param_file, "w")
                                q_params.write(f"read_lef {lef_file}\n")
                                q_params.write(f"read_def {def_file}\n")

                                # Write qrouter parameters
                                for param in qrouterParams:
                                        if qrouterParams[param] != None:
                                                if param=="stage1"or param=="stage2" or param=="stage3" or param=="passes":
                                                        q_params.write(param +" "+ str(qrouterParams[param])+"\n")
                                                else:
                                                        q_params.write("cost " + param +" "+ str(qrouterParams[param])+"\n")

                                #q_params.write("layers 5\n")
                                q_params.write(f"write_def {out_file}\n")
                                q_params.write(f"write_failed {report_file}\n")
                                q_params.write("quit\n")
                                q_params.close()

                                command = ['qrouter', '-nog', '-s', param_file]
                                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                # Read the output in real-time
                                while True:
                                        output = process.stdout.readline()
                                        if output == '' and process.poll() is not None:
                                                break
                                        if output:
                                                print(output.strip())
                                rt_end = time.time()

                                gds_synthesis(process_params, design_area, project_name,project_path,routed_def=True, router_tool='qrouter')
                                fin_end = time.time()
                                pl_time = round(pl_end - pl_start, 3)
                                rt_time = round(rt_end - pl_end, 3)
                                merge_time = round(fin_end - rt_end, 3)
                                total_time = round(fin_end - pl_start, 3)
                                print(f"placement took {pl_time} s, routing took {rt_time} s, merging took {merge_time} s, total time {total_time} s")

                                with open(report_file,"a") as file:
                                        file.write("Placement Time: "+ str(pl_time)+"\n")
                                        file.write("Routing Time: "+ str(rt_time)+"\n")
                                        file.write("Merge Time: "+ str(merge_time)+"\n")
                                        file.write("Total Time: "+ str(total_time)+"\n")

                        elif triton_route:
                                tr_executable = os.path.join('TritonRoute','build','TritonRoute')
                                guide_file = os.path.join(project_name, project_name + '.guide')
                                out_file = os.path.join(project_name, project_name + '_routed.def')
                                num_threads = '8'
                                command = [tr_executable, '-lef', lef_file, '-def', def_file, '-guide', guide_file, '-output', out_file, '-threads', num_threads]
                                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                # Read the output in real-time
                                while True:
                                        output = process.stdout.readline()
                                        if output == '' and process.poll() is not None:
                                                break
                                        if output:
                                                print(output.strip())
                                gds_synthesis(process_params, design_area, project_name, routed_def=True, router_tool='triton')
