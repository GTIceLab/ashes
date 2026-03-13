from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Module:
    '''
    Represents a named design unit with its own interface, internal nets, and instances.
    It owns a namespace, defines an interface, and contains internal connectivity and intances.
    '''
    name: str = "Top"
    ports: dict[str, Port] = field(default_factory=dict)
    nets: dict[str, Net] = field(default_factory=dict)
    instances: dict[str, Instance] = field(default_factory=dict)

    def __str__(self):
        lines = [f"=== Module: {self.name} ==="]

        lines.append("Ports:")
        if not self.ports:
            lines.append("\t(none)")
        for p_name, port in self.ports.items():
            lines.append(f"\t- {p_name} ({port.direction})")

        lines.append("Instances:")
        if not self.instances:
            lines.append("\t(none)")
        for i_name, inst in self.instances.items():
            lines.append(f"\t- {inst.name} [model: {inst.model}]")
            if inst.attrs:
                lines.append(f"\t\tAttrs: {inst.attrs}")

        lines.append("Nets:")
        if not self.nets:
            lines.append("\t(none)")
        for n_name, net in self.nets.items():
            driver_str = str(net.driver) if net.driver else "(none)"
            sinks_str = ", ".join(str(s) for s in net.sinks) if net.sinks else "(none)"
            lines.append(f"\t- {net.name}")
            lines.append(f"\t\tDriver:\t{driver_str}")
            lines.append(f"\t\tSinks:\t[{sinks_str}]")

        return "\n".join(lines)


@dataclass
class Port:
    '''
    A connection point belonging to either a module interface or an instance
    '''
    name: str
    direction: str
    owner: Module | Instance
    net: Net | None = None

    def __str__(self):
        '''
        Print as "OwnerName.PortName" (e.g. "inpad_5.out")
        '''
        owner_name = self.owner.name if self.owner else "UNKNOWN"
        return f"{owner_name}.{self.name}"

    def __repr__(self):
        '''
        Short representation to prevent messy recursive print out
        '''
        return f"<Port {self.__str__()} ({self.direction})"


@dataclass
class Net:
    '''
    Represents a wire/signal connecting components. Currently, the net is a single-driver
    connectivity object with zero or more sinks.
    '''
    name: str
    driver: Port
    sinks: list[Port] = field(default_factory=list)

    def __str__(self):
        '''
        Print as "NetName | Driver: DriverInfo | Sinks: [SinkInfo]"
        '''
        driver_str = str(self.driver) if self.driver else "None"
        sinks_str = ", ".join(str(s) for s in self.sinks)
        return f"{self.name} | Driver: {driver_str} | Sinks: [{sinks_str}]"

    def __repr__(self):
        '''
        Short representation to prevent messy recursive print out
        '''
        return f"<Net '{self.name}'>"


@dataclass
class Instance:
    '''
    Represents a primitive block in the circuit
    '''
    name: str
    model: str
    ports: dict[str, Port] = field(default_factory=dict)
    attrs: dict[str, any] = field(default_factory=dict)

    def __str__(self):
        '''
        Print as "InstanceName (model: ModelName)"
        '''
        return f"{self.name} (model: {self.model})"

    def __repr__(self):
        '''
        Short representation to prevent messy recursive print out
        '''
        return f"<Instance '{self.name}'>"   
