"""
Provides a class implementing Dijkstra's Algorithm with support of heuristics (A*)
"""


from queue import PriorityQueue
from typing import Callable, Dict, Generic, List, Optional, TypeVar

from .dijkstraitem import DijkstraItem

T = TypeVar('T')

class Dijkstra(Generic[T]):
    """Class implementing Dijkstra's Algorithm with support for heuristics"""

    def __init__(self, start:T, target:T,
                 adjacency_function: Callable[[T],List[T]],
                 validation_function: Optional[Callable[[T],bool]] = None,
                 cost_function: Optional[Callable[[T],int]] = None,
                 heuristic_function: Optional[Callable[[T,T],int]] = None):
        self.start = start
        self.target = target
        self._adjacency_function = adjacency_function
        self._validation_function = validation_function
        self._cost_function = cost_function
        self._heuristic_function = heuristic_function
        self._dist = -1

        self.seen = set()
        self.prev = {}
        self.q = PriorityQueue()

        estimate = DijkstraItem.get_h(self.start,self.target,self._heuristic_function)
        self.q.put(DijkstraItem(self.start,0,estimate))

    def search(self, max_cost: Optional[int] = None) -> int:
        """Perform the shortest path search for the target"""

        if self.target in self.seen:
            return self._dist

        g_scores:Dict[T,int] = {self.start:0}

        while not self.q.empty():
            item:DijkstraItem = self.q.get()

            if item.payload in self.seen:
                continue
            self.seen.add(item.payload)

            if item.payload == self.target:
                self._dist = item.g
                return item.g

            if max_cost is not None and item.g > max_cost:
                continue
            if self._cost_function is None:
                g = item.g + 1

            for adj in self._adjacency_function(item.payload):
                if self._validation_function is None or self._validation_function(adj):
                    if self._cost_function is not None:
                        g = item.g + self._cost_function(item.payload,adj)
                    if g < g_scores.get(adj,float('inf')):
                        g_scores[adj] = g
                        self.prev[adj] = item.payload
                        h = DijkstraItem.get_h(adj,self.target,self._heuristic_function)
                        self.q.put(DijkstraItem(adj,g,h))
        return -1

    @property
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
