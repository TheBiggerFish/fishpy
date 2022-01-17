"""Provides a class to be used in priority queue for Dijkstra pathfinding search"""

from typing import Callable, Generic, TypeVar

T = TypeVar('T')


class DijkstraItem(Generic[T]):
    """Class to be used in priority queue for Dijkstra pathfinding search"""

    def __init__(self, payload: T, g: int, h: int = 0):
        self.payload = payload
        self.g = g
        self.h = h

    @staticmethod
    def get_h(source, target, heuristic_function: Callable[[T], int]) -> int:
        """Return the heuristic value for a given source and target"""
        if heuristic_function is not None:
            return heuristic_function(source, target)
        return 0

    def __lt__(self, other: 'DijkstraItem') -> bool:
        return (self.g+self.h, self.g, self.h) < (other.g+other.h, other.g, other.h)

    def __hash__(self) -> int:
        return hash(self.payload)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(payload={self.payload}, g={self.g}, h={self.h})'
