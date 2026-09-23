import json
import re
from ashes_fg.asic.pd_tools import get_pd_tool

def dict_to_tcl_brace(d):
    """Helper to convert {M1: 0.3} to { M1 0.3 }"""
    if not d: return "{ }"
    return "{ " + " ".join([f"{k} {v}" for k, v in d.items()]) + " }"

def _cadence_main(filepath, subdir="inputs"):
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

def _cadence_init(config_data, filepath, top_level="proj_name"):
    init_section = config_data.get("init", [])
    tlef_path, pwr_nets, gnd_nets, ndr_rules = [], "", "", []

    for entry in init_section:
        if "tlef_path" in entry:
            val = entry["tlef_path"]
            if isinstance(val, list):
                tlef_path.extend(val) # Add all elements if it's a list
            else:
                tlef_path.append(val) # Append if it's a single string
        if "pwr_nets" in entry: pwr_nets = entry["pwr_nets"].replace(",", " ")
        if "gnd_nets" in entry: gnd_nets = entry["gnd_nets"].replace(",", " ")
        if "ndr" in entry: ndr_rules = entry["ndr"]

    # Create a string for all the lef file path
    lef_files_str = " ".join([f'"{p}"' for p in tlef_path + ["../inputs/cells.lef"]])


    tcl = [
        "################### Read In Tech and Design Files ###################\n",
        f'set_db init_read_netlist_files [list "../inputs/{top_level}.v"]',
        f'set_db init_lef_files [list {lef_files_str}]',
        f'read_physical -lefs {{ {lef_files_str} }}',
        f'read_netlist ../inputs/{top_level}.v',
        "",
        #"set_multi_cpu_usage -local_cpu 16 -cpu_per_remote_host 16 -remote_host 8 -keep_license true",
        #"set_distributed_hosts -local",
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

def _cadence_pins(config_data, design_area, pin_signal_groups, filepath):
    pin_config_list = config_data.get("pins", [])
    full_pin_props = {}
    place_type = "side" 
    site = "core" 

    for item in pin_config_list:
        full_pin_props.update(item)
        if "place_type" in item:
            place_type = item["place_type"]
        if "site" in item:
            site = item["site"]
            
    edge_map = {"W": 0, "N": 1, "E": 2, "S": 3}
    
    # 1. Start with the Floorplan section
    tcl = [
        "######## Floorplan ########",
        f'create_floorplan -site {site} -core_size {design_area[2]/1000} {design_area[3]/1000} {design_area[0]/1000} {design_area[1]/1000} {design_area[0]/1000} {design_area[1]/1000} \n'
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

            # Correct the pin placement in opposite sides to match
            if side == "S" or side == "W":
                spread_direction = "counterclockwise"
            else:
                spread_direction = "clockwise"

                
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
                                  f"-spread_direction  {spread_direction} "
                                  f"-pin {pin_str} ")
            pin_tcl_buffer.append("set_db assign_pins_edit_in_batch false\n")

    # 3. Only append the Pin Assignment header and content if pins were actually found
    if pin_tcl_buffer:
        tcl.append("################### Pin Assignment ###################\n")
        tcl.extend(pin_tcl_buffer)

    # 4. Write to file
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))


def _cadence_power(config_data, filepath):
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

        
def _cadence_route(config_data, ndr_info, filepath):
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


def _cadence_signoff(config_data,filepath,top_level="proj_name"):
    sg_cfg = {}
    for item in config_data.get("signoff", []): sg_cfg.update(item)
    tcl = [
        f"write_netlist ../outputs/{top_level}.v",
        f"write_stream ../outputs/{top_level}.gds -map_file {sg_cfg.get('gds_map_file')} -lib_name DesignLib -unit {sg_cfg.get('unit')} -mode all",
        f"write_lef_abstract ../outputs/{top_level}.lef "
    ]
    with open(filepath, "w") as f:
        f.write("\n".join(tcl))


# OpenROAD uses the same PD configuration sections as the Cadence generator.
def _tcl_word(value):
    """Quote one Tcl word without executing paths, bus indices or substitutions."""
    text = str(value)
    for old, new in (("\\", "\\\\"), ('"', '\\"'), ("$", "\\$"),
                     ("[", "\\["), ("]", "\\]"), ("\n", "\\n"), ("\r", "\\r")):
        text = text.replace(old, new)
    return '"' + text + '"'


