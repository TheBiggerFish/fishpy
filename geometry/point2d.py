"""This module provides a class for storing points on an x-y plane"""

from random import uniform
from typing import Final, Iterable, List, Optional, Tuple

from .point import Point


class Point2D(Point):
    """
    This class can be used to represent and evaluate points on an x-y plane
    """

    def __init__(self,x:float,y:float):
        super().__init__((x,y))
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        """This property represents the x-value of self"""
        return self._x

    @x.setter
    def x(self,x:float):
        self._x = x

    @property
    def y(self) -> float:
        """This property represents the y-value of self"""
        return self._y

    @y.setter
    def y(self,y:float):
        self._y = y

    def __add__(self,other:'Point2D') -> 'Point2D':
        return Point2D(self.x+other.x,self.y+other.y)

    def __sub__(self,other:'Point2D') -> 'Point2D':
        return Point2D(self.x-other.x,self.y-other.y)

    def __neg__(self) -> 'Point2D':
        return Point2D(-self.x,-self.y)

    def __eq__(self,other:'Point2D') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(str(self.x * (10**10) + self.y))

    def __lt__(self,other:'Point2D') -> bool:
        return self.y < other.y and self.x < other.x

    def __gt__(self,other:'Point2D') -> bool:
        return not self < other and not self == other

    def __le__(self,other:'Point2D') -> bool:
        return self.y <= other.y and self.x <= other.x

    def __str__(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __repr__(self) -> str:
        return f'Point2D{str(self)}'

    def __mul__(self,scalar:float) -> 'Point2D':
        return Point2D(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:float) -> 'Point2D':
        return Point2D(self.x/scalar,self.y/scalar)

    def __floordiv__(self,scalar:float) -> 'Point2D':
        return Point2D(self.x//scalar,self.y//scalar)

    def __mod__(self,divisor:'Point2D') -> 'Point2D':
        return Point2D(self.x % divisor.x, self.y % divisor.y)

    def manhattan_distance(self,other:'Point2D') -> float:
        """Returns the manhattan distance between two points"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self,other:'Point2D') -> float:
        """Returns the actual distance between two points"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def midpoint(self,other:'Point2D') -> 'Point2D':
        """Returns the midpoint between two points"""
        return (self + other) / 2

    def copy(self) -> 'Point2D':
        """Returns a shallow copy of self"""
        return Point2D(self.x,self.y)

    def as_tuple(self) -> Tuple[float,float]:
        """Returns a tuple representing self"""
        return (self.x,self.y)

    def is_above(self,other:'Point2D') -> bool:
        """Predicate function which returns whether self is above other"""
        return self.y > other.y

    def is_below(self,other:'Point2D') -> bool:
        """Predicate function which returns whether self is below other"""
        return self.y < other.y

    def is_left_of(self,other:'Point2D') -> bool:
        """Predicate function which returns whether self is left of other"""
        return self.x < other.x

    def is_right_of(self,other:'Point2D') -> bool:
        """Predicate function which returns whether self is right of other"""
        return self.x > other.x

    @staticmethod
    def random(lower_bound:'Point2D',upper_bound:'Point2D') -> 'Point2D':
        """Returns a random point which lies in the rectangle between two bounds"""
        return Point2D(uniform(lower_bound.x,upper_bound.x),
                     uniform(lower_bound.y,upper_bound.y))

ORIGIN: Final[Point2D] = Point2D(0,0)
