"""
Provides a class implementing Dijkstra's Algorithm with support of heuristics (A*)
"""


from functools import cached_property
from queue import PriorityQueue
from typing import Callable, Generic, List, Optional, TypeVar

from .dijkstraitem import DijkstraItem

T = TypeVar('T')

class Dijkstra(Generic[T]):
    """Class implementing Dijkstra's Algorithm with support for heuristics"""

    def __init__(self, start:T, target:T,
                 adjacency_function: Callable[[T],List[T]],
                 validation_function: Optional[Callable[[T],bool]] = None,
                 heuristic_function: Optional[Callable[[T],int]] = None,
                 verbose: bool = False):
        self.start = start
        self.target = target
        self._adjacency_function = adjacency_function
        self._validation_function = validation_function
        self._heuristic_function = heuristic_function
        self.verbose = verbose
        self._dist = -1

        self.seen = set()
        self.prev = {}
        self.q = PriorityQueue()

        estimate = DijkstraItem.get_h(self.start,self.target,self._heuristic_function)
        self.q.put(DijkstraItem(self.start,0,estimate))

    def search(self, max_depth: int = -1) -> int:
        """Perform the shortest path search for the target"""

        if self.target in self.seen:
            return self._dist
        while not self.q.empty():
            item = self.q.get()
            if item.value in self.seen:
                continue
            if self.verbose:
                print(item.value,'\n')

            self.seen.add(item.value)

            if item.value == self.target:
                self._dist = item.g
                return item.g

            g = item.g + 1
            if g > max_depth > -1:
                continue
            for adj in self._adjacency_function(item.value):
                if self._validation_function is None or self._validation_function(adj):
                    if adj not in self.seen and adj not in self.prev:
                        h = DijkstraItem.get_h(adj,self.target,self._heuristic_function)
                        self.q.put(DijkstraItem(adj,g,h))
                        self.prev[adj] = item.value
        return -1

    @cached_property
    def path(self) -> List[T]:
        """
        Return the path taken from start to the target
        Can only be called after search has been performed
        """

        path = []
        cur = self.target
        while cur in self.prev:
            path.append(cur)
            cur = self.prev[cur]
        path.append(cur)
        return list(reversed(path))

    def stringify(self, string_function:Callable[[List[T],List[T]],str]) -> str:
        """Return a string version of the search built by a passed in string_function"""

        return string_function(path=self.path, seen=self.path)
