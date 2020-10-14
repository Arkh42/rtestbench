"""The core of the rtestbench package.

rtestbench relies on PyVISA, NumPy and pandas.
"""


import logging
import numpy as np
import pandas as pd
import pyvisa as visa

try:
    import tables
except ImportError:
    _HAS_TABLES = False
else:
    _HAS_TABLES = True
try:
    import feather
except ImportError:
    _HAS_FEATHER = False
else:
    _HAS_FEATHER = True

from rtestbench import constants
from rtestbench import _chat
from rtestbench import _logger


##########################
# Generic tool interface #
##########################

class ToolInfo(object):
    """Gathers all information related to any Tool.
    
    Attributes:
        family: A str representing the family of the tool (e.g., oscilloscope or multimeter).
        manufacturer: A str containing the name of the manufacturer.
        model: A str providing the specific model of the tool.
        serial_number: A str giving the serial number of the tool.
        software_version: A str including the software version number of the tool.
        interface: A str describing the type of interface that connects the tool.
    """

    def __init__(self):
        self.family = None
        self.manufacturer = None
        self.model = None
        self.serial_number = None
        self.software_version = None
        self._interface = None

    def __str__(self):
        return "{} from {}, {} model (SN = {}), connected by {}".format(
            self.family, self.manufacturer, self.model, self.serial_number, self._interface)
    

    @property
    def interface(self):
        return self._interface
    
    @interface.setter
    def interface(self, interface_type: visa.constants.InterfaceType):
        if interface_type is None:
            self._interface = None
        elif interface_type == visa.constants.InterfaceType.gpib:
            self._interface = "GPIB"
        elif interface_type == visa.constants.InterfaceType.vxi:
            self._interface = "VXI, VME or MXI"
        elif interface_type == visa.constants.InterfaceType.gpib_vxi:
            self._interface = "GPIB VXI"
        elif interface_type == visa.constants.InterfaceType.asrl:
            self._interface = "Serial (RS-232 or RS-485)"
        elif interface_type == visa.constants.InterfaceType.pxi:
            self._interface = "PXI"
        elif interface_type == visa.constants.InterfaceType.tcpip:
            self._interface = "TCP/IP"
        elif interface_type == visa.constants.InterfaceType.usb:
            self._interface = "USB"
        elif interface_type == visa.constants.InterfaceType.rio:
            self._interface = "Rio"
        elif interface_type == visa.constants.InterfaceType.firewire:
            self._interface = "Firewire"
        elif interface_type == visa.constants.InterfaceType.rsnrp:
            self._interface = "Rohde & Schwarz Device via Passport"
        elif interface_type == visa.constants.InterfaceType.unknown:
            self._interface = "Unknown"
        else:
            raise ResourceWarning("Unexpected interface type: {}.".format(interface_type))


