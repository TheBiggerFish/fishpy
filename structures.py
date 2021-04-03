from multiprocessing import Value
from typing import Any
from queue import PriorityQueue
import heapq

class Reverse:
    def __init__(self,payload):
        self.payload = payload

    def __lt__(self,other):
        return self.payload > other.payload
        
    def __gt__(self,other):
        return self.payload < other.payload

    def __eq__(self,other):
        return self.payload == other.payload

    def __str__(self):
        return str(self.payload)

    def __hash__(self):
        return hash(self.payload)

class ReversiblePriorityQueue(PriorityQueue):
    def __init__(self,max=False):
        super().__init__()
        self.max = max

    def __contains__(self,item):
        return item in self.queue

    def _put(self,item):
        if self.max:
            heapq.heappush(self.queue,Reverse(item))
        else:
            heapq.heappush(self.queue,item)
        
    def _get(self):
        if self.max:
            return heapq.heappop(self.queue).payload
        else:
            return heapq.heappop(self.queue)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self,val):
        self._max = val

class Range:
    def __init__(self,lower,upper,lower_inclusive:bool=True,upper_inclusive:bool=False):
        self.lower = lower
        self.lower_inclusive = lower_inclusive

        self.upper = upper
        self.upper_inclusive = upper_inclusive

    def size(self):
        offset = (1 if self.lower_inclusive else 0) + (1 if self.upper_inclusive else 0) - 1
        return self.upper - self.lower + offset

    def __len__(self):
        return self.size()

    def __lt__(self,other):
        return self.lower < other.lower
    
    def __gt__(self,other):
        return self.lower > other.lower
    
    def __str__(self):
        return f'Lower={self.lower},Upper={self.upper}'

    def __contains__(self,item):
        if self.lower_inclusive:
            if self.upper_inclusive:
                return self.lower <= item <= self.upper
            else:
                return self.lower <= item < self.upper
        else:
            if self.upper_inclusive:
                return self.lower < item <= self.upper
            else:
                return self.lower < item < self.upper

    def division(self,parts,which):
        # if self.size() % parts:
        #     raise ValueError(f'Range should be evenly divided, {self.size()} % {parts} != 0')
        if which >= parts:
            raise IndexError('Cannot select a chunk out of range')
        step = (self.upper-self.lower) / parts
        if float(step).is_integer():
            step = int(step)
        lower = self.lower + (step * which)
        upper = lower + step
        return Range(lower,upper)

    def __iter__(self):
        if not isinstance(self.lower,int):
            raise TypeError(f'\'{type(self.lower)}\' cannot be interpreted as an integer')
        if not isinstance(self.upper,int):
            raise TypeError(f'\'{type(self.upper)}\' cannot be interpreted as an integer')
        lower = self.lower if self.lower_inclusive else self.lower+1
        upper = self.upper+1 if self.upper_inclusive else self.upper
        for i in range(lower,upper):
            yield i

class Stack:
    def __init__(self,max_size=None):
        self._stack = []
        if max_size < 0:
            raise ValueError(f'{max_size} is an invalid number for Stack.max_size (cannot be less than 0)')
        self.max_size = max_size

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self._stack)    
    
    def full(self):
        if self.max_size is None:
            return False
        return self.size() >= self.max_size

    def top(self):
        return self._stack[-1]

    def peek(self):
        return self.top()

    def push(self,item):
        if self.full():
            raise Exception(f'Cannot push to a filled Stack (stack max_size={self.max_size}')
        self._stack.append(item)

    def pop(self):
        return self._stack.pop()

class Node:
    def __init__(self,value,name:str='',children:list=[],parent=None):
        self.value = value
        self.name = name
        self.children = children
        self.parent = parent

    def adjacent(self):
        if self.parent is not None:
            return [self.parent] + self.children
        return self.children
    
    def root(self):
        cur = self
        while cur.parent is not None:
            cur = cur.parent
        return cur

class Cycle(list):
    def __getitem__(self,key:int):
        return super().__getitem__(key%len(self))

    def __setitem__(self,key:int,value:Any):
        super().__setitem__(key%len(self),value)