from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')

class Node(Generic[T]):
    def __init__(self,value:T,name:str='',
                 children:Optional[List['Node']]=None,
                 parent:Optional['Node']=None):
        if children is None:
            children = []
        self.value = value
        self.name = name
        self.children = children
        self.parent = parent

    def adjacent(self) -> List['Node']:
        if self.parent is not None:
            return [self.parent] + self.children
        return self.children

    def root(self) -> 'Node':
        cur = self
        while cur.parent is not None:
            cur = cur.parent
        return cur

    def add_child(self,child) -> None:
        self.children.append(child)

    def __hash__(self) -> int:
        return hash(self.name)