def _tcl_list(values):
    return '[list ' + ' '.join(_tcl_word(value) for value in values) + ']'


def _pd_section(config, name):
    section = config.get(name, [])
    if isinstance(section, dict):
        return section.copy()
    result = {}
    for item in section:
        for key, value in item.items():
            if key in ('tlef_path', 'liberty_path'):
                result.setdefault(key, []).extend(value if isinstance(value, list) else [value])
            else:
                result[key] = value
    return result


def _as_list(value):
    return value if isinstance(value, (list, tuple)) else [value]


def _write_openroad(filepath, lines):
    with open(filepath, 'w') as stream:
        stream.write('# Generated for OpenROAD; distances are in microns.\n')
        stream.write('\n'.join(lines) + '\n')


def _openroad_main(filepath, subdir):
    lines = ['set ashes_project [file dirname [file normalize [info script]]]',
             'file mkdir [file join $ashes_project run]',
             'file mkdir [file join $ashes_project outputs]',
             'cd [file join $ashes_project run]']
    for step in ('init', 'pins', 'power', 'route', 'signoff'):
        lines += [f'puts "--- Executing: {step}.tcl ---"',
                  f'source [file join $ashes_project run {_tcl_word(subdir)} {step}.tcl]']
    lines.append('puts "--- OpenROAD flow completed ---"')
    _write_openroad(filepath, lines)


def _openroad_init(config, filepath, top):
    cfg = _pd_section(config, 'init')
    lefs = _as_list(cfg.get('tlef_path', []))
    if not lefs:
        raise ValueError('OpenROAD requires init.tlef_path for the technology LEF.')
    lines = [f'read_lef {_tcl_word(path)}' for path in lefs]
    lines.append('read_lef ../inputs/cells.lef')
    lines.extend(f'read_liberty {_tcl_word(path)}' for path in _as_list(cfg.get('liberty_path', [])))
    lines += [f'read_verilog {_tcl_word("../inputs/" + top + ".v")}',
              f'link_design {_tcl_word(top)}',
              '# Merge ASHES placement and blockages while preserving netlist connectivity.',
              f'read_def -floorplan_initialize {_tcl_word("../inputs/" + top + ".def")}']
    for rule in cfg.get('ndr', []):
        command = f'create_ndr -name {_tcl_word(rule["name"])}'
        for prop in ('width', 'spacing'):
            if rule.get(prop):
                command += f' -{prop} ' + _tcl_list(v for pair in rule[prop].items() for v in pair)
        if rule.get('via'):
            command += ' -via ' + _tcl_list(_as_list(rule['via']))
        lines.append(command)
        for layer, count in rule.get('min_cut', {}).items():
            if int(count) != count or count < 1:
                raise ValueError('NDR min_cut counts must be positive integers.')
            lines += [f'set ashes_ndr [[ord::get_db_block] findNonDefaultRule {_tcl_word(rule["name"])}]',
                      f'set ashes_layer [[ord::get_db_tech] findLayer {_tcl_word(layer)}]',
                      'if {$ashes_layer == "NULL"} {error "Unknown NDR cut layer"}',
                      'if {[$ashes_layer getType] ne "CUT"} {error "NDR min_cut requires a cut layer"}',
                      f'$ashes_ndr setMinCuts $ashes_layer {int(count)}']
    _write_openroad(filepath, lines)


