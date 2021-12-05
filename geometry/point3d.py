"""This module provides a class for storing points which lie in 3-space"""

from typing import List, Optional

from .point import Point


class Point3D(Point):
    """Class for storing points which lie in 3-space"""

    def __init__(self,x:float,y:float,z:float):
        super().__init__(x,y,z)

    def __add__(self,other:'Point3D') -> bool:
        return Point3D(self.x+other.x,self.y+other.y,self.z+other.z)

    def __sub__(self,other:'Point3D') -> bool:
        return Point3D(self.x-other.x,self.y-other.y,self.z-other.z)

    def get_adjacent_points(self,diagonals:bool=False,
                            lower_bound:Optional['Point3D']=None,
                            upper_bound:Optional['Point3D']=None) -> List['Point3D']:
        """Returns the adjacent lattice points of a given point"""

        adj = [Point3D(1,0,0),Point3D(-1,0,0),
               Point3D(0,1,0),Point3D(0,-1,0),
               Point3D(0,0,1),Point3D(0,0,-1)]
        if diagonals:
            adj += [Point3D(1,1,0),Point3D(-1,-1,0),Point3D(1,-1,0),Point3D(-1,1,0),
                    Point3D(1,0,1),Point3D(-1,0,-1),Point3D(1,0,-1),Point3D(-1,0,1),
                    Point3D(0,1,1),Point3D(0,-1,-1),Point3D(0,1,-1),Point3D(0,-1,1)]
            adj += [Point3D(1,1,1),Point3D(1,1,-1),Point3D(1,-1,1),Point3D(1,-1,-1),
                    Point3D(-1,1,1),Point3D(-1,1,-1),Point3D(-1,-1,1),Point3D(-1,-1,-1)]
        adj = [self + p for p in adj]
        return Point.bounded_filter(adj,lower_bound,upper_bound)
