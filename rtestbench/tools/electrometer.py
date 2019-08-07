
from rtestbench.tools.tool import Tool


class Electrometer(Tool):

    """Interface class for features common to all electrometers.

    All functions defined here must be overriden in daughter classes implementing actual electrometers.
    """


    def __init__(self, brand=None, model=None, serial_num=None):

        Tool.__init__(self, family='electrometer', brand=brand, model=model, serial_num=serial_num)
    
    
    # Display
    ###

    # Enable/disable
    def switch_display(self, switch):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')

    def enable_display(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def disable_display(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')

    
    # View mode and channels
    def config_display_view(self, mode):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    

    # Scale and offset
    def config_scale(self, axis, scale):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_offset(self, axis, offset):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')

    def config_xscale(self, scale):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_xoffset(self, offset):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_yscale(self, scale):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_yoffset(self, offset):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    

    # Measurements conditions
    ###

    # Range
    def switch_autorange(self, switch):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    
    def enable_autorange(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def disable_autorange(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    
    def config_range(self, value):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')


    # Aperture/integration time
    def config_aperture_time(self, value):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    
    def config_aperture_time_min(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_aperture_time_max(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    

    # Trigger
    def config_trigger_count(self, value):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    
    def config_trigger_count_min(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_trigger_count_max(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    
    def config_trigger_timer(self, value):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    
    def config_trigger_timer_min(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
    def config_trigger_timer_max(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')


    # Measurements operations
    ###

    def init_meas(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')

    def fetch_data(self, data_label):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