class ToolProperties(object):
    """Gathers all properties to configure any Tool.
    
    Attributes:
        data_container: A container class to store the data retrieved from the tool (recommended: numpy.ndarray).
        transfer_format: A list representing the available transfer formats for communication between the tool and the computer.
        bin_data_header: A str for the optional header that is in front of binary data.
        bin_data_endianness: A str stating if binary data is big or little endian.
        read_msg_terminator: A str describing the terminator for read messages.
        write_msg_terminator: A str describing the terminator for write messages.
        text_data_converter: A str that specifies the format in which the text (ASCII) data are received.
        text_data_separator: A character that specifies the separator used for text (ASCII) data.
        timeout: A float that expresses the timeout in milliseconds for all tool I/O operations.
        activated_transfer_format: A str specified the transfer format currently in use.
    """

    def __init__(self):
        self._data_container = np.ndarray
        self._transfer_formats = []

        self._bin_data_endianness = "little"
        self._bin_data_header = "ieee"
        self._bin_data_type = 'f'

        self._read_msg_terminator = '\n'
        self._write_msg_terminator = '\n'

        self._text_data_converter = 'f'
        self._text_data_separator = ','

        self._timeout = 0

        self._activated_transfer_format = None
    

    @property
    def data_container(self):
        return self._data_container

    @data_container.setter
    def data_container(self, class_name):
        if class_name in constants.RTB_DATA_CONTAINERS:
            self._data_container = class_name
        else:
            raise ValueError("The class_name argument must be in {}.".format(constants.RTB_DATA_CONTAINERS))

    @property
    def transfer_formats(self):
        return self._transfer_formats
    @transfer_formats.setter
    def transfer_formats(self, formats: list):
        if all(fmt in constants.RTB_TRANSFERT_FORMATS for fmt in formats):
            self._transfer_formats = formats
        else:
            raise ValueError("The formats argument must be a list containing at least one element among {}.".format(constants.RTB_TRANSFERT_FORMATS))

    @property
    def bin_data_endianness(self):
        return self._bin_data_endianness
    @bin_data_endianness.setter
    def bin_data_endianness(self, endianness: str):
        if endianness in constants.RTB_BIN_DATA_ENDIANNESSES:
            self._bin_data_endianness = endianness
        else:
            raise ValueError("The order argument must be in {}.".format(constants.RTB_BIN_DATA_ENDIANNESSES))

    @property
    def bin_data_header(self):
        return self._bin_data_header
    @bin_data_header.setter
    def bin_data_header(self, header_format):
        if header_format in constants.RTB_BIN_DATA_HEADERS:
            self._bin_data_header = header_format
        else:
            raise ValueError("The header_format argument must be in {}.".format(constants.RTB_BIN_DATA_HEADERS))

    @property
    def bin_data_type(self):
        return self._bin_data_type
    @bin_data_type.setter
    def bin_data_type(self, datatype):
        if datatype in constants.RTB_BIN_DATA_TYPES_FLOAT:
            self._bin_data_type = 'f'
        elif datatype in constants.RTB_BIN_DATA_TYPES_DOUBLE:
            self._bin_data_type = 'd'
        elif datatype in constants.RTB_BIN_DATA_TYPES_INT16:
            self._bin_data_type = 'h'
        elif datatype in constants.RTB_BIN_DATA_TYPES_INT32:
            self._bin_data_type = 'i'
        elif datatype in constants.RTB_BIN_DATA_TYPES_INT64:
            self._bin_data_type = 'q'
        elif datatype in constants.RTB_BIN_DATA_TYPES_UINT16:
            self._bin_data_type = 'H'
        elif datatype in constants.RTB_BIN_DATA_TYPES_UINT32:
            self._bin_data_type = 'I'
        elif datatype in constants.RTB_BIN_DATA_TYPES_UINT64:
            self._bin_data_type = 'Q'
        else:
            raise ValueError("The datatype argument must be in {}.".format(constants.RTB_BIN_DATA_TYPES))

    def parse_msg_terminator(self, msg_terminator: str) -> str:
        if msg_terminator in constants.RTB_MSG_CR_TERMINATORS:
            return '\r'
        elif msg_terminator in constants.RTB_MSG_CRLF_TERMINATORS:
            return '\r\n'
        elif msg_terminator in constants.RTB_MSG_LF_TERMINATORS:
            return '\n'
        else:
            raise ValueError("The msg_terminator argument must be in {}.".format(constants.RTB_MSG_TERMINATORS))

    @property
    def read_msg_terminator(self):
        return self._read_msg_terminator
    @read_msg_terminator.setter
    def read_msg_terminator(self, msg_terminator: str):
        self._read_msg_terminator = self.parse_msg_terminator(msg_terminator)

    @property
    def write_msg_terminator(self):
        return self._write_msg_terminator
    @write_msg_terminator.setter
    def write_msg_terminator(self, msg_terminator: str):
        self._write_msg_terminator = self.parse_msg_terminator(msg_terminator)

    @property
    def text_data_converter(self):
        return self._text_data_converter
    @text_data_converter.setter
    def text_data_converter(self, converter):
        if converter in constants.RTB_TEXT_DATA_CONVERTERS_BIN:
            self._text_data_converter = 'b'
        elif converter in constants.RTB_TEXT_DATA_CONVERTERS_OCT:
            self._text_data_converter = 'o'
        elif converter in constants.RTB_TEXT_DATA_CONVERTERS_HEX:
            self._text_data_converter = 'x'
        elif converter in constants.RTB_TEXT_DATA_CONVERTERS_DEC:
            self._text_data_converter = 'd'
        elif converter in constants.RTB_TEXT_DATA_CONVERTERS_FIX:
            self._text_data_converter = 'f'
        elif converter in constants.RTB_TEXT_DATA_CONVERTERS_EXP:
            self._text_data_converter = 'e'
        elif converter in constants.RTB_TEXT_DATA_CONVERTERS_STR:
            self._text_data_converter = 's'
        else:
            raise ValueError("The converter argument must be in {}.".format(constants.RTB_TEXT_DATA_CONVERTERS))

    @property
    def text_data_separator(self):
        return self._text_data_separator
    @text_data_separator.setter
    def text_data_separator(self, sep):
        if sep in constants.RTB_TEXT_DATA_SEPARATORS:
            self._text_data_separator = sep
        else:
            raise ValueError("The sep argument must be in {}.".format(constants.RTB_TEXT_DATA_SEPARATORS))

    @property
    def timeout(self):
        return self._timeout
    @timeout.setter
    def timeout(self, time_ms):
        if time_ms == "infinite":
            self._timeout = float('+inf')
        elif time_ms == "immediate":
            self._timeout = 0
        else:
            self._timeout = time_ms

    @property
    def activated_transfer_format(self):
        return self._activated_transfer_format
    @activated_transfer_format.setter
    def activated_transfer_format(self, tsf_format: str):
        if tsf_format in self.transfer_formats:
            self._activated_transfer_format = tsf_format
        else:
            raise ValueError("The tsf_format must be selected among the available transfer formats {}.".format(self.transfer_formats))


    def get_properties(self) -> dict:
        return self.__dict__

    def update_properties(self, **properties):
        """Updates passed properties."""

        for k, v in properties.items():
            setattr(self, str(k), v)
    

