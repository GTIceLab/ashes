import json
import re

def dict_to_tcl_brace(d):
    """Helper to convert {M1: 0.3} to { M1 0.3 }"""
    if not d: return "{ }"
    return "{ " + " ".join([f"{k} {v}" for k, v in d.items()]) + " }"

def generate_main_tcl(filepath, subdir="inputs"):
    tcl = [
        "###########################################################",
        "##  Main EDA Flow Execution Script",
        "###########################################################\n"
    ]
    flow_steps = ["init.tcl", "pins.tcl", "power.tcl", "route.tcl"]
    for step in flow_steps:
        # Construct path using forward slashes for TCL compatibility
        tcl.append(f"puts \"--- Executing: {step} ---\"")
        tcl.append(f"source {subdir}/{step}")
    
    tcl.append("\nputs \"--- Flow Completed Successfully ---\"")
    tcl.append("exit")

    with open(filepath, "w") as f:
        f.write("\n".join(tcl))

def generate_init_tcl(config_data, filepath, top_level="openMSP430"):
    init_section = config_data.get("init", [])
    tlef_path, pwr_nets, gnd_nets, ndr_rules = "", "", "", []

    for entry in init_section:
        if "tlef_path" in entry: tlef_path = entry["tlef_path"]
        if "pwr_nets" in entry: pwr_nets = entry["pwr_nets"].replace(",", " ")
        if "gnd_nets" in entry: gnd_nets = entry["gnd_nets"].replace(",", " ")
        if "ndr" in entry: ndr_rules = entry["ndr"]

    tcl = [
        "################### Read In Tech and Design Files ###################\n",
        f'set top_level "{top_level}"',
        f'set_db init_read_netlist_files [list "../inputs/${{top_level}}.v"]',
        f'set_db init_lef_files [list "{tlef_path}" "../inputs/cells.lef"]',
        f'read_physical -lefs "{tlef_path}" "../inputs/cells.lef"',
        f'read_netlist ../inputs/${{top_level}}.v',
        "",
        "set_multi_cpu_usage -local_cpu 16 -cpu_per_remote_host 16 -remote_host 8 -keep_license true",
        "set_distributed_hosts -local",
        f"set_db init_ground_nets {gnd_nets}",
        f"set_db init_power_nets {pwr_nets}",
        "init_design",
        f'read_def ../inputs/${{top_level}}.def\n',
        "################### Define NDRs ###################"
    ]

    for rule in ndr_rules:
        tcl.append(f"create_route_rule -name {rule.get('name')} \\")
        tcl.append(f"  -width {dict_to_tcl_brace(rule.get('width'))} \\")
        tcl.append(f"  -spacing {dict_to_tcl_brace(rule.get('spacing'))} \\")
        tcl.append(f"  -min_cut {dict_to_tcl_brace(rule.get('min_cut'))}")

    with open(filepath, "w") as f:
        f.write("\n".join(tcl))

def generate_pins_tcl(config_data, pin_signal_groups, filepath):
    pin_config_list = config_data.get("pins", [])
    full_pin_props = {}
    place_type = "side" 

    for item in pin_config_list:
        full_pin_props.update(item)
        if "place_type" in item:
            place_type = item["place_type"]

    edge_map = {"W": 0, "N": 1, "E": 2, "S": 3}
    tcl = ["################### Pin Assignment ###################\n"]

    for side, edge_id in edge_map.items():
        if side in full_pin_props and side in pin_signal_groups:
            props = full_pin_props[side]
            signals = pin_signal_groups[side]
            layer = re.search(r'\d+', props.get("met_layer", "3")).group()
            
            formatted_pins = [f"{{{s}}}" if "[" in s else s for s in signals]
            pin_str = "{ " + " ".join(formatted_pins) + " }"

            tcl.append(f"# {side} Side")
            tcl.append("set_db assign_pins_edit_in_batch true")
            
            # Added -offset_start and -offset_end here
            tcl.append(f"edit_pin -pin_width {props.get('pin_width', 0.3)} "
                       f"-pin_depth {props.get('pin_height', 0.3)} "
                       f"-edge {edge_id} -layer {layer} "
                       f"-spread_type {place_type} "
                       f"-offset_start {props.get('offset_start', 0.6)} "
                       f"-offset_end {props.get('offset_end', 0.6)} "
                       f"-spread_direction clockwise "
                       f"-pin {pin_str} ")
            
            tcl.append("set_db assign_pins_edit_in_batch false\n")

    with open(filepath, "w") as f:
        f.write("\n".join(tcl))

def generate_power_tcl(config_data, filepath):
    p_cfg = {}
    for item in config_data.get("power", []): p_cfg.update(item)
    nets = p_cfg.get("nets_order", "VDD GND").replace(",", " ")
    
    tcl = [
        "################### Power Ring ###################",
        f"set_db add_rings_stacked_via_top_layer {p_cfg.get('top_via_stack')}",
        f"set_db add_rings_stacked_via_bottom_layer {p_cfg.get('bot_via_stack')}",
        #Defaults
        f"set_db add_rings_target default ",
        f"set_db add_rings_extend_over_row 0 ",
        f"set_db add_rings_ignore_rows 0 ",
        f"set_db add_rings_avoid_short 0 ",
        f"set_db add_rings_skip_shared_inner_ring none ",
        f"set_db add_rings_via_using_exact_crossover_size 1 ",
        f"set_db add_rings_orthogonal_only true ",
        f"set_db add_rings_skip_via_on_pin {{ standardcell }} ",
        f"set_db add_rings_skip_via_on_wire_shape {{ noshape }} ",
        f"add_rings -nets {{ {nets} }} -type core_rings -follow core "
        f"-layer {{top {p_cfg.get('horiz_ly')} bottom {p_cfg.get('horiz_ly')} left {p_cfg.get('vert_ly')} right {p_cfg.get('vert_ly')}}} "
        f"-width {{top {p_cfg.get('met_width')} bottom {p_cfg.get('met_width')} left {p_cfg.get('met_width')} right {p_cfg.get('met_width')}}}"  
        f"-spacing {{top {p_cfg.get('net_spacing')} bottom {p_cfg.get('net_spacing')} left {p_cfg.get('net_spacing')} right {p_cfg.get('net_spacing')}}}" 
        f"-offset {{top {p_cfg.get('offset')} bottom {p_cfg.get('offset')} left {p_cfg.get('offset')} right {p_cfg.get('offset')}}}" 
        f"-center 0 -threshold 0 -jog_distance 0 -snap_wire_center_to_grid none"
    ]
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))

def generate_route_tcl(config_data, filepath):
    r_cfg = {}
    for item in config_data.get("route", []): r_cfg.update(item)
    tcl = [
        "################### Routing ###################",
        f"set_db route_antenna_cell_name {r_cfg.get('ant_dio_cell', 'ANT1')}",
        f"set_db design_top_routing_layer {r_cfg.get('top_layer')}",
        f"set_db design_bottom_routing_layer {r_cfg.get('bot_layer')}",
        f"set_db route_antenna_diode_insertion 1",
        f"set_db route_with_timing_driven 1",
        f"set_db route_with_eco 0",
        f"set_db route_with_litho_driven 1",
        f"set_db route_detail_post_route_litho_repair 1",
        f"set_db route_with_si_driven 1",
        f"set_db route_detail_auto_stop 0",
        f"set_db route_selected_net_only 0",
        f"set_db route_detail_end_iteration 10",
        f"set_db route_with_timing_driven true",
        f"set_db route_with_si_driven true",
        "route_design -global_detail"
    ]
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))