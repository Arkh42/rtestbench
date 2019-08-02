
from rtestbench.tools.tool import Tool


class Electrometer(Tool):

    """Interface class for features common to all electrometers.

    All functions defined here must be overriden in daughter classes implementing actual electrometers.
    """


    def __init__(self, brand=None, model=None, serial_num=None):

        Tool.__init__(self, family='electrometer', brand=brand, model=model, serial_num=serial_num)
