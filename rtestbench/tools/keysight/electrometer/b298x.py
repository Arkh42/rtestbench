"""Module dedicated to the control of the Keysight electrometers B298x series."""


import logging

import rtestbench.constants as const 
from rtestbench.core import ToolInfo
from rtestbench.tools.electrometer import Electrometer


KEYSIGHT_B298X_VIEW_MODE_METER = ("SINGle1")
KEYSIGHT_B298X_VIEW_MODE_ROLL = ("ROLL")
KEYSIGHT_B298X_VIEW_MODE_HISTOGRAM = ("HISTogram")
KEYSIGHT_B298X_VIEW_MODE_GRAPH = ("GRAPH")
KEYSIGHT_B298X_VIEW_MODES = KEYSIGHT_B298X_VIEW_MODE_METER + KEYSIGHT_B298X_VIEW_MODE_ROLL + KEYSIGHT_B298X_VIEW_MODE_HISTOGRAM + KEYSIGHT_B298X_VIEW_MODE_GRAPH

KEYSIGHT_B298X_SUBVIEW_MODE_ROLL = ("ROLL")
KEYSIGHT_B298X_SUBVIEW_MODE_HISTOGRAM = ("HISTogram")
KEYSIGHT_B298X_SUBVIEW_MODE_RANGE = ("RANGe")
KEYSIGHT_B298X_SUBVIEW_MODE_TRIGGER = ("TRIGger")
KEYSIGHT_B298X_SUBVIEW_MODE_FUNCTION = ("FUNCtion")
KEYSIGHT_B298X_SUBVIEW_MODES = KEYSIGHT_B298X_SUBVIEW_MODE_ROLL + KEYSIGHT_B298X_SUBVIEW_MODE_HISTOGRAM + KEYSIGHT_B298X_SUBVIEW_MODE_RANGE + KEYSIGHT_B298X_SUBVIEW_MODE_TRIGGER + KEYSIGHT_B298X_SUBVIEW_MODE_FUNCTION

KEYSIGHT_B298X_MEAS_DATA_TYPE_CHARGE = ("CHARge")
KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT = ("CURRent")
KEYSIGHT_B298X_MEAS_DATA_TYPE_HUMIDITY = ("HUMidity")
KEYSIGHT_B298X_MEAS_DATA_TYPE_RESISTANCE = ("RESistance")
KEYSIGHT_B298X_MEAS_DATA_TYPE_TEMPERATURE = ("TEMPerature")
KEYSIGHT_B298X_MEAS_DATA_TYPE_TIME = ("TIME")
KEYSIGHT_B298X_MEAS_DATA_TYPE_VOLTAGE = ("VOLTage")

KEYSIGHT_B2981_DISPLAY_XDATA_TYPES = KEYSIGHT_B298X_MEAS_DATA_TYPE_TIME
KEYSIGHT_B2981_DISPLAY_YDATA_TYPES = KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT
KEYSIGHT_B2981_MEAS_DATA_TYPES = KEYSIGHT_B2981_DISPLAY_XDATA_TYPES + KEYSIGHT_B2981_DISPLAY_YDATA_TYPES

KEYSIGHT_B2983_DISPLAY_XDATA_TYPES = KEYSIGHT_B2981_DISPLAY_XDATA_TYPES
KEYSIGHT_B2983_DISPLAY_YDATA_TYPES = KEYSIGHT_B2981_DISPLAY_YDATA_TYPES
KEYSIGHT_B2983_MEAS_DATA_TYPES = KEYSIGHT_B2981_MEAS_DATA_TYPES

