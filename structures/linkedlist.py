"""This module provides an implementation of a linked list"""

from typing import Generic, Optional, TypeVar

from .node import Node


class LinkedList(Node):
    """An implementation of a linked list"""

    def __init__(self, value, name: str = '',
                 next_: Optional['LinkedList'] = None,
                 prev: Optional['LinkedList'] = None):
        super().__init__(value, name, children=[next_], parent=prev)

    @property
    def prev(self) -> 'LinkedList':
        """This property represents the previous node of the linked list"""
        return self.parent

    @prev.setter
    def prev(self, value: 'LinkedList') -> None:
        self.parent = value

    @property
    def next(self) -> 'LinkedList':
        """This property represents the next node of the linked list"""
        return self.children[0]

    @next.setter
    def next(self, value: 'LinkedList') -> None:
        self.children[0] = value

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'
