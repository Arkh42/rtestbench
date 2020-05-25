"""Module dedicated to the control of the Keysight electrometers B298x series."""


import logging

from rtestbench import constants
from rtestbench.core import ToolInfo
from rtestbench.tools.electrometer import Electrometer


KEYSIGHT_B298X_VIEW_MODE_METER = "SINGle1"
KEYSIGHT_B298X_VIEW_MODE_ROLL = "ROLL"
KEYSIGHT_B298X_VIEW_MODE_HISTOGRAM = "HISTogram"
KEYSIGHT_B298X_VIEW_MODE_GRAPH = "GRAPH"
KEYSIGHT_B298X_VIEW_MODES = (
    KEYSIGHT_B298X_VIEW_MODE_METER,
    KEYSIGHT_B298X_VIEW_MODE_ROLL,
    KEYSIGHT_B298X_VIEW_MODE_HISTOGRAM,
    KEYSIGHT_B298X_VIEW_MODE_GRAPH
)

KEYSIGHT_B298X_SUBVIEW_MODE_ROLL = "ROLL"
KEYSIGHT_B298X_SUBVIEW_MODE_HISTOGRAM = "HISTogram"
KEYSIGHT_B298X_SUBVIEW_MODE_RANGE = "RANGe"
KEYSIGHT_B298X_SUBVIEW_MODE_TRIGGER = "TRIGger"
KEYSIGHT_B298X_SUBVIEW_MODE_FUNCTION = "FUNCtion"
KEYSIGHT_B298X_SUBVIEW_MODES = (
    KEYSIGHT_B298X_SUBVIEW_MODE_ROLL,
    KEYSIGHT_B298X_SUBVIEW_MODE_HISTOGRAM,
    KEYSIGHT_B298X_SUBVIEW_MODE_RANGE,
    KEYSIGHT_B298X_SUBVIEW_MODE_TRIGGER,
    KEYSIGHT_B298X_SUBVIEW_MODE_FUNCTION
)

KEYSIGHT_B298X_MEAS_DATA_TYPE_CHARGE = "CHARge"
KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT = "CURRent"
KEYSIGHT_B298X_MEAS_DATA_TYPE_RESISTANCE = "RESistance"
KEYSIGHT_B298X_MEAS_DATA_TYPE_VOLTAGE = "VOLTage"
KEYSIGHT_B2981_MEAS_DATA_TYPES = (KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT)
KEYSIGHT_B2983_MEAS_DATA_TYPES = KEYSIGHT_B2981_MEAS_DATA_TYPES
KEYSIGHT_B2985_MEAS_DATA_TYPES = (
    KEYSIGHT_B298X_MEAS_DATA_TYPE_CHARGE,
    KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT,
    KEYSIGHT_B298X_MEAS_DATA_TYPE_RESISTANCE,
    KEYSIGHT_B298X_MEAS_DATA_TYPE_VOLTAGE
)
KEYSIGHT_B2987_MEAS_DATA_TYPES = KEYSIGHT_B2985_MEAS_DATA_TYPES



class B298X(Electrometer):
    """Interface common to all electrometers from the Keysight B298X series."""

    def __init__(self, info: ToolInfo):
        Electrometer.__init__(self, info)

        # Generic properties
        self._properties.transfer_formats = constants.RTB_TRANSFERT_FORMATS

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
            activated_meas_data_type=KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT
        )


    # Common SCPI commands
    def lock(self):
        """Requests a remote lock of the tool's I/O interface."""

        try:
            lock_status = self.query_data(":SYSTem:LOCK:REQuest?")
            if lock_status[0] != 1.0:
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
    def set_ydata_type(self, data_type: str):
        raise NotImplementedError("This function must be implemented in daughter classes.")

    def get_ydata_type(self) -> str:
        try:
            self.send(":DISPlay:VIEW:{}:Y:ELEMent?".format(self._properties.activated_view_mode))
        except IOError:
            logging.error("Cannot get the data type on the Y-axis.")
            raise


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
        except IOError as err_msg:
            logging.error(err_msg)
            raise RuntimeError("Cannot set the X-axis scale on {}.".format(self._info))

    def set_yscale(self, scale: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:Y:PDIVision:{} {}".format(self._properties.activated_meas_data_type, scale))
        except IOError as err_msg:
            logging.error(err_msg)
            raise RuntimeError("Cannot set the Y-axis scale on {}.".format(self._info))

    def set_xoffset(self, offset: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:X:OFFSet {}".format(offset))
        except IOError as err_msg:
            logging.error(err_msg)
            raise RuntimeError("Cannot set the X-axis offset on {}.".format(self._info))
    
    def set_yoffset(self, offset: float):
        try:
            self.send(":DISPlay:VIEW:ROLL:Y:OFFSet:{} {}".format(self._properties.activated_meas_data_type, scale))
        except IOError as err_msg:
            logging.error(err_msg)
            raise RuntimeError("Cannot set the Y-axis offset on {}.".format(self._info))


    # Range interface
    def set_range(self, value):
        raise NotImplementedError('This function must be implemented in daughter classes.')

    def set_autorange(self, switch: bool):
        raise NotImplementedError('This function must be implemented in daughter classes.')

    def set_range_min(self):
        raise NotImplementedError('This function must be implemented in daughter classes.')
    def set_range_max(self):
        raise NotImplementedError('This function must be implemented in daughter classes.')

    # Aperture (integration) time interface
    def set_aperture_time(self, value):
        raise NotImplementedError('This function must be implemented in daughter classes.')
    def set_integration_time(self, value):
        self.set_aperture_time(value)

    def set_aperture_time_min(self):
        raise NotImplementedError('This function must be implemented in daughter classes.')
    def set_aperture_time_max(self):
        raise NotImplementedError('This function must be implemented in daughter classes.')


class B2981(B298X):
    """Interface specific to the Keysight B2981 electrometer."""

    def __init__(self, info: ToolInfo):
        B298X.__init__(self, info)
    
    # Measurement type interface
    def set_ydata_type(self, data_type: str):
        if data_type in KEYSIGHT_B2981_MEAS_DATA_TYPES:
            try:
                self.send(":DISPlay:VIEW:{}:Y:ELEMent {}".format(self._properties.activated_view_mode, data_type))
            except IOError:
                logging.error("Cannot set the data type on the Y-axis.")
                raise
            else:
                self._properties.activated_meas_data_type = data_type
        else:
            raise ValueError("The data_type argument must be in {}.".format(KEYSIGHT_B2981_MEAS_DATA_TYPES))


class B2983(B2981):
    """Interface specific to the Keysight B2983 electrometer."""

    def __init__(self, info: ToolInfo):
        B2981.__init__(self, info)


class B2985(B298X):
    """Interface specific to the Keysight B2985 electrometer."""

    def __init__(self, info: ToolInfo):
        B298X.__init__(self, info)
    
    # Measurement type interface
    def set_ydata_type(self, data_type: str):
        if data_type in KEYSIGHT_B2985_MEAS_DATA_TYPES:
            try:
                self.send(":DISPlay:VIEW:{}:Y:ELEMent {}".format(self._properties.activated_view_mode, data_type))
            except IOError:
                logging.error("Cannot set the data type on the Y-axis.")
                raise
            else:
                self._properties.activated_meas_data_type = data_type
        else:
            raise ValueError("The data_type argument must be in {}.".format(KEYSIGHT_B2985_MEAS_DATA_TYPES))


class B2987(B2985):
    """Interface specific to the Keysight B2987 electrometer."""

    def __init__(self, info: ToolInfo):
        B2987.__init__(self, info)
