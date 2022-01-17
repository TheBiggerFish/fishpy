"""Module to simplify logging configuration"""

import logging
import logging.handlers
import socket
import sys
from typing import Optional


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
        else:
            handler = logging.handlers.SysLogHandler(address=(host, int(port)))

        formatter = logging.Formatter(fmt=f'{socket.gethostname()} '
                                      '[%(levelname)s] %(process)s '
                                      '{%(name)s} %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(level)
