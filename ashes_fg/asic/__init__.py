from ashes_fg.asic.py_to_verilog import asic_compiler
from ashes_fg.asic.verilog_to_gds import gds_synthesis
import os
import subprocess
import re
import time
import json
from pathlib import Path

#def compile(system, project_name=None, tech_process='privA_65', dbu=1000, track_spacing=250, cell_pitch=22000, x_offset=None, y_offset=None, design_area=(0,0,1,1), location_islands=None,drainmux_space_isle_idx=0, drainmux_space = 4.2, gatemux_space_isle_idx=None, gatemux_space=10,route=True,qparams=None):
def compile(circuit,process="Process",fileName = "compiled",path = "./example_verilog", p_and_r = True, location_islands=None, design_limits = [1e6, 6.1e5],drainSpaceIdx=None,drainSpace=10,gateSpaceIdx=None,gateSpace=10,route=True,qparams=None):
        """
        Main ASIC compilation function
        - Makes Verilog netlist for a given Circuit
        - Creates directory for physical design
        - Calls P&R tools
        """

        drainmux_space_isle_idx=drainSpaceIdx
        drainmux_space = drainSpace
        gatemux_space_isle_idx=gateSpaceIdx
        gatemux_space = gateSpace

        # Create project directory
        project_name = fileName
        projectPath = os.path.join('.', project_name, 'verilog_files')
        if not os.path.exists(projectPath):
                os.makedirs(projectPath)


        verilogPath = os.path.join(projectPath,fileName+".v")
        f = open(verilogPath, "w")
        f.write(circuit.print(process))
        f.close() # Close file so that P&R can access netlist

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



        design_area = (0, 0, design_limits[0], design_limits[1], x_offset, y_offset)

        if p_and_r == True:
                #drainmux_space_isle_idx = 0
                process_params = (tech_process, dbu, track_spacing, x_offset, y_offset, cell_pitch, drainmux_space_isle_idx, drainmux_space, gatemux_space_isle_idx, gatemux_space)
                pl_start = time.time()
                gds_synthesis(process_params, design_area, project_name, isle_loc=location_islands)
                pl_end = time.time()


                if qparams == None:
                        qdefpath = os.path.join(Path(__file__).parent,'qrouter_default.json')
                        with open(qdefpath) as file:
                                qrouterParams = json.load(file)
                else:
                        qrouterParams = qparams


                # Pick the detailed router and default to qrouter. If not available, check for Triton.
                qrouter = True if os.system('command -v qrouter') == 0 else False
                triton_route = os.path.exists(os.path.join('TritonRoute','build','TritonRoute'))
                lef_file = os.path.join(project_name, project_name + '.lef')
                def_file = os.path.join(project_name, project_name + '.def')
                report_file = os.path.join(project_name, project_name + '_report.txt')
                if qrouter and route==True:
                        base_cost = 10
                        out_file = os.path.join(project_name, project_name + '_qroute.def')
                        param_file = os.path.join(project_name, "qrouter_params.tcl")
                        info_file = os.path.join(project_name, "layers_info.lef") ##Added
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
                        #command = ['qrouter', '-s', param_file]
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        # Read the output in real-time
                        while True:
                                output = process.stdout.readline()
                                if output == '' and process.poll() is not None:
                                        break
                                if output:
                                        print(output.strip())
                        rt_end = time.time()

                ##############################################################################################################
                        # log_filename = os.path.join(project_name, "qrouter_full_log.txt")
                        # command = ['qrouter', '-noc', '-v', '2', '-s', param_file]
                        # #command = ['qrouter', '-v', '2', '-s', param_file]

                        # # 1. Open the file for writing
                        # with open(log_filename, "w") as log_file:
                        # 	# 2. Use stderr=subprocess.STDOUT to merge Errors and Output into one stream
                        # 	process = subprocess.Popen(
                        # 		command,
                        # 		stdout=subprocess.PIPE,
                        # 		stderr=subprocess.STDOUT,
                        # 		text=True,
                        # 		bufsize=1  # Line buffered
                        # 	)

                        # 	rt_start = time.time()

                        # 	# 3. Read the merged stream
                        # 	for line in iter(process.stdout.readline, ''):
                        # 		# Print to terminal
                        # 		print(line.strip())

                        # 		# Write to file
                        # 		log_file.write(line)
                        # 		log_file.flush() # Ensure it writes to disk immediately

                        # 	process.wait()
                        # 	rt_end = time.time()

                        # print(f"\nExecution finished in {rt_end - rt_start:.2f}s")
                        # print(f"Full report saved to: {log_filename}")

                ##############################################################################################################

                        gds_synthesis(process_params, design_area, project_name, routed_def=True, router_tool='qrouter')
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
