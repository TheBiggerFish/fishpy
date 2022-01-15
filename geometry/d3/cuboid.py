"""This module provides a class for storing and evaluating cuboids"""

from functools import singledispatchmethod
from itertools import product
from typing import Optional

from .point3d import Point3D


class Cuboid:
    def __init__(self, lower: Point3D, upper: Point3D):
        self.lower = lower
        self.upper = upper

    @property
    def volume(self):
        return self.lower.volume(self.upper)

    def points(self):
        return [Point3D(*prod) for prod in product((self.lower.y, self.upper.x),
                                                   (self.lower.y, self.upper.y),
                                                   (self.lower.z, self.upper.z))]

    def overlap(self, other: 'Cuboid') -> Optional['Cuboid']:
        low_x, high_x = max(self.lower.x, other.lower.x), min(
            self.upper.x, other.upper.x)
        low_y, high_y = max(self.lower.y, other.lower.y), min(
            self.upper.y, other.upper.y)
        low_z, high_z = max(self.lower.z, other.lower.z), min(
            self.upper.z, other.upper.z)
        low, high = Point3D(low_x, low_y, low_z), Point3D(
            high_x, high_y, high_z)
        if low_x > high_x or low_y > high_y or low_z > high_z:
            return None
        return Cuboid(low, high)

    @singledispatchmethod
    def __contains__(self, arg):
        raise NotImplementedError(
            f'Cuboid.__contains__ not defined for {type(arg)}')

    def __repr__(self):
        return f'Cuboid({self.lower},{self.upper})'

    def __str__(self):
        return f'[{self.lower}..{self.upper}]'


@Cuboid.__contains__.register
def _(self: Cuboid, pt: Point3D):
    return self.lower <= pt <= self.upper


@Cuboid.__contains__.register
def _(self: Cuboid, other: 'Cuboid'):
    return self.lower <= other.lower and other.upper <= self.upper
