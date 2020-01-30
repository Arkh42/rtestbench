"""A logger configurator for the application.

Relies on the logging module.
"""


import logging


def make_logger(logger_name: str = '', verbose: bool = True) -> logging.Logger:
    """Returns a logger for handling log file and stream.

    Args:
        logger_name: The name of the logger.
        verbose: A boolean to choose between INFO and WARNING level printed in the terminal
    """

    if logger_name:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_loghandler = logging.StreamHandler()
    if verbose:
        console_loghandler.setLevel(logging.INFO)
    else:
        console_loghandler.setLevel(logging.WARNING)

    file_loghandler = logging.FileHandler(filename='rtestbench.log', mode='w')
    file_loghandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s: %(asctime)s - %(levelname)s - %(message)s')
    console_loghandler.setFormatter(formatter)
    file_loghandler.setFormatter(formatter)

    logger.addHandler(console_loghandler)
    logger.addHandler(file_loghandler)

    return logger
