from queue import PriorityQueue
from typing import Iterable, List,Dict,Callable,Any, Optional, Type, Union
from functools import cached_property
from enum import Enum

from fishpy.geometry import Point
from fishpy.structures import Stack
from fishpy.physics import Point3D

class Location(Point):
    OPEN = 0
    IMPASSABLE = 1
    def __init__(self,x:int,y:int,type:Enum,rep:str=' '):
        super().__init__(x,y)
        self.type = type
        self.rep = rep

    def copy(self) -> 'Location':
        return Location(self.x,self.y,self.type,self.rep[:])

    def __str__(self) -> str:
        return self.rep

    def __eq__(self,other:'Location') -> None:
        return super().__eq__(other) and self.type == other.type and self.rep == other.rep

    def is_passible(self) -> bool:
        return self.type != Location.IMPASSABLE

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
        map = {}
        for char in chars:
            map[char] = []
        for x in range(self._offset.x,self._offset.x+self.width):
            for y in range(self._offset.y,self._offset.y+self.height):
                pt = Point(x,y)
                if self[pt].rep in map:
                    map[self[pt].rep].append(pt)
        return map

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

        g = type(self)(grid)
        g._offset = self._offset
        return g

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
  
class ExpandableGrid(Grid):
    @staticmethod
    def _assert_positive_integer(n:int) -> bool:
        if isinstance(n,int) and n > 0:
            return True
        raise ValueError('Can only expand with positive integers')

    def expand_up(self,steps:int,fill_char:str='.') -> None:
        ExpandableGrid._assert_positive_integer(steps)
        self._offset.y -= steps
        for y in range(self._offset.y,self._offset.y+steps):
            row = []
            for x in range(self.width):
                row.append(Location(self._offset.x+x,y,Location.OPEN,fill_char))
            self.grid = [row] + self.grid

    def expand_down(self,steps:int,fill_char:str='.') -> None:
        ExpandableGrid._assert_positive_integer(steps)
        low_y = self._offset.y + self.height
        for y in range(low_y,low_y+steps):
            row = []
            for x in range(self.width):
                row.append(Location(self._offset.x+x,y,Location.OPEN,fill_char))
            self.grid.append(row)

    def expand_left(self,steps:int,fill_char:str='.') -> None:
        ExpandableGrid._assert_positive_integer(steps)
        self._offset.x -= steps
        for y in range(self.height):
            for x in range(self._offset.x,self._offset.x+steps):
                self.grid[y] = [Location(x,self._offset.y+y,Location.OPEN,fill_char)] + self.grid[y]

    def expand_right(self,steps:int,fill_char:str='.') -> None:
        ExpandableGrid._assert_positive_integer(steps)
        low_x = self._offset.x + self.width
        for y in range(self.height):
            for x in range(low_x,low_x+steps):
                self.grid[y] = self.grid[y] + [Location(x,self._offset.y+y,Location.OPEN,fill_char)]
                
    def shift(self,step:Point) -> None:
        for pt in self:
            pt.x += step.x
            pt.y += step.y
        self._offset += step
     
    
# class SymmetricGrid(Grid):
#     def rotate(self,steps):
#         new = self.blank(self.bounds,offset=self._offset)
#         for 

class DijkstraItem:
    def __init__(self, value, g:int, h: int = 0):
        self.value = value
        self.g = g
        self.h = h

    @staticmethod
    def get_h(source, target, heuristic_function:Callable[[Any],int]) -> int:
        if heuristic_function is not None:
            return heuristic_function(source,target)
        return 0
    
    def __lt__(self,other:'DijkstraItem') -> bool:
        return (self.g+self.h,self.h,self.g) < (other.g+other.h,other.h,other.g)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return f'DijkstraItem: value=\'{str(self.value)}\', g={self.g}, h={self.h}'