class Tool(object):
    """Generic class that defines the features common to all electronic tools.
    
    Tool can be used to implement a generic interface to send raw SCPI commands if the specific class does not exist.

    Attributes:
        _info: A ToolInfo object including family, manufacturer, model and serial number.
        _properties: A ToolProperties object for configuration.
        _virtual_interface: An object that represents the virtual software interface which allows to communicate with the tool.
    """

    def __init__(self, info: ToolInfo):
        self._info = info
        self._properties = ToolProperties()
        self._virtual_interface = None


    # Virtual interface management
    def connect_virtual_interface(self, interface):
        """Connects a virtual interface to the Tool object.

        Raises:
            AttributeError: An unexpected type of virtual interface has been passed.
            IOError: The VISA session is not valid.
            RuntimeError: A virtual interface is already attached.
        """

        if self._virtual_interface is None:
            try:
                interface.session
            except AttributeError:
                raise AttributeError("Unexpected virtual interface type {}.".format(interface))
            except visa.InvalidSession as error_msg:
                raise IOError(error_msg)
            else:
                self._virtual_interface = interface
                self._info.interface = self._virtual_interface.interface_type
                self._virtual_interface.read_termination = self._properties.read_msg_terminator
                self._virtual_interface.write_termination = self._properties.write_msg_terminator
        else:
            raise RuntimeError("A virtual interface has already been attached to the tool {}.".format(self._info))
    
    def disconnect_virtual_interface(self):
        """Disconnects the current virtual interface from the Tool object.
        """

        if self._virtual_interface is not None:
            self._virtual_interface.close()
            self._virtual_interface = None
    

    # Generic commands
    def send(self, command: str) -> int:
        """Sends an SCPI command which does not expect any return from the tool (e.g., '*RST').
        
        Returns:
            An int given the number of bytes sent to the tool.
        Raises:
            UnboundLocalError: No virtual interface is connected to the tool to send a command.
            IOError: An error occured while sending the command.
        """

        if self._virtual_interface is None:
            raise UnboundLocalError("No virtual interface connected to the tool {}.".format(self._info))
        else:
            try:
                self._virtual_interface.write(command)
            except visa.InvalidSession as err:
                raise RuntimeError("Cannot send the command {}; {}".format(command, err))
            except visa.VisaIOError as err:
                raise IOError("Cannot send the command {}; origin comes from {}.".format(command, err.description))
    
    def query(self, request: str) -> str:
        """Sends an SCPI request which expects an answer from the tool (e.g., '*IDN?').
        
        Returns:
            An str embedding the tool's answer.
        Raises:
            UnboundLocalError: No virtual interface is connected to the tool to send a command.
            IOError: An error occured because no answer was received from the tool.
        """

        if self._virtual_interface is None:
            raise UnboundLocalError("No virtual interface connected to the tool {}.".format(self._info))
        else:
            try:
                return self._virtual_interface.query(request)
            except visa.InvalidSession as err:
                raise RuntimeError("Cannot get an answer from the request {}; {}".format(request, err))
            except visa.VisaIOError as err:
                raise IOError("Cannot get an answer from the request {}; origin comes from {}.".format(request, err.description))
    
    def query_number_data(self):
        """Queries the number of data available in the buffer.
        
        This function must be implemented to use query_data() in binary values."""
        
        raise NotImplementedError("This function must be implemented by daughter classes.")

    def query_data(self, request, number_data="auto"):
        """Sends an SCPI request which expects data from the tool.
        
        Returns:
            A container embedding the tool's answer (see the container property).
        Raises:
            UnboundLocalError: No virtual interface is connected to the tool to send a command.
            IOError: An error occured because no answer was received from the tool.
        """

        if self._virtual_interface is None:
            raise UnboundLocalError("No virtual interface connected to the tool {}.".format(self._info))
        else:
            transfer_format = self._properties.activated_transfer_format
            if transfer_format is None:
                raise UnboundLocalError("No transfer format is activated for the tool {}.".format(self._info))
            else:
                try:
                    if transfer_format in ("text", "ascii"):
                        return self._virtual_interface.query_ascii_values(
                            request,
                            converter=self._properties.text_data_converter,
                            separator=self._properties.text_data_separator,
                            container=self._properties.data_container
                        )
                    elif transfer_format in ("bin", "binary"):
                        if number_data == "auto":
                            number_data = int(self.query_number_data())
                        else:
                            return self._virtual_interface.query_binary_values(
                                request,
                                datatype=self._properties.bin_data_type,
                                is_big_endian=True if self._properties.bin_data_endianness == "big" else False,
                                container=self._properties.data_container,
                                header_fmt=self._properties.bin_data_header,
                                data_points=number_data
                            )
                    else:
                        raise NotImplementedError("Unsupported transfer format {} is currently activated.".format(transfer_format))
                except visa.InvalidSession as err:
                    raise RuntimeError("Cannot get an answer from the request {}; {}".format(request, err))
                except visa.VisaIOError as err:
                    raise IOError("Cannot get an answer from the request {}; origin comes from {}.".format(request, err.description))


    # Common SCPI commands
    def set_timeout(self, time_ms):
        """Sets the timeout in milliseconds for all IO operations."""

        current_timeout = self._virtual_interface.timeout
        try:
            self._properties.timeout = time_ms
            self._virtual_interface.timeout = self._properties.timeout
        except:
            self._properties.timeout = current_timeout
            raise


    def set_data_transfer_format(self, tsf_format: str, data_type: str):
        """Sets the data transfer format of the tool."""

        raise NotImplementedError("This function must be implemented by daughter classes.")


    def clear_status(self):
        """Sends a command to clear the status registers."""

        self.send("*CLS")
    
    def reset(self):
        """Sends a command to reset the configuration."""

        self.send("*RST")


    def lock(self):
        """Requests a remote lock of the tool's I/O interface."""

        raise NotImplementedError("This function must be implemented by daughter classes.")

    def unlock(self):
        """Releases the remote lock of the tool's I/O interface."""

        raise NotImplementedError("This function must be implemented by daughter classes.")



