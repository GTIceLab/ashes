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
    flow_steps = ["init.tcl", "pins.tcl", "power.tcl", "route.tcl","signoff.tcl"]
    for step in flow_steps:
        # Construct path using forward slashes for TCL compatibility
        tcl.append(f"puts \"--- Executing: {step} ---\"")
        tcl.append(f"source {subdir}/{step}")
    
    tcl.append("\nputs \"--- Flow Completed Successfully ---\"")
    #tcl.append("exit")

    with open(filepath, "w") as f:
        f.write("\n".join(tcl))

def generate_init_tcl(config_data, filepath, top_level="proj_name"):
    init_section = config_data.get("init", [])
    tlef_path, pwr_nets, gnd_nets, ndr_rules = "", "", "", []

    for entry in init_section:
        if "tlef_path" in entry: tlef_path = entry["tlef_path"]
        if "pwr_nets" in entry: pwr_nets = entry["pwr_nets"].replace(",", " ")
        if "gnd_nets" in entry: gnd_nets = entry["gnd_nets"].replace(",", " ")
        if "ndr" in entry: ndr_rules = entry["ndr"]

    tcl = [
        "################### Read In Tech and Design Files ###################\n",
        f'set_db init_read_netlist_files [list "../inputs/{top_level}.v"]',
        f'set_db init_lef_files [list "{tlef_path}" "../inputs/cells.lef"]',
        f'read_physical -lefs "{tlef_path}" "../inputs/cells.lef"',
        f'read_netlist ../inputs/{top_level}.v',
        "",
        "set_multi_cpu_usage -local_cpu 16 -cpu_per_remote_host 16 -remote_host 8 -keep_license true",
        "set_distributed_hosts -local",
        f"set_db init_ground_nets {gnd_nets}",
        f"set_db init_power_nets {{{pwr_nets}}}",
        "init_design",
        f'read_def ../inputs/{top_level}.def\n',
        "################### Define NDRs ###################"
    ]

    for rule in ndr_rules:
        tcl.append(f"create_route_rule -name {rule.get('name')} \\")
        tcl.append(f"  -width {dict_to_tcl_brace(rule.get('width'))} \\")
        tcl.append(f"  -spacing {dict_to_tcl_brace(rule.get('spacing'))} \\")
        tcl.append(f"  -min_cut {dict_to_tcl_brace(rule.get('min_cut'))}")

    with open(filepath, "w") as f:
        f.write("\n".join(tcl))

import re

