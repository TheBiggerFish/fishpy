"""This module provides a class for storing and evaluating circles"""

from functools import cached_property
from math import pi
from typing import Optional, Tuple

from .point2d import Point2D
from .vector2d import Vector2D


class Circle:
    """This class stores and provides methods for evaluating circles"""

    def __init__(self, center: Point2D, radius: float):
        self.center = center
        self.radius = radius

    @cached_property
    def diameter(self):
        """This property calculates the radius of the circle"""
        return self.radius * 2

    @cached_property
    def circumference(self):
        """This property calculates the circumference of the circle"""
        return self.diameter * pi

    @cached_property
    def area(self):
        """This property calculates the area of the circle"""
        return pi * self.radius ** 2

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(center={repr(self.center)}, radius={self._radius})'

    def __contains__(self, pt: Point2D) -> bool:
        return self.center.euclidean_distance(pt) <= self.radius

    def intersects(self, other: 'Circle') -> bool:
        """Predicate function which returns whether two circles have intersections"""

        d = (self.center - other.center).magnitude()
        if d == 0:
            return self.radius == other.radius
        if d > self.radius + other.radius:
            return False
        if d < abs(self.radius - other.radius):
            return False
        return True

    # Find intersection points on two arcs:
    #  https://stackoverflow.com/questions/47863261/find-point-of-intersection-between-two-arc
    def intersecting_points(self, other: 'Circle') -> Optional[Tuple[Point2D]]:
        """Returns the intersecting point(s) of two circles"""

        other: Circle = other
        if self.center == other.center and self.radius == other.radius:
            raise ValueError('Intersecting circles of the same size '
                             'cannot share the same center')

        if not self.intersects(other):
            return None

        d = Vector2D.from_point(self.center - other.center).magnitude()
        a = (self.radius**2-other.radius**2+d**2)/(2*d)
        h = (self.radius**2-a**2)**0.5

        p2 = self.center + (other.center-self.center) * a/d
        p3, p4 = Point2D(0, 0), Point2D(0, 0)
        p3.x = round(p2.x + (other.center.y-self.center.y)*h/d, 8)
        p3.y = round(p2.y - (other.center.x-self.center.x)*h/d, 8)
        p4.x = round(p2.x - (other.center.y-self.center.y)*h/d, 8)
        p4.y = round(p2.y + (other.center.x-self.center.x)*h/d, 8)
        if p3 == p4:
            return p3,
        return p3, p4

    @property
    def radius(self):
        """This property works as a getter for radius"""
        return self._radius

    @radius.setter
    def radius(self, radius: float):
        """
        Set the radius property of the circle, invalidate caches
        which depend on radius
        """

        if radius < 0:
            raise ValueError('Circle\'s radius cannot be negative')

        # Invalidate diameter cache
        try:
            del self.diameter
        except AttributeError:
            pass

        # Invalidate circumference cache
        try:
            del self.circumference
        except AttributeError:
            pass

        # Invalidate area cache
        try:
            del self.area
        except AttributeError:
            pass

        self._radius = radius
