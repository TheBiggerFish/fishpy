from typing import Tuple, List
from random import randint
from math import cos,sin,pi,atan

class Point:
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
        
    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)

    def __neg__(self):
        return Point(-self.x,-self.y)

    def __eq__(self,other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(str(self.x * (10**10) + self.y))

    def __lt__(self,other) -> bool:
        return self.y < other.y and self.x < other.x

    def __gt__(self,other) -> bool:
        return not self < other and not self == other

    def __le__(self,other) -> bool:
        return self.y <= other.y and self.x <= other.x

    def __str__(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __mul__(self,scalar:float):
        return Point(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:float):
        return Point(self.x/scalar,self.y/scalar)

    def __floordiv__(self,scalar:float):
        return Point(self.x//scalar,self.y//scalar)

    def __mod__(self,divisor):
        return Point(self.x % divisor.x, self.y % divisor.y)

    def manhattan_distance(self,other) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self,other) -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def midpoint(self,other):
        return (self + other) / 2

    def get_adjacent_points(self,diagonals=False,lower_bound=None,upper_bound=None) -> list:
        adj = [Point(0,1),Point(0,-1),Point(1,0),Point(-1,0)]
        if diagonals:
            adj += [Point(1,1),Point(-1,-1),Point(1,-1),Point(-1,1)]
        adj = [self + p for p in adj]    
        if lower_bound is not None:
            adj = filter(lambda x: lower_bound <= x, adj)
        if upper_bound is not None:
            adj = filter(lambda x: x < upper_bound, adj)
        return list(adj)

    def in_bounds(self,lower_bound,upper_bound):
        return lower_bound <= self < upper_bound
    
    def copy(self):
        return Point(self.x,self.y)

    def as_tuple(self):
        return (self.x,self.y)

    def is_above(self,other):
        return self.y > other.y
    
    def is_below(self,other):
        return self.y < other.y

    def is_left_of(self,other):
        return self.x < other.x

    def is_right_of(self,other):
        return self.x > other.x
    
    def up(self):
        return self + Point(0,1)
    
    def down(self):
        return self + Point(0,-1)
    
    def left(self):
        return self + Point(-1,0)
    
    def right(self):
        return self + Point(1,0)

    @staticmethod
    def random(lower_bound,upper_bound):
        return Point(randint(lower_bound.x,upper_bound.x),randint(lower_bound.y,upper_bound.y))

    def to_vector(self):
        return Vector(self.x,self.y)


ORIGIN = Point(0,0)



class Vector(Point):
    def __mul__(self,scalar:float):
        return Vector(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:float):
        return Vector(self.x/scalar,self.y/scalar)

    def __neg__(self):
        return Vector(-self.x,-self.y)

    # def __mul__(self,other):
    #     return Vector(self.x*other.x,self.y*other.y)

    # def __div__(self,other):
    #     return Vector(self.x/other.x,self.y/other.y)

    def cross(self,other):
        return (self.x*other.y) - (self.y*other.x)

    def dot(self,other):
        return (self.x*other.x) + (self.y*other.y)
    
    def magnitude(self):
        val = (self.x**2 + self.y**2)**0.5
        return int(val) if val.is_integer() else val

    def normalize(self):
        return self / self.magnitude()

    def rotate(self,degree):
        return Vector.from_vel(self.angle()+degree,1)

    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)

    def area(self):
        return self.x*self.y

    @staticmethod
    def from_vel(angle,step):
        return Vector(step*cos(angle),step*sin(angle))

    @staticmethod
    def from_vel_degree(degree,step):
        rad = degree / 180 * pi
        return Vector.from_vel(rad,step)

    def angle(self) -> float:
        if self.x == 0:
            if self.y == 0:
                raise ValueError('Zero vector (0,0) does not have an angle')
            return 90.0 if self.y > 0 else 270.0
        return (atan(self.y/self.x)) / pi * 180 + (180 if self.x < 0 else 360 if self.y < 0 else 0)


import numpy as np
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

    def is_parallel_to(self,other) -> bool:
        delta_x = (self.get_run(),other.get_run())
        delta_y = (self.get_rise(),other.get_rise())
        return np.linalg.det(np.array((delta_x,delta_y))) == 0
    
    def intersects(self,other) -> bool:
        # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
        ccw = lambda A,B,C: (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
        return ccw(self.p1,other.p1,other.p2) != ccw(self.p2,other.p1,other.p2) and ccw(self.p1,self.p2,other.p1) != ccw(self.p1,self.p2,other.p2)

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
        x = int(x) if x.is_integer() else x
        y = int(y) if y.is_integer() else y
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
            if isclose(y - round(y),0,abs_tol=10**-4) and lower_bound.y <= y <= upper_bound.y:
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
        leg1 = LineSegment(self.vertex,self.p1)
        leg2 = LineSegment(self.vertex,self.p2)

        a = (leg1.p1.x - leg1.p2.x, leg1.p1.y - leg1.p2.y)
        b = (leg2.p1.x - leg2.p2.x, leg2.p1.y - leg2.p2.y)

        dot = a[0] * b[0] + a[1] * b[1]
        return isclose(dot,0,abs_tol=10**-5)


class Triangle:
    def __init__(self, p1:Point, p2:Point, p3:Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __contains__(self,pt):
        return pt == self.p1 or pt == self.p2 or pt == self.p3

    def __str__(self):
        return (f'{str(self.p1)},{str(self.p2)},{str(self.p3)}')

    def __hash__(self):
        p1 = min((self.p1,self.p2,self.p3))
        p3 = max((self.p1,self.p2,self.p3))
        p2 = self.p1 if p1 in (self.p2,self.p3) and p3 in (self.p2,self.p3) else self.p2 if p1 in (self.p1,self.p3) and p3 in (self.p1,self.p3) else self.p3
        return hash(str(p1)+str(p2)+str(p3))

    def __eq__(self,other):
        return self.p1 in other and self.p2 in other and self.p3 in other
    
    def is_right(self) -> bool:
        c1 = Corner(self.p1,self.p2,self.p3)
        c2 = Corner(self.p2,self.p3,self.p1)
        c3 = Corner(self.p3,self.p1,self.p2)
        return c1.is_right() or c2.is_right() or c3.is_right()

    def as_list_of_edges(self) -> list:
        return [list(self.p1.as_tuple()),list(self.p2.as_tuple()),list(self.p3.as_tuple())]
        # l1 = [self.p1.as_tuple(),self.p2.as_tuple()]
        # l2 = [self.p2.as_tuple(),self.p3.as_tuple()]
        # l3 = [self.p1.as_tuple(),self.p3.as_tuple()]
        # return [l1,l2,l3]

    def signed_area(self) -> int :
        return 0.5 *(-self.p2.y*self.p3.x + self.p1.y*(-self.p2.x + self.p3.x) + self.p1.x*(self.p2.y - self.p3.y) + self.p2.x*self.p3.y)
    
    def area(self) -> int:
        return abs(self.signed_area())
    
    def barycentric_coordinates(self,pt:Point) -> Tuple[float,float,float]:
        s = 1/(2*self.signed_area())*(self.p1.y*self.p3.x - self.p1.x*self.p3.y + (self.p3.y - self.p1.y)*pt.x + (self.p1.x - self.p3.x)*pt.y)
        t = 1/(2*self.signed_area())*(self.p1.x*self.p2.y - self.p1.y*self.p2.x + (self.p1.y - self.p2.y)*pt.x + (self.p2.x - self.p1.x)*pt.y)
        return s,t,1-s-t
    
    def __contains__(self,pt:Point) -> bool:
        s,t,_ = self.barycentric_coordinates(pt)
        return s > 0 and t > 0 and 1-s-t > 0
    
    def as_tuple(self):
        return tuple(item for pt in (self.p1,self.p2,self.p3) for item in pt.as_tuple())


import math
class Circle:
    PI = math.pi
    def __init__(self,center:Point,radius:float):
        self.center = center
        self.radius = radius
    
    @property
    def diameter(self):
        return self.radius * 2

    @property
    def circumference(self):
        return self.diameter * Circle.PI

    @property
    def area(self):
        return Circle.PI * self.radius ** 2

    def __contains__(self,pt:Point) -> bool:
        return self.center.euclidean_distance(pt) <= self.radius

    def intersects(self,other) -> bool:
        d = (self.center - other.center).magnitude()
        if d == 0:
            return self.radius == other.radius
        elif d > self.radius + other.radius:
            return False
        elif d < abs(self.radius - other.radius):
            return False
        return True
        
    # Find intersection points on two arcs: https://stackoverflow.com/questions/47863261/find-point-of-intersection-between-two-arc
    def intersecting_points(self,other) -> List[Point]:
        other:Circle = other
        if self.center == other.center:
            raise ValueError('Intersecting circles cannot share the same center')

        if not self.intersects(other):
            return []
        d = (self.center - other.center).magnitude()
        a=(self.radius**2-other.radius**2+d**2)/(2*d)
        h=math.sqrt(self.radius**2-a**2)

        p2 = self.center +  (other.center-self.center) * a/d
        x3 = round(p2.x + (other.center.y-self.center.y)*h/d,8)
        y3 = round(p2.y - (other.center.x-self.center.x)*h/d,8)
        x4 = round(p2.x - (other.center.y-self.center.y)*h/d,8)
        y4 = round(p2.y + (other.center.x-self.center.x)*h/d,8)
        return [Point(x3,y3),Point(x4,y4)]

class Ellipse:
    def __init__(self,focus1:Point,focus2:Point,point_on_ellipse:Point):
        self.focus1 = focus1
        self.focus2 = focus2
        a = focus1.euclidean_distance(point_on_ellipse)
        b = focus2.euclidean_distance(point_on_ellipse)
        f = (focus2 - focus1).magnitude()
        self.minor_axis = ((a+b)**2 - f**2)**0.5
        self.major_axis = a+b
        
        c = (focus1,focus2) if focus1.x < focus2.x else (focus2,focus1)
        self.angle = Corner(c[0],c[1],c[0]+Point(1,0)).get_angle()

    def center(self) -> Point:
        return self.focus1.midpoint(self.focus2)

    def __contains__(self,pt:Point) -> bool:
        c = self.center()
        angle = self.angle * pi / 180
        t1 = (cos(angle)*(pt.x-c.x) + sin(angle)*(pt.y-c.y))**2 / (self.major_axis/2)**2
        t2 = (sin(angle)*(pt.x-c.x) - cos(angle)*(pt.y-c.y))**2 / (self.minor_axis/2)**2
        return t1 + t2 <= 1

    # Construction of tangent lines from a point outside of an ellipse: http://www.nabla.hr/Z_MemoHU-029.htm
    def tangent_lines(self,pt:Point) -> List[LineSegment]:
        if pt in self:
            raise ValueError('Point within ellipse cannot create tangent lines')
        # Set f1 as farther focus, f2 as nearer focus
        if (f1_d := pt.euclidean_distance(self.focus1)) > (f2_d := pt.euclidean_distance(self.focus2)):
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
