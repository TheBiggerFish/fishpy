"""This module provides a class for storing and evaluating circles"""

from functools import cached_property
from math import pi
from typing import Optional, Tuple

from .point import Point


class Circle:
    """This class stores and provides methods for evaluating circles"""
    def __init__(self,center:Point,radius:float):
        self.center = center
        self._radius = radius

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

    def __contains__(self,pt:Point) -> bool:
        return self.center.euclidean_distance(pt) <= self.radius

    def intersects(self,other:'Circle') -> bool:
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
    def intersecting_points(self,other:'Circle') -> Optional[Tuple[Point,Point]]:
        """Returns the intersecting points of two circles"""

        other:Circle = other
        if self.center == other.center:
            raise ValueError('Intersecting circles cannot share the same center')

        if not self.intersects(other):
            return None

        d = (self.center - other.center).magnitude()
        a = (self.radius**2-other.radius**2+d**2)/(2*d)
        h = (self.radius**2-a**2)**0.5

        p2 = self.center + (other.center-self.center) * a/d
        x3 = round(p2.x + (other.center.y-self.center.y)*h/d,8)
        y3 = round(p2.y - (other.center.x-self.center.x)*h/d,8)
        x4 = round(p2.x - (other.center.y-self.center.y)*h/d,8)
        y4 = round(p2.y + (other.center.x-self.center.x)*h/d,8)
        return Point(x3,y3),Point(x4,y4)

    @property
    def radius(self):
        """This property works as a getter for radius"""
        return self._radius

    @radius.setter
    def radius(self,radius):
        """
        Set the radius property of the circle, invalidate caches
        which depend on radius
        """

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
