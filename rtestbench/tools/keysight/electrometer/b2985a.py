
from rtestbench.tools.keysight.electrometer._interface import Interface


class B2985A(Interface):
    """Specific class to control a Keysight B2985A electrometer.

    This instrument allows current, charge and resistance measurement.
    It textends the commands defined in the Keysight electrometer interface to its own peculiar abilities.
    """


    # Initialization & properties
    ###

    # Initialization
    def __init__(self, serial_num):

        Interface.__init__(self, model='B2985A', serial_num=serial_num)

        self._available_meas_data_types.update({
            'Q': 'CHARge', 'q': 'CHARge',
            'V': 'VOLTage', 'v': 'VOLTage',
            'R': 'RESistance', 'r': 'RESistance'})
        self._available_result_data_types.update(self._available_meas_data_types)
        self._available_result_data_types.update({'source': 'SOURce'})

        self._available_output_off_cond = {
            'default': 'NORMal', 'normal': 'NORMal',
            'hiz': 'HIZ', 'HiZ': 'HIZ', 'HIZ': 'HIZ',
            'zero': 'ZERO', 0:'ZERO', '0':'ZERO'}
        self._available_output_low_states = {'float': 'FLOat', 'com': 'COMMon'}

        self._available_T_sensors = {
            'thermocouple': 'TC', 'tc': 'TC', 'TC': 'TC',
            'humidity_sensor': 'HSENsor', 'hs': 'HSENsor', 'HS': 'HSENsor'}
        self._available_T_units = {
            'celsius': 'C', 'C': 'C',
            'kelvin': 'K', 'K': 'K',
            'fahrenheit': 'F', 'F': 'F'}

    # Output source conditions/states
    def is_available_output_off_cond(self, key):
        if key in self._available_output_off_cond.keys():
            return True
        else:
            return False

    def is_available_output_low_state(self, key):
        if key in self._available_output_low_states.keys():
            return True
        else:
            return False
    
    # Temperature measurements
    def is_available_T_sensor(self, key):
        if key in self._available_T_sensors.keys():
            return True
        else:
            return False
    
    def is_available_T_unit(self, key):
        if key in self._available_T_units.keys():
            return True
        else:
            return False


    # Measurements conditions
    ###

    # Output source
    def switch_output_source(self, switch):
        try:
            if self.is_boolean_string(switch):
                self.send(':OUTPut:STATe {}'.format(switch.upper()))
            elif switch in (0, 1):
                self.send(':OUTPut:STATe {}'.format(switch))
            else:
                raise ValueError("Parameter switch={} should be 'ON' or 'OFF'.".format(switch))
        except:
            raise
        else:
            self.logger.info('The system {} output source has been switched to {}.'.format(self.id, switch))

    def enable_output_source(self):
        self.switch_output_source('ON')
    def disable_output_source(self):
        self.switch_output_source('OFF')
    

    def config_output_source_off_cond(self, condition):
        try:
            if self.is_available_output_off_cond(condition):
                self.send(':OUTPut:OFF:MODE {}'.format(self._available_output_off_cond[condition]))
            else:
                raise ValueError(
                    "Output source's OFF condition {0} is not available in system {1}.\nLegal conditions are: {2}".format(
                        condition, self.id, self._available_output_off_cond))
        except:
            raise
        else:
            self.logger.info("The system {} output source's OFF condition has been set to {}.".format(self.id, condition))

    def config_output_source_low_state(self, state):
        try:
            if self.is_available_output_low_state(state):
                self.send(':OUTPut:LOW {}'.format(self._available_output_low_states[state]))
            else:
                raise ValueError(
                    "Output source's low state {0} is not available in system {1}.\nLegal states are: {2}".format(
                        condition, self.id, self._available_output_low_states))
        except:
            raise
        else:
            self.logger.info("The system {} output source's low state has been set to {}.".format(self.id, condition))


    # Temperature sensing
    def config_temperature_sensor(self, sensor):
        try:
            if self.is_available_T_sensor(sensor):
                self.send(':SYSTem:TEMPerature:SELect {}'.format(self._available_T_sensors[sensor]))
            else:
                raise ValueError(
                    "Temperature sensor {0} is not available in system {1}.\nLegal values are: {2}".format(
                        sensor, self.id, self._available_T_sensors))
        except:
            raise
        else:
            self.logger.info("The system {} temperature sensor has been set to {}.".format(self.id, sensor))

    def config_temperature_unit(self, unit):
        try:
            if self.is_available_T_unit(unit):
                self.send(':SYSTem:TEMPerature:UNIT {}'.format(self._available_T_units[unit]))
            else:
                raise ValueError(
                    "Temperature unit {0} is not available in system {1}.\nLegal values are: {2}".format(
                        unit, self.id, self._available_T_units))
        except:
            raise
        else:
            self.logger.info("The system {} temperature unit has been set to {}.".format(self.id, unit))


    # Measurements operations
    ###

    # Temperature sensing
    def meas_temperature(self):
        try:
            temperature = self.query_data(':SYSTem:TEMPerature?')
        except:
            raise
        else:
            return temperature[0]
