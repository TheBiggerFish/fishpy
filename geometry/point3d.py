from typing import List, Optional, Union

from .point import Point


class Point3D(Point):
    def __init__(self,x:Union[int,float],y:Union[int,float],z:Union[int,float]):
        super().__init__(x,y)
        self.z = z

    def __add__(self,other:'Point3D') -> bool:
        return Point3D(self.x+other.x,self.y+other.y,self.z+other.z)

    def __sub__(self,other:'Point3D') -> bool:
        return Point3D(self.x-other.x,self.y-other.y,self.z-other.z)

    def __lt__(self,other:'Point3D') -> bool:
        return super().__lt__(other) and self.z < other.z

    def __gt__(self,other:'Point3D') -> bool:
        return super().__gt__(other) and self.z > other.z

    def __le__(self,other:'Point3D') -> bool:
        return super().__le__(other) and self.z <= other.z

    def __eq__(self,other:'Point3D') -> bool:
        return super().__eq__(other) and self.z == other.z

    def __str__(self) -> str:
        return f'({self.x},{self.y},{self.z})'

    def copy(self) -> 'Point3D':
        return Point3D(self.x,self.y,self.z)

    def get_adjacent_points(self,diagonals:bool=False,lower_bound:Optional['Point3D']=None,upper_bound:Optional['Point3D']=None) -> List['Point3D']:
        adj = [Point3D(0,1,0),Point3D(0,-1,0),Point3D(1,0,0),Point3D(-1,0,0),Point3D(0,0,1),Point3D(0,0,-1)]
        if diagonals:
            adj += [Point3D(1,1,0),Point3D(-1,-1,0),Point3D(1,-1,0),Point3D(-1,1,0),
                    Point3D(1,0,1),Point3D(-1,0,-1),Point3D(1,0,-1),Point3D(-1,0,1),
                    Point3D(0,1,1),Point3D(0,-1,-1),Point3D(0,1,-1),Point3D(0,-1,1)]
            adj += [Point3D(1,1,1),Point3D(1,1,-1),Point3D(1,-1,1),Point3D(1,-1,-1),
                    Point3D(-1,1,1),Point3D(-1,1,-1),Point3D(-1,-1,1),Point3D(-1,-1,-1)]
        adj = [self + p for p in adj]
        if lower_bound is not None:
            adj = filter(lambda x: lower_bound <= x, adj)
        if upper_bound is not None:
            adj = filter(lambda x: x < upper_bound, adj)
        return list(adj)
