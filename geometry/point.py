"""
This module provides a class for storing points which lie in n-dimensional
space
"""

from functools import cached_property
from random import uniform
from typing import Iterable, List, Optional, Tuple, Union


class Point:
    """Class for storing points which lie in n-dimensional space"""

    def __init__(self, *coords: int):
        self._coords = list(coords)

    def __getitem__(self, key: Union[int, slice]) -> float:
        if isinstance(key, int):
            if key < 0:
                raise IndexError('Dimension index must be positive')
            if key >= self.dimensions:
                return 0
            return self._coords[key]

        if isinstance(key, slice):
            return self._coords[key]

        raise TypeError('Point accessor must be an integer')

    def __setitem__(self, index: int, value: float) -> None:
        if not isinstance(index, int):
            raise TypeError('Dimension index must be an integer')

        if index < 0:
            raise IndexError('Dimension index must be positive')
        if index >= self.dimensions:
            raise IndexError('Dimension index out of range')

        self._coords[index] = value

    @staticmethod
    def origin(dimensions: int) -> 'Point':
        """Returns the origin of an n-dimensional space"""
        return Point(*((0,)*dimensions))

    @cached_property
    def dimensions(self) -> int:
        """Property representing the dimensionality of self"""
        return len(self._coords)

    def __str__(self) -> str:
        return str(self.as_tuple())

    def __repr__(self) -> str:
        return f'Point{str(self)}'

    def copy(self) -> 'Point':
        """Returns a shallow copy of self"""
        return Point(*tuple(self._coords))

    def __add__(self, other: 'Point') -> 'Point':
        iterations = max(self.dimensions, other.dimensions)
        t = (self[i]+other[i] for i in range(iterations))
        return Point(*t)

    def __sub__(self, other: 'Point') -> 'Point':
        iterations = max(self.dimensions, other.dimensions)
        t = (self[i]-other[i] for i in range(iterations))
        return Point(*t)

    def __neg__(self) -> 'Point':
        t = (-self[i] for i in range(self.dimensions))
        return Point(*t)

    def __iter__(self):
        for c in self._coords:
            yield c

    def __eq__(self, other: 'Point') -> bool:
        iterations = max(self.dimensions, other.dimensions)
        for i in range(iterations):
            if self[i] != other[i]:
                return False
        return True

    def __le__(self, other: 'Point') -> bool:
        iterations = max(self.dimensions, other.dimensions)
        for i in range(iterations):
            if self[i] <= other[i]:
                return True
        return False

    def __lt__(self, other: 'Point') -> bool:
        iterations = max(self.dimensions, other.dimensions)
        for i in range(iterations):
            if self[i] < other[i]:
                return True
        return False

    def __gt__(self, other: 'Point') -> bool:
        return not self <= other

    def __ge__(self, other: 'Point') -> bool:
        return not self < other

    def __hash__(self) -> int:
        return hash(tuple(self._coords))

    def __mul__(self, scalar: float) -> 'Point':
        p = self.copy()
        for i in range(p.dimensions):
            p[i] *= scalar
        return p

    def __truediv__(self, scalar: float) -> 'Point':
        p = self.copy()
        for i in range(p.dimensions):
            p[i] /= scalar
        return p

    def __floordiv__(self, scalar: float) -> 'Point':
        p = self.copy()
        for i in range(p.dimensions):
            p[i] //= scalar
        return p

    def __mod__(self, divisor: 'Point') -> 'Point':
        p = self.copy()
        for i in range(p.dimensions):
            p[i] %= divisor
        return p

    def manhattan_distance(self, other: 'Point') -> float:
        """Returns the manhattan distance between two points"""

        distance = 0
        iterations = max(self.dimensions, other.dimensions)
        for dimension in range(iterations):
            distance += abs(self[dimension] - other[dimension])
        return distance

    def euclidean_distance(self, other: 'Point') -> float:
        """Returns the actual distance between two points"""

        distance = 0
        iterations = max(self.dimensions, other.dimensions)
        for dimension in range(iterations):
            distance += (self[dimension] - other[dimension])**2
        return distance**0.5

    def midpoint(self, other: 'Point') -> 'Point':
        """Returns the midpoint between two points"""
        return (self + other) / 2

    @staticmethod
    def bounded_filter(points: Iterable['Point'],
                       lower_bound: Optional['Point'] = None,
                       upper_bound: Optional['Point'] = None) -> List['Point']:
        """
        Takes an iterable of points, and returns the list of points which lie
        within a bound
        """

        if lower_bound is not None:
            points = filter(lambda x: lower_bound <= x, points)
        if upper_bound is not None:
            points = filter(lambda x: x < upper_bound, points)
        return list(points)

    def in_bounds(self, lower_bound: 'Point', upper_bound: 'Point') -> bool:
        """
        Returns whether a point lies within the rectangle between two points
        """
        return lower_bound <= self < upper_bound

    def clamp_bounds(self, lower_bound: 'Point', upper_bound: 'Point') -> 'Point':
        """
        Returns a point clamped within a rectangle between two points
        """
        rv = self.copy()
        for dimension in range(self.dimensions):
            if self[dimension] < lower_bound[dimension]:
                rv[dimension] = lower_bound[dimension]
            elif self[dimension] > upper_bound[dimension]:
                rv[dimension] = upper_bound[dimension]
        return rv

    def as_tuple(self) -> Tuple[float]:
        """Returns a tuple representing self"""
        return tuple(self._coords)

    @staticmethod
    def random(lower_bound: 'Point', upper_bound: 'Point') -> 'Point':
        """Returns a random point which lies in the rectangle between two bounds"""

        coords = []
        iterations = max(lower_bound.dimensions, upper_bound.dimensions)
        for i in range(iterations):
            coords.append(uniform(lower_bound[i], upper_bound[i]))
        return Point(*tuple(coords))

    def volume(self, other: 'Point') -> float:
        """Returns the volume of the cuboid created by self and other"""
        prod = 1
        for dim in self-other:
            prod *= dim
        return abs(prod)

    def _assert_dimension(self, dim: int, coord: str) -> None:
        if self.dimensions < dim:
            raise IndexError(f'{self.dimensions} dimensional points do not '
                             f'have a <{coord}> coordinate, required dim >= {dim}')

    @property
    def x(self) -> float:
        """Returns the value in the first dimension"""
        return self[0]

    @x.setter
    def x(self, value: float) -> None:
        self._assert_dimension(1, 'x')
        self._coords[0] = value

    @property
    def y(self) -> float:
        """Returns the value in the second dimension"""
        return self[1]

    @y.setter
    def y(self, value: float) -> None:
        self._assert_dimension(2, 'y')
        self._coords[1] = value

    @property
    def z(self) -> float:
        """Returns the value in the third dimension"""
        return self[2]

    @z.setter
    def z(self, value: float) -> None:
        self._assert_dimension(3, 'z')
        self._coords[2] = value

    @property
    def w(self) -> float:
        """Returns the value in the fourth dimension"""
        return self[3]

    @w.setter
    def w(self, value: float) -> None:
        self._assert_dimension(4, 'w')
        self._coords[3] = value
