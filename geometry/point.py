"""This module provides a class for storing points on an x-y plane"""

from random import uniform
from typing import Final, Iterable, List, Optional, Tuple, Union

Number = Union[float,int]

class Point:
    """
    This class can be used to represent and evaluate points on an x-y plane
    """

    def __init__(self,x:Number,y:Number):
        self.x = x
        self.y = y

    def __add__(self,other:'Point') -> 'Point':
        return Point(self.x+other.x,self.y+other.y)

    def __sub__(self,other:'Point') -> 'Point':
        return Point(self.x-other.x,self.y-other.y)

    def __neg__(self) -> 'Point':
        return Point(-self.x,-self.y)

    def __eq__(self,other:'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(str(self.x * (10**10) + self.y))

    def __lt__(self,other:'Point') -> bool:
        return self.y < other.y and self.x < other.x

    def __gt__(self,other:'Point') -> bool:
        return not self < other and not self == other

    def __le__(self,other:'Point') -> bool:
        return self.y <= other.y and self.x <= other.x

    def __str__(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __repr__(self) -> str:
        return f'Point{str(self)}'

    def __mul__(self,scalar:float) -> 'Point':
        return Point(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:float) -> 'Point':
        return Point(self.x/scalar,self.y/scalar)

    def __floordiv__(self,scalar:float) -> 'Point':
        return Point(self.x//scalar,self.y//scalar)

    def __mod__(self,divisor:'Point') -> 'Point':
        return Point(self.x % divisor.x, self.y % divisor.y)

    def manhattan_distance(self,other:'Point') -> float:
        """Returns the manhattan distance between two points"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self,other:'Point') -> float:
        """Returns the actual distance between two points"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def midpoint(self,other:'Point') -> 'Point':
        """Returns the midpoint between two points"""
        return (self + other) / 2

    @staticmethod
    def bounded_filter(points:Iterable['Point'],
                       lower_bound:Optional['Point']=None,
                       upper_bound:Optional['Point']=None) -> List['Point']:
        """
        Takes an iterable of points, and returns the list of points which lie
        within a bound
        """

        if lower_bound is not None:
            points = filter(lambda x: lower_bound <= x, points)
        if upper_bound is not None:
            points = filter(lambda x: x < upper_bound, points)
        return list(points)

    def get_adjacent_points(self,diagonals:bool=False,
                            lower_bound:Optional['Point']=None,
                            upper_bound:Optional['Point']=None) -> list:
        """Returns the adjacent lattice points of a given point"""

        adj = [Point(0,1),Point(0,-1),Point(1,0),Point(-1,0)]
        if diagonals:
            adj += [Point(1,1),Point(-1,-1),Point(1,-1),Point(-1,1)]
        adj = [self + p for p in adj]
        return Point.bounded_filter(adj,lower_bound,upper_bound)

    def in_bounds(self,lower_bound:'Point',upper_bound:'Point') -> bool:
        """
        Returns whether a point lies within the rectangle between two points
        """
        return lower_bound <= self < upper_bound

    def copy(self) -> 'Point':
        """Returns a shallow copy of self"""
        return Point(self.x,self.y)

    def as_tuple(self) -> Tuple[float,float]:
        """Returns a tuple representing self"""
        return (self.x,self.y)

    def is_above(self,other:'Point') -> bool:
        """Predicate function which returns whether self is above other"""
        return self.y > other.y

    def is_below(self,other:'Point') -> bool:
        """Predicate function which returns whether self is below other"""
        return self.y < other.y

    def is_left_of(self,other:'Point') -> bool:
        """Predicate function which returns whether self is left of other"""
        return self.x < other.x

    def is_right_of(self,other:'Point') -> bool:
        """Predicate function which returns whether self is right of other"""
        return self.x > other.x

    def up(self) -> 'Point':
        """Returns the point one above self"""
        return self + Point(0,1)

    def down(self) -> 'Point':
        """Returns the point one below self"""
        return self + Point(0,-1)

    def left(self) -> 'Point':
        """Returns the point one left of self"""
        return self + Point(-1,0)

    def right(self) -> 'Point':
        """Returns the point one right of self"""
        return self + Point(1,0)

    @staticmethod
    def random(lower_bound:'Point',upper_bound:'Point') -> 'Point':
        """Returns a random point which lies in the rectangle between two bounds"""
        return Point(uniform(lower_bound.x,upper_bound.x),
                     uniform(lower_bound.y,upper_bound.y))

ORIGIN: Final[Point] = Point(0,0)
