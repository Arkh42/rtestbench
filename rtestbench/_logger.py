
import logging


def config(logger_name=''):

    # set logger
    if logger_name:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # define handlers
    console_loghandler = logging.StreamHandler()
    console_loghandler.setLevel(logging.INFO)

    file_loghandler = logging.FileHandler(filename='rtestbench.log', mode='w')
    file_loghandler.setLevel(logging.DEBUG)

    # set format
    formatter = logging.Formatter('%(name)s: %(asctime)s - %(levelname)s - %(message)s')

    console_loghandler.setFormatter(formatter)
    file_loghandler.setFormatter(formatter)

    # assign handlers
    logger.addHandler(console_loghandler)
    logger.addHandler(file_loghandler)

    return logger
