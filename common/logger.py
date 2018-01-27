"""Log Handler Implementation"""
import os
import logging

from . import config, util


logging_config = config.Section('logging')
_loggers = []


def _get_handlers(
        log_dirs, log_type, log_file, stream_level, file_level,
        add_stream=True):
    """Helper for generating the loggers for directories"""
    handlers = []
    main_level = logging_config.get('main-level')
    if not hasattr(logging, main_level):
        raise ValueError('%s is not a valid log level!' % main_level)

    for log_dir in log_dirs:
        util.make_dir(log_dir)
        main_handler = logging.FileHandler(
            os.path.join(log_dir, logging_config.get('main-log')))

        main_handler.setLevel(getattr(logging, main_level))

        file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
        file_handler.setLevel(file_level)

        handlers.extend([main_handler, file_handler])

    if add_stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_level)
        handlers.append(stream_handler)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)8s - %(name)s - '
        '%(filename)s:%(lineno)s - %(funcName)s - %(message)s')

    for handler in handlers:
        handler.setFormatter(formatter)

    return handlers


def get_logger(
        log_type,
        log_file,
        stream_level=logging.ERROR,
        file_level=logging.DEBUG):
    """
    Return a logger
        - log_type: name to display
        - log_file: file to log to
        - stream_level: what level of logging should be displayed to the screen
        - file_level: what level of logging should be sent to the file
    """
    logger = logging.getLogger(log_type)
    while logger.handlers:
        logger.removeHandler(logger.handlers[0])

    logger.setLevel(logging.DEBUG)

    direc = os.path.abspath(logging_config.get('log-dir'))
    util.make_dir(direc)
    
    handlers = _get_handlers(
        log_dirs, log_type, log_file,
        stream_level, file_level)

    for handler in handlers:
        logger.addHandler(handler)
    _loggers.append(logger)

    return logger
