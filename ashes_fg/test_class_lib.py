from ashes_fg.fpaa.ir import Module, Instance, Port, Net
import math

class std_cell:
	def __init__(self, input, num_instances, cell_type):
		self.input = input
		self.num_instances = num_instances
		self.cell_type = cell_type

class inpad:
	def __init__(self, pad_number):
		self.pad_number = pad_number
		self.name = f"inpad_{pad_number}"

	def build(self, top: Module) -> Net:
		inst = Instance(name=self.name, model="inpad")
		inst.attrs = {"pad_number": self.pad_number}
		top.instances[inst.name] = inst
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports["out"] = out_port
		out_net = Net(name=f'net_{inst.name}', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class outpad:
	def __init__(self,input, pad_number):
		self.input=input
		self.pad_number = pad_number
		self.name = f"outpad_{pad_number}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="outpad")
		inst.attrs = {"pad_number": self.pad_number}
		top.instances[inst.name] = inst
		in_port = Port(name="in", direction="output", owner=inst, net=self.input)
		inst.ports["in"] = in_port
		self.input.sinks.append(in_port)

class outpada:
	def __init__(self,input, pad_number, fix_loc=[0, 0, 0]):
		self.input=input
		self.pad_number = pad_number
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"outpada_{pad_number}"

class BPF:
	def __init__(self, input, num_instances='1', type='both', Gain_Bias='3e-07', Gain_Bias_n='3e-07', Gain_Bias_p='3e-07', Feedback_bias='3e-07', Feedback_bias_n='3e-07', Feedback_bias_p='3e-07', Input_cap='2', foundry='skywater', process_node='130nm', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.Gain_Bias = Gain_Bias
		self.Gain_Bias_n = Gain_Bias_n
		self.Gain_Bias_p = Gain_Bias_p
		self.Feedback_bias = Feedback_bias
		self.Feedback_bias_n = Feedback_bias_n
		self.Feedback_bias_p = Feedback_bias_p
		self.Input_cap = Input_cap
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"BPF_{id(self)}"

class AmpDetect(std_cell):
	pass

class SHblock1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], SHblock1_ls='0', SHblock1_Ibias='3e-06', SHblock1_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.SHblock1_ls = SHblock1_ls
		self.SHblock1_Ibias = SHblock1_Ibias
		self.SHblock1_cap0_1x_cs = SHblock1_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"SHblock1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="SHblock1")
		inst.attrs = {
			"SHblock1_ls": self.SHblock1_ls,
			"SHblock1_Ibias": self.SHblock1_Ibias,
			"SHblock1_cap0_1x_cs": self.SHblock1_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class switchint1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], switchint1_ls='0', switchint1_Ibias1='3e-06', switchint1_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.switchint1_ls = switchint1_ls
		self.switchint1_Ibias1 = switchint1_Ibias1
		self.switchint1_cap0_1x_cs = switchint1_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"switchint1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="switchint1")
		inst.attrs = {
			"switchint1_ls": self.switchint1_ls,
			"switchint1_Ibias1": self.switchint1_Ibias1,
			"switchint1_cap0_1x_cs": self.switchint1_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class lpfota:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], ota_bias='1.01e-10', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.ota_bias = ota_bias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"lpfota_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="lpfota")
		inst.attrs = {
			"ota_bias": self.ota_bias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class test:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], test_ls='0', test_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.test_ls = test_ls
		self.test_cap0_1x_cs = test_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"test_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="test")
		inst.attrs = {
			"test_ls": self.test_ls,
			"test_cap0_1x_cs": self.test_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class hhn_debug:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], hhn_debug_ls='0', hhn_debug_fgswc_ibias='5.000D-08', hhn_debug_fgota1_ibias='2e-06', hhn_debug_fgota1_pbias='2e-06', hhn_debug_fgota1_nbias='2e-06', hhn_debug_fgota0_ibias='2e-06', hhn_debug_fgota0_pbias='2e-06', hhn_debug_fgota0_nbias='2e-06', hhn_debug_ota0_ibias='2e-06', hhn_debug_ota1_ibias='2e-06', hhn_debug_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.hhn_debug_ls = hhn_debug_ls
		self.hhn_debug_fgswc_ibias = hhn_debug_fgswc_ibias
		self.hhn_debug_fgota1_ibias = hhn_debug_fgota1_ibias
		self.hhn_debug_fgota1_pbias = hhn_debug_fgota1_pbias
		self.hhn_debug_fgota1_nbias = hhn_debug_fgota1_nbias
		self.hhn_debug_fgota0_ibias = hhn_debug_fgota0_ibias
		self.hhn_debug_fgota0_pbias = hhn_debug_fgota0_pbias
		self.hhn_debug_fgota0_nbias = hhn_debug_fgota0_nbias
		self.hhn_debug_ota0_ibias = hhn_debug_ota0_ibias
		self.hhn_debug_ota1_ibias = hhn_debug_ota1_ibias
		self.hhn_debug_cap0_1x_cs = hhn_debug_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"hhn_debug_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="hhn_debug")
		inst.attrs = {
			"hhn_debug_ls": self.hhn_debug_ls,
			"hhn_debug_fgswc_ibias": self.hhn_debug_fgswc_ibias,
			"hhn_debug_fgota1_ibias": self.hhn_debug_fgota1_ibias,
			"hhn_debug_fgota1_pbias": self.hhn_debug_fgota1_pbias,
			"hhn_debug_fgota1_nbias": self.hhn_debug_fgota1_nbias,
			"hhn_debug_fgota0_ibias": self.hhn_debug_fgota0_ibias,
			"hhn_debug_fgota0_pbias": self.hhn_debug_fgota0_pbias,
			"hhn_debug_fgota0_nbias": self.hhn_debug_fgota0_nbias,
			"hhn_debug_ota0_ibias": self.hhn_debug_ota0_ibias,
			"hhn_debug_ota1_ibias": self.hhn_debug_ota1_ibias,
			"hhn_debug_cap0_1x_cs": self.hhn_debug_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class HH_RG_2s:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], HH_RG_2s_ls='0', HH_RG_2s_Nafb_ibias='5.000D-08', HH_RG_2s_syn0_ibias='5.000D-08', HH_RG_2s_syn1_ibias='5.000D-08', HH_RG_2s_pfet_ibias='5.000D-08', HH_RG_2s_nmr_ibias='5.000D-08', HH_RG_2s_Na_ibias='2e-06', HH_RG_2s_Na_pbias='2e-06', HH_RG_2s_Na_nbias='2e-06', HH_RG_2s_K_ibias='2e-06', HH_RG_2s_K_pbias='2e-06', HH_RG_2s_K_nbias='2e-06', HH_RG_2s_buf_ibias='2e-06', HH_RG_2s_comp_ibias='2e-06', HH_RG_2s_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.HH_RG_2s_ls = HH_RG_2s_ls
		self.HH_RG_2s_Nafb_ibias = HH_RG_2s_Nafb_ibias
		self.HH_RG_2s_syn0_ibias = HH_RG_2s_syn0_ibias
		self.HH_RG_2s_syn1_ibias = HH_RG_2s_syn1_ibias
		self.HH_RG_2s_pfet_ibias = HH_RG_2s_pfet_ibias
		self.HH_RG_2s_nmr_ibias = HH_RG_2s_nmr_ibias
		self.HH_RG_2s_Na_ibias = HH_RG_2s_Na_ibias
		self.HH_RG_2s_Na_pbias = HH_RG_2s_Na_pbias
		self.HH_RG_2s_Na_nbias = HH_RG_2s_Na_nbias
		self.HH_RG_2s_K_ibias = HH_RG_2s_K_ibias
		self.HH_RG_2s_K_pbias = HH_RG_2s_K_pbias
		self.HH_RG_2s_K_nbias = HH_RG_2s_K_nbias
		self.HH_RG_2s_buf_ibias = HH_RG_2s_buf_ibias
		self.HH_RG_2s_comp_ibias = HH_RG_2s_comp_ibias
		self.HH_RG_2s_cap0_1x_cs = HH_RG_2s_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"HH_RG_2s_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="HH_RG_2s")
		inst.attrs = {
			"HH_RG_2s_ls": self.HH_RG_2s_ls,
			"HH_RG_2s_Nafb_ibias": self.HH_RG_2s_Nafb_ibias,
			"HH_RG_2s_syn0_ibias": self.HH_RG_2s_syn0_ibias,
			"HH_RG_2s_syn1_ibias": self.HH_RG_2s_syn1_ibias,
			"HH_RG_2s_pfet_ibias": self.HH_RG_2s_pfet_ibias,
			"HH_RG_2s_nmr_ibias": self.HH_RG_2s_nmr_ibias,
			"HH_RG_2s_Na_ibias": self.HH_RG_2s_Na_ibias,
			"HH_RG_2s_Na_pbias": self.HH_RG_2s_Na_pbias,
			"HH_RG_2s_Na_nbias": self.HH_RG_2s_Na_nbias,
			"HH_RG_2s_K_ibias": self.HH_RG_2s_K_ibias,
			"HH_RG_2s_K_pbias": self.HH_RG_2s_K_pbias,
			"HH_RG_2s_K_nbias": self.HH_RG_2s_K_nbias,
			"HH_RG_2s_buf_ibias": self.HH_RG_2s_buf_ibias,
			"HH_RG_2s_comp_ibias": self.HH_RG_2s_comp_ibias,
			"HH_RG_2s_cap0_1x_cs": self.HH_RG_2s_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class subbandArray:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], SubbandArray_ls='0', SubbandArray_FBbias='5.000D-10', SubbandArray_FBpbias='5.000D-08', SubbandArray_FBnbias='5.000D-08', SubbandArray_FFbias='5.000D-08', SubbandArray_FFpbias='5.000D-08', SubbandArray_FFnbias='5.000D-08', SubbandArray_Maxota='5.000D-08', SubbandArray_LPF='3.000D-09', SubbandArray_FFcap_1x_cs='1', SubbandArray_FBcap_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.SubbandArray_ls = SubbandArray_ls
		self.SubbandArray_FBbias = SubbandArray_FBbias
		self.SubbandArray_FBpbias = SubbandArray_FBpbias
		self.SubbandArray_FBnbias = SubbandArray_FBnbias
		self.SubbandArray_FFbias = SubbandArray_FFbias
		self.SubbandArray_FFpbias = SubbandArray_FFpbias
		self.SubbandArray_FFnbias = SubbandArray_FFnbias
		self.SubbandArray_Maxota = SubbandArray_Maxota
		self.SubbandArray_LPF = SubbandArray_LPF
		self.SubbandArray_FFcap_1x_cs = SubbandArray_FFcap_1x_cs
		self.SubbandArray_FBcap_1x_cs = SubbandArray_FBcap_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"subbandArray_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="subbandArray")
		inst.attrs = {
			"SubbandArray_ls": self.SubbandArray_ls,
			"SubbandArray_FBbias": self.SubbandArray_FBbias,
			"SubbandArray_FBpbias": self.SubbandArray_FBpbias,
			"SubbandArray_FBnbias": self.SubbandArray_FBnbias,
			"SubbandArray_FFbias": self.SubbandArray_FFbias,
			"SubbandArray_FFpbias": self.SubbandArray_FFpbias,
			"SubbandArray_FFnbias": self.SubbandArray_FFnbias,
			"SubbandArray_Maxota": self.SubbandArray_Maxota,
			"SubbandArray_LPF": self.SubbandArray_LPF,
			"SubbandArray_FFcap_1x_cs": self.SubbandArray_FFcap_1x_cs,
			"SubbandArray_FBcap_1x_cs": self.SubbandArray_FBcap_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class common_drain:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], common_drain_ls='0', common_drain_fgswc_ibias='5.000D-08', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.common_drain_ls = common_drain_ls
		self.common_drain_fgswc_ibias = common_drain_fgswc_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"common_drain_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="common_drain")
		inst.attrs = {
			"common_drain_ls": self.common_drain_ls,
			"common_drain_fgswc_ibias": self.common_drain_fgswc_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class Senseamp1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], Senseamp1_ls='0', Senseamp1_fgota0_ibias='5e-07', Senseamp1_fgota0_pbias='2e-07', Senseamp1_fgota0_nbias='2e-07', Senseamp1_ota0_ibias='3e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.Senseamp1_ls = Senseamp1_ls
		self.Senseamp1_fgota0_ibias = Senseamp1_fgota0_ibias
		self.Senseamp1_fgota0_pbias = Senseamp1_fgota0_pbias
		self.Senseamp1_fgota0_nbias = Senseamp1_fgota0_nbias
		self.Senseamp1_ota0_ibias = Senseamp1_ota0_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"Senseamp1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="Senseamp1")
		inst.attrs = {
			"Senseamp1_ls": self.Senseamp1_ls,
			"Senseamp1_fgota0_ibias": self.Senseamp1_fgota0_ibias,
			"Senseamp1_fgota0_pbias": self.Senseamp1_fgota0_pbias,
			"Senseamp1_fgota0_nbias": self.Senseamp1_fgota0_nbias,
			"Senseamp1_ota0_ibias": self.Senseamp1_ota0_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class Hyst_diff:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], Hyst_diff_ls='0', Hyst_diff_ota1_ibias='2e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.Hyst_diff_ls = Hyst_diff_ls
		self.Hyst_diff_ota1_ibias = Hyst_diff_ota1_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"Hyst_diff_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="Hyst_diff")
		inst.attrs = {
			"Hyst_diff_ls": self.Hyst_diff_ls,
			"Hyst_diff_ota1_ibias": self.Hyst_diff_ota1_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class common_drain_nfet:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], common_drain_nfet_ls='0', common_drain_nfet_ibias='5.000D-08', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.common_drain_nfet_ls = common_drain_nfet_ls
		self.common_drain_nfet_ibias = common_drain_nfet_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"common_drain_nfet_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="common_drain_nfet")
		inst.attrs = {
			"common_drain_nfet_ls": self.common_drain_nfet_ls,
			"common_drain_nfet_ibias": self.common_drain_nfet_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class ota_buf:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], ota_buf_bias='1e-05', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.ota_buf_bias = ota_buf_bias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"ota_buf_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="ota_buf")
		inst.attrs = {
			"ota_buf_bias": self.ota_buf_bias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class hhn:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], hhn_ls='0', hhn_fgswc_ibias='5.000D-08', hhn_fgota1_ibias='2e-06', hhn_fgota1_pbias='2e-06', hhn_fgota1_nbias='2e-06', hhn_fgota0_ibias='2e-06', hhn_fgota0_pbias='2e-06', hhn_fgota0_nbias='2e-06', hhn_ota0_ibias='2e-06', hhn_ota1_ibias='2e-06', hhn_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.hhn_ls = hhn_ls
		self.hhn_fgswc_ibias = hhn_fgswc_ibias
		self.hhn_fgota1_ibias = hhn_fgota1_ibias
		self.hhn_fgota1_pbias = hhn_fgota1_pbias
		self.hhn_fgota1_nbias = hhn_fgota1_nbias
		self.hhn_fgota0_ibias = hhn_fgota0_ibias
		self.hhn_fgota0_pbias = hhn_fgota0_pbias
		self.hhn_fgota0_nbias = hhn_fgota0_nbias
		self.hhn_ota0_ibias = hhn_ota0_ibias
		self.hhn_ota1_ibias = hhn_ota1_ibias
		self.hhn_cap0_1x_cs = hhn_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"hhn_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="hhn")
		inst.attrs = {
			"hhn_ls": self.hhn_ls,
			"hhn_fgswc_ibias": self.hhn_fgswc_ibias,
			"hhn_fgota1_ibias": self.hhn_fgota1_ibias,
			"hhn_fgota1_pbias": self.hhn_fgota1_pbias,
			"hhn_fgota1_nbias": self.hhn_fgota1_nbias,
			"hhn_fgota0_ibias": self.hhn_fgota0_ibias,
			"hhn_fgota0_pbias": self.hhn_fgota0_pbias,
			"hhn_fgota0_nbias": self.hhn_fgota0_nbias,
			"hhn_ota0_ibias": self.hhn_ota0_ibias,
			"hhn_ota1_ibias": self.hhn_ota1_ibias,
			"hhn_cap0_1x_cs": self.hhn_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class Min_detect:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], Min_detect_ls='0', Min_detect_fgswc_ibias='5.000D-08', Min_detect_ota0_ibias='2e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.Min_detect_ls = Min_detect_ls
		self.Min_detect_fgswc_ibias = Min_detect_fgswc_ibias
		self.Min_detect_ota0_ibias = Min_detect_ota0_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"Min_detect_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="Min_detect")
		inst.attrs = {
			"Min_detect_ls": self.Min_detect_ls,
			"Min_detect_fgswc_ibias": self.Min_detect_fgswc_ibias,
			"Min_detect_ota0_ibias": self.Min_detect_ota0_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class signalmult:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], signalmult_fg='1e-06', signalmult_v1p='5e-08', signalmult_v1n='5e-08', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.signalmult_fg = signalmult_fg
		self.signalmult_v1p = signalmult_v1p
		self.signalmult_v1n = signalmult_v1n
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"signalmult_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="signalmult")
		inst.attrs = {
			"signalmult_fg": self.signalmult_fg,
			"signalmult_v1p": self.signalmult_v1p,
			"signalmult_v1n": self.signalmult_v1n,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class common_source:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], common_source_ls='0', common_source_ibias='5.000D-08', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.common_source_ls = common_source_ls
		self.common_source_ibias = common_source_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"common_source_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="common_source")
		inst.attrs = {
			"common_source_ls": self.common_source_ls,
			"common_source_ibias": self.common_source_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class VolDivide1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], VolDivide1_ls='0', VolDivide1_fgota0_ibias='2e-06', VolDivide1_fgota0_pbias='2e-06', VolDivide1_fgota0_nbias='2e-06', VolDivide1_ota0_ibias='2e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.VolDivide1_ls = VolDivide1_ls
		self.VolDivide1_fgota0_ibias = VolDivide1_fgota0_ibias
		self.VolDivide1_fgota0_pbias = VolDivide1_fgota0_pbias
		self.VolDivide1_fgota0_nbias = VolDivide1_fgota0_nbias
		self.VolDivide1_ota0_ibias = VolDivide1_ota0_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"VolDivide1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="VolDivide1")
		inst.attrs = {
			"VolDivide1_ls": self.VolDivide1_ls,
			"VolDivide1_fgota0_ibias": self.VolDivide1_fgota0_ibias,
			"VolDivide1_fgota0_pbias": self.VolDivide1_fgota0_pbias,
			"VolDivide1_fgota0_nbias": self.VolDivide1_fgota0_nbias,
			"VolDivide1_ota0_ibias": self.VolDivide1_ota0_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class HH_RG_3s:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], HH_RG_3s_ls='0', HH_RG_3s_Nafb_ibias='5.000D-08', HH_RG_3s_syn0_ibias='5.000D-08', HH_RG_3s_syn1_ibias='5.000D-08', HH_RG_3s_syn2_ibias='5.000D-08', HH_RG_3s_pfet_ibias='5.000D-08', HH_RG_3s_nmr_ibias='5.000D-08', HH_RG_3s_Na_ibias='2e-06', HH_RG_3s_Na_pbias='2e-06', HH_RG_3s_Na_nbias='2e-06', HH_RG_3s_K_ibias='2e-06', HH_RG_3s_K_pbias='2e-06', HH_RG_3s_K_nbias='2e-06', HH_RG_3s_buf_ibias='2e-06', HH_RG_3s_comp_ibias='2e-06', HH_RG_3s_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.HH_RG_3s_ls = HH_RG_3s_ls
		self.HH_RG_3s_Nafb_ibias = HH_RG_3s_Nafb_ibias
		self.HH_RG_3s_syn0_ibias = HH_RG_3s_syn0_ibias
		self.HH_RG_3s_syn1_ibias = HH_RG_3s_syn1_ibias
		self.HH_RG_3s_syn2_ibias = HH_RG_3s_syn2_ibias
		self.HH_RG_3s_pfet_ibias = HH_RG_3s_pfet_ibias
		self.HH_RG_3s_nmr_ibias = HH_RG_3s_nmr_ibias
		self.HH_RG_3s_Na_ibias = HH_RG_3s_Na_ibias
		self.HH_RG_3s_Na_pbias = HH_RG_3s_Na_pbias
		self.HH_RG_3s_Na_nbias = HH_RG_3s_Na_nbias
		self.HH_RG_3s_K_ibias = HH_RG_3s_K_ibias
		self.HH_RG_3s_K_pbias = HH_RG_3s_K_pbias
		self.HH_RG_3s_K_nbias = HH_RG_3s_K_nbias
		self.HH_RG_3s_buf_ibias = HH_RG_3s_buf_ibias
		self.HH_RG_3s_comp_ibias = HH_RG_3s_comp_ibias
		self.HH_RG_3s_cap0_1x_cs = HH_RG_3s_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"HH_RG_3s_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="HH_RG_3s")
		inst.attrs = {
			"HH_RG_3s_ls": self.HH_RG_3s_ls,
			"HH_RG_3s_Nafb_ibias": self.HH_RG_3s_Nafb_ibias,
			"HH_RG_3s_syn0_ibias": self.HH_RG_3s_syn0_ibias,
			"HH_RG_3s_syn1_ibias": self.HH_RG_3s_syn1_ibias,
			"HH_RG_3s_syn2_ibias": self.HH_RG_3s_syn2_ibias,
			"HH_RG_3s_pfet_ibias": self.HH_RG_3s_pfet_ibias,
			"HH_RG_3s_nmr_ibias": self.HH_RG_3s_nmr_ibias,
			"HH_RG_3s_Na_ibias": self.HH_RG_3s_Na_ibias,
			"HH_RG_3s_Na_pbias": self.HH_RG_3s_Na_pbias,
			"HH_RG_3s_Na_nbias": self.HH_RG_3s_Na_nbias,
			"HH_RG_3s_K_ibias": self.HH_RG_3s_K_ibias,
			"HH_RG_3s_K_pbias": self.HH_RG_3s_K_pbias,
			"HH_RG_3s_K_nbias": self.HH_RG_3s_K_nbias,
			"HH_RG_3s_buf_ibias": self.HH_RG_3s_buf_ibias,
			"HH_RG_3s_comp_ibias": self.HH_RG_3s_comp_ibias,
			"HH_RG_3s_cap0_1x_cs": self.HH_RG_3s_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class switchcapint1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], switchcapint1_Bias='3e-06', switchcapint1_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.switchcapint1_Bias = switchcapint1_Bias
		self.switchcapint1_cap0_1x_cs = switchcapint1_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"switchcapint1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="switchcapint1")
		inst.attrs = {
			"switchcapint1_Bias": self.switchcapint1_Bias,
			"switchcapint1_cap0_1x_cs": self.switchcapint1_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class switchAmplifier1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], switchAmplifier1_ls='0', switchAmplifier1_ota0_ibias='3e-06', switchAmplifier1_cap0_1x_cs='1', switchAmplifier1_cap1_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.switchAmplifier1_ls = switchAmplifier1_ls
		self.switchAmplifier1_ota0_ibias = switchAmplifier1_ota0_ibias
		self.switchAmplifier1_cap0_1x_cs = switchAmplifier1_cap0_1x_cs
		self.switchAmplifier1_cap1_1x_cs = switchAmplifier1_cap1_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"switchAmplifier1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="switchAmplifier1")
		inst.attrs = {
			"switchAmplifier1_ls": self.switchAmplifier1_ls,
			"switchAmplifier1_ota0_ibias": self.switchAmplifier1_ota0_ibias,
			"switchAmplifier1_cap0_1x_cs": self.switchAmplifier1_cap0_1x_cs,
			"switchAmplifier1_cap1_1x_cs": self.switchAmplifier1_cap1_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class SOSLPF:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], SOSLPF_ls='0', SOSLPF_Ibias2='2e-07', SOSLPF_FG2p='1e-06', SOSLPF_FG2n='1e-06', SOSLPF_Ibias1='2e-07', SOSLPF_FG1p='1e-06', SOSLPF_FG1n='1e-06', SOSLPF_Feedback='4.000D-09', SOSLPF_Buffer='1e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.SOSLPF_ls = SOSLPF_ls
		self.SOSLPF_Ibias2 = SOSLPF_Ibias2
		self.SOSLPF_FG2p = SOSLPF_FG2p
		self.SOSLPF_FG2n = SOSLPF_FG2n
		self.SOSLPF_Ibias1 = SOSLPF_Ibias1
		self.SOSLPF_FG1p = SOSLPF_FG1p
		self.SOSLPF_FG1n = SOSLPF_FG1n
		self.SOSLPF_Feedback = SOSLPF_Feedback
		self.SOSLPF_Buffer = SOSLPF_Buffer
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"SOSLPF_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="SOSLPF")
		inst.attrs = {
			"SOSLPF_ls": self.SOSLPF_ls,
			"SOSLPF_Ibias2": self.SOSLPF_Ibias2,
			"SOSLPF_FG2p": self.SOSLPF_FG2p,
			"SOSLPF_FG2n": self.SOSLPF_FG2n,
			"SOSLPF_Ibias1": self.SOSLPF_Ibias1,
			"SOSLPF_FG1p": self.SOSLPF_FG1p,
			"SOSLPF_FG1n": self.SOSLPF_FG1n,
			"SOSLPF_Feedback": self.SOSLPF_Feedback,
			"SOSLPF_Buffer": self.SOSLPF_Buffer,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class Max_detect:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], Max_detect_ls='0', Max_detect_fgswc_ibias='5.000D-08', Max_detect_ota0_ibias='2e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.Max_detect_ls = Max_detect_ls
		self.Max_detect_fgswc_ibias = Max_detect_fgswc_ibias
		self.Max_detect_ota0_ibias = Max_detect_ota0_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"Max_detect_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="Max_detect")
		inst.attrs = {
			"Max_detect_ls": self.Max_detect_ls,
			"Max_detect_fgswc_ibias": self.Max_detect_fgswc_ibias,
			"Max_detect_ota0_ibias": self.Max_detect_ota0_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class MSOS02:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], MSOS02_ls='0', MSOS02_Ibias2='2e-07', MSOS02_Wbp='1e-06', MSOS02_Wbn='1e-06', MSOS02_Ibias1='2e-07', MSOS02_Wap='1e-06', MSOS02_Wan='1e-06', MSOS02_Feedback='4.000D-09', MSOS02_Buffer='3e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.MSOS02_ls = MSOS02_ls
		self.MSOS02_Ibias2 = MSOS02_Ibias2
		self.MSOS02_Wbp = MSOS02_Wbp
		self.MSOS02_Wbn = MSOS02_Wbn
		self.MSOS02_Ibias1 = MSOS02_Ibias1
		self.MSOS02_Wap = MSOS02_Wap
		self.MSOS02_Wan = MSOS02_Wan
		self.MSOS02_Feedback = MSOS02_Feedback
		self.MSOS02_Buffer = MSOS02_Buffer
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"MSOS02_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="MSOS02")
		inst.attrs = {
			"MSOS02_ls": self.MSOS02_ls,
			"MSOS02_Ibias2": self.MSOS02_Ibias2,
			"MSOS02_Wbp": self.MSOS02_Wbp,
			"MSOS02_Wbn": self.MSOS02_Wbn,
			"MSOS02_Ibias1": self.MSOS02_Ibias1,
			"MSOS02_Wap": self.MSOS02_Wap,
			"MSOS02_Wan": self.MSOS02_Wan,
			"MSOS02_Feedback": self.MSOS02_Feedback,
			"MSOS02_Buffer": self.MSOS02_Buffer,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class c4_sp:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], c4_sp_ota_bias_0='3e-06', c4_sp_ota_bias_1='3e-09', c4_sp_fg_0='0', c4_sp_ota_small_cap_0='0', c4_sp_ota_small_cap_1='0', c4_sp_ota_p_bias_0='1e-06', c4_sp_ota_n_bias_0='1e-06', c4_sp_ota_p_bias_1='1e-09', c4_sp_ota_n_bias_1='1e-09', c4_sp_cap_3x_0='0', c4_sp_cap_2x_0='0', c4_sp_cap_1x_0='0', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.c4_sp_ota_bias_0 = c4_sp_ota_bias_0
		self.c4_sp_ota_bias_1 = c4_sp_ota_bias_1
		self.c4_sp_fg_0 = c4_sp_fg_0
		self.c4_sp_ota_small_cap_0 = c4_sp_ota_small_cap_0
		self.c4_sp_ota_small_cap_1 = c4_sp_ota_small_cap_1
		self.c4_sp_ota_p_bias_0 = c4_sp_ota_p_bias_0
		self.c4_sp_ota_n_bias_0 = c4_sp_ota_n_bias_0
		self.c4_sp_ota_p_bias_1 = c4_sp_ota_p_bias_1
		self.c4_sp_ota_n_bias_1 = c4_sp_ota_n_bias_1
		self.c4_sp_cap_3x_0 = c4_sp_cap_3x_0
		self.c4_sp_cap_2x_0 = c4_sp_cap_2x_0
		self.c4_sp_cap_1x_0 = c4_sp_cap_1x_0
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"c4_sp_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="c4_sp")
		inst.attrs = {
			"c4_sp_ota_bias_0": self.c4_sp_ota_bias_0,
			"c4_sp_ota_bias_1": self.c4_sp_ota_bias_1,
			"c4_sp_fg_0": self.c4_sp_fg_0,
			"c4_sp_ota_small_cap_0": self.c4_sp_ota_small_cap_0,
			"c4_sp_ota_small_cap_1": self.c4_sp_ota_small_cap_1,
			"c4_sp_ota_p_bias_0": self.c4_sp_ota_p_bias_0,
			"c4_sp_ota_n_bias_0": self.c4_sp_ota_n_bias_0,
			"c4_sp_ota_p_bias_1": self.c4_sp_ota_p_bias_1,
			"c4_sp_ota_n_bias_1": self.c4_sp_ota_n_bias_1,
			"c4_sp_cap_3x_0": self.c4_sp_cap_3x_0,
			"c4_sp_cap_2x_0": self.c4_sp_cap_2x_0,
			"c4_sp_cap_1x_0": self.c4_sp_cap_1x_0,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class HH_RG:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], HH_RG_ls='0', HH_RG_Nafb_ibias='5.000D-08', HH_RG_in0_ibias='5.000D-08', HH_RG_pfet_ibias='5.000D-08', HH_RG_nmr_ibias='5.000D-08', HH_RG_Na_ibias='2e-06', HH_RG_Na_pbias='2e-06', HH_RG_Na_nbias='2e-06', HH_RG_K_ibias='2e-06', HH_RG_K_pbias='2e-06', HH_RG_K_nbias='2e-06', HH_RG_buf_ibias='2e-06', HH_RG_comp_ibias='2e-06', HH_RG_cap0_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.HH_RG_ls = HH_RG_ls
		self.HH_RG_Nafb_ibias = HH_RG_Nafb_ibias
		self.HH_RG_in0_ibias = HH_RG_in0_ibias
		self.HH_RG_pfet_ibias = HH_RG_pfet_ibias
		self.HH_RG_nmr_ibias = HH_RG_nmr_ibias
		self.HH_RG_Na_ibias = HH_RG_Na_ibias
		self.HH_RG_Na_pbias = HH_RG_Na_pbias
		self.HH_RG_Na_nbias = HH_RG_Na_nbias
		self.HH_RG_K_ibias = HH_RG_K_ibias
		self.HH_RG_K_pbias = HH_RG_K_pbias
		self.HH_RG_K_nbias = HH_RG_K_nbias
		self.HH_RG_buf_ibias = HH_RG_buf_ibias
		self.HH_RG_comp_ibias = HH_RG_comp_ibias
		self.HH_RG_cap0_1x_cs = HH_RG_cap0_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"HH_RG_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="HH_RG")
		inst.attrs = {
			"HH_RG_ls": self.HH_RG_ls,
			"HH_RG_Nafb_ibias": self.HH_RG_Nafb_ibias,
			"HH_RG_in0_ibias": self.HH_RG_in0_ibias,
			"HH_RG_pfet_ibias": self.HH_RG_pfet_ibias,
			"HH_RG_nmr_ibias": self.HH_RG_nmr_ibias,
			"HH_RG_Na_ibias": self.HH_RG_Na_ibias,
			"HH_RG_Na_pbias": self.HH_RG_Na_pbias,
			"HH_RG_Na_nbias": self.HH_RG_Na_nbias,
			"HH_RG_K_ibias": self.HH_RG_K_ibias,
			"HH_RG_K_pbias": self.HH_RG_K_pbias,
			"HH_RG_K_nbias": self.HH_RG_K_nbias,
			"HH_RG_buf_ibias": self.HH_RG_buf_ibias,
			"HH_RG_comp_ibias": self.HH_RG_comp_ibias,
			"HH_RG_cap0_1x_cs": self.HH_RG_cap0_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class cap:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], cap_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.cap_1x_cs = cap_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"cap_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="cap")
		inst.attrs = {
			"cap_1x_cs": self.cap_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class I_SenseAmp:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], I_SenseAmp_ls='0', I_SenseAmp_fgota0_ibias='2e-06', I_SenseAmp_fgota0_pbias='2e-06', I_SenseAmp_fgota0_nbias='2e-06', I_SenseAmp_ota0_ibias='2e-06', I_SenseAmp_cap0_1x_cs='1', I_SenseAmp_cap1_1x_cs='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.I_SenseAmp_ls = I_SenseAmp_ls
		self.I_SenseAmp_fgota0_ibias = I_SenseAmp_fgota0_ibias
		self.I_SenseAmp_fgota0_pbias = I_SenseAmp_fgota0_pbias
		self.I_SenseAmp_fgota0_nbias = I_SenseAmp_fgota0_nbias
		self.I_SenseAmp_ota0_ibias = I_SenseAmp_ota0_ibias
		self.I_SenseAmp_cap0_1x_cs = I_SenseAmp_cap0_1x_cs
		self.I_SenseAmp_cap1_1x_cs = I_SenseAmp_cap1_1x_cs
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"I_SenseAmp_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="I_SenseAmp")
		inst.attrs = {
			"I_SenseAmp_ls": self.I_SenseAmp_ls,
			"I_SenseAmp_fgota0_ibias": self.I_SenseAmp_fgota0_ibias,
			"I_SenseAmp_fgota0_pbias": self.I_SenseAmp_fgota0_pbias,
			"I_SenseAmp_fgota0_nbias": self.I_SenseAmp_fgota0_nbias,
			"I_SenseAmp_ota0_ibias": self.I_SenseAmp_ota0_ibias,
			"I_SenseAmp_cap0_1x_cs": self.I_SenseAmp_cap0_1x_cs,
			"I_SenseAmp_cap1_1x_cs": self.I_SenseAmp_cap1_1x_cs,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class ota:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], ota_bias='1e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.ota_bias = ota_bias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"ota_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="ota")
		inst.attrs = {
			"ota_bias": self.ota_bias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class tgate2:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"tgate2_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="tgate2")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class pfet:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"pfet_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="pfet")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class nfet:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"nfet_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="nfet")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class mite_FG:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], mite_fg0='1.000D-07', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.mite_fg0 = mite_fg0
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"mite_FG_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="mite_FG")
		inst.attrs = {
			"mite_fg0": self.mite_fg0,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class wta_new:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], wta_new_ls='0', wta_new_wta_bias='1.000D-08', wta_new_buf_bias='2e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.wta_new_ls = wta_new_ls
		self.wta_new_wta_bias = wta_new_wta_bias
		self.wta_new_buf_bias = wta_new_buf_bias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"wta_new_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="wta_new")
		inst.attrs = {
			"wta_new_ls": self.wta_new_ls,
			"wta_new_wta_bias": self.wta_new_wta_bias,
			"wta_new_buf_bias": self.wta_new_buf_bias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class vmm12x1_wowta:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], vmm12x1_wowta_fg='0', vmm12x1_target =[4e-06, '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', 3e-06, 3e-06, '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09'], vmm12x1_offsetbias='5.000D-09', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.vmm12x1_wowta_fg = vmm12x1_wowta_fg
		self.vmm12x1_target = vmm12x1_target
		self.vmm12x1_offsetbias = vmm12x1_offsetbias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"vmm12x1_wowta_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="vmm12x1_wowta")
		inst.attrs = {
			"vmm12x1_wowta_fg": self.vmm12x1_wowta_fg,
			"vmm12x1_target": self.vmm12x1_target,
			"vmm12x1_offsetbias": self.vmm12x1_offsetbias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class fgswitch:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fgswitch_ls='0', fgswitch_fgswc_ibias='5.000D-08', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fgswitch_ls = fgswitch_ls
		self.fgswitch_fgswc_ibias = fgswitch_fgswc_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"fgswitch_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="fgswitch")
		inst.attrs = {
			"fgswitch_ls": self.fgswitch_ls,
			"fgswitch_fgswc_ibias": self.fgswitch_fgswc_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class fgota:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fgota_bias='1.000D-08', fgota_p_bias='1.9', fgota_n_bias='1.9', fgota_small_cap='1', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fgota_bias = fgota_bias
		self.fgota_p_bias = fgota_p_bias
		self.fgota_n_bias = fgota_n_bias
		self.fgota_small_cap = fgota_small_cap
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"fgota_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="fgota")
		inst.attrs = {
			"fgota_bias": self.fgota_bias,
			"fgota_p_bias": self.fgota_p_bias,
			"fgota_n_bias": self.fgota_n_bias,
			"fgota_small_cap": self.fgota_small_cap,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class tgate:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"tgate_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="tgate")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class nmirror_w_bias:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], nmirror_w_bias_ls='0', nmirror_w_bias_ibias='5.000D-08', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.nmirror_w_bias_ls = nmirror_w_bias_ls
		self.nmirror_w_bias_ibias = nmirror_w_bias_ibias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"nmirror_w_bias_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="nmirror_w_bias")
		inst.attrs = {
			"nmirror_w_bias_ls": self.nmirror_w_bias_ls,
			"nmirror_w_bias_ibias": self.nmirror_w_bias_ibias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class ota2:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], ota2_bias='1e-06', fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.ota2_bias = ota2_bias
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"ota2_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="ota2")
		inst.attrs = {
			"ota2_bias": self.ota2_bias,
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class nmirror:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"nmirror_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="nmirror")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class vdd_i:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"vdd_i_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="vdd_i")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class gnd_dig:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"gnd_dig_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="gnd_dig")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class gnd_i:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"gnd_i_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="gnd_i")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class vdd_dig:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"vdd_dig_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="vdd_dig")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class vdd_out:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"vdd_out_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="vdd_out")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class gnd_out:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"gnd_out_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="gnd_out")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class in2in_x6:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"in2in_x6_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="in2in_x6")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

class in2in_x1:
	def __init__(self, input, num_instances='1', type='FPAA', board =['3.0', '3.0a'], fix_loc=[0, 0, 0]):
		self.input=input
		self.num_instances=num_instances
		self.fix_loc_enabled = fix_loc[0]
		self.fix_loc_x = fix_loc[1]
		self.fix_loc_y = fix_loc[2]
		self.name = f"in2in_x1_{id(self)}"

	def build(self, top: Module):
		inst = Instance(name=self.name, model="in2in_x1")
		inst.attrs = {
			"fix_loc_enabled": self.fix_loc_enabled,
			"fix_loc_x": self.fix_loc_x,
			"fix_loc_y": self.fix_loc_y,
		}
		top.instances[inst.name] = inst
		in_port = Port(name="in0", direction="input", owner=inst, net=self.input)
		inst.ports[in_port.name] = in_port
		self.input.sinks.append(in_port)
		out_port = Port(name="out", direction="output", owner=inst)
		inst.ports[out_port.name] = out_port
		out_net = Net(name=f'net_{inst.name}_out', driver=out_port)
		out_port.net = out_net
		top.nets[out_net.name] = out_net
		return out_net

