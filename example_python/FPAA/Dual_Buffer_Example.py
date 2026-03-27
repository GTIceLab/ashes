import ashes_fg.fpaa as fpaa
import ashes_fg.test_class_lib as lib
from ashes_fg.fpaa import Module

def dual_buffer(name):
    top = Module(name=name)

    inpad1 = lib.inpad(pad_number=5)
    net1 = inpad1.build(top)
    
    buf1 = lib.ota_buf(input=net1, fix_loc=[1, 5, 5])
    net2 = buf1.build(top)
    
    buf2 = lib.ota_buf(input=net2, fix_loc=[1, 5, 6])
    net3 = buf2.build(top)
    
    outpad1 = lib.outpad(input=net3, pad_number=6)
    outpad1.build(top)
    
    return top

if __name__ == "__main__":
    top = dual_buffer("dual_buf")

    fpaa.compile(top, "dual_buf", 16)