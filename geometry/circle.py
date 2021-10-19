from math import pi
from typing import Optional, Tuple

from .point import Point


class Circle:
    def __init__(self,center:Point,radius:float):
        self.center = center
        self.radius = radius

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def circumference(self):
        return self.diameter * pi

    @property
    def area(self):
        return pi * self.radius ** 2

    def __contains__(self,pt:Point) -> bool:
        return self.center.euclidean_distance(pt) <= self.radius

    def intersects(self,other:'Circle') -> bool:
        d = (self.center - other.center).magnitude()
        if d == 0:
            return self.radius == other.radius
        elif d > self.radius + other.radius:
            return False
        elif d < abs(self.radius - other.radius):
            return False
        return True

    # Find intersection points on two arcs: https://stackoverflow.com/questions/47863261/find-point-of-intersection-between-two-arc
    def intersecting_points(self,other:'Circle') -> Optional[Tuple[Point,Point]]:
        other:Circle = other
        if self.center == other.center:
            raise ValueError('Intersecting circles cannot share the same center')

        if not self.intersects(other):
            return None
        d = (self.center - other.center).magnitude()
        a=(self.radius**2-other.radius**2+d**2)/(2*d)
        h=(self.radius**2-a**2)**0.5

        p2 = self.center +  (other.center-self.center) * a/d
        x3 = round(p2.x + (other.center.y-self.center.y)*h/d,8)
        y3 = round(p2.y - (other.center.x-self.center.x)*h/d,8)
        x4 = round(p2.x - (other.center.y-self.center.y)*h/d,8)
        y4 = round(p2.y + (other.center.x-self.center.x)*h/d,8)
        return Point(x3,y3),Point(x4,y4)