def _openroad_pins(config, area, groups, filepath):
    cfg = _pd_section(config, 'pins')
    if cfg.get('place_type', 'side') != 'side':
        raise ValueError('OpenROAD pin placement supports place_type="side".')
    x, y, width, height = (value / 1000 for value in area[:4])
    die_w, die_h = width + 2*x, height + 2*y
    # Match the existing Cadence core_size interpretation; preserve imported instances.
    command = (f'initialize_floorplan -die_area {{0 0 {die_w} {die_h}}} '
               f'-core_area {{{x} {y} {x+width} {y+height}}}')
    if cfg.get('site'):
        command += f' -site {_tcl_word(cfg["site"])}'
    lines = [command, 'make_tracks']
    for side in ('W', 'N', 'E', 'S'):
        signals = groups.get(side, [])
        if not signals or side not in cfg:
            continue
        props = cfg[side]
        layer = props.get('met_layer', 'M3')
        length = die_h if side in ('W', 'E') else die_w
        start, end = float(props.get('offset_start', 0.6)), float(props.get('offset_end', 0.6))
        if start < 0 or end < 0 or start + end >= length:
            raise ValueError(f'Invalid pin offsets on {side} edge.')
        for i, signal in enumerate(signals):
            pos = start + (length-start-end) * (i/(len(signals)-1) if len(signals)>1 else 0.5)
            px, py = {'W': (0, pos), 'E': (die_w, pos), 'S': (pos, 0), 'N': (pos, die_h)}[side]
            lines.append(f'place_pin -pin_name {_tcl_word(signal)} -layer {_tcl_word(layer)} '
                         f'-location {{{px} {py}}} -pin_size {{{props.get("pin_width", 0.3)} '
                         f'{props.get("pin_height", 0.3)}}} -force_to_die_boundary')
    _write_openroad(filepath, lines)


def _openroad_power(config, filepath):
    cfg = _pd_section(config, 'power')
    init = _pd_section(config, 'init')
    globals_cfg = cfg.get('power_globals', {})
    nets = globals_cfg.get('nets', ['VDD', 'GND'])
    if isinstance(nets, str):
        nets = nets.replace(',', ' ').split()
    if len(nets) < 2:
        raise ValueError('power_globals.nets must include power and ground.')
    def net_names(value):
        return value.replace(',', ' ').split() if isinstance(value, str) else list(value)
    powers = net_names(init.get('pwr_nets', nets[0]))
    grounds = net_names(init.get('gnd_nets', nets[-1]))
    if not powers or not grounds or set(powers) & set(grounds):
        raise ValueError('OpenROAD requires distinct power and ground nets.')
    lines = []
    for names, kind in ((powers, 'power'), (grounds, 'ground')):
        for net in names:
            lines.append(f'add_global_connection -net {_tcl_word(net)} '
                         f'-pin_pattern {_tcl_word("^" + re.escape(net) + "$")} -{kind}')
    lines.append('global_connect')
    route_type = globals_cfg.get('type', 'rings')
    if route_type not in ('rings', 'stripes'):
        raise ValueError('OpenROAD power_globals.type must be rings or stripes.')
    shapes = cfg.get(route_type, [])
    if shapes:
        if len(powers) != 1 or len(grounds) != 1 or set(nets) != set(powers + grounds):
            raise ValueError('OpenROAD PDN currently supports one power/ground pair; align init nets and power_globals.nets.')
        lines += [f'set_voltage_domain -name CORE -power {_tcl_word(powers[0])} -ground {_tcl_word(grounds[0])}',
                  'define_pdn_grid -name ashes_grid -voltage_domains {CORE}']
        for shape in shapes:
            if route_type == 'rings':
                if shape.get('center'):
                    raise ValueError('Centered Cadence rings need explicit OpenROAD offsets; set center=false.')
                lines.append('add_pdn_ring -grid ashes_grid -layers ' +
                             _tcl_list([shape['horiz_layer'], shape['vert_layer']]) +
                             f' -widths {shape["width"]} -spacings {shape["spacing"]} '
                             f'-core_offsets {shape["offset"]} -add_connect')
            else:
                if shape.get('direction'):
                    lines += [f'set ashes_layer [[ord::get_db_tech] findLayer {_tcl_word(shape["layer"])}]',
                              'if {$ashes_layer == "NULL"} {error "Unknown stripe layer"}',
                              f'if {{[string tolower [$ashes_layer getDirection]] ne {_tcl_word(shape["direction"].lower())}}} '
                              '{error "Stripe direction must match the technology LEF"}']
                pitch = shape.get('pitch', 2*(shape['width'] + shape['spacing']))
                lines.append(f'add_pdn_stripe -grid ashes_grid -layer {_tcl_word(shape["layer"])} '
                             f'-width {shape["width"]} -spacing {shape["spacing"]} -pitch {pitch} '
                             f'-offset {shape.get("start_offset", 0)} -number_of_straps {int(shape.get("no_of_sets", 1))}')
        for connection in cfg.get('connect', []):
            if len(connection) != 2:
                raise ValueError('Each power.connect entry must contain two layer names.')
            lines.append('add_pdn_connect -grid ashes_grid -layers ' + _tcl_list(connection))
        if not cfg.get('connect'):
            lines.append('puts "WARNING: Add power.connect layer pairs to connect the grid to cell power pins."')
        if globals_cfg.get('top_via_stack') or globals_cfg.get('bot_via_stack'):
            lines.append('puts "WARNING: Cadence via-stack limits are not translated; OpenROAD uses power.connect layer pairs."')
        lines.append('pdngen')
    _write_openroad(filepath, lines)


