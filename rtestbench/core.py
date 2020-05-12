"""The core of the rtestbench package.

rtestbench relies on PyVISA, NumPy and pandas.
"""


import numpy as np
import pandas as pd
import visa

from rtestbench import _chat
from rtestbench import _logger
import rtestbench.tools
import rtestbench.tools._factory as tool_factory


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
    """

    def __init__(self):
        self.family = None
        self.manufacturer = None
        self.model = None
        self.serial_number = None

    def __str__(self):
        return "The tool is a(n) {} from {}, {} model (SN = {})".format(
            self.family, self.manufacturer, self.model, self.serial_number)


class ToolProperties(object):
    """Gathers all properties to configure any Tool.
    
    Attributes:
        _data_container: A container class to store the data retrieved from the tool (recommended: numpy.ndarray).
        _transfer_format: A list representing the available transfer formats for communication between the tool and the computer.
        bin_data_header: A str for the optional header that is in front of binary data.
        _endian: A str stating if data is big or little endian.
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



class Tool(object):
    """Generic class that defines the features common to all electronic tools.
    
    Tool can be used to implement a generic interface to send raw SCPI commands if the specific class does not exist.

    Attributes:
        _virtual_interface: An object that represents the virtual software interface which allows to communicate with the tool.
        _info: A ToolInfo object including family, manufacturer, model and serial number.
        _properties: A ToolProperties object for configuration.
    """

    def __init__(self):
        self._virtual_interface = None

        self._info = ToolInfo()
        self._properties = ToolProperties()





#######################
# R-testbench manager #
#######################

class RTestBenchManager(object):

    """Manager for Remote Test Bench.

    Attributes:
        _VERBOSE: A boolean indicating the quantity of information sent through the terminal.
        _attached_resources: A list of the resources (instruments) attached to the remote testbench.
        _visa_rm: A ResourceManager from the visa module.
        chat: A TerminalChat for user interaction via the terminal.
        logger: A Logger handling log messages for streaming and printing.
    """
    

    # Constructor

    def __init__(self, verbose=True):
        """Initializes RTestBenchManager with chat, logger, and VISA resource manager."""

        self._VERBOSE = verbose
        
        self._attached_resources = list()

        self.logger = _logger.make_logger('rtestbench', self._VERBOSE)
        self.chat = _chat.TerminalChat()


        self.logger.debug('Initializing the rtestbench manager...')

        if self._VERBOSE: self.chat.say_welcome()
        
        self.logger.debug('Calling the VISA resource manager...')
        try:
            self._visa_rm = visa.ResourceManager()
        except OSError as err:
            self.logger.critical(error_msg)
            raise OSError('R-testbench cannot be properly initialized.')
        else:
            self.logger.debug('Calling the VISA resource manager...done')
            if self._VERBOSE: self.chat.say_ready()
        
        self.logger.debug('Initializing the rtestbench manager...done')
    

    # Destructor and related close functions

    def __del__(self):
        """Ensures that all resources are properly closed at destruction."""

        self.close(enable_log=False) # Disable logging at destruction: cf. Issue #1

        if self._VERBOSE: self.chat.say_goodbye()
    

    def close(self, enable_log: bool = True):
        """Closes the R-testbench Manager."""

        if self._attached_resources:
            self.close_all_resources(enable_log)

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
    
    def close_all_resources(self, enable_log: bool = True):
        """Closes all resources attached to the Manager and clear the corresponding list."""

        if enable_log:
            self.logger.debug('Closing all connected resources...')
        for device in self._attached_resources:
            device.detach_visa_resource()
            if enable_log:
                self.logger.info('Resource detached from R-testbench: {}'.format(device))
        self._attached_resources.clear()
        if enable_log:
            self.logger.debug('Closing all connected resources...done')

    
    # Information about resources

    def detect_resources(self) -> tuple:
        return self._visa_rm.list_resources()
    
    def print_available_resources(self):
        available_resources = self.detect_resources()

        if available_resources:
            print('Available resources:', available_resources)
        else:
            print('No available resources')
    

    # Resource management

    def attach_resource(self, addr: str):
        """
        Attaches the resource at the specified address to the R-testbench manager.

        Args:
            addr: The address of the resource to attach to R-testbench manager.

        Returns:
            A Tool (or any daughter-class object) corresponding to the resource attached to the Manager.

        Raises:
            ValueError: An error occured reaching the specified address.
        """

        try:
            new_resource = tool_factory.construct_tool(self._visa_rm, addr)
        except (RuntimeError, ValueError) as error_msg:
            self.logger.error(error_msg)
            raise ValueError('Impossible to attach resource to R-testbench')
        else:
            self.logger.info('New resource attached to R-testbench: {}'.format(new_resource))
            self._attached_resources.append(new_resource)
            return new_resource


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
