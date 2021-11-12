"""This module provides a class for storing and evaluating ellipses"""

from functools import cached_property
from math import cos, radians, sin
from typing import List

from .circle import Circle
from .corner import Corner
from .linesegment import LineSegment
from .point import Point


class Ellipse:
    """This class stores and provides methods for evaluating ellipses"""

    def __init__(self,focus1:Point,focus2:Point,point_on_ellipse:Point):
        self.focus1 = focus1
        self.focus2 = focus2
        a = focus1.euclidean_distance(point_on_ellipse)
        b = focus2.euclidean_distance(point_on_ellipse)
        f = (focus2 - focus1).to_vector().magnitude()
        self.minor_axis = ((a+b)**2 - f**2)**0.5
        self.major_axis = a+b

        c = (focus1,focus2) if focus1.x < focus2.x else (focus2,focus1)
        self.angle = Corner(c[0],c[1],c[0]+Point(1,0)).get_angle()

    @cached_property
    def center(self) -> Point:
        """
        Find the center of the ellipse, cache must be invalidated if
        one of the focus points is updated
        """
        return self.focus1.midpoint(self.focus2)

    def __contains__(self,pt:Point) -> bool:
        c = self.center()
        angle = radians(self.angle)
        t1 = (cos(angle)*(pt.x-c.x) + sin(angle)*(pt.y-c.y))**2 / (self.major_axis/2)**2
        t2 = (sin(angle)*(pt.x-c.x) - cos(angle)*(pt.y-c.y))**2 / (self.minor_axis/2)**2
        return t1 + t2 <= 1

    # Construction of tangent lines from a point outside of an ellipse:
    #  http://www.nabla.hr/Z_MemoHU-029.htm
    def tangent_lines(self,pt:Point) -> List[LineSegment]:
        """Find the tangent lines from a point lying outside of the ellipse"""

        if pt in self:
            raise ValueError('Point within ellipse cannot create tangent lines')

        # Set f1 as farther focus, f2 as nearer focus
        f1_d = pt.euclidean_distance(self.focus1)
        f2_d = pt.euclidean_distance(self.focus2)
        if f1_d > f2_d:
            F1 = self.focus1
            F2 = self.focus2
        elif f1_d < f2_d:
            F1 = self.focus2
            F2 = self.focus1
        else:
            raise NotImplementedError('Point cannot lie on minor axis')

        dist_f2 = pt.euclidean_distance(F2)
        C1 = Circle(pt,dist_f2)
        C2 = Circle(F1,self.major_axis)
        int_pts = C1.intersecting_points(C2)
        if not int_pts:
            return None
        M1 = F2.midpoint(int_pts[0])
        M2 = F2.midpoint(int_pts[1])
        return [LineSegment(pt,M1),LineSegment(pt,M2)]
