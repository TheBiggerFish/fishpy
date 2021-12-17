"""Provides a class to represent 2D locations"""


from enum import Enum
from copy import copy

from ..geometry import LatticePoint


class Location(LatticePoint):
    """A class used to represent 2D locations"""

    OPEN = 0
    IMPASSABLE = 1
    def __init__(self,x:int,y:int,loc_type:Enum,rep:str=' '):
        super().__init__(x,y)
        self.type = loc_type
        self.rep = rep

    def copy(self) -> 'Location':
        return Location(self.x,self.y,self.type,copy(self.rep))

    def __str__(self) -> str:
        return str(self.rep)

    def __repr__(self) -> str:
        return f'Location(x={self.x},y={self.y},rep={self.rep},type={self.type})'

    def __eq__(self,other:'Location') -> None:
        return super().__eq__(other) and self.type == other.type and self.rep == other.rep

    def __hash__(self) -> int:
        return hash((self.x,self.y))

    def is_passible(self) -> bool:
        """Returns whether this location is passible"""
        return self.type != Location.IMPASSABLE
