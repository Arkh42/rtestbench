
from rtestbench.core import Tool


class Oscilloscope(Tool):

    """Interface class for features common to all oscilloscopes.

    All functions defined here must be overriden in daughter classes implementing actual oscilloscopes.
    """


    def __init__(self, info):
        info.family = "oscilloscope"

        Tool.__init__(self, info)
    

    # Coupling
    def set_coupling(self, channel, mode):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_coupling(self, channel):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Probe attenuation factor
    def set_probe_attenuation(self, channel, attenuation_factor):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_probe_attenuation(self, channel):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Timebase, scale and offset interface
    def autoscale(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_timebase_mode(self, mode):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_timebase_scale(self, scale):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_timebase_offset(self, offset):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_yscale(self, channel, scale):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_yoffset(self, channel, offset):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Trigger interface
    def set_trigger_source(self, source_name: str):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_trigger_source(self) -> str:
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Measurement actions interface
    def fetch_data(self, source_name):
        raise NotImplementedError("This function must be implemented in daughter classes.")
