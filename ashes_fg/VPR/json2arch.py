# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 11:54:06 2025

@author: lyang
"""

import json
import os
from lxml import etree
from collections import Counter
import math

FPAA = "FPAA_35"

with open(FPAA+".json","r") as j:
    top = json.load(j)
    
with open("analog_std_cells.json","r") as l:
    lib = json.load(l)
    
with open(top["foundry"]+"_"+top["process_node"]+"_Tech.json") as t:
    tech = json.load(t)
    
root = etree.Element("architecture")
tree = etree.ElementTree(root)


if "cab2" in top:
    cab2 = top["cab2"]
    cab1 = top["cab1"]
else:
    cab1 = top["cab1"]
    cab2=[]


seen_models = set()
seen_models_cab1 = set()
models_container = etree.SubElement(root, "models")
for entry in cab1:
    if "__" in entry:
        entry_trim = entry.split("__")[0]
        seen_models_cab1.add(entry_trim)
        seen_models.add(entry_trim)
    else:
        seen_models_cab1.add(entry)
        seen_models.add(entry)
        
seen_models_cab2 = set()
for entry in cab2:
    if "__" in entry:
        entry_trim = entry.split("__")[0]
        seen_models_cab2.add(entry_trim)
        seen_models.add(entry_trim)
    else:
        seen_models_cab2.add(entry)
        seen_models.add(entry)
        
        
for entry in seen_models:
    model_node = etree.SubElement(models_container, "model", name=entry)
    input_ports=etree.SubElement(model_node, "input_ports")
    etree.SubElement(input_ports,"port",name="in")
    output_ports=etree.SubElement(model_node, "output_ports")
    etree.SubElement(output_ports,"port",name="out")
    
model_node = etree.SubElement(models_container, "model", name="volswc")
input_ports=etree.SubElement(model_node, "input_ports")
etree.SubElement(input_ports,"port",name="in")
etree.SubElement(input_ports,"port",name="ci")
output_ports=etree.SubElement(model_node, "output_ports")
etree.SubElement(output_ports,"port",name="out")
etree.SubElement(output_ports,"port",name="co")


# ==========================================
# 1. TILES SECTION (Physical definitions)
# ==========================================
tiles = etree.SubElement(root, "tiles")

# --- IO Tile ---
tile_io = etree.SubElement(tiles, "tile", name="io", area="0")
sub_io = etree.SubElement(tile_io, "sub_tile", name="io")
eq_sites_io = etree.SubElement(sub_io, "equivalent_sites")
etree.SubElement(eq_sites_io, "site", pb_type="io", pin_mapping="direct")

if FPAA == "FPAA_35p":
    etree.SubElement(sub_io, "input", name="outpad", num_pins="8", is_non_clock_global="false")
    etree.SubElement(sub_io, "output", name="inpad", num_pins="8")
else:
    etree.SubElement(sub_io, "input", name="outpad", num_pins="20", is_non_clock_global="false")
    etree.SubElement(sub_io, "output", name="inpad", num_pins="20")
etree.SubElement(sub_io, "fc", in_type="abs", in_val="2", out_type="abs", out_val="2")
pinlocs_io = etree.SubElement(sub_io, "pinlocations", pattern="custom")
for side in ["left", "top", "right", "bottom"]:
    loc = etree.SubElement(pinlocs_io, "loc", side=side)
    loc.text = "io.outpad io.inpad"

# --- CAB1 Tile ---
tile_cab1 = etree.SubElement(tiles, "tile", name="cab1", area="30000")
sub_cab1 = etree.SubElement(tile_cab1, "sub_tile", name="cab1")
eq_sites_cab1 = etree.SubElement(sub_cab1, "equivalent_sites")
etree.SubElement(eq_sites_cab1, "site", pb_type="cab1", pin_mapping="direct")
etree.SubElement(sub_cab1, "input", name="I", num_pins=str(top["cab1_in"]), is_non_clock_global="false")
etree.SubElement(sub_cab1, "input", name="si", num_pins="1")
etree.SubElement(sub_cab1, "output", name="O", num_pins="8")
etree.SubElement(sub_cab1, "output", name="so", num_pins="12")
etree.SubElement(sub_cab1, "fc", in_type="frac", in_val="1.0", out_type="frac", out_val="1.0")

pin_locations = etree.SubElement(sub_cab1, "pinlocations", pattern="custom")
cab1_in_val = int(top["cab1_in"])

if cab1_in_val % 4 == 0:
    left_pin = int(cab1_in_val/4)
    top_pin = int(cab1_in_val/4)
    right_pin = int(cab1_in_val/4)
    bot_pin = int(cab1_in_val/4)
elif cab1_in_val % 4 == 1:
    left_pin = math.ceil(cab1_in_val/4)
    top_pin = math.floor(cab1_in_val/4)
    right_pin = math.floor(cab1_in_val/4)
    bot_pin = math.floor(cab1_in_val/4)
elif cab1_in_val % 4 == 2:
    left_pin = math.ceil(cab1_in_val/4)
    top_pin = math.ceil(cab1_in_val/4)
    right_pin = math.floor(cab1_in_val/4)
    bot_pin = math.floor(cab1_in_val/4)
else:
    left_pin = math.ceil(cab1_in_val/4)
    top_pin = math.ceil(cab1_in_val/4)
    right_pin = math.ceil(cab1_in_val/4)
    bot_pin = math.floor(cab1_in_val/4)

if FPAA=="FPAA_35p":
    loc_left = etree.SubElement(pin_locations, "loc", side="left")
    loc_left.text = "cab1.I[0] cab1.O[3:0] cab1.si cab1.so[2:0]"
    loc_top = etree.SubElement(pin_locations, "loc", side="top")
    loc_top.text = "cab1.I[1] cab1.so[5:3]"
    loc_right = etree.SubElement(pin_locations, "loc", side="right")
    loc_right.text = "cab1.I[2] cab1.so[8:6]"
    loc_bottom = etree.SubElement(pin_locations, "loc", side="bottom")
    loc_bottom.text = "cab1.I[3] cab1.O[7:4] cab1.so[11:9]"
else:    
    pin_counter = 0
    loc_left = etree.SubElement(pin_locations, "loc", side="left")
    loc_left.text = "cab1.I["+str(left_pin-1)+":"+str(pin_counter)+"] cab1.O[3:0] cab1.si cab1.so[2:0]"
    pin_counter += left_pin
    loc_top = etree.SubElement(pin_locations, "loc", side="top")
    loc_top.text = "cab1.I["+str(pin_counter+top_pin-1)+":"+str(pin_counter)+"] cab1.so[5:3]"
    pin_counter += top_pin
    loc_right = etree.SubElement(pin_locations, "loc", side="right")
    if FPAA=="FPAA_35n":
        loc_right.text = "cab1.I[4] cab1.so[8:6]"
    else:
        loc_right.text = "cab1.I["+str(pin_counter+right_pin-1)+":"+str(pin_counter)+"] cab1.so[8:6]"
        pin_counter += right_pin
    loc_bottom = etree.SubElement(pin_locations, "loc", side="bottom")
    if FPAA=="FPAA_35n":
        loc_bottom.text = "cab1.I[5] cab1.O[7:4] cab1.so[11:9]"
    else:
        loc_bottom.text = "cab1.I["+str(pin_counter+bot_pin-1)+":"+str(pin_counter)+"] cab1.O[7:4] cab1.so[11:9]"

# --- CAB2 Tile ---
if cab2!=[]:
    tile_cab2 = etree.SubElement(tiles, "tile", name="cab2", area="30000")
    sub_cab2 = etree.SubElement(tile_cab2, "sub_tile", name="cab2")
    eq_sites_cab2 = etree.SubElement(sub_cab2, "equivalent_sites")
    etree.SubElement(eq_sites_cab2, "site", pb_type="cab2", pin_mapping="direct")
    etree.SubElement(sub_cab2, "input", name="I", num_pins=str(top["cab2_in"]), is_non_clock_global="false")
    etree.SubElement(sub_cab2, "input", name="si", num_pins="1")
    etree.SubElement(sub_cab2, "output", name="O", num_pins="8")
    etree.SubElement(sub_cab2, "output", name="so", num_pins="12")
    etree.SubElement(sub_cab2, "fc", in_type="frac", in_val="1.0", out_type="frac", out_val="1.0")
    
    pin_locations2 = etree.SubElement(sub_cab2, "pinlocations", pattern="custom")
    cab2_in_val = int(top["cab2_in"])

    if cab2_in_val % 4 == 0:
        left_pin2 = int(cab2_in_val/4)
        top_pin2 = int(cab2_in_val/4)
        right_pin2 = int(cab2_in_val/4)
        bot_pin2 = int(cab2_in_val/4)
    elif cab2_in_val % 4 == 1:
        left_pin2 = math.ceil(cab2_in_val/4)
        top_pin2 = math.floor(cab2_in_val/4)
        right_pin2 = math.floor(cab2_in_val/4)
        bot_pin2 = math.floor(cab2_in_val/4)
    elif cab2_in_val % 4 == 2:
        left_pin2 = math.ceil(cab2_in_val/4)
        top_pin2 = math.ceil(cab2_in_val/4)
        right_pin2 = math.floor(cab2_in_val/4)
        bot_pin2 = math.floor(cab2_in_val/4)
    else:
        left_pin2 = math.ceil(cab2_in_val/4)
        top_pin2 = math.ceil(cab2_in_val/4)
        right_pin2 = math.ceil(cab2_in_val/4)
        bot_pin2 = math.floor(cab2_in_val/4)
        
    pin_counter2 = 0
    loc_left2 = etree.SubElement(pin_locations2, "loc", side="left")
    loc_left2.text = "cab2.I["+str(left_pin2-1)+":"+str(pin_counter2)+"] cab2.O[3:0] cab2.si cab2.so[2:0]"
    pin_counter2 += left_pin2
    
    loc_top2 = etree.SubElement(pin_locations2, "loc", side="top")
    loc_top2.text = "cab2.I["+str(pin_counter2+top_pin2-1)+":"+str(pin_counter2)+"] cab2.so[5:3]"
    pin_counter2 += top_pin2
    
    loc_right2 = etree.SubElement(pin_locations2, "loc", side="right")
    loc_right2.text = "cab2.I["+str(pin_counter2+right_pin2-1)+":"+str(pin_counter2)+"] cab2.so[8:6]"
    pin_counter2 += right_pin2
    
    loc_bottom2 = etree.SubElement(pin_locations2, "loc", side="bottom")
    loc_bottom2.text = "cab2.I["+str(pin_counter2+bot_pin2-1)+":"+str(pin_counter2)+"] cab2.O[7:4] cab2.so[11:9]"


# ==========================================
# 2. LAYOUT SECTION (Grid assignments)
# ==========================================
layout = etree.SubElement(root, "layout")

if FPAA == "FPAA_35p":
    fixed_layout = etree.SubElement(layout, "fixed_layout", name="device", width="11", height="11")
else:
    fixed_layout = etree.SubElement(layout, "fixed_layout", name="device", width="9", height="9")
    
etree.SubElement(fixed_layout, "fill", type="cab1", priority="10")
etree.SubElement(fixed_layout, "perimeter", type="io", priority="100")

if cab2!=[]:
    for i in top["col_cab2"]:
        etree.SubElement(fixed_layout, "col", type="cab2", startx=str(i), priority="50")


# ==========================================
# 3. DEVICE & NETWORKS (Switch/Segment)
# ==========================================
device = etree.SubElement(root, "device")
etree.SubElement(device,"sizing",R_minW_nmos=tech["R_minW_nmos"],R_minW_pmos=tech["R_minW_pmos"])
etree.SubElement(device,"connection_block",input_switch_name="ipin_cblock")
etree.SubElement(device,"area",grid_logic_tile_area="30000.000000")
chan_width_distr = etree.SubElement(device,"chan_width_distr")
etree.SubElement(chan_width_distr,"x",distr="uniform",peak="1.000000")
etree.SubElement(chan_width_distr,"y",distr="uniform",peak="2.000000")
etree.SubElement(device,"switch_block",type="subset",fs="3")

switchlist = etree.SubElement(root, "switchlist")
etree.SubElement(switchlist, "switch",type="mux",name="0",R=tech["R"],Cin=tech["Cin"],Cout=tech["Cout"],Tdel=tech["Tdel"],mux_trans_size=tech["mux_trans_size"],buf_size="1")
etree.SubElement(switchlist, "switch",type="mux",name="delayless_switch",R='0',Cin='0',Cout='0',Tdel='0',mux_trans_size='0',buf_size="1")
etree.SubElement(switchlist, "switch",type="mux",name="ipin_cblock",R='0',Cin=tech["C_ipin_cblock"],Cout='0',Tdel=tech["T_ipin_cblock"],buf_size="1")

segmentlist = etree.SubElement(root,"segmentlist")
segment = etree.SubElement(segmentlist,"segment", name="SC",freq="1",length="1",type="bidir", axis="y", Rmetal=tech["Rmetal"],Cmetal=tech["Cmetal"])
sb = etree.SubElement(segment,"sb", type="pattern")
sb.text = "0 0"
cb = etree.SubElement(segment,"cb", type="pattern")
cb.text = "1"
etree.SubElement(segment, "wire_switch", name="0")
etree.SubElement(segment, "opin_switch",name="0")

S_short = etree.SubElement(segmentlist,"segment", name="SS",freq="1",length="1",type="bidir",axis="y",Rmetal="0",Cmetal="0")
sb = etree.SubElement(S_short,"sb", type="pattern")
sb.text = "0 0"
cb = etree.SubElement(S_short,"cb", type="pattern")
cb.text = "0"
etree.SubElement(S_short, "wire_switch", name="delayless_switch")
etree.SubElement(S_short, "opin_switch",name="delayless_switch")

C_short = etree.SubElement(segmentlist,"segment", name="CS",freq="1",length="1",type="bidir",axis="x",Rmetal=tech["Rmetal"],Cmetal=tech["Cmetal"])
sb = etree.SubElement(C_short,"sb", type="pattern")
sb.text = "0 0"
cb = etree.SubElement(C_short,"cb", type="pattern")
cb.text = "1"
etree.SubElement(C_short, "wire_switch", name="0")
etree.SubElement(C_short, "opin_switch",name="0")




# ==========================================
# 4. COMPLEXBLOCKLIST (Logical definitions)
# ==========================================
cabs = etree.SubElement(root,"complexblocklist")

# --- IO Complex Block ---
io_pb = etree.SubElement(cabs, "pb_type", name="io")
if FPAA == "FPAA_35p":
    etree.SubElement(io_pb, "input", name="outpad", num_pins="8")
    etree.SubElement(io_pb, "output", name="inpad", num_pins="8")
else:
    etree.SubElement(io_pb, "input", name="outpad", num_pins="20")
    etree.SubElement(io_pb, "output", name="inpad", num_pins="20")

if FPAA == "FPAA_35p":
    io_cell = etree.SubElement(io_pb, "pb_type", name="io_cell", num_pb="8")
else:
    io_cell = etree.SubElement(io_pb, "pb_type", name="io_cell", num_pb="20")
etree.SubElement(io_cell, "input", name="outpad", num_pins="1")
etree.SubElement(io_cell, "output", name="inpad", num_pins="1")

mode_in = etree.SubElement(io_cell, "mode", name="inpad")
pb_in = etree.SubElement(mode_in, "pb_type", name="inpad", blif_model=".input", num_pb="1")
etree.SubElement(pb_in, "output", name="inpad", num_pins="1")

inter_in = etree.SubElement(mode_in, "interconnect")
direct_in = etree.SubElement(inter_in, "direct", name="inpad", input="inpad.inpad", output="io_cell.inpad")
etree.SubElement(direct_in, "delay_constant", max=tech["Tdel"], in_port="inpad.inpad", out_port="io_cell.inpad")

mode_out = etree.SubElement(io_cell, "mode", name="outpad")
pb_out = etree.SubElement(mode_out, "pb_type", name="outpad", blif_model=".output", num_pb="1")
etree.SubElement(pb_out, "input", name="outpad", num_pins="1")

inter_out = etree.SubElement(mode_out, "interconnect")
direct_out = etree.SubElement(inter_out, "direct", name="outpad", input="io_cell.outpad", output="outpad.outpad")
etree.SubElement(direct_out, "delay_constant", max=tech["Tdel"], in_port="io_cell.outpad", out_port="outpad.outpad")

inter_io = etree.SubElement(io_pb, "interconnect")
etree.SubElement(inter_io, "direct", name="outpad_direct", input="io.outpad", output="io_cell.outpad")
etree.SubElement(inter_io, "direct", name="inpad_direct", input="io_cell.inpad", output="io.inpad")

# --- CAB1 Complex Block ---
type1 = etree.SubElement(cabs,"pb_type",name="cab1")
etree.SubElement(type1, "input",name="I",num_pins=str(top["cab1_in"]))
etree.SubElement(type1, "input",name="si",num_pins="1")
etree.SubElement(type1, "output",name="O",num_pins="8")
etree.SubElement(type1, "output",name="so",num_pins="12")

names_before_symbol = [entry.split("__")[0] for entry in cab1]
frequencies = Counter(names_before_symbol)
cab1_dict = dict(frequencies)

for entry in cab1_dict:
    cab_device = etree.SubElement(type1,"pb_type",name=entry,num_pb=str(cab1_dict[entry]),blif_model=".subckt "+entry)
    etree.SubElement(cab_device,"input",name="in",num_pins=lib[entry]["In"])
    etree.SubElement(cab_device,"output",name="out",num_pins=lib[entry]["Out"])
    etree.SubElement(cab_device,"delay_constant",max=tech["delay_constant"],in_port=entry+".in",out_port=entry+".out")
    
cab_device = etree.SubElement(type1,"pb_type",name="volswc",num_pb="1",blif_model=".subckt volswc")
etree.SubElement(cab_device,"input",name="in",num_pins="12")
etree.SubElement(cab_device,"input",name="ci",num_pins="8")
etree.SubElement(cab_device,"output",name="out",num_pins="1")
etree.SubElement(cab_device,"output",name="co",num_pins="8")
etree.SubElement(cab_device,"delay_constant",max=tech["delay_constant"],in_port="volswc.in",out_port="volswc.out")

interconnect = etree.SubElement(type1,"interconnect")
if int(top["cab1_in"])>=12:
    etree.SubElement(interconnect,"direct",name="volswc1",input="cab1.I[11:0]",output="volswc.in[11:0]")
else:
    etree.SubElement(interconnect,"direct",name="volswc1",input="cab1.I["+str(int(top["cab1_in"])-1)+":0]",output="volswc.in["+str(int(top["cab1_in"])-1)+":0]")
if int(top["cab1_in"])>=8:
    etree.SubElement(interconnect,"direct",name="volswc2",input="cab1.I[7:0]",output="volswc.ci[7:0]")
else:
    etree.SubElement(interconnect,"direct",name="volswc2",input="cab1.I["+str(int(top["cab1_in"])-1)+":0]",output="volswc.ci["+str(int(top["cab1_in"])-1)+":0]")
etree.SubElement(interconnect,"direct",name="volswc3",input="volswc.co[7:0]",output="cab1.O[7:0]")
cab_dev_out = "cab1.I["+str(int(top["cab1_in"])-1)+":0] "
cab_dev_in = ""
for i in seen_models_cab1:
    if cab1_dict[i] == 1:
        cab_dev_out += i+".out "
        cab_dev_in += i+".in "
    else:
        cab_dev_out += i+"["+str(cab1_dict[i]-1)+":0].out "
        cab_dev_in += i+"["+str(cab1_dict[i]-1)+":0].in "
etree.SubElement(interconnect,"complete",name="crossbar1",input=cab_dev_out.rstrip(),output=cab_dev_in.rstrip())
etree.SubElement(interconnect,"complete",name="crossbar2",input=cab_dev_out.rstrip(),output="cab1.O[7:0]")

# --- CAB2 Complex Block ---
if cab2!=[]:
    type2 = etree.SubElement(cabs,"pb_type",name="cab2")
    etree.SubElement(type2, "input",name="I",num_pins=str(top["cab2_in"]))
    etree.SubElement(type2, "input",name="si",num_pins="1")
    etree.SubElement(type2, "output",name="O",num_pins="8")
    etree.SubElement(type2, "output",name="so",num_pins="12")
    
    names_before_symbol = [entry.split("__")[0] for entry in cab2]
    frequencies = Counter(names_before_symbol)
    cab2_dict = dict(frequencies)
    
    for entry in cab2_dict:
        cab_device = etree.SubElement(type2,"pb_type",name=entry,num_pb=str(cab2_dict[entry]),blif_model=".subckt "+entry)
        etree.SubElement(cab_device,"input",name="in",num_pins=lib[entry]["In"])
        etree.SubElement(cab_device,"output",name="out",num_pins=lib[entry]["Out"])
        etree.SubElement(cab_device,"delay_constant",max=tech["delay_constant"],in_port=entry+".in",out_port=entry+".out")
        
    cab_device = etree.SubElement(type2,"pb_type",name="volswc",num_pb="1",blif_model=".subckt volswc")
    etree.SubElement(cab_device,"input",name="in",num_pins="12")
    etree.SubElement(cab_device,"input",name="ci",num_pins="8")
    etree.SubElement(cab_device,"output",name="out",num_pins="1")
    etree.SubElement(cab_device,"output",name="co",num_pins="8")
    etree.SubElement(cab_device,"delay_constant",max=tech["delay_constant"],in_port="volswc.in",out_port="volswc.out")
    
    interconnect = etree.SubElement(type2,"interconnect")
    if int(top["cab2_in"])>=12:
        etree.SubElement(interconnect,"direct",name="volswc1",input="cab2.I[11:0]",output="volswc.in[11:0]")
    else:
        etree.SubElement(interconnect,"direct",name="volswc1",input="cab2.I["+str(int(top["cab2_in"])-1)+":0]",output="volswc.in["+str(int(top["cab2_in"])-1)+":0]")
    if int(top["cab2_in"])>=8:
        etree.SubElement(interconnect,"direct",name="volswc2",input="cab2.I[7:0]",output="volswc.ci[7:0]")
    else:
        etree.SubElement(interconnect,"direct",name="volswc2",input="cab2.I["+str(int(top["cab2_in"])-1)+":0]",output="volswc.ci["+str(int(top["cab2_in"])-1)+":0]")
    etree.SubElement(interconnect,"direct",name="volswc3",input="volswc.co[7:0]",output="cab2.O[7:0]")
    cab_dev_out = "cab2.I["+str(int(top["cab2_in"])-1)+":0] "
    cab_dev_in = ""
    for i in seen_models_cab2:
        if cab2_dict[i] == 1:
            cab_dev_out += i+".out "
            cab_dev_in += i+".in "
        else:
            cab_dev_out += i+"["+str(cab2_dict[i]-1)+":0].out "
            cab_dev_in += i+"["+str(cab2_dict[i]-1)+":0].in "
    etree.SubElement(interconnect,"complete",name="crossbar1",input=cab_dev_out.rstrip(),output=cab_dev_in.rstrip())
    etree.SubElement(interconnect,"complete",name="crossbar2",input=cab_dev_out.rstrip(),output="cab2.O[7:0]")

# Write XML structure to file
tree.write(
    FPAA+".xml", 
    pretty_print=True, 
    xml_declaration=True, 
    encoding="UTF-8"
)