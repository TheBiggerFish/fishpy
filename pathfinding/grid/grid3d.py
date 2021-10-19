from typing import Any, Dict, Iterable, List

from fishpy.geometry import Point3D

from ..location3d import Location3D
from .grid import Grid


class Grid3D:
    def __init__(self,grid:List[List[List[Location3D]]],offset:Point3D=Point3D(0,0,0)):
        self.grid = [Grid(sub,offset.copy()) for sub in grid]
        self._iter = Point3D(0,0,0)
        self._offset = offset

    def __getitem__(self,pt:Point3D) -> Location3D:
        if not isinstance(pt,Point3D):
            raise TypeError('Grid accessor must be of type Point3D')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        return self.grid[pt.z-self._offset.z][pt]

    def __setitem__(self,pt:Point3D,value:Any) -> None:
        if not isinstance(pt,Point3D):
            raise TypeError('Grid accessor must be of type Point3D')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        self.grid[pt.z-self._offset.z][pt] = value

    def __contains__(self,pt:Point3D) -> bool:
        if not isinstance(pt,Point3D):
            raise TypeError('Grid accessor must be of type Point')
        return 0 <= pt.x-self._offset.x < self.width and 0 <= pt.y-self._offset.y < self.height and  0 <= pt.z-self._offset.z < self.depth

    def __iter__(self) -> Iterable[Location3D]:
        for subgrid in self.grid:
            for pt in subgrid:
                yield pt

    @staticmethod
    def from_list_of_list_of_strings(rows:List[List[str]],wall_char:str='#',offset:Point3D=Point3D(0,0,0)) -> 'Grid3D':
        bounds = Point3D(len(rows[0][0]),len(rows[0]),len(rows))
        grid = Grid3D.blank(bounds,offset)
        for x in range(bounds.x):
            for y in range(bounds.y):
                for z in range(bounds.z):
                    is_wall = Location3D.IMPASSABLE if rows[z][y][x]==wall_char else Location3D.OPEN
                    loc = Location3D(x+offset.x,y+offset.y,z+offset.z,is_wall,rows[z][y][x])
                    grid[Point3D(x+offset.x,y+offset.y,z+offset.z)] = loc
        return grid

    @staticmethod
    def blank(bounds:Point3D,offset:Point3D=Point3D(0,0,0)) -> 'Grid3D':
        cube = []
        for z in range(bounds.z):
            subgrid = []
            for y in range(bounds.y):
                row = []
                for x in range(bounds.x):
                    row += [Location3D(x+offset.x,y+offset.y,z+offset.z,Location3D.OPEN,'.')]
                subgrid += [row]
            cube += [subgrid]
        return Grid3D(cube,offset)

    @property
    def width(self) -> int:
        return self.grid[0].width

    @property
    def height(self) -> int:
        if self.depth == 0:
            return 0
        return self.grid[0].height

    @property
    def depth(self) -> int:
        return len(self.grid)

    @property
    def bounds(self) -> Point3D:
        return Point3D(self.width,self.height,self.depth)

    def __str__(self) -> str:
        return '\n\n'.join([str(subgrid) for subgrid in self.grid])

    def copy(self) -> 'Grid3D':
        return Grid3D([subgrid.copy().grid for subgrid in self.grid],offset=self._offset.copy())

    @staticmethod
    def _assert_positive_integer(n:int) -> bool:
        if isinstance(n,int) and n > 0:
            return True
        raise ValueError('Can only expand with positive integers')

    def expand_up(self,steps:int,fill_char:str='.') -> None:
        Grid3D._assert_positive_integer(steps)
        self._offset.y -= steps
        for z in range(self.depth):
            self.grid[z]._offset.y -= steps
            for y in range(self._offset.y,self._offset.y+steps):
                row = []
                for x in range(self.width):
                    row.append(Location3D(self._offset.x+x,y,self._offset.z+z,Location3D.OPEN,fill_char))
                self.grid[z].grid = [row] + self.grid[z].grid

    def expand_down(self,steps:int,fill_char:str='.') -> None:
        Grid3D._assert_positive_integer(steps)
        low_y = self._offset.y + self.height
        for z in range(self.depth):
            for y in range(low_y,low_y+steps):
                row = []
                for x in range(self.width):
                    row.append(Location3D(self._offset.x+x,y,self._offset.z+z,Location3D.OPEN,fill_char))
                self.grid[z].grid.append(row)

    def expand_left(self,steps:int,fill_char:str='.') -> None:
        Grid3D._assert_positive_integer(steps)
        self._offset.x -= steps
        for z in range(self.depth):
            self.grid[z]._offset.x -= steps
            for y in range(self.height):
                for x in range(self._offset.x,self._offset.x+steps):
                    self.grid[z].grid[y] = [Location3D(x,self._offset.y+y,self._offset.z+z,Location3D.OPEN,fill_char)] + self.grid[z].grid[y]

    def expand_right(self,steps:int,fill_char:str='.') -> None:
        Grid3D._assert_positive_integer(steps)
        low_x = self._offset.x + self.width
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(low_x,low_x+steps):
                    self.grid[z].grid[y] = self.grid[z].grid[y] + [Location3D(x,self._offset.y+y,self._offset.z+z,Location3D.OPEN,fill_char)]

    def expand_in(self,steps:int,fill_char:str='.') -> None:
        Grid3D._assert_positive_integer(steps)
        self._offset.z -= steps
        for z in range(self._offset.z,self._offset.z+steps):
            new_subgrid = []
            for y in range(self.height):
                new_row = []
                for x in range(self.width):
                    new_row.append(Location3D(self._offset.x+x,self._offset.y+y,z,Location3D.OPEN,fill_char))
                new_subgrid.append(new_row)
            self.grid = [Grid(new_subgrid,self._offset.copy())] + self.grid

    def expand_out(self,steps:int,fill_char:str='.') -> None:
        Grid3D._assert_positive_integer(steps)
        low_z = self._offset.z + self.depth
        for z in range(low_z,low_z+steps):
            new_subgrid = []
            for y in range(self.height):
                new_row = []
                for x in range(self.width):
                    new_row.append(Location3D(self._offset.x+x,self._offset.y+y,z,Location3D.OPEN,fill_char))
                new_subgrid.append(new_row)
            self.grid.append(Grid(new_subgrid,self._offset.copy()))

    def char_positions(self,chars:List[str]) -> Dict[str,List[Point3D]]:
        map = {}
        for char in chars:
            map[char] = []
        for z in range(self.depth):
            rcvd = self.grid[z].char_positions(chars)
            for char in rcvd:
                for i,pt in enumerate(rcvd[char]):
                    rcvd[char][i] = Point3D(pt.x,pt.y,self._offset.z+z)
                map[char] += rcvd[char]
        return map