KEYSIGHT_B2985_DISPLAY_XDATA_TYPES = KEYSIGHT_B298X_MEAS_DATA_TYPE_TIME
KEYSIGHT_B2985_DISPLAY_YDATA_TYPES = KEYSIGHT_B298X_MEAS_DATA_TYPE_CHARGE + KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT + KEYSIGHT_B298X_MEAS_DATA_TYPE_RESISTANCE + KEYSIGHT_B298X_MEAS_DATA_TYPE_VOLTAGE
KEYSIGHT_B2985_MEAS_DATA_TYPES = KEYSIGHT_B2985_DISPLAY_XDATA_TYPES + KEYSIGHT_B2985_DISPLAY_YDATA_TYPES + KEYSIGHT_B298X_MEAS_DATA_TYPE_HUMIDITY + KEYSIGHT_B298X_MEAS_DATA_TYPE_TEMPERATURE

KEYSIGHT_B2987_DISPLAY_XDATA_TYPES = KEYSIGHT_B2985_DISPLAY_XDATA_TYPES
KEYSIGHT_B2987_DISPLAY_YDATA_TYPES = KEYSIGHT_B2985_DISPLAY_YDATA_TYPES
KEYSIGHT_B2987_MEAS_DATA_TYPES = KEYSIGHT_B2985_MEAS_DATA_TYPES

KEYSIGHT_B298X_TRIGGER_SOURCE_AUTO = ("AINT")
KEYSIGHT_B298X_TRIGGER_SOURCE_BUS = ("BUS")
KEYSIGHT_B298X_TRIGGER_SOURCE_TIMER = ("TIMer")
KEYSIGHT_B298X_TRIGGER_SOURCE_INTERNAL1 = ("INT1")
KEYSIGHT_B298X_TRIGGER_SOURCE_INTERNAL2 = ("INT2")
KEYSIGHT_B298X_TRIGGER_SOURCE_LAN = ("LAN")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL1 = ("EXT1")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL2 = ("EXT2")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL3 = ("EXT3")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL4 = ("EXT4")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL5 = ("EXT5")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL6 = ("EXT6")
KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL7 = ("EXT7")
KEYSIGHT_B298X_TRIGGER_SOURCE_TRIGGER_IN = ("TIN")
KEYSIGHT_B298X_TRIGGER_SOURCES = KEYSIGHT_B298X_TRIGGER_SOURCE_AUTO + KEYSIGHT_B298X_TRIGGER_SOURCE_BUS + KEYSIGHT_B298X_TRIGGER_SOURCE_TIMER + KEYSIGHT_B298X_TRIGGER_SOURCE_INTERNAL1 + KEYSIGHT_B298X_TRIGGER_SOURCE_INTERNAL2 + KEYSIGHT_B298X_TRIGGER_SOURCE_LAN + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL1 + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL2 + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL3 + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL4 + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL5 + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL6 + KEYSIGHT_B298X_TRIGGER_SOURCE_EXTERNAL7 + KEYSIGHT_B298X_TRIGGER_SOURCE_TRIGGER_IN

KEYSIGHT_B2985_TEMPERATURE_SENSOR_THERMOCOUPLE = ("TC")
KEYSIGHT_B2985_TEMPERATURE_SENSOR_HUMIDITY = ("HSENsor")
KEYSIGHT_B2985_TEMPERATURE_SENSORS = KEYSIGHT_B2985_TEMPERATURE_SENSOR_THERMOCOUPLE + KEYSIGHT_B2985_TEMPERATURE_SENSOR_HUMIDITY

KEYSIGHT_B2987_TEMPERATURE_SENSOR_THERMOCOUPLE = KEYSIGHT_B2985_TEMPERATURE_SENSOR_THERMOCOUPLE
KEYSIGHT_B2987_TEMPERATURE_SENSOR_HUMIDITY = KEYSIGHT_B2985_TEMPERATURE_SENSOR_HUMIDITY
KEYSIGHT_B2987_TEMPERATURE_SENSORS = KEYSIGHT_B2985_TEMPERATURE_SENSORS

