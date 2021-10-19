from typing import Any, Callable, Dict, Iterable, List, Optional

from fishpy.geometry import Point

from ..location import Location


class Grid:
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

    def __eq__(self,other:Location) -> bool:
        if self.bounds != other.bounds or self._offset != other._offset:
            return False
        for pt in self:
            if self[pt] != other[pt]:
                return False
        return True

    def char_positions(self,chars:List[str]) -> Dict[str,List[Point]]:
        mapping = {}
        for char in chars:
            mapping[char] = []
        for x in range(self._offset.x,self._offset.x+self.width):
            for y in range(self._offset.y,self._offset.y+self.height):
                pt = Point(x,y)
                if self[pt].rep in mapping:
                    mapping[self[pt].rep].append(pt)
        return mapping

    @classmethod
    def from_list_of_strings(cls,rows:List[str],wall_char:str='#',offset:Point=Point(0,0)) -> 'Grid':
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
        grid = []
        for y in range(bounds.y):
            row = []
            for x in range(bounds.x):
                row += [Location(x+offset.x,y+offset.y,Location.OPEN,'.')]
            grid = [row] + grid
        return cls(grid,offset=offset)

    @property
    def width(self) -> int:
        if self.height == 0:
            return 0
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def bounds(self) -> Point:
        return Point(self.width,self.height)

    def copy(self) -> 'Grid':
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
        new = self.copy()
        for y in range(self._offset.y,self._offset.y+new.height):
            for x in range(self._offset.x,self._offset.x+new.width):
                pt = Point(x,y)
                if predicate_function(pt):
                    new[pt] = Location(x,y,Location.IMPASSABLE,char)
        return new

    def draw_search(self,path:list,explored:set,path_char:str='*',explored_char:str='o') -> str:
        for pt in explored:
            if pt in self:
                self[pt].rep = explored_char
        for pt in path:
            if pt in self:
                self[pt].rep = path_char

    def overlay(self,other:'Grid',empty:str='.'):
        if self.bounds != other.bounds or self._offset != other._offset:
            raise ValueError('Grids must be exactly overlapping to overlay')

        new = self.copy()
        for loc in other:
            if loc.rep != empty:
                new[loc] = loc
        return new


    def to_string(self,separator:str=' '):
        return '\n'.join([separator.join([str(col) for col in row]) for row in self.grid])


    def __str__(self) -> str:
        return self.to_string()


    def subgrid(self,lower_bound:Optional[Point]=None,upper_bound:Optional[Point]=None,reference:bool=False) -> 'Grid':
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