###########
# Factory #
###########

from rtestbench.tools.keysight._factory import get_keysight_tool


class ToolFactory(object):
    """Factory for Tool objects.
    
    Attributes:
        _tool_manager: A manager class for tools detection and connection.
    """

    def __init__(self, tool_manager):
        
        self._tool_manager = tool_manager
    

    def get_tool(self, address: str) -> Tool:
        try:
            new_tool_interface = self._find_tool(address)
            tool_id = self._identify_tool(new_tool_interface)
            tool_info = self._parse_tool_id(tool_id)
        except (AttributeError, ValueError, IOError):
            raise

        try:
            new_tool = self._build_specific_tool(tool_info)
            logging.info("A specific/dedicated tool interface has been created for {}.".format(new_tool._info))
        except (NotImplementedError, ValueError) as err_msg:
            logging.warning("No specific/dedicated tool interface is available for the following reason: {}.".format(err_msg))
            new_tool = self._build_generic_tool(tool_info)
            logging.info("A generic tool interface has been created for {}.".format(new_tool._info))
        
        try:
            new_tool.connect_virtual_interface(new_tool_interface)
        except (AttributeError, IOError, RuntimeError):
            raise
        else:
            return new_tool

    
    def _find_tool(self, address: str) -> visa.Resource:
        try:
            new_tool_interface = self._tool_manager.open_resource(address)
        except AttributeError:
            raise AttributeError("The interface type is not recognized in {}.".format(address))
        except ValueError:
            raise ValueError("Something is wrong in the address {}.".format(address))
        except visa.VisaIOError as err:
            raise IOError("The tool cannot be reached @ {}; origin comes from: {}".format(address, err.description))
        else:
            return new_tool_interface
    
    def _identify_tool(self, tool_interface: visa.Resource) -> str:
        """Sends the '*IDN?' SCPI command to identify the tool that is connected.

        Raises:
            RuntimeError: The tool does not answer the identification request.
        """

        try:
            full_id = tool_interface.query('*IDN?')
        except visa.VisaIOError as err:
            raise IOError("No response: impossible to identify the tool {}. Origin comes from: {}".format(tool_interface, err.description))
        else:
            return full_id

    def _parse_tool_id(self, full_id: str) -> ToolInfo:
        """Parses the identifation string of the tool to create the corresponding ToolInfo.

        Raises:
            ValueError: The string cannot be parsed correctly.
        """

        info = full_id.split(",")

        if len(info) == 4:
            tool_info = ToolInfo()
            tool_info.manufacturer = info[0]
            tool_info.model = info[1]
            tool_info.serial_number = info[2]
            tool_info.software_version = info[3]
        else:
            raise ValueError("The full_id {} is not formatted as <manufacturer>, <model>, <serial number, <software version number>.".format(full_id))

        return tool_info
    
    def _build_specific_tool(self, tool_info) -> Tool:
        if tool_info.manufacturer == "Keysight Technologies":
            try:
                return get_keysight_tool(tool_info)
            except ValueError:
                raise
        else:
            raise NotImplementedError("The manufacturer {} has not been implemented yet.".format(tool_info.manufacturer))
    
    def _build_generic_tool(self, tool_info):
        return Tool(tool_info)



