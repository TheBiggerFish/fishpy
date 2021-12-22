"""This module provides a class for storing and evaluating triangles"""

from typing import List, Tuple

from .corner import Corner
from ..point import Point


class Triangle:
    """This class stores and provides methods for evaluating triangles"""

    def __init__(self, p1:Point, p2:Point, p3:Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __contains__(self,pt:Point):
        return pt in (self.p1,self.p2,self.p3)

    def __str__(self) -> str:
        return f'{str(self.p1)},{str(self.p2)},{str(self.p3)}'

    def __hash__(self) -> int:
        p1 = min((self.p1,self.p2,self.p3))
        p3 = max((self.p1,self.p2,self.p3))
        p2 = self.p1 if p1 in (self.p2,self.p3) and p3 in (self.p2,self.p3) \
            else self.p2 if p1 in (self.p1,self.p3) and p3 in (self.p1,self.p3) \
                else self.p3
        return hash(str(p1)+str(p2)+str(p3))

    def __eq__(self,other:'Triangle') -> bool:
        return self.p1 in other and self.p2 in other and self.p3 in other

    def is_right(self) -> bool:
        """Predicate method which returns whether self is a right triangle"""
        c1 = Corner(self.p1,self.p2,self.p3)
        c2 = Corner(self.p2,self.p3,self.p1)
        c3 = Corner(self.p3,self.p1,self.p2)
        return c1.is_right() or c2.is_right() or c3.is_right()

    def as_list_of_edges(self) -> List[List[float]]:
        """Returns a list of edges representing self"""
        l1 = [self.p1.as_tuple(),self.p2.as_tuple()]
        l2 = [self.p2.as_tuple(),self.p3.as_tuple()]
        l3 = [self.p1.as_tuple(),self.p3.as_tuple()]
        return [l1,l2,l3]

    def signed_area(self) -> int:
        """Returns the signed area of self"""
        return 0.5 * (
            -self.p2.y*self.p3.x +
            self.p1.y*(-self.p2.x + self.p3.x) +
            self.p1.x*(self.p2.y - self.p3.y) +
            self.p2.x*self.p3.y
        )

    def area(self) -> int:
        """Returns the area of self"""
        return abs(self.signed_area())

    def barycentric_coordinates(self,pt:Point) -> Tuple[float,float,float]:
        """Returns the barycentric_coordinates of pt"""

        s = 1/(2*self.signed_area())*(
            self.p1.y*self.p3.x -
            self.p1.x*self.p3.y +
            (self.p3.y - self.p1.y)*pt.x +
            (self.p1.x - self.p3.x)*pt.y
        )
        t = 1/(2*self.signed_area())*(
            self.p1.x*self.p2.y -
            self.p1.y*self.p2.x +
            (self.p1.y - self.p2.y)*pt.x +
            (self.p2.x - self.p1.x)*pt.y
        )
        return s,t,1-s-t

    def contains(self,pt:Point) -> bool:
        """Predicate function which returns whether pt lies within self"""
        s,t,_ = self.barycentric_coordinates(pt)
        return s > 0 and t > 0 and 1-s-t > 0

    def as_tuple(self) -> Tuple[Tuple[float,float]]:
        """Returns a representation of self as a tuple of tuples of floats"""
        return tuple(item for pt in (self.p1,self.p2,self.p3) for item in pt.as_tuple())
