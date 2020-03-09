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



class RTestBench(object):

    """Manager for Remote Test Bench.

    Attributes:
        _VERBOSE: A boolean indicating the quantity of information sent through the terminal.
        _attached_resources: A list of the resources (instruments) attached to the remote testbench.
        _visa_rm: A ResourceManager from the visa module.
        chat: A TerminalChat for user interaction via the terminal.
        logger: A Logger handling log messages for streaming and printing.
    """
    

    def __init__(self, verbose=True):
        """Inits RTestBench with chat, logger, and VISA resource manager."""

        self._VERBOSE = verbose
        
        self._attached_resources = list()

        self.logger = _logger.make_logger('rtestbench', self._VERBOSE)
        self.chat = _chat.TerminalChat()


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
    

    def __del__(self):
        # logger.debug('Closing all connected resources...')
        for device in self._attached_resources:
            device.detach_visa_resource()
        # logger.debug('Closing all connected resources...')

        # logger.debug('Closing the VISA resource manager...')
        self._visa_rm.close()
        # logger.debug('Closing the VISA resource manager...done')

        if self._VERBOSE:
            self.chat.say_goodbye()

    
    # Resources management
    ###

    def detect_resources(self):
        return self._visa_rm.list_resources()
    
    def print_available_resources(self):
        available_resources = self.detect_resources()

        if available_resources:
            print('Available resources:', available_resources)
        else:
            print('No available resources')
    

    def attach_resource(self, addr):
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
    ###

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
    ###

    def log_data(self, format, path, *args):
        """Log data into a file.

        format: csv, pickle.
        
        path: absolute/relative path to the file into which the data is saved.
        The function assumes that the path exists.

        args: any number of tuples (header, data) where header is a string and data an iterable.
        """

        data_to_log = pd.DataFrame()

        for item in args:
            data_to_log[item[0]] = item[1]

        if format=='csv':
            data_to_log.to_csv(path + '.csv')
        elif format=='pickle':
            data_to_log.to_pickle(path + '.pkl')
        elif format=='feather':
            raise NotImplemented('Not supported because needs dependencies.') # data_to_log.to_feather(path + '.feather')
        elif format=='hdf5':
            raise NotImplemented('Not supported because needs dependencies.') # data_to_log.to_hdf(path + '.h5', key='data', format='fixed')
        else:
            self.log_warning("Unknown format {} passed to the log_data() function. Ignored.".format(format))
