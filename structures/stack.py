"""This module provides an implementation of stack with optional maximum size."""

from typing import Optional


class Stack:
    """An implementation of stack with optional maximum size"""

    def __init__(self, max_size: Optional[int] = None, initial: Optional[list] = None):
        self._stack = [] if initial is None else initial
        if max_size is not None and max_size < 0:
            raise ValueError(f'{max_size} is an invalid number for '
                             'Stack.max_size (cannot be less than 0)')
        self.max_size = max_size

    def __iter__(self):
        return iter(self._stack)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._stack!r})'

    def empty(self) -> bool:
        """Predicate method which returns true if the stack is empty"""
        return self.size() == 0

    def size(self) -> int:
        """Returns the number of items in the stack"""
        return len(self._stack)

    def full(self) -> bool:
        """
        Returns whether the stack is full. If no maximum size is set, always
        returns false
        """

        if self.max_size is None:
            return False
        return self.size() >= self.max_size

    def top(self):
        """Return the top value of the stack"""
        return self._stack[-1]

    def peek(self):
        """Return the top value of the stack"""
        return self.top()

    def push(self, item) -> None:
        """Push an additional item onto the stack"""
        if self.full():
            raise IndexError('Cannot push to a filled Stack'
                            f'(max_size={self.max_size}')
        self._stack.append(item)

    def pop(self):
        """Remove and return the top value of the stack"""
        return self._stack.pop()
