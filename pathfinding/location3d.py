from enum import Enum

from ..geometry import Point3D


class Location3D(Point3D):
    OPEN = 0
    IMPASSABLE = 1
    def __init__(self,x:int,y:int,z:int,type_:Enum,rep:str=' '):
        super().__init__(x,y,z)
        self.type = type_
        self.rep = rep

    def copy(self) -> 'Location3D':
        return Location3D(self.x,self.y,self.z,self.type,self.rep[:])

    def __str__(self) -> str:
        return self.rep

    def __eq__(self,other:'Location3D') -> bool:
        return super().__eq__(other) and self.type == other.type and self.rep == other.rep
