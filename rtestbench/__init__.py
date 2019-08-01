
# VISA protocol
import visa

# Logger
import logging

logging.basicConfig(
    filename='rtestbench.log', filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Scientific computations
import numpy as np
import pandas as pd



class RTestBench():

    """Manager for Remote Test Bench.
    """


    # Messages
    ###

    def say_welcome(self):
        msg = '\n------------------------'
        msg += ' Welcome to R-testbench'
        msg += '------------------------\n\n'
        return msg

    def say_goodbye(self):
        return '\n\nBye!\n'

    def say_ready(self):
        msg = 'R-testbench is ready for use\n'
        msg += '----------------------------\n'
        msg += '----------------------------\n\n'
    

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
            logging.debug('Calling the VISA resource manager...')
            self.__visa_rm = visa.ResourceManager()
            logging.debug('Calling the VISA resource manager...done')
        except OSError as error_msg:
            logging.critical(error_msg)
            raise OSError("CRITICAL error: R-testbench cannot continue working.")
        else:
            if self._verbose:
                print(self.say_ready())
    

    def __del__(self):
        logging.debug('Closing the VISA resource manager...')
        self.__visa_rm.close()
        logging.debug('Closing the VISA resource manager...done')

    
    # Resources management
    ###

    def detect_resources(self):
        return self.__visa_rm.list_resources()
    

    def attach_resource(self):
        pass