KEYSIGHT_B2985_TEMPERATURE_UNIT_CELSIUS = ('C')
KEYSIGHT_B2985_TEMPERATURE_UNIT_FAHRENHEIT = ('F')
KEYSIGHT_B2985_TEMPERATURE_UNIT_KELVIN = ('K')
KEYSIGHT_B2985_TEMPERATURE_UNITS = KEYSIGHT_B2985_TEMPERATURE_UNIT_CELSIUS + KEYSIGHT_B2985_TEMPERATURE_UNIT_FAHRENHEIT + KEYSIGHT_B2985_TEMPERATURE_UNIT_KELVIN

KEYSIGHT_B2987_TEMPERATURE_UNIT_CELSIUS = KEYSIGHT_B2985_TEMPERATURE_UNIT_CELSIUS
KEYSIGHT_B2987_TEMPERATURE_UNIT_FAHRENHEIT = KEYSIGHT_B2985_TEMPERATURE_UNIT_FAHRENHEIT
KEYSIGHT_B2987_TEMPERATURE_UNIT_KELVIN = KEYSIGHT_B2985_TEMPERATURE_UNIT_KELVIN
KEYSIGHT_B2987_TEMPERATURE_UNITS = KEYSIGHT_B2985_TEMPERATURE_UNITS

KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_NORMAL = ("NORMal")
KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_HIGHZ = ("HIZ")
KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_ZERO = ("ZERO")
KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITIONS = KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_NORMAL + KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_HIGHZ + KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_ZERO

KEYSIGHT_B2987_OUTPUT_SOURCE_OFFCONDITION_NORMAL = KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_NORMAL
KEYSIGHT_B2987_OUTPUT_SOURCE_OFFCONDITION_HIGHZ = KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_HIGHZ
KEYSIGHT_B2987_OUTPUT_SOURCE_OFFCONDITION_ZERO = KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_ZERO
KEYSIGHT_B2987_OUTPUT_SOURCE_OFFCONDITIONS = KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITIONS

KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATE_COMMON = ("COMMon")
KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATE_FLOAT = ("FLOat")
KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATES = KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATE_COMMON + KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATE_FLOAT

KEYSIGHT_B2987_OUTPUT_SOURCE_LOW_STATE_COMMON = KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATE_COMMON
KEYSIGHT_B2987_OUTPUT_SOURCE_LOW_STATE_FLOAT = KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATE_FLOAT
KEYSIGHT_B2987_OUTPUT_SOURCE_LOW_STATES = KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATES



