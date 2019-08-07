
from rtestbench import tools


# High-level interface
###

def construct_tool(visa_rm, addr):
    try:
        visa_resource = connect_tool(visa_rm, addr)
        tool_full_id = identify_tool(visa_resource)
        brand, model, serial_num = parse_tool_id(tool_id)
        new_tool = find_and_build_tool(brand, model, serial_num)
    except (RuntimeError, ValueError):
        raise
    else:
        return new_tool


# Low-level engine
###

def connect_tool(visa_rm, addr):
    try:
        new_device = visa_rm.open_resource(addr)
    except:
        raise RuntimeError("Impossible to find the device @ {}".format(addr))
    else:
        return new_device

def identify_tool(visa_device):
    try:
        full_id = visa_device.query('*IDN?')
    except:
        raise RuntimeError("Impossible to determine ID of device {}".format(visa_device))
    else:
        return id_n

def parse_tool_id(full_id):
    info = full_id.split(",")

    brand = info[0]
    model = info[1]
    serial_num = info[2]

    return brand, model, serial_num


import rtestbench.tools.keysight._factory as keysight_factory

def find_and_build_tool(brand, model, serial_num):
    try:
        if brand == "Keysight Technologies":
            return keysight_factory.find_and_build(model, serial_num)
        else:
            raise ValueError("Unknown brand {0}".format(brand))
    except ValueError:
        raise
