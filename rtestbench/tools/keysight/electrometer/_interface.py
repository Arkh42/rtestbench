
from rtestbench.tools.electrometer import Electrometer


class Interface(Electrometer):

    """Defines the commands common to all Keysight electrometers."""


    # Initialization & properties
    ###

    def __init__(self, model, serial_num):

        Electrometer.__init__(self, brand='Keysight', model=model, serial_num=serial_num)

        self._available_transfer_formats.update({
            'text':'ASCii',
            'bin':'REAL,32', 'bin32':'REAL,32',
            'bin64':'REAL,64'})
        
        self._available_view_modes = {
            'meter':'SINGle1', 'roll':'ROLL', 'hist':'HISTogram', 'graph':'GRAPH'}
        
        self._view_mode = 'meter'
        
        
        # Defaults
        self.transfer_format = 'text'
        # select default view mode


    def is_available_view_mode(self, key):
        if key in self._available_view_modes.keys():
            return True
        else:
            return False

    @property
    def view_mode(self):
        """Get the main view mode."""

        return self._view_mode

    @view_mode.setter
    def view_mode(self, mode):
        """Set the main view mode."""

        if self.is_available_view_mode(mode):
            self._view_mode = mode
        else:
            raise ValueError('The {0} view mode is not available for the {1} tool.\n\
                Valid modes are: {2}'.format(mode, self._id, self._available_view_modes))

    
    # High-level abstract interface (common to all tools)
    ###

    def config_data_transfer_format(self, data_format):
        try:
            self.transfer_format = data_format
        except (NotImplementedError, ValueError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot configure the data transfer format {} for {}'.format(data_format, self._id))
        else:
            self.send(':FORMat:DATA {}'.format(self._available_transfer_formats[data_format]))

    
    def lock(self):
        try:
            lock_status = self.query_data(':SYSTem:LOCK:REQuest?')
            if lock_status[0] != 1.0:
                raise RuntimeError('The system {} returned a lock status other than 1.'.format(self._id))
        except (UnboundLocalError, RuntimeError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot lock the system {}'.format(self._id))
        else:
            self.logger.info('The system {} is now remotely locked.'.format(self._id))
    
    def unlock(self):
        try:
            self.send(':SYSTem:LOCK:RELease')
        except (UnboundLocalError, RuntimeError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot unlock the system {}'.format(self._id))
        else:
            self.logger.info('The system {} is now unlocked.'.format(self._id))


    # Display
    ###

    # Enable/disable
    def switch_display(self, switch):
        try:
            if switch.upper() in ('ON', 'OFF', 1, '1', 0, '0'):
                self.send(':DISPlay:ENABle {}'.format(switch).upper())
            else:
                raise ValueError("Parameter switch={} should be 'ON' or 'OFF'.".format(switch))
        except (UnboundLocalError, RuntimeError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot switch the display of the system {}'.format(self._id))
        else:
            self.logger.debug('The system {} is now unlocked.'.format(self._id))

    def enable_display(self):
        self.switch_display('ON')
    def disable_display(self):
        self.switch_display('OFF')

    
    # View mode and channels
    def config_display_view(self, mode):
        try:
            self.view_mode = mode
        except (NotImplementedError, ValueError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot configure the main view mode as {} for {}'.format(mode, self._id))
        else:
            self.send(':DISPlay:VIEW {}'.format(self._available_view_modes[mode]))
    

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