class B298X(Electrometer):
    """Interface common to all electrometers from the Keysight B298X series."""

    def __init__(self, info: ToolInfo):
        Electrometer.__init__(self, info)

        # Generic properties
        self._properties.transfer_formats = const.RTB_TRANSFERT_FORMATS

        self._properties.bin_data_endianness = "big"
        self._properties.bin_data_header = "ieee"
        self._properties.bin_data_type = 'f'

        self._properties.read_msg_terminator = '\n'
        self._properties.write_msg_terminator = '\n'

        self._properties.text_data_converter = 'e'
        self._properties.text_data_separator = ','

        # Specific properties
        self._properties.update_properties(
            activated_view_mode=None,
            activated_subview_mode=None,
            activated_display_ydata_type=KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT,
            activated_meas_data_types=KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT
        )


    # Generic commands
    def query_number_data(self):
        """Queries the number of data available in the buffer."""

        try:
            number_data = self.query(":SYSTem:DATA:QUANtity?")
        except IOError as err:
            logging.warning("{} cannot send the number of data available!".format(self._info))
        else:
            logging.debug("{} is going to send data: {} expected.".format(self._info, number_data))
            return number_data


    # Common SCPI commands
    def set_data_transfer_format(self, tsf_format: str, data_type: str):
        """Sets the data transfer format of the tool."""

        try:
            self._properties.activated_transfer_format = tsf_format
        except ValueError as err:
            logging.error(err)
            raise RuntimeError("Cannot sets the data transfer format as {} for the tool {}.".format(tsf_format, self._info))

        if tsf_format in const.RTB_TRANSFERT_FORMAT_TEXT:
            try:
                self.send(":FORMat:DATA ASCii")
                self._properties.text_data_converter = data_type
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot sets the data transfer format as ASCII for the tool {}.".format(self._info))
            except ValueError:
                raise
            else:
                logging.debug("The data transfer format is now ASCII.")
        elif tsf_format in const.RTB_TRANSFERT_FORMAT_BIN:
            if data_type in const.RTB_BIN_DATA_TYPES_FLOAT:
                try:
                    self.send(":FORMat:DATA REAL,32")
                    self._properties.bin_data_type = data_type
                except IOError as err:
                    logging.error(err)
                    raise RuntimeError("Cannot sets the data transfer format as bin32 for the tool {}.".format(self._info))
                else:
                    logging.debug("The data transfer format is now binary (32 bits).")
            elif data_type in const.RTB_BIN_DATA_TYPES_DOUBLE:
                try:
                    self.send(":FORMat:DATA REAL,64")
                    self._properties.bin_data_type = data_type
                except IOError as err:
                    logging.error(err)
                    raise RuntimeError("Cannot sets the data transfer format as bin64 for the tool {}.".format(self._info))
                else:
                    logging.debug("The data transfer format is now binary (64 bits).")
            else:
                raise NotImplementedError("The data_type argument must be in {} or in {} to use binary data for the tool {}.".format(
                    const.RTB_BIN_DATA_TYPES_FLOAT,
                    const.RTB_BIN_DATA_TYPES_DOUBLE,
                    self._info
                ))


    def lock(self):
        """Requests a remote lock of the tool's I/O interface."""

        try:
            lock_status = self.query(":SYSTem:LOCK:REQuest?")
            if lock_status != "1":
                logging.warning("{} cannot be locked!".format(self._info))
        except IOError:
            logging.warning("{} cannot be locked!".format(self._info))
            raise
        else:
            logging.info("{} is now locked.".format(self._info))

    def unlock(self):
        """Releases the remote lock of the tool's I/O interface."""

        try:
            self.send(":SYSTem:LOCK:RELease")
        except IOError:
            logging.warning("{} cannot be unlocked!".format(self._info))
            raise
        else:
            logging.info("{} is now unlocked.".format(self._info))


    # View mode
    def set_display(self, switch: bool):
        try:
            if switch:
                self.send(":DISPlay:ENABle ON")
            else:
                self.send(":DISPlay:ENABle OFF")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot switch the display of {}.".format(self._info))
                

    def set_view_mode(self, mode: str):
        if mode in KEYSIGHT_B298X_VIEW_MODES:
            try:
                self.send(":DISPlay:VIEW {}".format(mode))
            except IOError:
                logging.error("Cannot change the view mode!")
                raise
            else:
                self._properties.activated_view_mode = mode
        else:
            raise ValueError("The mode argument must be in {}".format(KEYSIGHT_B298X_VIEW_MODES))

    def get_view_mode(self) -> str:
        try:
            self._properties.activated_view_mode = self.query(":DISP:VIEW?")
        except IOError:
            raise
        else:
            return self._properties.activated_view_mode

    def set_subview_mode(self, mode: str):
        if mode in KEYSIGHT_B298X_SUBVIEW_MODES:
            try:
                self.send(":DISPlay:VIEW:SINGle:SPANel {}".format(mode))
            except IOError:
                logging.error("Cannot change the subview mode!")
                raise
            else:
                self._properties.activated_subview_mode = mode
        else:
            raise ValueError("The mode argument must be in {}".format(KEYSIGHT_B298X_VIEW_MODES))

    def get_subview_mode(self) -> str:
        try:
            self._properties.activated_subview_mode = self.query(":DISPlay:VIEW:SINGle:SPANel?")
        except IOError:
            raise
        else:
            return self._properties.activated_subview_mode


    # Measurement type interface
    def set_meas_data_types(self, data_types: list):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def get_meas_data_types(self) -> str:
        try:
            return self.query(":FORMat:ELEMents:SENSe?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the measurement data type.")


    def set_display_xdata_type(self, data_type: str):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def get_display_xdata_type(self) -> str:
        try:
            return self.query(":DISPlay:VIEW:GRAPh:X:ELEMent?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the data type on the X-axis.")


    def set_display_ydata_type(self, data_type: str):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def get_display_ydata_type(self) -> str:
        try:
            return self.query(":DISPlay:VIEW:{}:Y:ELEMent?".format(self._properties.activated_view_mode))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the data type on the Y-axis.")


    # Scale and offset interface
    def set_scale(self, axis: str, scale: float):
        if axis.upper() == 'X':
            self.set_xscale(scale)
        elif axis.upper() == 'Y':
            self.set_yscale(scale)
        else:
            raise ValueError("The axis argument must be in ('x', 'X', 'y', 'Y').")

    def set_offset(self, axis: str, offset: float):
        if axis.upper() == 'X':
            self.set_xoffset(offset)
        elif axis.upper() == 'Y':
            self.set_yoffset(offset)
        else:
            raise ValueError("The axis argument must be in ('x', 'X', 'y', 'Y').")

    def set_xscale(self, scale: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:X:PDIVision {}".format(scale))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the X-axis scale on {}.".format(self._info))

    def set_yscale(self, scale: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:Y:PDIVision:{} {}".format(self._properties.activated_display_ydata_type, scale))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the Y-axis scale on {}.".format(self._info))

    def set_xoffset(self, offset: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:X:OFFSet {}".format(offset))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the X-axis offset on {}.".format(self._info))
    
    def set_yoffset(self, offset: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:Y:OFFSet:{} {}".format(self._properties.activated_display_ydata_type, offset))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the Y-axis offset on {}.".format(self._info))


    # Range interface
    def set_range(self, value: float):
        try:
            self.send(":SENSe:{}:RANGe:UPPer {}".format(self._properties.activated_display_ydata_type, value))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the range to {} on {}.".format(value, self._info))
    def get_range(self):
        try:
            return self.query(":SENSe:{}:RANGe:UPPer?".format(self._properties.activated_meas_data_type))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the range from {}.".format(self._info))

    def set_autorange(self, switch: bool):
        try:
            if switch:
                self.send(":SENSe:{}:RANGe:AUTO ON".format(self._properties.activated_display_ydata_type))
            else:
                self.send(":SENSe:{}:RANGe:AUTO OFF".format(self._properties.activated_display_ydata_type))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot modify autorange configuration on {}.".format(self._info))

    def set_range_min(self):
        self.set_range("MIN")
    def set_range_max(self):
        self.set_range("MAX")


    # Aperture (integration) time interface
    def set_aperture_time(self, value: float):
        try:
            self.send(":SENSe:{}:APERture {}".format(self._properties.activated_display_ydata_type, value))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the aperture/integration time to {} on {}.".format(value, self._info))
    def get_aperture_time(self):
        try:
            return self.query(":SENSe:{}:APERture?".format(self._properties.activated_meas_data_type))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the aperture/integration time from {}.".format(self._info))

    def set_aperture_time_min(self):
        self.set_aperture_time("MIN")
    def set_aperture_time_max(self):
        self.set_aperture_time("MAX")


    # Trigger interface
    def set_trigger_source(self, source_name: str):
        if source_name in KEYSIGHT_B298X_TRIGGER_SOURCES:
            try:
                self.send(":TRIGger:ACQuire:SOURce:SIGNal {}".format(source_name))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the trigger source to {} on {}.".format(source_name, self._info))
        else:
            raise ValueError("The source_name argument must be in {}.".format(KEYSIGHT_B298X_TRIGGER_SOURCES))
    def get_trigger_source(self) -> str:
        try:
            return self.query(":TRIGger:ACQuire:SOURce:SIGNal?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the trigger source from {}.".format(self._info))

    def set_trigger_count(self, value: int):
        try:
            self.send(":TRIGger:ACQuire:COUNt {}".format(value))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the trigger count to {} on {}.".format(value, self._info))

    def set_trigger_count_min(self):
        self.set_trigger_count("MIN")
    def set_trigger_count_max(self):
        self.set_trigger_count("MAX")

    def get_trigger_count(self) -> int:
        try:
            return self.query(":TRIGger:ACQuire:COUNt?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the trigger count from {}.".format(self._info))

    def set_trigger_timer(self, value: float):
        try:
            self.send(":TRIGger:ACQuire:TIMer {}".format(value))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot set the trigger timer interval to {} on {}.".format(value, self._info))

    def set_trigger_timer_min(self):
        self.set_trigger_timer("MIN")
    def set_trigger_timer_max(self):
        self.set_trigger_timer("MAX")

    def get_trigger_timer(self) -> float:
        try:
            return self.query(":TRIGger:ACQuire:TIMer?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the trigger timer interval from {}.".format(self._info))


    # Amperemeter interface
    def enable_amperemeter(self):
        try:
            self.send(":INPut:STATe ON")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot enable the ampemeter input on {}.".format(self._info))
    def disable_amperemeter(self):
        try:
            self.send(":INPut:STATe OFF")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot disable the ampemeter input on {}.".format(self._info))


    # Measurement actions interface
    def initiate_measurement(self):
        try:
            self.send(":INITiate:IMMediate:ACQuire")
        except IOError as err:
            logging.log(err)
            raise RuntimeError("Cannot initiate measurement with {}.".format(self._info))

    def fetch_data(self, meas_data_type):
        try:
            return self.query_data(":FETCh:ARRay:{}?".format(meas_data_type))
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot fetch data from {}.".format(self._info))
    
    def fetch_all_data(self):
        try:
            return self.query_data(":FETCh:ARRay?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot fetch data from {}.".format(self._info))


