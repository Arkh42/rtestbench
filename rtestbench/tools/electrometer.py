
from rtestbench.core import Tool


class Electrometer(Tool):
    """Interface class for features common to all electrometers.

    All functions defined here must be overriden in daughter classes implementing actual electrometers.
    """

    def __init__(self, info):
        info.family = "electrometer"

        Tool.__init__(self, info)
    

    # Scale and offset interface
    def set_scale(self, axis, scale):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_offset(self, axis, offset):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_xscale(self, scale):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_xoffset(self, offset):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_yscale(self, scale):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_yoffset(self, offset):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Range interface
    def set_range(self, value):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_range(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_autorange(self, switch: bool):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_range_min(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_range_max(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Aperture (integration) time interface
    def set_aperture_time(self, value):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_aperture_time(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_integration_time(self, value):
        self.set_aperture_time(value)
    def get_integration_time(self):
        self.get_aperture_time()

    def set_aperture_time_min(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_aperture_time_max(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_integration_time_min(self):
        self.set_aperture_time_min()
    def set_integration_time_max(self):
        self.set_aperture_time_max()

    # Trigger interface
    def set_trigger_source(self, source_name: str):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_trigger_source(self) -> str:
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_trigger_count(self, value: int):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_trigger_count_min(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_trigger_count_max(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_trigger_count(self) -> int:
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def set_trigger_timer(self, value: float):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_trigger_timer_min(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def set_trigger_timer_max(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def get_trigger_timer(self) -> float:
        raise NotImplementedError("This function must be implemented in daughter classes.")

    # Measurement actions interface
    def initiate_measurement(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def fetch_data(self, meas_data_type):
        raise NotImplementedError("This function must be implemented in daughter classes.")
    def fetch_all_data(self):
        raise NotImplementedError("This function must be implemented in daughter classes.")
