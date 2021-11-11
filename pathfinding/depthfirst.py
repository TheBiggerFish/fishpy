"""Provides a class implementing a depth first search"""

from typing import Callable, Generic, List, Optional, TypeVar, Union

from ..structures import Stack

T = TypeVar('T')

class DepthFirstTraversal(Generic[T]):
    """A class implementing a depth first search"""

    def __init__(self, start:T, target:T,
                 adjacency_function: Callable[[T],List[T]],
                 distance_function: Optional[Callable[[T,T],Union[int,float]]] = None,
                 validation_function: Optional[Callable[[T],bool]]  =None,
                 cyclic: bool = False,
                 longest_path: bool = False,
                 verbose: bool = False):
        if cyclic and longest_path:
            raise ValueError('DepthFirstTraversal cannot be both cyclic and longest_path')
        self.start = start
        self.target = target
        self._adjacency_function = adjacency_function
        self._distance_function = distance_function
        self._validation_function = validation_function
        self.longest_path = longest_path
        self.cyclic = cyclic
        self.verbose = verbose

        self.distance = {self.start:0}
        self.prev = {self.start:None}
        self.stack = Stack()
        self.stack.push(self.start)

    def execute(self):
        """Execute the depth first search and return the length of shortest path to target"""

        while not self.stack.empty():
            cur = self.stack.pop()
            neighbors = self._adjacency_function(cur)
            for adj in neighbors:
                if self._validation_function is not None and not self._validation_function(adj):
                    continue
                if not self.cyclic and adj in self.prev:
                    continue
                d = 1
                if self._distance_function is not None:
                    self._distance_function(cur,adj)
                new_distance = self.distance[cur] + d
                if (adj not in self.distance
                    or (self.longest_path and self.distance[adj] < new_distance)
                    or (not self.longest_path and self.distance[adj] > new_distance)):

                    self.distance[adj] = new_distance
                    self.prev[adj] = cur
                    if not(self.longest_path and adj == self.target):
                        self.stack.push(adj)
        return self.distance[self.target]
