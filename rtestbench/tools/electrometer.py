
from rtestbench.tools.tool import Tool


class Electrometer(Tool):
    """Interface class for features common to all electrometers.

    All functions defined here must be overriden in daughter classes implementing actual electrometers.
    """


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, brand=None, model=None, serial_num=None):
        """Initialize the generic electrometer.

        The constructor arguments are necessary to build the _id attribute.
        """

        Tool.__init__(self, family='electrometer', brand=brand, model=model, serial_num=serial_num)

        self._available_meas_data_types = dict()
        self._available_result_data_types = dict()
        self._meas_data_type = None
        self._result_data_type = list()


    # Data types for results and measurements
    def is_available_meas_data_type(self, key):
        """Returns True if the passed argument is a measurement data type that is available for the electrometer; False otherwise."""
        if key in self._available_meas_data_types.keys():
            return True
        else:
            return False
    
    def is_implemented_meas_data_type(self, key):
        """Returns True is the passed argument is an available measurement data type and if the corresponding value is not None; False otherwise."""
        if self.is_available_meas_data_type(key) and self._available_meas_data_types[key] is not None:
            return True
        else:
            return False

    def is_available_result_data_type(self, key):
        """Returns True if the passed argument is a result data type that is available for the electrometer; False otherwise."""
        if key in self._available_result_data_types.keys():
            return True
        else:
            return False

    def is_implemented_result_data_type(self, key):
        """Returns True is the passed argument is an available result data type and if the corresponding value is not None; False otherwise."""
        if self.is_available_result_data_type(key) and self._available_result_data_types[key] is not None:
            return True
        else:
            return False


    @property
    def meas_data_type(self):
        """Get the current measurement data type."""
        return self._meas_data_type

    @meas_data_type.setter
    def meas_data_type(self, data_type):
        """Set the measurement data type if and only if the new data type is available for the tool."""
        if self.is_available_meas_data_type(data_type):
            if self._available_meas_data_types[data_type] is None:
                raise NotImplementedError(
                    'The {0} measurement data type is available but not implemented for the {1} tool.'.format(data_type, self.id))
            else:
                self._meas_data_type = data_type
        else:
            raise ValueError('The {0} measurement data type is not available for the {1} tool.\n\
                Valid types are: {2}'.format(data_type, self._id, self._available_meas_data_types))

    @property
    def result_data_type(self):

        """Get the current result data type."""

        return self._result_data_type

    @result_data_type.setter
    def result_data_type(self, data_type: list):
        """Set the result data type if and only if the new data type is available for the tool."""
        for elem in data_type:
            if self.is_available_result_data_type(elem):
                if self._available_result_data_types[elem] is None:
                    raise NotImplementedError(
                        'The {0} result data type is available but not implemented for the {1} tool.'.format(elem, self.id))
                else:
                    continue
            else:
                raise ValueError('The {0} result data type is not available for the {1} tool.\n\
                    Valid types are: {2}'.format(elem, self._id, self._available_result_data_types))

        self._result_data_type = data_type


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
    
    # Data to measure
    def config_meas_data_type(self, data_type):
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

    # Data type
    def config_result_data_type(self, data_type):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')


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

    # Measurements actions
    def init_meas(self):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')

    def fetch_data(self, data_label):
        raise NotImplementedError('Function not implemented by the Electrometer class. \
            Must be implemented by daughter classes.')
