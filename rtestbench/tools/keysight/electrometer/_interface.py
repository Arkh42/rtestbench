
from rtestbench.tools.electrometer import Electrometer
from rtestbench.tools.tool import Tool


class Interface(Electrometer):
    """Defines the commands common to all Keysight electrometers."""


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, model, serial_num):
        """Initialize the generic interface for Keysight electrometers.

        The constructor arguments are necessary to build the _id attribute.
        """

        Electrometer.__init__(self, brand='Keysight', model=model, serial_num=serial_num)

        self._available_transfer_formats.update({
            'text':'ASCii',
            'bin':'REAL,32', 'bin32':'REAL,32',
            'bin64':'REAL,64'})
        
        self._available_meas_data_types.update({'I': 'CURRent', 'i': 'CURRent'})
        self._available_result_data_types.update(self._available_meas_data_types)
        self._available_result_data_types.update({'t': 'TIME', 'math': 'MATH'})

        self._available_trigger_sources.update({
            'auto': 'AINT',
            'time': 'TIMer', 'timer': 'TIMer',
            'int1': 'INT1', 'int2': 'INT2'})
        self.trigger_source = 'auto'
        
        self._available_view_modes = {
            'meter':'SINGle1', 'roll':'ROLL', 'hist':'HISTogram', 'graph':'GRAPH'}
        self._available_subview_modes = {
            'roll':'ROLL', 'hist':'HISTogram', 'range':'RANGe', 'trigger': 'TRIGger', 'source': 'FUNCtion'}
        self._main_view_mode = None
        self._sub_view_mode = None


    def config_defaults(self):
        self.config_data_transfer_format('text')

        self.config_display_view('meter')
        self.config_display_subview('roll')

    def attach_visa_resource(self, visa_resource):
        """Redefine the Tool's method to configure defaults after having attached the VISA resource."""
        Tool.attach_visa_resource(self, visa_resource)

        self.config_defaults()


    # View modes
    def is_available_view_mode(self, key):
        """Returns True if the passed argument is a view mode that is available for the electrometer; False otherwise."""
        if key in self._available_view_modes.keys():
            return True
        else:
            return False

    def is_implemented_view_mode(self, key):
        """Returns True is the passed argument is an available view mode and if the corresponding value is not None; False otherwise."""
        if self.is_available_view_mode(key) and self._available_view_modes[key] is not None:
            return True
        else:
            return False

    @property
    def view_mode(self):
        """Get the current main view mode."""
        return self._main_view_mode

    @view_mode.setter
    def view_mode(self, mode):
        """Set the main view mode if and only if the new mode is available for the tool."""
        if self.is_available_view_mode(mode):
            if self._available_view_modes[mode] is None:
                raise NotImplementedError(
                    'The {0} view mode is available but not implemented for the {1} tool.'.format(mode, self.id))
            else:
                self._main_view_mode = mode
        else:
            raise ValueError('The {0} view mode is not available for the {1} tool.\n\
                Valid modes are: {2}'.format(mode, self.id, self._available_view_modes))


    def is_available_subview_mode(self, key):
        """Returns True if the passed argument is a subview mode that is available for the electrometer; False otherwise."""
        if key in self._available_subview_modes.keys():
            return True
        else:
            return False

    def is_implemented_subview_mode(self, key):
        """Returns True is the passed argument is an available subview mode and if the corresponding value is not None; False otherwise."""
        if self.is_available_subview_mode(key) and self._available_subview_modes[key] is not None:
            return True
        else:
            return False

    @property
    def subview_mode(self):
        """Get the current subview mode."""
        return self._sub_view_mode

    @subview_mode.setter
    def subview_mode(self, mode):
        """Set the subview view mode if and only if the new mode is available for the tool."""
        if self.is_available_subview_mode(mode):
            if self._available_subview_modes[mode] is None:
                raise NotImplementedError(
                    'The {0} subview mode is available but not implemented for the {1} tool.'.format(mode, self.id))
            else:
                self._sub_view_mode = mode
        else:
            raise ValueError('The {0} subview mode is not available for the {1} tool.\n\
                Valid modes are: {2}'.format(mode, self.id, self._available_subview_modes))

    
    # High-level abstract interface (common to all tools)
    ###

    def config_data_transfer_format(self, data_format):
        try:
            self.transfer_format = data_format
        except (NotImplementedError, ValueError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot configure the data transfer format as {} for {}'.format(data_format, self.id))
        else:
            self.send(':FORMat:DATA {}'.format(self._available_transfer_formats[data_format]))

    
    def lock(self):
        try:
            lock_status = self.query_data(':SYSTem:LOCK:REQuest?')
            if lock_status[0] != 1.0:
                raise RuntimeError('The system {} returned a lock status other than 1.'.format(self.id))
        except:
            raise
        else:
            self.logger.info('The system {} is now remotely locked.'.format(self.id))
    
    def unlock(self):
        try:
            self.send(':SYSTem:LOCK:RELease')
        except:
            raise
        else:
            self.logger.info('The system {} is now unlocked.'.format(self.id))


    # Display
    ###

    # Enable/disable
    def switch_display(self, switch):
        try:
            if self.is_boolean_string(switch):
                self.send(':DISPlay:ENABle {}'.format(switch).upper())
            elif switch in (0, 1):
                self.send(':DISPlay:ENABle {}'.format(switch))
            else:
                raise ValueError("Parameter switch={} should be 'ON' or 'OFF'.".format(switch))
        except:
            raise
        else:
            self.logger.debug('The display of system {} has been switched to {}.'.format(self.id, switch))

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
            raise RuntimeError('Cannot configure the main view mode as {} for {}'.format(mode, self.id))
        else:
            self.send(':DISPlay:VIEW {}'.format(self._available_view_modes[mode]))
    
    def config_display_subview(self, mode):
        try:
            self.subview_mode = mode
        except (NotImplementedError, ValueError) as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot configure the subview mode as {} for {}'.format(mode, self.id))
        else:
            self.send(':DISPlay:VIEW:SINGle:SPANel {}'.format(self._available_subview_modes[mode]))
    
    # Data to measure
    def config_display_xdata_type(self, data_type):
        """Select the data type assigned to the X-axis."""
        if self.view_mode == 'graph':
            try:
                self.meas_data_type = data_type
            except (NotImplementedError, ValueError) as error_msg:
                self.logger.error(error_msg)
                raise RuntimeError('Cannot configure the X-axis data type as {} for {}'.format(data_type, self._id))
            else:
                self.send(':DISPlay:VIEW:GRAPh:X:ELEMent {}'.format(self._available_result_data_types[data_type]))
        else:
            raise RuntimeError("X-data type can only be assigned in 'graph' mode for {}".format(self._id))

    def config_display_ydata_type(self, data_type):
        """Select the data type assigned to the Y-axis."""
        if self.view_mode in ('graph', 'hist', 'roll') or (self.view_mode == 'meter' and self.subview_mode in ('hist', 'roll')):
            try:
                self.meas_data_type = data_type
            except (NotImplementedError, ValueError) as error_msg:
                self.logger.error(error_msg)
                raise RuntimeError('Cannot configure the Y-axis data type as {} for {}'.format(data_type, self._id))
            else:
                if self.view_mode == 'meter':
                    mode = self._available_view_modes[self.subview_mode]
                else:
                    mode = self._available_view_modes[self.view_mode]
                self.send(':DISPlay:VIEW:{}:Y:ELEMent {}'.format(mode, self._available_meas_data_types[data_type]))
        else:
            raise RuntimeError("Y-data type can only be assigned in 'meter' mode if subview mode is ('hist', 'roll') for {}".format(self._id))
    

    # Scale and offset
    def config_scale(self, axis, scale):
        if axis.upper() == 'X':
            self.config_xscale(scale)
        elif axis.upper() == 'Y':
            self.config_yscale(scale)
        else:
            raise ValueError("{} is not a valid axis. Correct values are ('x', 'X', 'y', 'Y')".format(axis))

    def config_offset(self, axis, offset):
        if axis.upper() == 'X':
            self.config_xoffset(offset)
        elif axis.upper() == 'Y':
            self.config_yoffset(offset)
        else:
            raise ValueError("{} is not a valid axis. Correct values are ('x', 'X', 'y', 'Y')".format(axis))

    def config_xscale(self, scale):
        if self.view_mode == 'roll' or (self.view_mode == 'meter' and self.subview_mode == 'roll'):
            self.send(':DISPlay:VIEW:ROLL:X:PDIVision {}'.format(scale))
        else:
            raise RuntimeError("X-scale cannot be specified in the currently selected mode {} for {}".format(
                self.view_mode, self.id))

    def config_xoffset(self, offset):
        if self.view_mode == 'roll' or (self.view_mode == 'meter' and self.subview_mode == 'roll'):
            self.send(':DISPlay:VIEW:ROLL:X:OFFSet {}'.format(offset))
        else:
            raise RuntimeError("X-offset cannot be specified in the currently selected mode {} for {}".format(
                self.view_mode, self.id))

    def config_yscale(self, scale):
        if self.view_mode == 'roll' or (self.view_mode == 'meter' and self.subview_mode == 'roll'):
            if self.meas_data_type is None:
                raise RuntimeError("No measure data type has been selected.")
            else:
                self.send(':DISPlay:VIEW:ROLL:Y:PDIVision:{} {}'.format(
                    self._available_meas_data_types[self.meas_data_type], scale))
        else:
            raise RuntimeError("Y-scale cannot be specified in the currently selected mode {} for {}".format(
                self.view_mode, self.id))

    def config_yoffset(self, offset):
        if self.view_mode == 'roll' or (self.view_mode == 'meter' and self.subview_mode == 'roll'):
            if self.meas_data_type is None:
                raise RuntimeError("No measure data type has been selected.")
            else:
                self.send(':DISPlay:VIEW:ROLL:Y:OFFSet:{} {}'.format(
                    self._available_meas_data_types[self.meas_data_type], offset))
        else:
            raise RuntimeError("Y-offset cannot be specified in the currently selected mode {} for {}".format(
                self.view_mode, self.id))
    

    # Measurements conditions
    ###

    # Data type
    def config_result_data_type(self, data_type):
        try:
            self.result_data_type = data_type
        except ValueError as error_msg:
            self.logger.error(error_msg)
            raise RuntimeError('Cannot configure the result data type as {} for {}'.format(data_type, self._id))
        else:
            sequence = list()
            for elem in data_type:
                sequence.append(self._available_result_data_types[elem])
            self.send(':FORMat:ELEMents:SENSe {}'.format(','.join(sequence)))


    # Range
    def switch_autorange(self, switch):
        try:
            if self.meas_data_type is None:
                raise RuntimeError("No measure data type has been selected.")
            else:
                if self.is_boolean_string(switch):
                    self.send(':SENSe:{0}:RANGe:AUTO {1}'.format(
                        self._available_meas_data_types[self.meas_data_type], switch.upper()))
                elif switch in (0, 1):
                    self.send(':SENSe:{0}:RANGe:AUTO {1}'.format(
                        self._available_meas_data_types[self.meas_data_type], switch))
                else:
                    raise ValueError("Parameter switch={} should be 'ON' or 'OFF'.".format(switch))
        except:
            raise
        else:
            self.logger.info('The system {} autorange mode has been switched to {}.'.format(self.id, switch))
    
    def enable_autorange(self):
        self.switch_autorange('ON')
    def disable_autorange(self):
        self.switch_autorange('OFF')
    
    def config_range(self, value):
        try:
            if self.meas_data_type is None:
                raise RuntimeError("No measure data type has been selected.")
            else:
                self.send(':SENSe:{0}:RANGe:AUTO {1}'.format(
                    self._available_meas_data_types[self.meas_data_type], value))
        except:
            raise
        else:
            self.logger.info('The system {} range has been set to {}.'.format(self.id, value))


    # Aperture/integration time
    def config_aperture_time(self, value):
        try:
            if self.meas_data_type is None:
                raise RuntimeError("No measure data type has been selected.")
            else:
                self.send(':SENSe:{0}:APERture {1}'.format(
                    self._available_meas_data_types[self.meas_data_type], value))
        except:
            raise
        else:
            self.logger.info('The system {} aperture (integration) time has been set to {}.'.format(self.id, value))
    
    def config_aperture_time_min(self):
        self.config_aperture_time('MINimum')
    def config_aperture_time_max(self):
        self.config_aperture_time('MAXimum')
    

    # Trigger
    def config_trigger_source(self, source_name):
        try:
            self.trigger_source = source_name
            self.send(':TRIGger:ACQuire:SOURce:SIGNal {}'.format(self._available_trigger_sources[source_name]))
        except:
            raise
        else:
            self.logger.info('The system {} trigger source has been set to {}.'.format(self.id, source_name))

    def config_trigger_count(self, value):
        try:
            if isinstance(value, int):
                if value < 1:
                    value = 1
                    self.logger.warning("Value for trigger count can't be < 1. Forced to 1.")
                elif value > 100000:
                    value = 100000
                    self.logger.warning("Value for trigger count can't be > 100 000. Forced to 100 000.")
            self.send(':TRIGger:ACQuire:COUNt {}'.format(value))
        except:
            raise
        else:
            self.logger.info('The system {} trigger count has been set to {}.'.format(self.id, value))
    
    def config_trigger_count_min(self):
        self.config_trigger_count('MINimum')
    def config_trigger_count_max(self):
        self.config_trigger_count('MAXimum')
    
    def config_trigger_timer(self, value):
        try:
            if isinstance(value, float):
                if value < 1e-5:
                    value = 1e-5
                    self.logger.warning("Value for trigger timer interval can't be < 1e-5 s. Forced to 1e-5 s.")
                elif value > 1e5:
                    value = 1e5
                    self.logger.warning("Value for trigger timer interval can't be > 1e+5 s. Forced to 1e+5 s.")
            self.send(':TRIGger:ACQuire:TIMer {}'.format(value))
        except:
            raise
        else:
            self.logger.info('The system {} trigger timer interval has been set to {}.'.format(self.id, value))
    
    def config_trigger_timer_min(self):
        self.config_trigger_timer('MINimum')
    def config_trigger_timer_max(self):
        self.config_trigger_timer('MAXimum')


    # Measurements operations
    ###

    # Amperemeter
    def switch_amperemeter(self, switch):
        try:
            if self.is_boolean_string(switch):
                self.send(':INPut:STATe {}'.format(switch).upper())
            elif switch in (0, 1):
                self.send(':INPut:STATe {}'.format(switch))
            else:
                raise ValueError("Parameter switch={} should be 'ON' or 'OFF'.".format(switch))
        except:
            raise
        else:
            self.logger.info('The amperemeter of {} has been switched to {}.'.format(self.id, switch))
    
    def enable_amperemeter(self):
        self.switch_amperemeter('ON')
    def disable_amperemeter(self):
        self.switch_amperemeter('OFF')

    # Measurements actions
    def init_meas(self):
        try:
            self.send(':INITiate:IMMediate:ACQuire')
        except:
            raise
        else:
            self.logger.info('Measurements have been initiated by {}.'.format(self.id))

    def fetch_data(self, data_label):
        try:
            if data_label in self.result_data_type:
                return self.query_data(':FETCh:ARRay:{}?'.format(self._available_result_data_types[data_label]))
            else:
                raise RuntimeError('The specified result data type {} has not been selected before measurements.'.format(data_label))
        except:
            raise
        else:
            self.logger.info('Measurements have been initiated by {}.'.format(self.id))

    # def run_data_meas(self):
    #     try:
    #         self.logger.info('{} is running measurements...'.format(self.id))
    #         return self.query_data(':READ:ARRay?')
    #     except:
    #         raise
    #     else:
    #         self.logger.info('{} is running measurements...done!'.format(self.id))
