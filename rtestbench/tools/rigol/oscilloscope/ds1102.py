"""Module dedicated to the control of the Rigol electrometers ds1102x series."""


import logging

import rtestbench.constants as const 
from rtestbench.core import ToolInfo
from rtestbench.tools.electrometer import Electrometer


class DS1102E(Electrometer):
    """Interface common to all electrometers from the Rigol ds1102x series."""

    def __init__(self, info: ToolInfo):
        Electrometer.__init__(self, info)

        # Generic properties
        self._properties.transfer_formats = const.RTB_TRANSFERT_FORMATS

        self._properties.bin_data_endianness = "big"
        self._properties.bin_data_header = "ieee"
        self._properties.bin_data_type = 'Q'

        self._properties.read_msg_terminator = '\n'
        self._properties.write_msg_terminator = '\n'

        self._properties.text_data_converter = 'e'
        self._properties.text_data_separator = ','

        self._properties.activated_transfer_format = 'ascii'

        # Specific properties
        self._properties.update_properties(
            activated_view_mode=None,
            activated_subview_mode=None
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
        if mode in Rigol_ds1102x_VIEW_MODES:
            try:
                self.send(":DISPlay:VIEW {}".format(mode))
            except IOError:
                logging.error("Cannot change the view mode!")
                raise
            else:
                self._properties.activated_view_mode = mode
        else:
            raise ValueError("The mode argument must be in {}".format(Rigol_ds1102x_VIEW_MODES))

    def get_view_mode(self) -> str:
        try:
            self._properties.activated_view_mode = self.query(":DISP:VIEW?")
        except IOError:
            raise
        else:
            return self._properties.activated_view_mode

    def set_subview_mode(self, mode: str):
        if mode in Rigol_ds1102x_SUBVIEW_MODES:
            try:
                self.send(":DISPlay:VIEW:SINGle:SPANel {}".format(mode))
            except IOError:
                logging.error("Cannot change the subview mode!")
                raise
            else:
                self._properties.activated_subview_mode = mode
        else:
            raise ValueError("The mode argument must be in {}".format(Rigol_ds1102x_VIEW_MODES))

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
        if source_name in Rigol_ds1102x_TRIGGER_SOURCES:
            try:
                self.send(":TRIGger:ACQuire:SOURce:SIGNal {}".format(source_name))
            except IOError as err:
                logging.error(err)
                raise RuntimeError("Cannot set the trigger source to {} on {}.".format(source_name, self._info))
        else:
            raise ValueError("The source_name argument must be in {}.".format(Rigol_ds1102x_TRIGGER_SOURCES))
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
