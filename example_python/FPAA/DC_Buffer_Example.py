import ashes_fg.fpaa as fpaa
import ashes_fg.test_class_lib as lib
from ashes_fg.fpaa import Module


def dc_buffer(name="dc_buffer"):
    top = Module(name=name)

    dc1 = lib.dc_in(DC_value=1.9, fix_loc=[1, 5, 5])
    net1 = dc1.build(top)

    buf1 = lib.ota_buf(net1, fix_loc=[1, 5, 6])
    net2 = buf1.build(top)

    outpad1 = lib.outpad(net2, pad_number=6)
    outpad1.build(top)

    return top


if __name__ == "__main__":
    top = dc_buffer("dc_buf")

    fpaa.compile(top, "dc_buf", 16)
