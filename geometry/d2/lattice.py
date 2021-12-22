"""This module provides a class for storing points on an x-y lattice plane"""

from random import randint
from typing import Optional

from ..point import Point
from .point2d import Point2D
from .vector2d import DOWN, LEFT, RIGHT, UP


class LatticePoint(Point2D):
    """Class for storing points on an x-y lattice plane"""

    def __init__(self,x:int,y:int):
        if not isinstance(x,int):
            raise TypeError('x property of LatticePoint must be of type int')
        if not isinstance(y,int):
            raise TypeError('y property of LatticePoint must be of type int')
        super().__init__(x,y)

    @property
    def x(self) -> int:
        """This property represents the x-value of self"""
        return self._coords[0]

    @x.setter
    def x(self,x:int):
        if not isinstance(x,int):
            raise TypeError('x property of LatticePoint must be of type int')
        self._coords[0] = x

    @property
    def y(self) -> int:
        """This property represents the y-value of self"""
        return self._coords[1]

    @y.setter
    def y(self,y:int):
        if not isinstance(y,int):
            raise TypeError('y property of LatticePoint must be of type int')
        self._coords[1] = y

    def __add__(self,other:'LatticePoint') -> 'LatticePoint':
        return LatticePoint(self.x+other.x,self.y+other.y)

    def __sub__(self,other:'LatticePoint') -> 'LatticePoint':
        return LatticePoint(self.x-other.x,self.y-other.y)

    def __neg__(self) -> 'LatticePoint':
        return LatticePoint(-self.x,-self.y)

    def __repr__(self) -> str:
        return f'LatticePoint{str(self)}'

    def __mul__(self,scalar:int) -> 'LatticePoint':
        if not isinstance(scalar,int):
            raise TypeError('scalar must be of type int')
        return LatticePoint(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:int) -> 'LatticePoint':
        if self.x % scalar != 0 or self.y % scalar != 0:
            raise ValueError('Division scalar creates point not on lattice')
        return self // scalar

    def __floordiv__(self,scalar:int) -> 'LatticePoint':
        return LatticePoint(self.x//scalar,self.y//scalar)

    def __mod__(self,divisor:'LatticePoint') -> 'LatticePoint':
        return LatticePoint(self.x % divisor.x, self.y % divisor.y)

    def __abs__(self) -> 'LatticePoint':
        return LatticePoint(abs(self.x),abs(self.y))

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def lattice_midpoint(self,other:'LatticePoint') -> 'LatticePoint':
        """Returns the midpoint between two points"""
        return (self + other) // 2

    def get_adjacent_points(self,diagonals:bool=False,
                            lower_bound:Optional['LatticePoint']=None,
                            upper_bound:Optional['LatticePoint']=None
                            ) -> list:
        """Returns the adjacent lattice points of a given point"""

        adj = [LatticePoint(0,1),LatticePoint(0,-1),LatticePoint(1,0),LatticePoint(-1,0)]
        if diagonals:
            adj += [LatticePoint(1,1),LatticePoint(-1,-1),LatticePoint(1,-1),LatticePoint(-1,1)]
        adj = [self + p for p in adj]
        return Point.bounded_filter(adj,lower_bound,upper_bound)

    def copy(self) -> 'LatticePoint':
        """Returns a shallow copy of self"""
        return LatticePoint(self.x,self.y)

    def up(self) -> 'LatticePoint':
        """Returns the point one above self"""
        return self + UP

    def down(self) -> 'LatticePoint':
        """Returns the point one below self"""
        return self + DOWN

    def left(self) -> 'LatticePoint':
        """Returns the point one left of self"""
        return self + LEFT

    def right(self) -> 'LatticePoint':
        """Returns the point one right of self"""
        return self + RIGHT

    @staticmethod
    def random(lower_bound:'LatticePoint',upper_bound:'LatticePoint') -> 'LatticePoint':
        """
        Returns a random point which lies in the rectangle between two bounds

        lower_bound is inclusive
        upper_bound is exclusive
        """
        return LatticePoint(randint(lower_bound.x,upper_bound.x),
                            randint(lower_bound.y,upper_bound.y))
