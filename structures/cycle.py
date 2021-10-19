from typing import Generic, TypeVar

T = TypeVar('T')

class Cycle(list,Generic[T]):
    def __getitem__(self,key:int) -> T:
        return super().__getitem__(key%len(self))

    def __setitem__(self,key:int,value:T):
        super().__setitem__(key%len(self),value)

    def remove(self,index:int):
        del self[index]
