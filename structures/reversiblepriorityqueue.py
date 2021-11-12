"""
This module provides an implementation of priority queue which can be set to
min or max. The sorting direction cannot be changed after creation.
"""

import heapq
from queue import PriorityQueue
from typing import Generic, TypeVar

from .reverse import Reverse

T = TypeVar('T')

class ReversiblePriorityQueue(PriorityQueue,Generic[T]):
    """An implementation of priority queue which can be set to min or max"""

    def __init__(self,max_:bool=False):
        super().__init__()
        self._max = max_

    def __contains__(self,item) -> bool:
        return item in self.queue

    def _put(self,item:T) -> None:
        if self.max:
            heapq.heappush(self.queue,Reverse(item))
        else:
            heapq.heappush(self.queue,item)

    def _get(self) -> T:
        if self.max:
            return heapq.heappop(self.queue).payload
        return heapq.heappop(self.queue)

    @property
    def max(self) -> bool:
        """This property represents the boolean sort-direction option"""
        return self._max