class B2981(B298X):
    """Interface specific to the Keysight B2981 electrometer."""

    def __init__(self, info: ToolInfo):
        B298X.__init__(self, info)


    # Measurement type interface
    def set_meas_data_types(self, data_types: list):
        if all(data_type in KEYSIGHT_B2981_MEAS_DATA_TYPES for data_type in data_types):
            try:
                self.send(":FORMat:ELEMents:SENSe {}".format(','.join(data_types)))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the measurement data type.")
            else:
                self._properties.activated_meas_data_types = data_types
        else:
            raise ValueError("The data_types argument must be in {}.".format(KEYSIGHT_B2981_MEAS_DATA_TYPES))


    def set_display_xdata_type(self, data_type: str):
        if data_type in KEYSIGHT_B2981_DISPLAY_XDATA_TYPES:
            try:
                self.send(":DISPlay:VIEW:GRAPh:X:ELEMent {}".format(data_type))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the data type on the X-axis.")
        else:
            raise ValueError("The data_type argument must be in {}.".format(KEYSIGHT_B2981_DISPLAY_XDATA_TYPES))

    def set_display_ydata_type(self, data_type: str):
        if data_type in KEYSIGHT_B2981_DISPLAY_YDATA_TYPES:
            try:
                self.send(":DISPlay:VIEW:{}:Y:ELEMent {}".format(self._properties.activated_view_mode, data_type))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the data type on the Y-axis.")
            else:
                self._properties.activated_display_ydata_type = data_type
        else:
            raise ValueError("The data_type argument must be in {}.".format(KEYSIGHT_B2981_DISPLAY_YDATA_TYPES))


