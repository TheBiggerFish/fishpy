"""This module provides a class to represent a range of numbers"""

from typing import Iterable, Union

from .bound import Bound


class Range:
    """
    This class represents a range of numbers and provides several methods to
    interact with the range
    """

    def __init__(self,lower:Union[int,float],
                 upper:Union[int,float],
                 lower_inclusive:bool=True,
                 upper_inclusive:bool=False):
        self.lower = Bound(lower,lower_inclusive)
        self.upper = Bound(upper,upper_inclusive)

    @staticmethod
    def from_string(string,lower_inclusive:bool=True,upper_inclusive:bool=False) -> 'Range':
        """Generate a range from a string in format (low-high)"""

        split = string.split('-')
        l,r = int(split[0]),int(split[1])
        return Range(l,r,lower_inclusive,upper_inclusive)

    def size(self) -> Union[int,float]:
        """Return the size of the range"""
        offset = (1 if self.lower.inclusive else 0) + (1 if self.upper.inclusive else 0) - 1
        return self.upper - self.lower + offset

    def __len__(self) -> Union[int,float]:
        return self.size()

    def __lt__(self,other) -> bool:
        return self.lower < other.lower

    def __gt__(self,other) -> bool:
        return self.lower > other.lower

    def __str__(self) -> str:
        lchar = '[' if self.lower.inclusive else '('
        rchar = ']' if self.upper.inclusive else ')'
        return f'{lchar}{self.lower}-{self.upper}{rchar}'

    def __contains__(self,item) -> bool:
        if self.lower.inclusive:
            if self.upper.inclusive:
                return self.lower <= item <= self.upper
            return self.lower <= item < self.upper

        if self.upper.inclusive:
            return self.lower < item <= self.upper
        return self.lower < item < self.upper

    def division(self,parts:int,which:int) -> 'Range':
        """
        Return a section of the range by splitting the range into parts and
        selecting one
        """

        if which >= parts:
            raise IndexError('Cannot select a chunk out of range')
        step = (self.upper-self.lower) / parts
        if float(step).is_integer():
            step = int(step)
        lower = self.lower + (step * which)
        upper = lower + step
        return Range(lower,upper)

    def __iter__(self) -> Iterable[Union[int,float]]:
        if not isinstance(self.lower,int):
            raise TypeError(f'\'{type(self.lower)}\' cannot be interpreted as an integer')
        if not isinstance(self.upper,int):
            raise TypeError(f'\'{type(self.upper)}\' cannot be interpreted as an integer')
        lower = self.lower if self.lower.inclusive else self.lower+1
        upper = self.upper+1 if self.upper.inclusive else self.upper
        for i in range(lower,upper):
            yield i
