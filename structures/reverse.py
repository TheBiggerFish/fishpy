from typing import Generic, TypeVar

T = TypeVar('T')

class Reverse(Generic[T]):
    def __init__(self,payload:T):
        self.payload = payload

    def __lt__(self,other:'Reverse') -> bool:
        return self.payload > other.payload

    def __gt__(self,other:'Reverse') -> bool:
        return self.payload < other.payload

    def __eq__(self,other:'Reverse') -> bool:
        return self.payload == other.payload

    def __str__(self) -> str:
        return str(self.payload)

    def __hash__(self) -> int:
        return hash(self.payload)
