"""The core of the rtestbench package.

rtestbench relies on PyVISA, NumPy and pandas.
"""


import numpy as np
import pandas as pd
import visa

from rtestbench import _chat
from rtestbench import _logger
from rtestbench.tools.keysight import _factory as keysight_factory


SUPPORTED_DATA_CONTAINERS = (np.ndarray, list, tuple)
SUPPORTED_TRANSFERT_FORMATS = ('text', 'ascii', 'bin', 'bin32', 'bin64')
SUPPORTED_ENDIAN_ORDER = ('big', 'little')



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
        return "The tool is a(n) {} from {}, {} model (SN = {}), connected by {}".format(
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
        _data_container: A container class to store the data retrieved from the tool (recommended: numpy.ndarray).
        _transfer_format: A list representing the available transfer formats for communication between the tool and the computer.
        bin_data_header: A str for the optional header that is in front of binary data.
        _endian: A str stating if binary data is big or little endian.
    """

    def __init__(self):
        self._data_container = np.ndarray

        self._transfer_formats = []

        self.bin_data_header = None
        self._endian = None
    

    @property
    def data_container(self):
        return self._data_container

    @data_container.setter
    def data_container(self, class_name):
        if class_name in SUPPORTED_DATA_CONTAINERS:
            self._data_container = class_name
        else:
            raise ValueError("The class_name argument must be in {}.".format(SUPPORTED_DATA_CONTAINERS))


    @property
    def transfer_formats(self):
        return self._transfer_formats

    @transfer_formats.setter
    def transfer_formats(self, formats: list):
        if all(fmt in SUPPORTED_TRANSFERT_FORMATS for fmt in formats):
            self._transfer_formats = formats
        else:
            raise ValueError("The formats argument must be a list containing at least one element among {}.".format(SUPPORTED_TRANSFERT_FORMATS))


    @property
    def endian(self):
        return self._endian

    @endian.setter
    def endian(self, order: str):
        if order in SUPPORTED_ENDIAN_ORDER:
            self._endian = order
        else:
            raise ValueError("The order argument must be in {}.".format(SUPPORTED_ENDIAN_ORDER))
    

    def add_properties(self, **kw):
        """Add all key-values as properties."""

        self.__dict__.update(kw)


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
        try:
            return self._virtual_interface.query(request)
        except visa.VisaIOError as err:
            raise IOError("Cannot get an answer from the request {}; origin comes from {}.".format(request, err.description))
    
    def query_data(self, request):
        pass


    # Common SCPI commands
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
            new_tool = self._build_specific_tool()
        except (NotImplementedError, ValueError):
            new_tool = self._build_generic_tool()
        
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
        else:
            return new_tool_interface
    
    def _identify_tool(self, tool_interface: visa.Resource) -> str:
        """Sends the '*IDN?' SCPI command to identify the tool that is connected.

        Raises:
            RuntimeError: The tool does not answer the identification request.
        """

        try:
            full_id = tool_interface.query('*IDN?')
        except visa.VisaIOError:
            raise IOError("No response: impossible to identify the tool {}".format(tool_interface))
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
                return keysight_factory.find_and_build(tool_info.model, tool_info.serial_number)
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
            device.detach_visa_resource()
            if enable_log:
                self.logger.info('Resource detached from R-testbench: {}'.format(device))
        self._attached_tools.clear()
        if enable_log:
            self.logger.debug('Closing all connected resources...done')

    
    # Information about tools
    def detect_tools(self) -> tuple:
        return self._visa_rm.list_resources()
    
    def print_available_tools(self):
        available_tools = self.detect_tools()

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
        except (AttributeError, ValueError, RuntimeError) as error_msg:
            self.logger.error(error_msg)
            raise ValueError('Impossible to attach the tool to R-testbench')
        else:
            self.logger.info('New tool attached to R-testbench: {}'.format(new_tool))
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
        self.log_data(file_type, path, args)

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
            raise NotImplemented('Not supported because needs dependencies.') # data_to_log.to_feather(path + '.feather')
        elif file_type == 'hdf5':
            raise NotImplemented('Not supported because needs dependencies.') # data_to_log.to_hdf(path + '.h5', key='data', format='fixed')
        else:
            self.log_warning("Unknown file_type {} passed to the log_data() function. Ignored.".format(file_type))
