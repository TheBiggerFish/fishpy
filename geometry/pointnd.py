"""
This module provides a class for storing points which lie in n-dimensional
space
"""

from itertools import product as cartesian
from typing import Callable, Iterable, List, Optional, Union


class PointND:
    """Class for storing points which lie in n-dimensional space"""

    def __init__(self,initial_values:Iterable[Union[int,float]]):
        self._dim = len(initial_values)
        if self._dim == 0:
            raise ValueError('Number of dimensions must be n>=1')
        self._coords = list(initial_values)

    def __getitem__(self,key:Union[int,slice]) -> Union[int,float]:
        if isinstance(key,int):
            if key < 0:
                raise IndexError('Index out of range')
            if key >= self._dim:
                return 0
            return self._coords[key]
        if isinstance(key,slice):
            return self._coords[key]
        raise TypeError('PointND accessor must be an integer')

    def __setitem__(self,index:int,value:Union[int,float]) -> None:
        if not isinstance(index,int):
            raise TypeError('PointND accessor must be an integer')
        if index < 0 or index >= self._dim:
            raise IndexError('Index out of range')
        self._coords[index] = value

    @staticmethod
    def zeros(dimensions:int) -> 'PointND':
        """Returns the origin of an n-dimensional space"""
        return PointND([0]*dimensions)

    def copy(self) -> 'PointND':
        """Returns a shallow copy of self"""
        return PointND(self._coords[:])

    def __add__(self,other:'PointND') -> 'PointND':
        steps = self._dim if self._dim >= other._dim else other._dim
        result = []
        for i in range(steps):
            result.append(self[i]+other[i])
        return PointND(result)

    def __str__(self) -> str:
        return str(tuple(self._coords))

    def __repr__(self) -> str:
        return f'PointND{str(self)}'

    def __iter__(self):
        for c in self._coords:
            yield c

    def __eq__(self,other:'PointND') -> bool:
        larger = other if self._dim < other._dim else self
        smaller = self if self._dim < other._dim else other
        diff = larger.dim - smaller.dim
        if larger[-diff:] != [0]*diff:
            return False
        for dim in range(larger.dim-diff):
            if larger[dim] != smaller[dim]:
                return False
        return True

    def __le__(self,other:'PointND') -> bool:
        larger = other._dim if self._dim < other._dim else self._dim
        for dim in range(larger):
            if self[dim] > other[dim]:
                return False
        return True

    def __lt__(self,other:'PointND') -> bool:
        larger = other._dim if self._dim < other._dim else self._dim
        for dim in range(larger):
            if self[dim] >= other[dim]:
                return False
        return True

    @property
    def dim(self) -> int:
        """Property representing the dimensionality of self"""
        return self._dim

    def _assert_dimension(self,dim:int,coord:str) -> None:
        if self._dim < dim:
            raise IndexError(f'{self._dim} dimensional points do not '\
                f'have a <{coord}> coordinate, required dim >= {dim}')

    def get_adjacent_points(self,
                            filter_function:Optional[Callable[['PointND'],bool]]=None
                            ) -> List['PointND']:
        """
        Returns the adjacent lattice points of a given point, optionally
        filtering out points with filter_function
        """

        self_rel = tuple([0]*self._dim)
        adj = list(cartesian([-1,0,1],repeat=self._dim))
        adj = [PointND(pt)+self for pt in adj if pt != self_rel]
        if filter_function is not None:
            adj = filter(filter_function,adj)
        return list(adj)

    @property
    def x(self) -> Union[int,float]:
        """Returns the value in the first dimension"""
        self._assert_dimension(1,'x')
        return self._coords[0]

    @x.setter
    def x(self,value:Union[int,float]) -> None:
        self._assert_dimension(1,'x')
        self._coords[0] = value

    @property
    def y(self) -> Union[int,float]:
        """Returns the value in the second dimension"""
        self._assert_dimension(2,'y')
        return self._coords[1]

    @y.setter
    def y(self,value:Union[int,float]) -> None:
        self._assert_dimension(2,'y')
        self._coords[1] = value

    @property
    def z(self) -> Union[int,float]:
        """Returns the value in the third dimension"""
        self._assert_dimension(3,'z')
        return self._coords[2]

    @z.setter
    def z(self,value:Union[int,float]) -> None:
        self._assert_dimension(3,'z')
        self._coords[2] = value

    @property
    def w(self) -> Union[int,float]:
        """Returns the value in the fourth dimension"""
        self._assert_dimension(4,'w')
        return self._coords[3]

    @w.setter
    def w(self,value:Union[int,float]) -> None:
        self._assert_dimension(4,'w')
        self._coords[3] = value
