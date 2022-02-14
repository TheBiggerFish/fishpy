"""Additional functions related to networking"""

import socket
from typing import Optional

from ..logging import Logger


def online(logger: Optional[Logger] = None) -> bool:
    """Predicate function to check if server has connected to internet"""

    try:
        if logger is not None:
            logger.debug('Checking internet connection')
        socket.create_connection(('8.8.8.8', 53)).close()
        if logger is not None:
            logger.debug('Connected to internet')
        return True
    except socket.error as err:
        if logger is not None:
            logger.error('Error connecting to internet: %s', str(err))
        return False
