"""
This module provides a sequence class which can be used for cyclic values
"""

from typing import Generic, TypeVar

T = TypeVar('T')


class Cycle(list, Generic[T]):
    """This class can be used to store cyclic values"""

    def __getitem__(self, key: int) -> T:
        return super().__getitem__(key % len(self))

    def __setitem__(self, key: int, value: T):
        super().__setitem__(key % len(self), value)

    def remove(self, index: int):
        """Remove value at location "index" """
        del self[index % len(self)]
