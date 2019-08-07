
from rtestbench.tools.keysight.electrometer import *


def find_and_build(model, serial_num):

    # Electrometers
    if model is "B2981A":
        return b2981a.B2981A(serial_num)
    elif model is "B2983A":
        return b2983a.B2983A(serial_num)
    elif model is "B2985A":
        return b2985a.B2985A(serial_num)
    elif model is "B2987A":
        return b2987a.B2987A(serial_num)
    else:
        raise ValueError("Unknown Keysight instrument model {}".format(model))