def generate_pins_tcl(config_data, design_area, pin_signal_groups, filepath):
    pin_config_list = config_data.get("pins", [])
    full_pin_props = {}
    place_type = "side" 

    for item in pin_config_list:
        full_pin_props.update(item)
        if "place_type" in item:
            place_type = item["place_type"]

    edge_map = {"W": 0, "N": 1, "E": 2, "S": 3}
    
    # 1. Start with the Floorplan section
    tcl = [
        "######## Floorplan ########",
        f'create_floorplan -site core -core_size {design_area[2]/1000} {design_area[3]/1000} {design_area[0]/1000} {design_area[1]/1000} {design_area[0]/1000} {design_area[1]/1000} \n'
    ]

    # 2. Buffer the Pin Assignment logic so we only add headers if pins exist
    pin_tcl_buffer = []

    for side, edge_id in edge_map.items():
        # Check if the side exists and if there are actually signals in that group
        if side in full_pin_props and side in pin_signal_groups:
            signals = pin_signal_groups[side]
            
            # Skip this side if the signals list is empty
            if not signals:
                continue
                
            props = full_pin_props[side]
            layer = re.search(r'\d+', props.get("met_layer", "3")).group()
            
            formatted_pins = [f"{{{s}}}" if "[" in s else s for s in signals]
            pin_str = "{ " + " ".join(formatted_pins) + " }"

            pin_tcl_buffer.append(f"# {side} Side")
            pin_tcl_buffer.append("set_db assign_pins_edit_in_batch true")
            pin_tcl_buffer.append(f"edit_pin -pin_width {props.get('pin_width', 0.3)} "
                                  f"-pin_depth {props.get('pin_height', 0.3)} "
                                  f"-edge {edge_id} -layer {layer} "
                                  f"-spread_type {place_type} "
                                  f"-offset_start {props.get('offset_start', 0.6)} "
                                  f"-offset_end {props.get('offset_end', 0.6)} "
                                  f"-spread_direction clockwise "
                                  f"-pin {pin_str} ")
            pin_tcl_buffer.append("set_db assign_pins_edit_in_batch false\n")

    # 3. Only append the Pin Assignment header and content if pins were actually found
    if pin_tcl_buffer:
        tcl.append("################### Pin Assignment ###################\n")
        tcl.extend(pin_tcl_buffer)

    # 4. Write to file
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))
def generate_power_tcl(config_data, filepath):
    # Get the main power block (assuming first item in list)
    power_entry = config_data.get("power", [{}])[0]
    
    # Extract Globals
    globals_cfg = power_entry.get("power_globals", {})
    nets_list = globals_cfg.get("nets", ["VDD", "GND"])
    nets_str = " ".join(nets_list)
    top_via = globals_cfg.get("top_via_stack", "M7")
    bot_via = globals_cfg.get("bot_via_stack", "M1")
    route_type = globals_cfg.get("type", "rings")

    tcl = []
    tcl.append("####################################################")
    tcl.append("## Power Routing Script (Generated)")
    tcl.append("####################################################\n")

    # 1. Global Via Settings
    tcl.append(f"set_db add_rings_stacked_via_top_layer {top_via}")
    tcl.append(f"set_db add_rings_stacked_via_bottom_layer {bot_via}")
    tcl.append(f"set_db add_stripes_stacked_via_top_layer {top_via}")
    tcl.append(f"set_db add_stripes_stacked_via_bottom_layer {bot_via}\n")

    if route_type == "rings":
        # 2. Process Rings
        rings = power_entry.get("rings", [])
        if rings:
            tcl.append("################### Power Rings ###################")
            for ring in rings:
                h_ly = ring.get("horiz_layer")
                v_ly = ring.get("vert_layer")
                wid  = ring.get("width")
                spc  = ring.get("spacing")
                off  = ring.get("offset")
                
                tcl.append(
                    f"add_rings -nets {{ {nets_str} }} -type core_rings -follow core "
                    f"-layer {{top {h_ly} bottom {h_ly} left {v_ly} right {v_ly}}} "
                    f"-width {{top {wid} bottom {wid} left {wid} right {wid}}} "
                    f"-spacing {{top {spc} bottom {spc} left {spc} right {spc}}} "
                    f"-offset {{top {off} bottom {off} left {off} right {off}}} "
                    f"-center {1 if ring.get('center') else 0} -threshold 0 -jog_distance 0 -snap_wire_center_to_grid none"
                )
            tcl.append("")

    if route_type == "stripes":
        # 3. Process Stripes
        stripes = power_entry.get("stripes", [])
        if stripes:
            tcl.append("################### Power Stripes ##################")
            #Default Conditions
            
            for stripe in stripes:
                layer = stripe.get("layer")
                direction = stripe.get("direction")
                width = stripe.get("width")
                spacing = stripe.get("spacing")
                sets = stripe.get("no_of_sets", 1)
                offset = stripe.get("start_offset", 0)
                
                # Using the command template you provided
                tcl.append(
                    f"add_stripes -nets {{ {nets_str} }} -layer {layer} -direction {direction} "
                    f"-width {width} -spacing {spacing} -number_of_sets {sets} "
                    f"-start_from bottom -start_offset {offset} -switch_layer_over_obs false "
                    f"-max_same_layer_jog_length 2 -pad_core_ring_top_layer_limit {top_via} "
                    f"-pad_core_ring_bottom_layer_limit {bot_via} -block_ring_top_layer_limit {top_via} "
                    f"-block_ring_bottom_layer_limit {bot_via} -use_wire_group 0 -snap_wire_center_to_grid none"
                )
            tcl.append("")
            tcl.append("update_power_vias -skip_via_on_pin standardcell -bottom_layer M1 -add_vias 1 -top_layer AP")
    # Write to file
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))
    print(f"Successfully generated: {filepath}")

        
