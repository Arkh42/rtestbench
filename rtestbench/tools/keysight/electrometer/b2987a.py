
from rtestbench.tools.keysight.electrometer.b2985a import B2985A


class B2987A(B2985A):
    """Specific class to control a Keysight B2987A electrometer.

    This instrument allows current, charge and resistance measurement.
    It is basically the same as Keysight B2985A electrometer but it can also operate in battery-mode.
    """


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, serial_num):

        B2985A.__init__(self, serial_num=serial_num)
        self._model = 'B2987A'