class B2983(B2981):
    """Interface specific to the Keysight B2983 electrometer."""

    def __init__(self, info: ToolInfo):
        B2981.__init__(self, info)


class B2985(B298X):
    """Interface specific to the Keysight B2985 electrometer."""

    def __init__(self, info: ToolInfo):
        B298X.__init__(self, info)
    
    # Measurement type interface
    def set_meas_data_types(self, data_types: list):
        if all(data_type in KEYSIGHT_B2985_MEAS_DATA_TYPES for data_type in data_types):
            try:
                self.send(":FORMat:ELEMents:SENSe {}".format(','.join(data_types)))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the measurement data type.")
            else:
                self._properties.activated_meas_data_types = data_types
        else:
            raise ValueError("The data_types argument must be in {}.".format(KEYSIGHT_B2985_MEAS_DATA_TYPES))

    def set_display_xdata_type(self, data_type: str):
        if data_type in KEYSIGHT_B2985_DISPLAY_XDATA_TYPES:
            try:
                self.send(":DISPlay:VIEW:GRAPh:X:ELEMent {}".format(data_type))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the data type on the X-axis.")
        else:
            raise ValueError("The data_type argument must be in {}.".format(KEYSIGHT_B2985_DISPLAY_XDATA_TYPES))

    def set_display_ydata_type(self, data_type: str):
        if data_type in KEYSIGHT_B2985_DISPLAY_YDATA_TYPES:
            try:
                self.send(":DISPlay:VIEW:{}:Y:ELEMent {}".format(self._properties.activated_view_mode, data_type))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the data type on the Y-axis.")
            else:
                self._properties.activated_display_ydata_type = data_type
        else:
            raise ValueError("The data_type argument must be in {}.".format(KEYSIGHT_B2985_DISPLAY_YDATA_TYPES))


    # Output source
    def enable_output_source(self):
        try:
            self.send(":OUTPut:STATe ON")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot enable the output source of {}.".format(self._info))
    def disable_output_source(self):
        try:
            self.send(":OUTPut:STATe OFF")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot enable the output source of {}.".format(self._info))

    def set_output_source_off_condition(self, condition:str):
        if condition in KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITIONS:
            try:
                self.send(":OUTPut:OFF:MODE {}".format(condition))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the output source off confition of {}.".format(self._info))
        else:
            raise ValueError("The condition argument must be in {}.".format(KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITIONS))
    def get_output_source_off_condition(self):
        try:
            return self.query(":OUTPut:OFF:MODE?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the output source off confition from {}.".format(self._info))

    def set_output_source_low_state(self, state:str):
        if state in KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATES:
            try:
                self.send(":OUTPut:LOW {}".format(state))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the output source low state of {}.".format(self._info))
        else:
            raise ValueError("The state argument must be in {}.".format(KEYSIGHT_B2985_OUTPUT_SOURCE_LOW_STATES))
    def get_output_source_low_state(self):
        try:
            return self.query(":OUTPut:LOW?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the output source low state from {}.".format(self._info))


    # Temperature sensing
    def set_temperature_sensor(self, sensor: str):
        if sensor in KEYSIGHT_B2985_TEMPERATURE_SENSORS:
            try:
                self.send(":SYSTem:TEMPerature:SELect {}".format(sensor))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the temperature sensor of {}.".format(self._info))
        else:
            raise ValueError("The sensor argument must be in {}.".format(KEYSIGHT_B2985_TEMPERATURE_SENSORS))
    def get_temperature_sensor(self):
        try:
            return self.query(":SYSTem:TEMPerature:SELect?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the temperature sensor from {}.".format(self._info))

    def set_temperature_unit(self, unit: str):
        if unit in KEYSIGHT_B2985_TEMPERATURE_UNITS:
            try:
                self.send(":SYSTem:TEMPerature:UNIT {}".format(unit))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the temperature unit of {}.".format(self._info))
        else:
            raise ValueError("The unit argument must be in {}.".format(KEYSIGHT_B2985_TEMPERATURE_UNITS))
    def get_temperature_unit(self):
        try:
            return self.query(":SYSTem:TEMPerature:UNIT?")
        except IOError as err:
            logging.error(err)
            raise RuntimeError("Cannot get the temperature unit from {}.".format(self._info))



class B2987(B2985):
    """Interface specific to the Keysight B2987 electrometer."""

    def __init__(self, info: ToolInfo):
        B2985.__init__(self, info)
