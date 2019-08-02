
# VISA protocol
import visa

# Logger
from . import _logger

logger = _logger.config(logger_name='rtestbench')

# Scientific computations
import numpy as np
import pandas as pd

# R-testbench packages
import tools



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

        if self._verbose:
            print(self.say_welcome())
        
        try:
            logger.debug('Calling the VISA resource manager...')
            self.__visa_rm = visa.ResourceManager()
            self.__visa_rm
            logger.debug('Calling the VISA resource manager...done')
        except OSError as error_msg:
            logger.critical(error_msg)
            raise OSError("CRITICAL error: R-testbench cannot continue working.")
        else:
            if self._verbose:
                logger.info(self.say_ready())
    

    def __del__(self):
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
    

    def attach_resource(self):
        pass
