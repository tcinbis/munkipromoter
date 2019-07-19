#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:54.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import logging
import os
import sys
from logging import handlers

from utils.config import conf

logfile_main = os.path.join(conf.LOG_DIR, conf.LOG_FILENAME)


def get_logger(name, formatter="default"):
    """
    This method returns a logger instance. If this method is called for the
    first time with a specific name two handlers, a file handler and a stream
    handler will be added to the logger so that the output of the logger will be
    displayed on the stdout and also written into a log file. If this method is
    called multiple times, each time the same logger instance is returned.
    By doing this it does not matter where the logger is instantiated and all
    loggers with the same name write into the same file.

    :param name: The name the logger should have. If the same as another these
    are two times the same loggers.
    :param formatter: Either 'default' (information: time, loglevel, filename,
    message) or 'simple' (only message)
    :return: The logger instance
    """
    logger = logging.getLogger(name)

    if len(logger.handlers) != 0:
        return logger

    # File Handler
    file_handler = handlers.RotatingFileHandler(
        logfile_main, mode="w", backupCount=conf.LOG_BACKUP_COUNT
    )

    if formatter == "default":
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s,%(lineno)d:\t%(message)s",
                datefmt="%b %d %Y %H:%M:%S %Z",
            )
        )
    elif formatter == "simple":
        file_handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        raise ValueError("Formatter must be simple or default")

    # Stream Handler
    stream_handler = logging.StreamHandler(sys.stdout)

    if formatter == "default":
        stream_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s,%(lineno)d:\t%(message)s",
                datefmt="%b %d %Y %H:%M:%S %Z",
            )
        )
    elif formatter == "simple":
        stream_handler.setFormatter(logging.Formatter("%(message)s"))

    logger.setLevel(conf.LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
