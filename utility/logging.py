"""Module to simplify logging configuration"""

import logging
import logging.handlers
import socket
import sys
from typing import Optional

NAME_TO_LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
}


class Logger(logging.Logger):
    """
    Class to simplify logging configuration

    Logs to stdout if no host provided
    """

    def __init__(self, service_name: str, host: Optional[str] = None,
                 port: str = '514', level: str = 'INFO'):
        super().__init__(service_name)

        if host is None:
            handler = logging.StreamHandler(sys.stdout)
            log_format = '%(asctime)s%(msecs)03d | ' + socket.gethostname() + \
                ' [%(levelname)s] %(process)s {%(name)s} %(message)s'
        else:
            handler = logging.handlers.SysLogHandler(address=(host, int(port)))
            log_format = socket.gethostname() + \
                ' [%(levelname)s] %(process)s {%(name)s} %(message)s'

        dt_format = '%Y-%m-%d %H:%M:%S.'
        formatter = logging.Formatter(fmt=log_format,
                                      datefmt=dt_format)
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(level)
