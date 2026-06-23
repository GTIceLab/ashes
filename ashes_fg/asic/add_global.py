#!/usr/bin/env python3
import os
from ashes_fg.asic.asic_compile import Port
from ashes_fg.asic.asic_compile import Pin
import ashes_fg.asic.asic_compile as ac
import json

class DynamicPort(Port):
    """
    Port which updates pin number to match max count
    """
    def __init__(self,circuit,cell,name,location,static = False):
        self.circuit = circuit
        self.name = name
        self.location = location
        self.cell = cell
        self.isStatic = static

        self.pins = []

    # Only allow assignment by loop
    def connectPort(self,connection):
        if isinstance(connection,Port) or isinstance(connection,list):
            # If less pins in current Port
            if len(self.pins) < len(connection):
                # Add pins to match
                for i in range(len(self.connection)-len(self.pins)):
                    self.pins.append(Pin(self.circuit,self,None))

            # Assign pins
            for i in range(0,len(connection)):
                self.assignPin(i,connection[i])
        elif isinstance(connection,Pin):
            raise Exception("Cannot short dynamic port")
        else:
            raise Exception("Invalid Assignment")

    def appendPin(self,addPin):
        newPin = self.pins.append(Pin(self.circuit,self,None))
        addPin += newPin

    def __getitem__(self,key):
        if key+1 > len(self.pins):
            self.pins.append(Pin(self.circuit,self,None))

        return self.pins[key]

def add_global_frame(Top,frame,global_net_path):
    with open(global_net_path) as f:
        global_ports = json.load(f)

    # Special Power Pins
    VINJ_N = frame.createPort("N","vinj")
    VINJ_N += Top.ports["VINJ"]
    VINJ_S = frame.createPort("S","vinj")
    VINJ_S += Top.ports["VINJ"]
    GND_N = frame.createPort("N","gnd")
    GND_N += Top.ports["GND"]
    GND_S = frame.createPort("S","gnd")
    GND_S += Top.ports["GND"]

    for key,p in Top.ports.items():
        if p.name.lower() != "vinj" and p.name.lower() != "gnd":
            newPort = frame.createPort(global_ports[key][1],p.name,len(p))
            newPort += p

    return True

def add_global(Top,global_net_path):
    with open(global_net_path) as f:
        global_ports = json.load(f)

    Top.ports = {}

    for portName, portInfo in global_ports.items():
        portNum = portInfo[0]
        if portNum > 0:
            newPort = ac.Port(Top,None,portName,None,portNum)
        else:
            newPort = DynamicPort(Top,None,portName,None)

        Top.ports[portName] = newPort

    return True
