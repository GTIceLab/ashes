import ashes_fg.fpaa as fpaa
import ashes_fg.test_class_lib as lib
from ashes_fg.fpaa import Module


def single_buffer(name):
    # Create top level module
    top = Module(name=name)

    # Create the input pad on pin 5
    inpad1 = lib.inpad(pad_number=5)
    net1 = inpad1.build(top)

    # Create the OTA buffer with default bias=1e-05, enabled fixed location at (x,y) = (11,6)
    ota_buf1 = lib.ota_buf(input=net1, fix_loc=[1, 5, 5])
    net2 = ota_buf1.build(top)

    # Create the output pad on pin 6
    outpad1 = lib.outpad(net2, pad_number=6)
    outpad1.build(top)

    return top


if __name__ == "__main__":
    top = single_buffer("single_buf")

    fpaa.compile(top, "single_buf", 16)
