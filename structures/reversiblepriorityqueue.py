
import heapq
from queue import PriorityQueue
from typing import Generic, TypeVar

from .reverse import Reverse

T = TypeVar('T')

class ReversiblePriorityQueue(PriorityQueue,Generic[T]):
    def __init__(self,max_:bool=False):
        super().__init__()
        self.max = max_

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
        else:
            return heapq.heappop(self.queue)

    @property
    def max(self) -> bool:
        return self._max

    @max.setter
    def max(self,val:bool) -> None:
        self._max = val
