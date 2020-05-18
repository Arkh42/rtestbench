
from rtestbench.tools.keysight.electrometer._interface_v1 import Interface


class B2981A(Interface):
    """Specific class to control a Keysight B2981A electrometer (amperemeter).

    This instrument allows only current measurement.
    It is basically the commands defined in the Keysight electrometer interface.
    """


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, serial_num):

        Interface.__init__(self, model='B2981A', serial_num=serial_num)
