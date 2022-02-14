"""This module provides a class for storing points on an x-y plane"""

from typing import Final

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


ORIGIN: Final[Point2D] = Point2D(0, 0)