#######################
# R-testbench manager #
#######################

class RTestBenchManager(object):

    """Manager for Remote Test Bench.

    Attributes:
        _VERBOSE: A boolean indicating the quantity of information sent through the terminal.
        _attached_tools: A list of the resources (instruments) attached to the remote testbench.
        _visa_rm: A ResourceManager from the visa module.
        chat: A TerminalChat for user interaction via the terminal.
        logger: A Logger handling log messages for streaming and printing.
    """
    

    # Constructor
    def __init__(self, verbose=True, visa_library=''):
        """Initializes RTestBenchManager with chat, logger, and VISA resource manager."""

        self._VERBOSE = verbose
        self._attached_tools = list()
        self._visa_rm = None
        self.logger = _logger.make_logger('rtestbench', self._VERBOSE)
        self.chat = _chat.TerminalChat()

        self.logger.debug('Initializing the rtestbench manager...')

        if self._VERBOSE:
            self.chat.say_welcome()
        
        self.logger.debug('Calling the VISA resource manager...')
        try:
            self._visa_rm = visa.ResourceManager(visa_library)
        except OSError as error_msg:
            self.logger.critical(error_msg)
            raise OSError('R-testbench cannot be properly initialized.')
        else:
            self.logger.debug('Calling the VISA resource manager...done')
            if self._VERBOSE:
                self.chat.say_ready()
        
        self.logger.debug('Initializing the rtestbench manager...done')
    

    # Destructor and related close functions
    def __del__(self):
        """Ensures that all resources are properly closed at destruction."""

        self.close(enable_log=False) # Disable logging at destruction: cf. Issue #1

        if self._VERBOSE:
            self.chat.say_goodbye()
    

    def close(self, enable_log: bool = True):
        """Closes the R-testbench Manager."""

        if self._attached_tools:
            self.close_all_tools(enable_log)

        if self._visa_rm is not None:
            self._close_visa_rm(enable_log)
    
    def _close_visa_rm(self, enable_log: bool = True):
        """Closes the visa resource manager and sets it to None."""

        if enable_log:
            self.logger.debug('Closing the VISA resource manager...')
        self._visa_rm.close()
        self._visa_rm = None
        if enable_log: 
            self.logger.debug('Closing the VISA resource manager...done')
    
    def close_all_tools(self, enable_log: bool = True):
        """Closes all resources attached to the Manager and clear the corresponding list."""

        if enable_log:
            self.logger.debug('Closing all connected resources...')
        for device in self._attached_tools:
            device.disconnect_virtual_interface()
            if enable_log:
                self.logger.info('Resource detached from R-testbench: {}'.format(device))
        self._attached_tools.clear()
        if enable_log:
            self.logger.debug('Closing all connected resources...done')

    
    # Information about tools
    def detect_tools(self) -> tuple:
        return self._visa_rm.list_resources()
    
    def print_available_tools(self):
        available_tools = []

        try:
            available_tools = self.detect_tools()
        except visa.VisaIOError as err:
            if err.error_code == visa.constants.VI_ERROR_RSRC_NFOUND:
                pass # available tools is empty
            else:
                raise IOError(err.description)
        
        if available_tools:
            print('Available tools:', available_tools)
        else:
            print('No available tools.')
    

    # Tools management
    def attach_tool(self, address: str):
        """Attaches the tool at the specified address to the R-testbench manager.

        Args:
            address: The address of the tool to attach to R-testbench manager.

        Returns:
            A Tool (or any daughter-class object) corresponding to the tool attached to the Manager.

        Raises:
            ValueError: An error occured when trying to reach the specified address.
        """

        factory = ToolFactory(self._visa_rm)
        try:
            new_tool = factory.get_tool(address)
        except (AttributeError, ValueError, IOError, RuntimeError) as error_msg:
            self.logger.error(error_msg)
            raise ValueError('Impossible to attach the tool to R-testbench!')
        else:
            self.logger.info('New tool attached to R-testbench: {}.'.format(new_tool))
            self._attached_tools.append(new_tool)
            return new_tool


    # High-level log functions
    def log_info(self, message):
        """Log a message at INFO level."""

        self.logger.info(message)
    
    def log_warning(self, message):
        """Log a message at WARNING level."""

        self.logger.warning(message)
    
    def log_error(self, message):
        """Log a message at ERROR level."""

        self.logger.error(message)
    
    def log_critical(self, message):
        """Log a message at CRITICAL level."""

        self.logger.critical(message)
    

    # Data management
    def save_data(self, file_type: str, path: str, *args):
        self.log_data(file_type, path, *args)

    def log_data(self, file_type: str, path: str, *args):
        """Log data into a file.

        Args:
            file_type: The type of file in which the data is saved.
                Supported types are csv, pickle.
            path: The absolute/relative path to the file.
                The function assumes that the path exists.
            args: Any number of tuples (header, data) where header is a string and data an iterable.
        """

        data_to_log = pd.DataFrame()

        for item in args:
            data_to_log[item[0]] = item[1]

        if file_type == 'csv':
            data_to_log.to_csv(path + '.csv')
        elif file_type == 'pickle':
            data_to_log.to_pickle(path + '.pkl')
        elif file_type == 'feather':
            if _HAS_FEATHER:
                data_to_log.to_feather(path + '.feather')
            else:
                raise ImportError("The feather-format package seems to be missing. Cannot save data as feather files.")
        elif file_type == 'hdf5_fixed':
            if _HAS_TABLES:
                data_to_log.to_hdf(path + '.fixed.h5', key='data', format='fixed')
            else:
                raise ImportError("The PyTables package seems to be missing. Cannot save data as HDF5 files.")
        elif file_type == 'hdf5_table':
            if _HAS_TABLES:
                data_to_log.to_hdf(path + '.table.h5', key='data', format='table')
            else:
                raise ImportError("The PyTables package seems to be missing. Cannot save data as HDF5 files.")
        else:
            self.log_warning("Unknown file_type {} passed to the log_data() function. Ignored.".format(file_type))
