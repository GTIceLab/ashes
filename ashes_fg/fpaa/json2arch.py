# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 11:54:06 2025

@author: lyang
"""

import json
import os
from lxml import etree
from collections import Counter

FPAA = "FPAA_35n"

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


if 9 in top["col_cab1"]:
    layout = etree.SubElement(root, "layout", width="9", height="9")
else:
    layout = etree.SubElement(root, "layout", width="7", height="7")
    
device = etree.SubElement(root, "device")
etree.SubElement(device,"sizing",R_minW_nmos=tech["R_minW_nmos"],R_minW_pmos=tech["R_minW_pmos"],ipin_mux_trans_size=tech["ipin_mux_trans_size"])
etree.SubElement(device,"timing",C_ipin_cblock=tech["C_ipin_cblock"],T_ipin_cblock=tech["T_ipin_cblock"])
etree.SubElement(device,"area",grid_logic_tile_area="30000.000000")
chan_width_distr = etree.SubElement(device,"chan_width_distr")
etree.SubElement(chan_width_distr,"io",width="1.000000")
etree.SubElement(chan_width_distr,"x",distr="uniform",peak="1.000000")
etree.SubElement(chan_width_distr,"y",distr="uniform",peak="1.000000")
etree.SubElement(device,"switch_block",type="subset",fs="3")

switchlist = etree.SubElement(root, "switchlist")
etree.SubElement(switchlist, "switch",type="mux",name="0",R=tech["R"],Cin=tech["Cin"],Cout=tech["Cout"],Tdel=tech["Tdel"],mux_trans_size=tech["mux_trans_size"],buf_size="1")

segmentlist = etree.SubElement(root,"segmentlist")
segment = etree.SubElement(segmentlist,"segment", freq="1.000000",length="1",type="bidir",Rmetal=tech["Rmetal"],Cmetal=tech["Cmetal"])
sb = etree.SubElement(segment,"sb", type="pattern")
sb.text = "1 1"
cb = etree.SubElement(segment,"cb", type="pattern")
cb.text = "1"
etree.SubElement(segment, "wire_switch", name="0")
etree.SubElement(segment, "opin_switch",name="0")


cabs = etree.SubElement(root,"complexblocklist")
io_pb = etree.SubElement(cabs, "pb_type", name="io", capacity="8")

# 3. Top-level ports for the IO block
etree.SubElement(io_pb, "input", name="outpad", num_pins="1")
etree.SubElement(io_pb, "output", name="inpad", num_pins="1")
etree.SubElement(io_pb, "clock", name="clock", num_pins="1")

# 4. Mode: inpad (Input Pad)
mode_in = etree.SubElement(io_pb, "mode", name="inpad")
pb_in = etree.SubElement(mode_in, "pb_type", name="inpad", blif_model=".input", num_pb="1")
etree.SubElement(pb_in, "output", name="inpad", num_pins="1")

inter_in = etree.SubElement(mode_in, "interconnect")
direct_in = etree.SubElement(inter_in, "direct", name="inpad", input="inpad.inpad", output="io.inpad")
delay_in = etree.SubElement(direct_in, "delay_constant", max="4.243e-11", in_port="inpad.inpad", out_port="io.inpad")

# 5. Mode: outpad (Output Pad)
mode_out = etree.SubElement(io_pb, "mode", name="outpad")
pb_out = etree.SubElement(mode_out, "pb_type", name="outpad", blif_model=".output", num_pb="1")
etree.SubElement(pb_out, "input", name="outpad", num_pins="1")

inter_out = etree.SubElement(mode_out, "interconnect")
direct_out = etree.SubElement(inter_out, "direct", name="outpad", input="io.outpad", output="outpad.outpad")
delay_out = etree.SubElement(direct_out, "delay_constant", max="1.394e-11", in_port="io.outpad", out_port="outpad.outpad")

# 6. Standard IO Configuration (Fc, Pin Locations, Grid Locations)
fc_in = etree.SubElement(io_pb, "fc_in", type="frac")
fc_in.text = "1"

fc_out = etree.SubElement(io_pb, "fc_out", type="frac")
fc_out.text = "1"

# Pin Locations
pinlocs = etree.SubElement(io_pb, "pinlocations", pattern="custom")
sides = ["left", "top", "right", "bottom"]
for side in sides:
    loc = etree.SubElement(pinlocs, "loc", side=side)
    loc.text = "io.outpad io.inpad io.clock"

# Grid Locations
gridlocs = etree.SubElement(io_pb, "gridlocations")
etree.SubElement(gridlocs, "loc", type="perimeter", priority="10")





type1 = etree.SubElement(cabs,"pb_type",name="cab1")
etree.SubElement(type1, "input",name="I",num_pins=top["cab1_in"])
etree.SubElement(type1, "input",name="si",num_pins="1")
etree.SubElement(type1, "output",name="O",num_pins="8")
etree.SubElement(type1, "output",name="so",num_pins="12")
etree.SubElement(type1,"clock",name="gnd",num_pins="1")
etree.SubElement(type1,"clock",name="vdd",num_pins="1")

names_before_symbol = [entry.split("__")[0] for entry in cab1]
frequencies = Counter(names_before_symbol)
cab1_dict = dict(frequencies)

for entry in cab1_dict:
    cab_device = etree.SubElement(type1,"pb_type",name=entry,num_pb=str(cab1_dict[entry]),blif_model="."+entry)
    etree.SubElement(cab_device,"input",name="in",num_pins=lib[entry]["In"])
    etree.SubElement(cab_device,"output",name="out",num_pins=lib[entry]["Out"])
    etree.SubElement(cab_device,"delay_constant",max=tech["delay_constant"],in_port=entry+".in",out_port=entry+".out")
    
cab_device = etree.SubElement(type1,"pb_type",name="volswc",num_pb="1",blif_model=".volswc")
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
    etree.SubElement(interconnect,"direct",name="volswc1",input="cab1.I["+str(int(top["cab1_in"])-1)+":0]",output="volswc.ci["+str(int(top["cab1_in"])-1)+":0]")
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
etree.SubElement(interconnect,"complete",name="crossbar2",input=cab_dev_out.rstrip(),output="cab1.O[5:0]")

fc_in = etree.SubElement(type1,"fc_in",type="frac")
fc_in.text = "1"
fc_out = etree.SubElement(type1,"fc_out",type="frac")
fc_out.text = "1"

etree.SubElement(type1, "pinlocations", pattern="spread")

gridlocations = etree.SubElement(type1, "gridlocations")
etree.SubElement(gridlocations,"loc",type="fill",priority="1")
    

if cab2!=[]:
    type2 = etree.SubElement(cabs,"pb_type",name="cab2")
    etree.SubElement(type2, "input",name="I",num_pins=top["cab2_in"])
    etree.SubElement(type2, "input",name="si",num_pins="1")
    etree.SubElement(type2, "output",name="O",num_pins="8")
    etree.SubElement(type2, "output",name="so",num_pins="12")
    etree.SubElement(type2,"clock",name="gnd",num_pins="1")
    etree.SubElement(type2,"clock",name="vdd",num_pins="1")
    
    names_before_symbol = [entry.split("__")[0] for entry in cab2]
    frequencies = Counter(names_before_symbol)
    cab2_dict = dict(frequencies)
    
    for entry in cab2_dict:
        cab_device = etree.SubElement(type2,"pb_type",name=entry,num_pb=str(cab2_dict[entry]),blif_model="."+entry)
        etree.SubElement(cab_device,"input",name="in",num_pins=lib[entry]["In"])
        etree.SubElement(cab_device,"output",name="out",num_pins=lib[entry]["Out"])
        etree.SubElement(cab_device,"delay_constant",max=tech["delay_constant"],in_port=entry+".in",out_port=entry+".out")
        
    cab_device = etree.SubElement(type2,"pb_type",name="volswc",num_pb="1",blif_model=".volswc")
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
        etree.SubElement(interconnect,"direct",name="volswc1",input="cab2.I["+str(int(top["cab2_in"])-1)+":0]",output="volswc.ci["+str(int(top["cab2_in"])-1)+":0]")
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
    etree.SubElement(interconnect,"complete",name="crossbar2",input=cab_dev_out.rstrip(),output="cab2.O[5:0]")
    
    fc_in = etree.SubElement(type2,"fc_in",type="frac")
    fc_in.text = "1"
    fc_out = etree.SubElement(type2,"fc_out",type="frac")
    fc_out.text = "1"
    
    etree.SubElement(type2, "pinlocations", pattern="spread")
    
    gridlocations = etree.SubElement(type2, "gridlocations")
    for i in top["col_cab2"]:
        etree.SubElement(gridlocations,"loc",type="col",start=str(i),priority="6")
































tree.write(
    FPAA+".xml", 
    pretty_print=True, 
    xml_declaration=True, 
    encoding="UTF-8"
)