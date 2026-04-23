import ashes_fg.fpaa as fpaa
import ashes_fg.test_class_lib as lib
from ashes_fg.fpaa import Module, emit_py_to_blif, save_blif


def C4_offchip(name="C4_offchip"):
    # Create top level module
    top = Module(name=name)

    # Create the input pad on pin 5
    inpad1 = lib.inpad(pad_number=5)
    net1 = inpad1.build(top)

    # Create an on chip dc input
    dc_in1 = lib.dc_in(DC_value=1.9, fix_loc=[1, 5, 5])
    input_voltage = dc_in1.build(top)

    # Create C4 offchip BPF
    c4_bpf = lib.C4_BPF(
        input=[input_voltage, net1],
        C4_BPF_Buffer_ibias=3.5e-10,
        C4_BPF_Forward_ibias=7.5e-10,
        fix_loc=[1, 5, 6],
    )
    net2 = c4_bpf.build(top)

    # Create the output pad on pin 6
    outpad1 = lib.outpad(net2, pad_number=6)
    outpad1.build(top)

    return top


if __name__ == "__main__":
    top = C4_offchip("C4_offchip")

    fpaa.compile(top, "C4_offchip", 16)
