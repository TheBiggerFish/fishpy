"""This module provides a class for storing and evaluating angles/corners"""

from functools import cached_property
from math import acos, degrees, isclose

from .linesegment import LineSegment
from .point import Point


class Corner:
    """Class for storing and evaluating angles/corners"""

    def __init__(self, vertex:Point, p1:Point, p2:Point):
        self.vertex = vertex
        self.p1 = p1
        self.p2 = p2

    def get_angle(self) -> float:
        """Determine the angle of the corner"""

        leg1 = LineSegment(self.vertex,self.p1)
        leg2 = LineSegment(self.vertex,self.p2)

        a = (leg1.p1.x - leg1.p2.x, leg1.p1.y - leg1.p2.y)
        b = (leg2.p1.x - leg2.p2.x, leg2.p1.y - leg2.p2.y)

        area = leg1.get_length() * leg2.get_length()

        dot = a[0] * b[0] + a[1] * b[1]
        return round(degrees(acos(dot/area)),5)

    @cached_property
    def angle(self):
        """
        Returns the cached angle of the corner, cache must be
        invalidated if any component points are updated
        """
        return self.get_angle()

    def is_right(self) -> bool:
        """
        Predicate function which returns true if the corner is a
        right angle
        """

        leg1 = LineSegment(self.vertex,self.p1)
        leg2 = LineSegment(self.vertex,self.p2)

        a = (leg1.p1.x - leg1.p2.x, leg1.p1.y - leg1.p2.y)
        b = (leg2.p1.x - leg2.p2.x, leg2.p1.y - leg2.p2.y)

        dot = a[0] * b[0] + a[1] * b[1]
        return isclose(dot,0,abs_tol=10**-5)
