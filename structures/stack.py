from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self,max_size:Optional[int]=None):
        self._stack = []
        if max_size is not None and max_size < 0:
            raise ValueError(f'{max_size} is an invalid number for '\
                'Stack.max_size (cannot be less than 0)')
        self.max_size = max_size

    def empty(self) -> bool:
        return self.size() == 0

    def size(self) -> int:
        return len(self._stack)    

    def full(self) -> bool:
        if self.max_size is None:
            return False
        return self.size() >= self.max_size

    def top(self) -> T:
        return self._stack[-1]

    def peek(self) -> T:
        return self.top()

    def push(self,item:T) -> None:
        if self.full():
            raise Exception(f'Cannot push to a filled Stack (stack max_size={self.max_size}')
        self._stack.append(item)

    def pop(self) -> T:
        return self._stack.pop()
