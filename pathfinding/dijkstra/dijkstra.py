"""
Provides a function implementing Dijkstra's Algorithm with support of heuristics (A*)
"""


from queue import PriorityQueue
from typing import Callable, Optional, TypeVar

from .dijkstraitem import DijkstraItem

T = TypeVar('T')


def dijkstra(start: T, target: T,
             adjacency_function: Callable[[T], list[T]],
             validation_function: Optional[Callable[[T, T], bool]] = None,
             cost_function: Optional[Callable[[T, T], int]] = None,
             heuristic_function: Optional[Callable[[T, T], int]] = None,
             max_cost: Optional[int] = None) -> tuple[int, dict[T, T]]:
    """Perform the shortest path search for the target"""

    seen = set()
    prev = {}
    q = PriorityQueue()
    g_scores: dict[T, int] = {start: 0}

    q.put(DijkstraItem(start, 0, 0))

    while not q.empty():
        item: DijkstraItem = q.get()

        if item.payload in seen:
            continue
        seen.add(item.payload)

        if item.payload == target:
            return item.g, prev

        if max_cost is not None and item.g > max_cost:
            continue
        if cost_function is None:
            g = item.g + 1

        for adj in adjacency_function(item.payload):
            if validation_function is None or validation_function(item.payload, adj):
                if cost_function is not None:
                    g = item.g + cost_function(item.payload, adj)
                if g < g_scores.get(adj, float('inf')):
                    g_scores[adj] = g
                    prev[adj] = item.payload
                    h = DijkstraItem.get_h(adj, target,
                                           heuristic_function)
                    q.put(DijkstraItem(adj, g, h))
    return -1, {}
