"""Decoder utilities independent of tree topology and physical placement."""
from operator import index


def address_width(output_count):
    """Return ceil(log2(output_count)) for a positive integer channel count."""
    output_count = index(output_count)
    if output_count < 1:
        raise ValueError('Decoder output count must be positive')
    return (output_count - 1).bit_length()
