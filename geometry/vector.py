from math import atan, cos, degrees, radians, sin
from typing import Union

from .point import Point


class Vector(Point):
    def __mul__(self,scalar:float) -> 'Vector':
        return Vector(self.x*scalar,self.y*scalar)

    def __truediv__(self,scalar:float) -> 'Vector':
        return Vector(self.x/scalar,self.y/scalar)

    def __neg__(self) -> 'Vector':
        return Vector(-self.x,-self.y)

    # def __div__(self,other):
    #     return Vector(self.x/other.x,self.y/other.y)

    def cross(self,other:'Vector') -> float:
        return (self.x*other.y) - (self.y*other.x)

    def dot(self,other:'Vector') -> float:
        return (self.x*other.x) + (self.y*other.y)

    def magnitude(self) -> Union[int,float]:
        val = (self.x**2 + self.y**2)**0.5
        return int(val) if val.is_integer() else val

    def normalize(self) -> 'Vector':
        return self / self.magnitude()

    def rotate(self,degree:float) -> 'Vector':
        return Vector.from_vel(self.angle()+degree,1)

    def __add__(self,other:'Vector') -> 'Vector':
        return Vector(self.x+other.x,self.y+other.y)

    def area(self) -> float:
        return self.x*self.y

    @staticmethod
    def from_vel(angle:float,step:float):
        return Vector(step*cos(angle),step*sin(angle))

    @staticmethod
    def from_vel_degree(degree:float,step:float) -> 'Vector':
        return Vector.from_vel(radians(degree),step)

    @staticmethod
    def from_point(point:Point) -> 'Vector':
        return Vector(point.x,point.y)

    def angle(self) -> float:
        if self.x == 0:
            if self.y == 0:
                raise ValueError('Zero vector (0,0) does not have an angle')
            return 90.0 if self.y > 0 else 270.0
        return degrees(atan(self.y/self.x)) + (180 if self.x < 0 else 360 if self.y < 0 else 0)
