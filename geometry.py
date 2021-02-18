class Point:
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)

    def __eq__(self,other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * (10**10) + self.y

    def __lt__(self,other) -> bool:
        if self.y < other.y:
            return True
        return self.x < other.x

    def __str__(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def manhattan_distance(self,other) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self,other) -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


import numpy as np
class LineSegment:
    def __init__(self,p1:Point,p2:Point):
        if p1 == p2:
            raise ValueError('Points cannot have same value')
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

    def is_parallel_to(self,other) -> bool:
        delta_x = (self.get_run(),other.get_run())
        delta_y = (self.get_rise(),other.get_rise())
        return np.linalg.det(np.array((delta_x,delta_y))) == 0

    def intersection(self,other) -> Point:
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
        return Point(x,y)

class Line:
    def __init__(self,y_int:float,slope:float,vertical:bool=False,vertical_x:float=None):
        self.vertical = vertical
        self.vertical_x = vertical_x
        self.y_int = y_int
        self.slope = slope
    
    def __str__(self):
        if self.vertical:
            return 'x = {}'.format(self.vertical_x)
        return 'y = {}x + {}'.format(int(self.slope) if float(self.slope).is_integer() else self.slope, int(self.y_int) if float(self.y_int).is_integer() else self.y_int)

    @staticmethod
    def extend_segment(segment:LineSegment):
        if segment.get_run() == 0:
            return Line.new_vertical(segment.p1.x)
        slope = segment.get_rise() / segment.get_run()
        y_int = segment.p1.y - slope * segment.p1.x
        return Line(y_int,slope)

    def get_y(self,x:float) -> float:
        return self.slope * x + self.y_int
    
    def integer_points_along(self,lower_bound:Point,upper_bound:Point) -> set:
        points = set()

        if self.vertical and lower_bound.x <= self.vertical_x <= upper_bound.x:
            for y in range(lower_bound.y, upper_bound.y+1):
                points.add(Point(self.vertical_x,y))
            return points
            
        for x in range(lower_bound.x,upper_bound.x+1):
            y = self.get_y(x)
            if (self.slope < 0 and y < lower_bound.y) or (self.slope > 0 and y > upper_bound.y):
                break
            if float(y).is_integer() and lower_bound.y <= y <= upper_bound.y:
                points.add(Point(x,int(y)))
        return points

    def contains_point(self,point:Point):
        if self.vertical:
            return self.vertical_x == point.x
        return isclose(self.get_y(point.x),point.y,abs_tol=10**-6)

    @staticmethod
    def new_vertical(x:float):
        return Line(None, float('inf'), True, x)

    def perpendicular(self,intersection:Point):
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
    def y_int(self):
        return self.__y_int

    @y_int.setter
    def y_int(self,y_int):
        if self.vertical and y_int is not None:
            raise ValueError('Cannot change y-intercept of vertical line')
        self.__y_int = y_int

from math import acos,pi,isclose
class Corner:
    def __init__(self, vertex:Point, p1:Point, p2:Point):
        self.vertex = vertex
        self.p1 = p1
        self.p2 = p2

    def get_angle(self) -> float:
        leg1 = LineSegment(self.vertex,self.p1)
        leg2 = LineSegment(self.vertex,self.p2)

        a = (leg1.p1.x - leg1.p2.x, leg1.p1.y - leg1.p2.y)
        b = (leg2.p1.x - leg2.p2.x, leg2.p1.y - leg2.p2.y)

        area = leg1.get_length() * leg2.get_length()

        dot = a[0] * b[0] + a[1] * b[1]
        return round(acos(dot/area) * 180 / pi,5)
    
    def is_right(self) -> bool:
        return isclose(self.get_angle(),90,abs_tol=10**-6)


class Triangle:
    def __init__(self, p1:Point, p2:Point, p3:Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def is_right(self) -> bool:
        c1 = Corner(self.p1,self.p2,self.p3)
        c2 = Corner(self.p2,self.p3,self.p1)
        c3 = Corner(self.p3,self.p1,self.p2)
        return c1.is_right() or c2.is_right() or c3.is_right()
