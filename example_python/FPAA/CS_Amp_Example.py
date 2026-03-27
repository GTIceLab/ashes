import ashes_fg.fpaa as fpaa
import ashes_fg.test_class_lib as lib
from ashes_fg.fpaa import Module


def cs_amp(name):
    top = Module(name=name)

    inpad1 = lib.inpad(pad_number=5)
    net1 = inpad1.build(top)
    
    amp = lib.common_source(net1, common_source_ibias='5e-06', fix_loc=[1, 1, 5])
    net2 = amp.build(top)
    
    buf1 = lib.ota_buf(net2, fix_loc=[1, 3, 5])
    net3 = buf1.build(top)
    
    outpad1 = lib.outpad(net3, pad_number=6)
    outpad1.build(top)
    
    return top


if __name__ == "__main__":
    top = cs_amp("cs_amp")

    fpaa.compile(top, "cs_amp", 16)