def generate_route_tcl(config_data, ndr_info, filepath):
    """
    Generates a Cadence Tcl script for routing.
    Maps 'default' NDR rules to 'ANALOG' and generates one command per net.
    """
    # Flatten routing config
    r_cfg = {}
    for item in config_data.get("route", []):
        r_cfg.update(item)

    tcl = []
    tcl.append("################################################")
    tcl.append("## 1. Define Non-Default Rules (NDR) for Nets ##")
    tcl.append("################################################")

    if ndr_info:
        # Group nets by their rule
        rules_map = {}
        for net_name, rule in ndr_info.items():
            # CHANGE: If rule is 'default', reassign to 'ANALOG'
            effective_rule = "ANALOG" if rule.lower() == "default" else rule
            rules_map.setdefault(effective_rule, []).append(net_name)

        for rule, nets in rules_map.items():
            for net in nets:
                # Rule Logic for CLOCK
                if "CLOCK" in rule.upper():
                    tcl.append(f"set_route_attributes -nets {{{net}}} \\")
                    tcl.append(f"   -route_rule {rule} -shield_nets GND -shield_side two_sides \\")
                    tcl.append(f"   -top_preferred_routing_layer {r_cfg.get('top_layer', 'M7')} \\")
                    tcl.append(f"   -bottom_preferred_routing_layer {r_cfg.get('bot_layer', 'M4')} \\")
                    tcl.append(f"   -si_post_route_fix true")
                
                # Rule Logic for ANALOG (including the former 'default' nets)
                elif "ANALOG" in rule.upper():
                    tcl.append(f"set_route_attributes -nets {{{net}}} \\")
                    tcl.append(f"   -route_rule {rule} \\")
                    # You can add specific analog constraints here if needed, e.g.:
                    # tcl.append(f"   -top_preferred_routing_layer {r_cfg.get('top_layer', 'M7')} \\")
                    tcl.append(f"   -si_post_route_fix true")
                
                # All other rules
                else:
                    tcl.append(f"set_route_attributes -nets {{{net}}} \\")
                    tcl.append(f"   -route_rule {rule}  \\")
                    tcl.append(f"   -si_post_route_fix true")
    else:
        tcl.append("# No non-default rules defined.")
    
    
    tcl.append("\n################################################")
    tcl.append("## 2. Routing Configuration                   ##")
    tcl.append("################################################")
    
    # List of database settings
    settings = [
        ("route_antenna_cell_name", r_cfg.get('ant_dio_cell')),
        ("design_top_routing_layer", r_cfg.get('top_layer')),
        ("design_bottom_routing_layer", r_cfg.get('bot_layer')),
        ("route_antenna_diode_insertion", "1"),
        ("route_with_timing_driven", "true"),
        ("route_with_si_driven", "true"),
        ("route_with_litho_driven", "1"),
        ("route_detail_post_route_litho_repair", "1"),
        ("route_detail_auto_stop", "0"),
        ("route_selected_net_only", "0"),
        ("route_detail_end_iteration", "10"),
        ("route_with_eco", "0")
    ]

    for db_name, value in settings:
        if value is not None:
            tcl.append(f"set_db {db_name} {value}")

    tcl.append("\n################################################")
    tcl.append("## 3. Execute Routing                         ##")
    tcl.append("################################################")
    tcl.append("route_design -global_detail")

    with open(filepath, "w") as f:
        f.write("\n".join(tcl))


def generate_signoff_tcl(config_data,filepath,top_level="proj_name"):
    sg_cfg = {}
    for item in config_data.get("signoff", []): sg_cfg.update(item)
    tcl = [
        f"write_netlist ../outputs/{top_level}.v",
        f"write_stream ../outputs/{top_level}.gds -map_file {sg_cfg.get('gds_map_file')} -lib_name DesignLib -unit {sg_cfg.get('unit')} -mode all",
        f"write_lef_abstract ../outputs/{top_level}.lef "
    ]
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))
