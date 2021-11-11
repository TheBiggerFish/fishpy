"""
This module provides a grid class which can be used in displaying 2D
pathfinding which follows a lattice grid
"""

#pylint:disable=protected-access

from typing import Any, Callable, Dict, Iterable, List, Optional

from ...geometry import Point
from ..location import Location


class Grid:
    """
    A class which can be used in displaying 2D pathfinding which follows a
    lattice grid
    """

    def __init__(self,grid:List[List[Location]],offset:Point=Point(0,0)):
        self.grid = grid
        self._iter = Point(0,0)
        self._offset = offset

    def __getitem__(self,pt:Point) -> Location:
        if not isinstance(pt,Point):
            raise TypeError(f'Grid accessor must be of type Point, type {type(pt)} provided')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        return self.grid[pt.y-self._offset.y][pt.x-self._offset.x]

    def __setitem__(self,pt:Point,value:Any) -> None:
        if not isinstance(pt,Point):
            raise TypeError(f'Grid accessor must be of type Point, type {type(pt)} provided')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        self.grid[pt.y-self._offset.y][pt.x-self._offset.x] = value

    def __contains__(self,pt:Point) -> bool:
        if not isinstance(pt,Point):
            raise TypeError(f'Grid accessor must be of type Point, type {type(pt)} provided')
        return 0 <= pt.x-self._offset.x < self.width and 0 <= pt.y-self._offset.y < self.height

    def __iter__(self) -> Iterable[Location]:
        for row in self.grid:
            for col in row:
                yield col

    def __eq__(self,other:'Grid') -> bool:
        if self.bounds != other.bounds or self._offset != other._offset:
            return False
        for pt in self:
            if self[pt] != other[pt]:
                return False
        return True

    def char_positions(self,chars:List[str]) -> Dict[str,List[Point]]:
        """
        Return a list of points for each character passed in the "chars" list
        which represents the list of positions in which that character can be
        found on the grid
        """

        mapping:Dict[str,List[Point]] = {}
        for char in chars:
            mapping[char] = []
        for x in range(self._offset.x,self._offset.x+self.width):
            for y in range(self._offset.y,self._offset.y+self.height):
                pt = Point(x,y)
                if self[pt].rep in mapping:
                    mapping[self[pt].rep].append(pt)
        return mapping

    @classmethod
    def from_list_of_strings(cls,rows:List[str],wall_char:str='#',
                             offset:Point=Point(0,0)) -> 'Grid':
        """Build a grid from a list of strings of equal length"""

        bounds = Point(len(rows[0]),len(rows))
        grid = cls.blank(bounds,offset)
        for x in range(bounds.x):
            for y in range(bounds.y):
                is_wall = Location.IMPASSABLE if rows[y][x]==wall_char else Location.OPEN
                loc = Location(x+offset.x,y+offset.y,is_wall,rows[y][x])
                grid[Point(x+offset.x,y+offset.y)] = loc
        return grid

    @classmethod
    def blank(cls,bounds:Point,offset:Point=Point(0,0)) -> 'Grid':
        """Return a blank grid of the given size \"bounds\""""

        grid = []
        for y in range(bounds.y):
            row = []
            for x in range(bounds.x):
                row += [Location(x+offset.x,y+offset.y,Location.OPEN,'.')]
            grid = [row] + grid
        return cls(grid,offset=offset)

    @property
    def width(self) -> int:
        """This property represents the width of the grid"""
        if self.height == 0:
            return 0
        return len(self.grid[0])

    @property
    def height(self) -> int:
        """This property represents the height of the grid"""
        return len(self.grid)

    @property
    def bounds(self) -> Point:
        """This property represents the width and height of the grid"""
        return Point(self.width,self.height)

    def copy(self) -> 'Grid':
        """This method returns a deep copy of self"""

        grid = []
        for y in range(self._offset.y,self._offset.y+self.height):
            row = []
            for x in range(self._offset.x,self._offset.x+self.width):
                row += [self[Point(x,y)].copy()]
            grid += [row]

        grid = type(self)(grid)
        grid._offset = self._offset
        return grid

    def conditional_walls(self,predicate_function:Callable[[Point],bool],char:str) -> 'Grid':
        """
        This method can be used to add walls based on the results of a
        function which takes in a Point and returns a boolean for whether
        there should be a wall at that point
        """

        new = self.copy()
        for y in range(self._offset.y,self._offset.y+new.height):
            for x in range(self._offset.x,self._offset.x+new.width):
                pt = Point(x,y)
                if predicate_function(pt):
                    new[pt] = Location(x,y,Location.IMPASSABLE,char)
        return new

    def draw_search(self,path:list,explored:Optional[set]=None,
                    path_char:str='*',explored_char:str='o') -> str:
        """
        This function can be used to draw a search by passing in the path
        taken and the set of explored points
        """

        for pt in explored:
            if pt in self:
                self[pt].rep = explored_char
        for pt in path:
            if pt in self:
                self[pt].rep = path_char

    def overlay(self,other:'Grid',empty:str='.'):
        """Overlay the self grid over top of another grid"""

        if self.bounds != other.bounds or self._offset != other._offset:
            raise ValueError('Grids must be exactly overlapping to overlay')

        new = self.copy()
        for loc in other:
            if loc.rep != empty:
                new[loc] = loc
        return new


    def to_string(self,separator:str=' '):
        """Returns a string representation with an arbitrary separator"""

        return '\n'.join([separator.join([str(col) for col in row]) for row in self.grid])


    def __str__(self) -> str:
        return self.to_string()


    def subgrid(self,lower_bound:Optional[Point]=None,
                upper_bound:Optional[Point]=None,
                reference:bool=False) -> 'Grid':
        """
        Generate a grid based on the sub-selection between "lower_bound" and
        "upper_bound"
        """

        if not lower_bound:
            lower_bound = self._offset
        if not upper_bound:
            upper_bound = self._offset + self.bounds

        grid = []
        for row in range(lower_bound.y,upper_bound.y):
            if reference:
                grid.append(self.grid[row][lower_bound.x:upper_bound.x])
            else:
                grid.append([col.copy() for col in self.grid[row][lower_bound.x:upper_bound.x]])

        g = type(self)(grid)
        g._offset = lower_bound
        return g
