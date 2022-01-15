"""Provides a class to be used in comparing a value to a bound"""


class Bound:
    """Class to be used in comparing a value to a bound"""

    def __init__(self,value,inclusive:bool):
        self.value = value
        self.inclusive = inclusive

class Bounds:
    """Class to be used in comparing a value to an upper and lower bound"""

    def __init__(self,lower,upper,upper_inclusive:bool=False):
        self.lower = Bound(lower,True)
        self.upper = Bound(upper,upper_inclusive)

    def __contains__(self,value):
        if self.upper.inclusive:
            return self.lower.value <= value <= self.upper.value
        return self.lower.value <= value < self.upper.value

    def __str__(self) -> str:
        rchar = ']' if self.upper.inclusive else ')'
        return f'[{self.lower.value}-{self.upper.value}{rchar}'

    def __repr__(self) -> str:
        return f'Bounds({repr(self.lower.value),repr(self.upper.value),self.upper.inclusive})'
