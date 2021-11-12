"""
This module provides a node class which can be used in building graphs, trees,
linked lists, etc.
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')

class Node(Generic[T]):
    """This class can be used for building graphs, trees, linked lists, etc."""

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
        """Return a list of nodes which are adjacent this this node"""

        if self.parent is not None:
            return [self.parent] + self.children
        return self.children

    def root(self) -> 'Node':
        """Find the root parent node of the structure of nodes"""

        cur = self
        while cur.parent is not None:
            cur = cur.parent
        return cur

    def add_child(self,child:'Node') -> None:
        """Add a child node to the list of children"""
        self.children.append(child)

    def __hash__(self) -> int:
        return hash(self.name)
