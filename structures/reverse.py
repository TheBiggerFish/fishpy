"""
This module provides a class to be used in reversing the sorting direction of the payload object
"""


class Reverse:
    """This class reverses the sorting direction of the payload object"""

    def __init__(self, payload):
        self.payload = payload

    def __lt__(self, other: 'Reverse') -> bool:
        return self.payload > other.payload

    def __gt__(self, other: 'Reverse') -> bool:
        return self.payload < other.payload

    def __eq__(self, other: 'Reverse') -> bool:
        return self.payload == other.payload

    def __str__(self) -> str:
        return str(self.payload)

    def __hash__(self) -> int:
        return hash(self.payload)
