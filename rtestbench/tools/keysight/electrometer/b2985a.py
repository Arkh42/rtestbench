
from rtestbench.tools.keysight.electrometer._interface import Interface


class B2985A(Interface):

    """Specific class to control a Keysight B2985A electrometer.

    This instrument allows current, charge and resistance measurement.
    It textends the commands defined in the Keysight electrometer interface to its own peculiar abilities.
    """


    def __init__(self, serial_num):

        Interface.__init__(self, model='B2985A', serial_num=serial_num)