class Dijkstra:
    def __init__(self, start, target,
                 adjacency_function: Callable[[Any],List[Any]],
                 validation_function: Optional[Callable[[Any],bool]] = None,
                 heuristic_function: Optional[Callable[[Any],int]] = None,
                 verbose: bool = False):
        self.start = start
        self.target = target
        self._adjacency_function = adjacency_function
        self._validation_function = validation_function
        self._heuristic_function = heuristic_function
        self.verbose = verbose
        self._dist = -1        
        
        self.seen = set()
        self.prev = {}
        self.q = PriorityQueue()

        estimate = DijkstraItem.get_h(self.start,self.target,self._heuristic_function)
        self.q.put(DijkstraItem(self.start,0,estimate))

    def search(self, max_depth: int = -1) -> int:
        if self.target in self.seen:
            return self._dist
        while not self.q.empty():
            item = self.q.get()
            if item.value in self.seen:
                continue
            if self.verbose:
                print(item.value,'\n')

            self.seen.add(item.value)

            if item.value == self.target:
                self._dist = item.g
                return item.g
            
            g = item.g + 1
            if g > max_depth > -1:
                continue
            for adj in self._adjacency_function(item.value):
                if self._validation_function is None or self._validation_function(adj): 
                    if adj not in self.seen and adj not in self.prev:
                        h = DijkstraItem.get_h(adj,self.target,self._heuristic_function)
                        self.q.put(DijkstraItem(adj,g,h))
                        self.prev[adj] = item.value
        return -1

    @cached_property
    def path(self) -> List[Any]:
        path = []
        cur = self.target
        while cur in self.prev:
            path.append(cur)
            cur = self.prev[cur]
        path.append(cur)
        return list(reversed(path))

    def stringify(self,
                  string_function:Callable[[List[Any],List[Any]],str]) -> str:
        return string_function(path=self.path, seen=self.path)


class DepthFirstTraversal:
    def __init__(self, start, target,
                 adjacency_function: Callable[[Any],List[Any]],
                 distance_function: Optional[Callable[[Any,Any],Union[int,float]]] = None,
                 validation_function: Optional[Callable[[Any],bool]]  =None,
                 cyclic: bool = False,
                 longest_path: bool = False,
                 verbose: bool = False):
        if cyclic and longest_path:
            raise ValueError('DepthFirstTraversal cannot be both cyclic and longest_path')
        self.start = start
        self.target = target
        self._adjacency_function = adjacency_function
        self._distance_function = distance_function
        self._validation_function = validation_function
        self.longest_path = longest_path
        self.cyclic = cyclic
        self.verbose = verbose
        
        self.distance = {self.start:0}
        self.prev = {self.start:None}
        self.stack = Stack()
        self.stack.push(self.start)

    def execute(self):
        while not self.stack.empty():
            cur = self.stack.pop()
            neighbors = self._adjacency_function(cur)
            for adj in neighbors:
                if self._validation_function is not None and not self._validation_function(adj):
                    continue
                if not self.cyclic and adj in self.prev:
                    continue
                d = 1
                if self._distance_function is not None:
                    self._distance_function(cur,adj)
                new_distance = self.distance[cur] + d
                if adj not in self.distance or (self.longest_path and self.distance[adj] < new_distance) or (not self.longest_path and self.distance[adj] > new_distance):
                    self.distance[adj] = new_distance
                    self.prev[adj] = cur
                    if not(self.longest_path and adj == self.target):
                        self.stack.push(adj)
        return self.distance[self.target]


class Location3D(Point3D):
    OPEN = 0
    IMPASSABLE = 1
    def __init__(self,x:int,y:int,z:int,type:Enum,rep:str=' '):
        super().__init__(x,y,z)
        self.type = type
        self.rep = rep

    def copy(self) -> 'Location3D':
        return Location3D(self.x,self.y,self.z,self.type,self.rep[:])
        
    def __str__(self) -> str:
        return self.rep
        
    def __eq__(self,other:'Location3D') -> bool:
        return super().__eq__(other) and self.type == other.type and self.rep == other.rep


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

    def __iter__(self) -> Iterable[Location]:
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
               
    def char_positions(self,chars:List[str]) -> Dict[str,List[Point]]:
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
