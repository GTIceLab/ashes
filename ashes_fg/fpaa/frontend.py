from ir import Instance, Module, Net, PortRef

class Builder:
    def __init__(self, name: str):
        self.module: Module = Module(name)


    def In(self, name) -> Net:
        '''
        Creates an input net for the current Module being built
        Returns the input net for convenience
        '''
        input_net = Net(name)
        if self.module.nets[name] == input_net:
            raise Exception("ERROR: Net {input_net.name} already exists in {self.module.name}.")
                
        self.module.inputs.append(input_net)
        self.module.nets[name] = input_net
        return input_net
        

    def Out(self, name) -> Net:
        '''
        Creates an output net for the current Module being built
        Returns the output net for convenience
        '''
        output_net = Net(name)
        if self.module.nets[name] == output_net:
            raise Exception("ERROR: Net {input_net.name} already exists in {self.module.name}.")
        
        self.module.outputs.append(output_net)
        self.module.nets[name] = output_net
        return output_net


    def Net(self, name: str) -> Net:
        '''
        Create a disconnected net for the current Module being built
        Returns net for convenience
        '''
        net = Net(name)
        if self.modules.nets[name] == net:
            raise Exception("ERROR: Net {net.name} already exists in {self.module.name}.")
        self.module.nets[name] = net
        return net


    def Inst(self, name: str, primitive: object, **ports) -> Instance:
        '''
        Create an instance (either a primitive or module) and add it to the current Module being built
        Returns instance for convenience
        '''
        inst = Instance(name, primitive, {})

        for port, net in ports.items():
            port_type, number = port.split("_")
            port_name = f"{port_type}[{number}]"

            inst.ports[port_name] = net
            port_ref = PortRef(inst, port_name)
            
            if port_type.lower() == "in":
                for sink in net.sinks:
                    if sink == port_ref:
                        raise Exception(f"ERROR: Net {net.name} already has {sink.port_name} port of {sink.instance.name} in its sinks list.")
                net.sinks.append(PortRef(inst, port_name))
            elif port_type.lower() == "out":
                if net.driver != None:
                    raise Exception(f"ERROR: Net {net.name} already has {net.driver.port_name} port of {net.driver.instance.name} as its driver.")
                net.driver = PortRef(inst, port_name)
        
        self.module.instances.append(inst)
        return inst


    def finalize(self) -> Module:
        '''
        Should check consistency and catch errors before emission. Basically, finally self.Module.
        For now, just return Module for the emitter
        '''
        return self.module