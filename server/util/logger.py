import logging
import sys


def setup_logger(filename):
    """
    Sets up a simple logger which logs to a 'output.log' file.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        f'%(asctime)s - %(levelname)7s - %(name)s: %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('Logger is created.')