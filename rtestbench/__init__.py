
# VISA protocol
import visa

# Logger
from . import _logger

# Scientific computations
import numpy as np
import pandas as pd

# R-testbench packages
import rtestbench.tools
import rtestbench.tools._factory as tool_factory



class RTestBench():

    """Manager for Remote Test Bench.
    """


    # Messages
    ###

    def say_welcome(self):
        msg = '\n<------------------------'
        msg += '   Welcome to R-testbench   '
        msg += '------------------------>\n\n'
        return msg

    def say_goodbye(self):
        msg = '\n\n<------------------------'
        msg += '            Bye!            '
        msg += '------------------------>\n'
        return msg
        # return '\n\nBye!\n'

    def say_ready(self):
        return 'R-testbench is ready for use\n'
    

    # Constructor and destructor
    ###
    
    def __init__(self, verbose=True):

        """Initialize the visa ressource manager.

        If verbose, prints the welcome and ready messages.
        """

        self._verbose = verbose

        self.logger = _logger.config(logger_name='rtestbench')

        if self._verbose:
            print(self.say_welcome())
        
        try:
            self.logger.debug('Calling the VISA resource manager...')
            self.__visa_rm = visa.ResourceManager()
            self.__visa_rm
            self.logger.debug('Calling the VISA resource manager...done')
        except OSError as error_msg:
            self.logger.critical(error_msg)
            raise OSError("CRITICAL error: R-testbench cannot continue working.")
        else:
            if self._verbose:
                self.logger.info(self.say_ready())
        
        self.__attached_resources = list()
    

    def __del__(self):
        # logger.debug('Closing all connected resources...')
        for device in self.__attached_resources:
            device.detach_visa_resource()
        # logger.debug('Closing all connected resources...')

        # logger.debug('Closing the VISA resource manager...')
        self.__visa_rm.close()
        # logger.debug('Closing the VISA resource manager...done')

        if self._verbose:
            print(self.say_goodbye())

    
    # Resources management
    ###

    def detect_resources(self):
        return self.__visa_rm.list_resources()
    
    def print_available_resources(self):
        available_resources = self.detect_resources()

        if available_resources:
            print('Available resources:', available_resources)
        else:
            print('No available resources')
    

    def attach_resource(self, addr):
        try:
            new_resource = tool_factory.construct_tool(self.__visa_rm, addr)
        except (RuntimeError, ValueError) as error_msg:
            self.logger.error(error_msg)
            raise ValueError('Impossible to attach resource to R-testbench')
        else:
            self.logger.info('New resource attached to R-testbench: {}'.format(new_resource))
            self.__attached_resources.append(new_resource)
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
