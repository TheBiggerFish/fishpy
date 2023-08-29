"""This module provides a class for storing points on an x-y plane"""

from typing import Final, Union

from ..point import Point
from .vector2d import Vector2D


class Point2D(Point):
    """
    This class can be used to represent and evaluate points on an x-y plane
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def __sub__(self, other: 'Point2D') -> Vector2D:
        return Vector2D(self.x-other.x, self.y-other.y)

    def __hash__(self) -> int:
        return hash(tuple(self._coords))

    def __getitem__(self, key: Union[int, slice]) -> float:
        if isinstance(key, int):
            if key > 1:
                raise IndexError(
                    f'{self.__class__.__name__} supports only 2 dimensions')
        return super().__getitem__(key)

    def __setitem__(self, index: int, value: float) -> None:
        if not isinstance(index, int):
            raise TypeError('Dimension index must be an integer')

        if index > 1:
            raise IndexError(
                f'{self.__class__.__name__} supports only 2 dimensions')
        return super().__setitem__(index, value)

    def is_above(self, other: 'Point2D') -> bool:
        """Predicate function which returns whether self is above other"""
        return self.y > other.y

    def is_below(self, other: 'Point2D') -> bool:
        """Predicate function which returns whether self is below other"""
        return self.y < other.y

    def is_left_of(self, other: 'Point2D') -> bool:
        """Predicate function which returns whether self is left of other"""
        return self.x < other.x

    def is_right_of(self, other: 'Point2D') -> bool:
        """Predicate function which returns whether self is right of other"""
        return self.x > other.x

    def is_lattice(self) -> bool:
        """
        Predicate function which returns whether self is a point on the
        integer lattice
        """
        return float(self.x).is_integer() and float(self.y).is_integer()


ORIGIN: Final[Point2D] = Point2D(0, 0)
