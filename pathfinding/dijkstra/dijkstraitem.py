"""Provides a class to be used in priority queue for Dijkstra pathfinding search"""

from typing import Callable, Generic, TypeVar

T = TypeVar('T')

class DijkstraItem(Generic[T]):
    """Class to be used in priority queue for Dijkstra pathfinding search"""

    def __init__(self, value:T, g:int, h: int = 0):
        self.value = value
        self.g = g
        self.h = h

    @staticmethod
    def get_h(source, target, heuristic_function:Callable[[T],int]) -> int:
        """Return the heuristic value for a given source and target"""
        if heuristic_function is not None:
            return heuristic_function(source,target)
        return 0

    def __lt__(self,other:'DijkstraItem') -> bool:
        return (self.g+self.h,self.h,self.g) < (other.g+other.h,other.h,other.g)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return f'DijkstraItem: value=\'{str(self.value)}\', g={self.g}, h={self.h}'
