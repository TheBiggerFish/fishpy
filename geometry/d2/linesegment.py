"""This module provides a class for storing and evaluating line segments"""

from math import ceil, floor
from typing import Optional, Set

import numpy as np
from .lattice import LatticePoint

from .point2d import Point2D


class LineSegment:
    """Class for storing and evaluating line segments"""

    def __init__(self,p1:Point2D,p2:Point2D):
        if p1 == p2:
            raise ValueError('Points cannot have same value in a line segment')
        self.p1 = p1
        self.p2 = p2

    def left_point(self) -> Point2D:
        """Returns the component point which is furthest left"""
        return self.p1 if self.p1.is_left_of(self.p2) else self.p2

    def right_point(self) -> Point2D:
        """Returns the component point which is furthest left"""
        return self.p1 if self.p1.is_right_of(self.p2) else self.p2

    def high_point(self) -> Point2D:
        """Returns the component point which is furthest left"""
        return self.p1 if self.p1.is_above(self.p2) else self.p2

    def low_point(self) -> Point2D:
        """Returns the component point which is furthest left"""
        return self.p1 if self.p1.is_below(self.p2) else self.p2

    def __str__(self) -> str:
        return f'({self.p1},{self.p2})'

    def __repr__(self) -> str:
        return f'LineSegment{str(self)}'

    def get_rise(self) -> float:
        """Returns the change in y-value"""
        if self.get_run() == 0:
            return self.high_point().y - self.low_point().y
        return self.right_point().y - self.left_point().y

    def get_run(self) -> float:
        """Returns the change in x-value"""
        return self.right_point().x - self.left_point().x

    def get_length(self) -> float:
        """Returns the length of the line"""
        return (self.get_rise()**2 + self.get_run()**2)**0.5

    def is_parallel_to(self,other:'LineSegment') -> bool:
        """Predicate function which returns whether two line segments are parallel"""
        delta_x = (self.get_run(),other.get_run())
        delta_y = (self.get_rise(),other.get_rise())
        return np.linalg.det(np.array((delta_x,delta_y))) == 0

    def lattice_points_along(self) -> Set[LatticePoint]:
        """Find all lattice points lying on the line segment"""
        points = set()
        left,right = self.left_point(),self.right_point()
        low,high = self.low_point(),self.high_point()
        if self.get_run() == 0:
            if float(self.p1.x).is_integer():
                for y in range(ceil(low.y),floor(high.y)+1):
                    points.add(LatticePoint(int(self.p1.x),y))
        else:
            slope = self.get_rise() / self.get_run()
            steps = ceil(left.x) - left.x
            for x in range(ceil(left.x),floor(right.x)+1):
                y = slope * steps + left.y
                if float(y).is_integer():
                    points.add(LatticePoint(x,int(y)))
                steps += 1
        return points

    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    def intersects(self,other:'LineSegment') -> bool:
        """Predicate function which returns whether two line segments intersect"""

        def ccw(A:Point2D,B:Point2D,C:Point2D) -> bool:
            return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
        return ccw(self.p1,other.p1,other.p2) \
                    != ccw(self.p2,other.p1,other.p2) \
                and ccw(self.p1,self.p2,other.p1) \
                    != ccw(self.p1,self.p2,other.p2)

    def intersection(self,other:'LineSegment') -> Optional[Point2D]:
        """Returns the intersection point of two lines, or none if no intersection point"""

        if not self.intersects(other):
            return None

        delta_x = (self.get_run(),other.get_run())
        delta_y = (self.get_rise(),other.get_rise())
        div = np.linalg.det(np.array((delta_x,delta_y)))

        self_det = np.linalg.det(np.array(((self.p1.x,self.p1.y),(self.p2.x,self.p2.y))))
        other_det = np.linalg.det(np.array(((other.p1.x,other.p1.y),(other.p2.x,other.p2.y))))
        d = (self_det,other_det)

        x = round(-np.linalg.det(np.array((d,delta_x))) / div,10)
        y = round(-np.linalg.det(np.array((d,delta_y))) / div,10)
        x = int(x) if float(x).is_integer() else x
        y = int(y) if float(y).is_integer() else y
        return Point2D(x,y)
