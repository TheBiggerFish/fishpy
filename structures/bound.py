"""Provides a class to be used in comparing a value to a bound"""

from typing import Any


class Bound:
    """Class to be used in comparing a value to a bound"""

    def __init__(self,value,inclusive:bool):
        self.value = value
        self.inclusive = inclusive

    def __lt__(self,other:Any):
        return self.value < other

    def __gt__(self,other:Any):
        return self.value > other

    def __le__(self,other:Any):
        return self.value <= other

    def __ge__(self,other:Any):
        return self.value >= other

    def __eq__(self,other:Any):
        return self.value == other

    def __ne__(self,other:Any):
        return self.value != other
