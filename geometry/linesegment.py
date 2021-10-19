import numpy as np

from .point import Point


class LineSegment:
    def __init__(self,p1:Point,p2:Point):
        if p1 == p2:
            raise ValueError('Points cannot have same value in a line segment')
        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        return '({},{})'.format(self.p1,self.p2)

    def get_rise(self) -> float:
        left = self.p1 if self.p1.x < self.p2.x else self.p2
        right = self.p2 if self.p1.x < self.p2.x else self.p1
        return right.y - left.y

    def get_run(self) -> float:
        left = self.p1 if self.p1.x < self.p2.x else self.p2
        right = self.p2 if self.p1.x < self.p2.x else self.p1
        return right.x - left.x

    def get_length(self) -> float:
        return (self.get_rise()**2 + self.get_run()**2)**0.5

    def is_parallel_to(self,other:'LineSegment') -> bool:
        delta_x = (self.get_run(),other.get_run())
        delta_y = (self.get_rise(),other.get_rise())
        return np.linalg.det(np.array((delta_x,delta_y))) == 0

    def intersects(self,other:'LineSegment') -> bool:
        # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
        def ccw(A:Point,B:Point,C:Point) -> bool:
            return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
        return ccw(self.p1,other.p1,other.p2) \
                    != ccw(self.p2,other.p1,other.p2) \
                and ccw(self.p1,self.p2,other.p1) \
                    != ccw(self.p1,self.p2,other.p2)

    def intersection(self,other:'LineSegment') -> Point:
        if self.is_parallel_to(other):
            return None

        delta_x = (self.get_run(),other.get_run())
        delta_y = (self.get_rise(),other.get_rise())
        div = np.linalg.det(np.array((delta_x,delta_y)))

        self_det = np.linalg.det(np.array(((self.p1.x,self.p1.y),(self.p2.x,self.p2.y))))
        other_det = np.linalg.det(np.array(((other.p1.x,other.p1.y),(other.p2.x,other.p2.y))))
        d = (self_det,other_det)

        x = round(-np.linalg.det(np.array((d,delta_x))) / div,10)
        y = round(-np.linalg.det(np.array((d,delta_y))) / div,10)
        x = int(x) if x.is_integer() else x
        y = int(y) if y.is_integer() else y
        return Point(x,y)
