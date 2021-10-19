from math import isclose
from typing import Optional, Set

from .linesegment import LineSegment
from .point import Point


class Line:
    def __init__(self,y_int:float,slope:float,vertical:bool=False,x_int:Optional[float]=None):
        self.vertical = vertical
        self.x_int = x_int
        self.y_int = y_int
        self.slope = slope

    def __str__(self) -> str:
        if self.vertical:
            return 'x = {}'.format(self.x_int)
        slope = int(self.slope) if float(self.slope).is_integer() else self.slope
        y_int = int(self.y_int) if float(self.y_int).is_integer() else self.y_int
        return 'y = {}x + {}'.format(slope,y_int)

    @staticmethod
    def extend_segment(segment:LineSegment) -> 'Line':
        if segment.get_run() == 0:
            return Line.new_vertical(segment.p1.x)
        slope = segment.get_rise() / segment.get_run()
        y_int = segment.p1.y - slope * segment.p1.x
        return Line(y_int,slope)

    def get_y(self,x:float) -> float:
        return self.slope * x + self.y_int

    def integer_points_along(self,lower_bound:Point,upper_bound:Point) -> Set[Point]:
        points = set()

        if self.vertical and lower_bound.x <= self.x_int <= upper_bound.x:
            for y in range(lower_bound.y, upper_bound.y+1):
                points.add(Point(self.x_int,y))
            return points

        for x in range(lower_bound.x,upper_bound.x+1):
            y = self.get_y(x)
            if (self.slope < 0 and y < lower_bound.y) or (self.slope > 0 and y > upper_bound.y):
                break
            if isclose(y - round(y),0,abs_tol=10**-4) and lower_bound.y <= y <= upper_bound.y:
                points.add(Point(x,int(y)))
        return points

    def contains_point(self,point:Point) -> bool:
        if self.vertical:
            return self.x_int == point.x
        return isclose(self.get_y(point.x),point.y,abs_tol=10**-6)

    @staticmethod
    def new_vertical(x:float) -> 'Line':
        return Line(None, float('inf'), True, x)

    def perpendicular(self,intersection:Point) -> 'Line':
        if not self.contains_point(intersection):
            raise ValueError('Intersection point must lie on line')

        if self.slope == 0:
            return Line.new_vertical(intersection.x)
        elif self.vertical:
            return Line(intersection.y,0)

        new_slope = -1/self.slope
        new_y_int = intersection.y - new_slope * intersection.x
        return Line(new_y_int,new_slope)

    @property
    def y_int(self) -> float:
        return self.__y_int

    @y_int.setter
    def y_int(self,y_int:float):
        if self.vertical and y_int is not None:
            raise ValueError('Cannot change y-intercept of vertical line')
        self.__y_int = y_int
