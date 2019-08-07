
from rtestbench.tools.electrometer import Electrometer


class Interface(Electrometer):

    """Defines the commands common to all Keysight electrometers."""


    def __init__(self, model, serial_num):

        Electrometer.__init__(self, brand='Keysight', model=model, serial_num=serial_num)

        self._available_transfer_formats.update({
            'text':'ASCii',
            'bin':'REAL,32', 'bin32':'REAL,32',
            'bin64':'REAL,64'})
