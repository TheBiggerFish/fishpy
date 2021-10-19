from enum import Enum

from fishpy.geometry import Point


class Location(Point):
    OPEN = 0
    IMPASSABLE = 1
    def __init__(self,x:int,y:int,loc_type:Enum,rep:str=' '):
        super().__init__(x,y)
        self.type = loc_type
        self.rep = rep

    def copy(self) -> 'Location':
        return Location(self.x,self.y,self.type,self.rep[:])

    def __str__(self) -> str:
        return self.rep

    def __eq__(self,other:'Location') -> None:
        return super().__eq__(other) and self.type == other.type and self.rep == other.rep

    def is_passible(self) -> bool:
        return self.type != Location.IMPASSABLE
