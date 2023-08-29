"""This module provides a class for storing and evaluating lines"""

from math import isclose
from typing import Optional, Set

from .lattice import LatticePoint
from .linesegment import LineSegment
from .point2d import Point2D


class Line:
    """Class for storing and evaluating lines"""

    def __init__(self, y_int: Optional[float], slope: float,
                 vertical: bool = False, x_int: Optional[float] = None):
        self.vertical = vertical
        self.x_int = x_int
        self.y_int = y_int
        self.slope = slope

    def __str__(self) -> str:
        if self.vertical:
            return f'x = {self.x_int}'
        slope = int(self.slope) if float(
            self.slope).is_integer() else self.slope
        y_int = int(self.y_int) if float(
            self.y_int).is_integer() else self.y_int

        slope_str = f'{slope}x' if slope != 0 else ''
        y_str = str(y_int) if y_int != 0 or slope == 0 else ''
        add_str = ' + ' if slope_str and y_str else ''
        return f'y = {slope_str}{add_str}{y_str}'

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(slope={self.slope}, y-intercept={self.y_int},'
                f'x-intercept={self.x_int}, is_vertical={self.vertical})')

    @staticmethod
    def extend_segment(segment: LineSegment) -> 'Line':
        """Returns a line by extending an existing line segment"""

        if segment.get_run() == 0:
            return Line.new_vertical(segment.p1.x)
        slope = segment.get_rise() / segment.get_run()
        y_int = segment.p1.y - slope * segment.p1.x
        return Line(y_int, slope)

    def get_y(self, x: float) -> float:
        """Returns the y-value of self at x-value"""
        return self.slope * x + self.y_int

    def lattice_points_along(self, lower_bound: Point2D, upper_bound: Point2D) -> Set[LatticePoint]:
        """
        Find all lattice points lying within the rectangle created by
        lower_bound and upper_bound
        """

        points = set()
        if self.vertical and lower_bound.x <= self.x_int <= upper_bound.x:
            for y in range(lower_bound.y, upper_bound.y+1):
                points.add(LatticePoint(self.x_int, y))
            return points

        for x in range(lower_bound.x, upper_bound.x+1):
            y = self.get_y(x)
            if (self.slope < 0 and y < lower_bound.y) or (self.slope > 0 and y > upper_bound.y):
                break
            if isclose(y - round(y), 0, abs_tol=10**-4) and lower_bound.y <= y <= upper_bound.y:
                points.add(LatticePoint(x, int(y)))
        return points

    def contains_point(self, point: Point2D) -> bool:
        """Predicate function which returns whether point lies on self"""
        if self.vertical:
            return self.x_int == point.x
        return isclose(self.get_y(point.x), point.y, abs_tol=10**-6)

    @staticmethod
    def new_vertical(x: float) -> 'Line':
        """Create a new vertical line at x"""
        return Line(None, float('inf'), True, x)

    def perpendicular(self, intersection: Point2D) -> 'Line':
        """Returns a line which is perpendicular to self at a given point"""

        if not self.contains_point(intersection):
            raise ValueError('Intersection point must lie on line')

        if self.slope == 0:
            return Line.new_vertical(intersection.x)
        if self.vertical:
            return Line(intersection.y, 0)

        new_slope = -1/self.slope
        new_y_int = intersection.y - new_slope * intersection.x
        return Line(new_y_int, new_slope)

    def reflect_point(self, p: Point2D) -> Point2D:
        """Reflect p across self"""

        if self.vertical:
            return Point2D(2*self.x_int-p.x, p.y)
        u = ((1-self.slope**2)*p.x + 2*self.slope*p.y -
             2*self.slope*self.y_int)/((self.slope**2)+1)
        v = ((self.slope**2 - 1)*p.y + 2*self.slope *
             p.x + 2*self.y_int)/((self.slope**2) + 1)
        return Point2D(u, v)

    def intersection(self, other: 'Line') -> Point2D:
        """Returns the intersection point of 2 lines"""
        a1, b1, c1 = self.slope, -1, -self.y_int
        a2, b2, c2 = other.slope, -1, -other.y_int
        det = a1*b2 - a2*b1
        if det == 0:
            raise ValueError('Cannot find intersection of parallel lines')
        x = (c1*b2 - c2*b1)/det
        y = (a1*c2 - a2*c1)/det
        return Point2D(x, y)

    @property
    def y_int(self) -> float:
        """Property representing the y-intercept of self"""
        return self.__y_int

    @y_int.setter
    def y_int(self, y_int: Optional[float]):
        if self.vertical and y_int is not None:
            raise ValueError('Cannot change y-intercept of vertical line')
        self.__y_int = y_int
