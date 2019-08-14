
from rtestbench.tools.keysight.electrometer.b2981a import B2981A


class B2983A(B2981A):
    """Specific class to control a Keysight B2983A electrometer (amperemeter).

    This instrument allows only current measurement.
    It is basically the same as Keysight B2981A electrometer but it can also operate in battery-mode.
    """


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, serial_num):

        B2981A.__init__(self, serial_num=serial_num)
        self._model = 'B2983A'
