from dataclasses import dataclass, field
from __future__ import annotations

@dataclass
class Module:
    '''
    Represents the whole circuit
    '''
    name: str = "Top"
    inputs: list[Net] = field(default_factory=list)         # keep track of top-level inputs
    outputs: list[Net] = field(default_factory=list)        # keep track of top-level outputs
    nets: dict[str, Net] = field(default_factory=dict)      # authoritative namespace for all nets
    instances: list[Instance] = field(default=list)

@dataclass
class Net:
    '''
    Represents a wire/signal connecting components
    '''
    name: str
    driver: PortRef = None
    sinks: list[PortRef] = field(default=list)

    def __eq__(self, other):
        if not isinstance(other, Net):
            return False
        return (
            self.name == other.name
        )

@dataclass
class Instance:
    '''
    Represents a primitive block in the circuit (can also represent module, but requires further implementation)
    '''
    name: str
    model: object
    ports: dict[str, Net]

@dataclass
class PortRef:
    '''
    Represents a specific port on a specific instance
    '''
    instance: Instance
    port_name: str

    def __eq__(self, other):
        if not isinstance(other, PortRef):
            return False
        return (
            self.instance.name == other.instance.name
            and self.port_name == other.port_name
        )
    