def _openroad_route(config, ndr_info, filepath):
    cfg = _pd_section(config, 'route')
    lines = []
    for net, rule in (ndr_info or {}).items():
        rule = 'ANALOG' if rule.lower() == 'default' else rule
        lines.append(f'assign_ndr -ndr {_tcl_word(rule)} -net {_tcl_word(net)}')
    if any('CLOCK' in rule.upper() for rule in (ndr_info or {}).values()):
        lines.append('puts "WARNING: OpenROAD NDRs do not reproduce Innovus clock shielding or SI repair."')
    bottom, top = cfg.get('bot_layer'), cfg.get('top_layer')
    if bool(bottom) != bool(top):
        raise ValueError('Specify both route.bot_layer and route.top_layer for OpenROAD.')
    if bottom and top:
        lines.append(f'set_routing_layers -signal {_tcl_word(bottom + "-" + top)}')
    lines.append('global_route -guide_file ../outputs/route.guide')
    if cfg.get('ant_dio_cell'):
        lines.append(f'repair_antennas {_tcl_word(cfg["ant_dio_cell"])}')
    lines += ['detailed_route -output_drc ../outputs/route_drc.rpt',
              'check_antennas -report_file ../outputs/antenna.rpt']
    _write_openroad(filepath, lines)


def _openroad_signoff(config, filepath, top):
    lines = [f'{command} {_tcl_word("../outputs/" + top + extension)}'
             for command, extension in (('write_db', '.odb'), ('write_def', '.def'),
                                        ('write_verilog', '.v'), ('write_abstract_lef', '.lef'))]
    lines.append('puts "OpenROAD outputs written. GDS stream-out requires the separate KLayout DEF-to-stream flow."')
    _write_openroad(filepath, lines)


def _generate_tcl(pd_tool, step, *args):
    tool = get_pd_tool(pd_tool)
    prefix = tool["tcl_prefix"]
    if not tool["external"] or not prefix:
        raise ValueError(f"{pd_tool!r} does not use external PD Tcl generation.")
    generator = globals().get(f"_{prefix}_{step}")
    if not callable(generator):
        raise ValueError(f"No {step} Tcl generator registered for {pd_tool!r}.")
    return generator(*args)

def generate_main_tcl(filepath, subdir="inputs", pd_tool="cadence"):
    return _generate_tcl(pd_tool, "main", filepath, subdir)


def generate_init_tcl(config_data, filepath, top_level="proj_name", pd_tool="cadence"):
    return _generate_tcl(pd_tool, "init", config_data, filepath, top_level)


def generate_pins_tcl(config_data, design_area, pin_signal_groups, filepath, pd_tool="cadence"):
    return _generate_tcl(pd_tool, "pins", config_data, design_area, pin_signal_groups, filepath)


def generate_power_tcl(config_data, filepath, pd_tool="cadence"):
    return _generate_tcl(pd_tool, "power", config_data, filepath)


def generate_route_tcl(config_data, ndr_info, filepath, pd_tool="cadence"):
    return _generate_tcl(pd_tool, "route", config_data, ndr_info, filepath)


def generate_signoff_tcl(config_data,filepath,top_level="proj_name", pd_tool="cadence"):
    return _generate_tcl(pd_tool, "signoff", config_data, filepath, top_level)
