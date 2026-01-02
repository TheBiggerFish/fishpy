from ...geometry import LatticePoint
from typing import TypeVar, Generic, Hashable
from copy import deepcopy

T = TypeVar('T', bound=Hashable)

class Cell(LatticePoint, Generic[T]):
    def __init__(self, x: int, y: int, value: T):
        super().__init__(x, y)
        self.value = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, value={self.value!r})'

    def copy(self) -> 'Cell':
        return Cell(self.x, self.y, deepcopy(self.value))

