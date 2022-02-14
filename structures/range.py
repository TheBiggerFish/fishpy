"""This module provides a class to represent a range of numbers"""

from typing import Union

from .bound import Bounds


class Range:
    """
    This class represents a range of numbers and provides several methods to
    interact with the range
    """

    def __init__(self, lower: Union[int, float],
                 upper: Union[int, float],
                 upper_inclusive: bool = False):
        self.bound = Bounds(lower, upper, upper_inclusive)
        self._max = upper + 1 if upper_inclusive else upper
        self._cur = lower

    @staticmethod
    def from_string(string: str, upper_inclusive: bool = False) -> 'Range':
        """Generate a range from a string in format (low-high)"""

        split = string.split('-')
        l, r = int(split[0]), int(split[1])
        return Range(l, r, upper_inclusive)

    def size(self) -> Union[int, float]:
        """Return the size of the range"""
        offset = (1 if self.bound.upper.inclusive else 0) - 1
        return self.bound.upper - self.bound.lower + offset

    def step(self, current_integer: int, step_size: int = 1) -> int:
        next_int = current_integer + step_size
        if next_int not in self:
            next_int = self.bound.lower.value
        return next_int

    def __len__(self) -> Union[int, float]:
        return self.size()

    def __lt__(self, other: 'Range') -> bool:
        return self.bound.lower < other.bound.lower

    def __gt__(self, other: 'Range') -> bool:
        return self.bound.lower > other.bound.lower

    def __str__(self) -> str:
        rchar = ']' if self.bound.upper.inclusive else ')'
        return f'[{self.bound.lower}-{self.bound.upper}{rchar}'

    def __contains__(self, item) -> bool:
        return item in self.bound

    def division(self, parts: int, which: int) -> 'Range':
        """
        Return a section of the range by splitting the range into parts and
        selecting one
        """

        if which >= parts:
            raise IndexError('Cannot select a chunk out of range')
        step = (self.bound.upper-self.bound.lower) // parts
        if float(step).is_integer():
            step = int(step)
        lower = self.bound.lower + (step * which)
        upper = lower + step
        return Range(lower, upper)

    def __iter__(self):
        if not isinstance(self.bound.lower, int):
            raise TypeError(
                f'\'{type(self.bound.lower.value)}\' cannot be interpreted as an integer')
        if not isinstance(self.bound.upper, int):
            raise TypeError(
                f'\'{type(self.bound.upper.value)}\' cannot be interpreted as an integer')
        return self

    def __next__(self) -> int:
        if self._cur >= self.bound.upper:
            raise StopIteration
        value = self._cur
        self._cur += 1
        return value
