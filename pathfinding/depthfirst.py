"""Provides a class implementing a depth first search"""

from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union

from ..structures import Stack

T = TypeVar('T')

def path(start:T,end:T,previous:Dict[T,T]):
    path = []
    cur = end
    while cur != start:
        path.append(cur)
        cur = previous[cur]
    path.append(cur)
    return list(reversed(path))

def shortest_path(start:T,target:T,
                  adjacency_function: Callable[[T],List[T]],
                  distance_function: Optional[Callable[[T,T],Union[int,float]]] = None,
                  validation_function: Optional[Callable[[T],bool]] = None
                 ) -> Tuple[int,List[T]]:
    """Execute a depth first search and return the length of shortest path to target"""

    distance = {start:0}
    prev = {}

    stack = Stack()
    stack.push(start)

    while not stack.empty():
        cur = stack.pop()
        if cur == target:
            return distance[target],path(start,target,prev)

        neighbors = adjacency_function(cur)
        for adj in neighbors:
            if validation_function is not None and not validation_function(adj):
                continue

            if distance_function is not None:
                d = distance_function(cur,adj)
            elif adj in prev:
                continue
            else:
                d = 1

            new_distance = distance[cur] + d
            if (adj not in distance
                or (new_distance < distance[adj])):
                distance[adj] = new_distance
                prev[adj] = cur
                stack.push(adj)
    return None, None

def longest_path(start:T,target:T,
                  adjacency_function: Callable[[T],List[T]],
                  distance_function: Optional[Callable[[T,T],Union[int,float]]] = None,
                  validation_function: Optional[Callable[[T],bool]] = None
                ) -> Tuple[int,List[T]]:
    """Execute a depth first search and return the length of longest path to target"""

    raise NotImplementedError('Longest path has not been implemented')
