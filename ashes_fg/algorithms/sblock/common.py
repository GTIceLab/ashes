"""Input validation shared by S-block builders using four-channel units."""


def validate_input_count(count):
    if count % 4 != 0:
        raise ValueError('The Sblock input size should be divisible by 4')
