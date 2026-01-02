"""
This module provides a grid class which can be used in displaying 2D
pathfinding which follows a lattice grid
"""


from queue import Queue
from typing import (Any, Callable, Dict, Iterable, List, Optional, Set, Tuple,
                    Union, TypeVar, Generic, Hashable, Self)

from ...geometry import LatticePoint, Vector2D
from .cell import Cell

T = TypeVar('T', bound=Hashable)

class Grid(Generic[T]):
    """
    A class which can be used in displaying 2D pathfinding which follows a
    lattice grid
    """

    def __init__(self, grid: List[List[Cell[T]]], offset: Optional[LatticePoint] = None):
        self.grid = grid
        self.offset = offset or LatticePoint(0, 0)
        self._iter = LatticePoint(0, 0)

    def __getitem__(self, key: Union[LatticePoint, slice, int]
                    ) -> Union[T, 'Grid[T]', list[Cell[T]]]:
        if isinstance(key, LatticePoint):
            if key not in self:
                raise KeyError('Point not located on the grid')
            return self.grid[key.y-self.offset.y][key.x-self.offset.x].value
        if isinstance(key, slice):
            if key.step is not None:
                raise NotImplementedError(f'{self.__class__.__name__}.__getitem__ '
                                          'cannot accept slices with a step value')
            start, stop = key.start, key.stop
            if not isinstance(start, LatticePoint) or not isinstance(stop, LatticePoint):
                raise TypeError(f'{self.__class__.__name__}.__getitem__ slice '
                                'accessors must be of type LatticePoint')
            return self.subgrid(start, stop)
        if isinstance(key, int):
            if key < 0 or key >= len(self.grid):
                raise IndexError('Row not defined on the grid')
            return self.grid[key]
        raise TypeError(f'{self.__class__.__name__}.__getitem__ cannot '
                        f'accept accessors of type {type(key)}')

    def __setitem__(self, pt: LatticePoint, value: T) -> None:
        if not isinstance(pt, LatticePoint):
            raise TypeError(
                f'Grid accessor must be of type Point, type {type(pt)} provided')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        self.grid[pt.y-self.offset.y][pt.x-self.offset.x].value = value

    def __contains__(self, pt: LatticePoint) -> bool:
        if not isinstance(pt, LatticePoint):
            raise TypeError(
                f'Grid accessor must be of type Point, type {type(pt)} provided')
        return 0 <= pt.x-self.offset.x < self.width and 0 <= pt.y-self.offset.y < self.height

    def __iter__(self):
        return iter([cell for row in self.grid for cell in row])

    def __eq__(self, other: 'Grid') -> bool:
        if self.size != other.size or self.offset != other.offset:
            return False
        for pt in self:
            if self[pt] != other[pt]:
                return False
        return True

    def value_positions(self, values: Iterable[T]) -> dict[T, list[LatticePoint]]:
        """
        Return a list of points for each value passed in the "values" list
        which represents the list of positions in which that value can be
        found on the grid
        """

        mapping: dict[T, list[LatticePoint]] = {value: [] for value in values}
        for x in range(self.offset.x, self.offset.x+self.width):
            for y in range(self.offset.y, self.offset.y+self.height):
                pt = LatticePoint(x, y)
                value: T = self[pt]
                if (value := self[pt]) in mapping:
                    mapping[value].append(pt)
        return mapping

    @classmethod
    def from_list_of_iterables(cls, rows: list[Iterable[T]],
                               offset: Optional[LatticePoint] = None) -> 'Grid[T]':
        """Build a grid from a list of iterables of equal length"""

        offset = offset or LatticePoint(0, 0)
        bounds = LatticePoint(len(rows[0]), len(rows))
        grid = cls.blank(bounds, offset)
        for x in range(bounds.x):
            for y in range(bounds.y):
                pos = LatticePoint(x, y) + offset
                grid[pos] = rows[y][x]
        return grid

    @classmethod
    def from_iterable_of_cells(cls, cells: Iterable[Cell[T]], default_value: T = '.') -> 'Grid[T]':
        """Build a grid of sufficient size for all of the included cells"""

        cells = list(cells)
        min_, max_ = LatticePoint(10**64, 10**64), LatticePoint(-10**64, -10**64)
        for cell in cells:
            if cell.x < min_.x:
                min_.x = cell.x
            if cell.x > max_.x:
                max_.x = cell.x
            if cell.y < min_.y:
                min_.y = cell.y
            if cell.y > max_.y:
                max_.y = cell.y

        grid = cls.blank(max_-min_+LatticePoint(1, 1), min_, default_value)
        for cell in cells:
            grid[cell] = cell.value
        return grid

    @classmethod
    def blank(cls, bounds: LatticePoint, offset: Optional[LatticePoint] = None, default_value: T = '.') -> 'Grid[T]':
        """Return a blank grid of the given size "bounds" """

        offset = offset or LatticePoint(0, 0)

        grid = []
        for y in range(bounds.y):
            row = []
            for x in range(bounds.x):
                row += [Cell(x+offset.x, y+offset.y, default_value)]
            grid += [row]
        return cls(grid, offset=offset)

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
    def size(self) -> LatticePoint:
        """This property represents the width and height of the grid"""
        return LatticePoint(self.width, self.height)

    @property
    def offset(self) -> LatticePoint:
        """This property represents the amount the grid's origin is shifted from (0,0)"""
        return self._offset

    @offset.setter
    def offset(self, value) -> None:
        """Setter for offset property"""
        self._offset = value

    @property
    def bounds(self) -> Tuple[LatticePoint, LatticePoint]:
        """This property represents the lower and upper bounds of the grid"""
        return self.offset, self.offset+self.size

    def copy(self) -> 'Grid[T]':
        """This method returns a deep copy of self"""

        grid = []
        for y in range(self.offset.y, self.offset.y+self.height):
            row = []
            for x in range(self.offset.x, self.offset.x+self.width):
                row += [Cell(x, y, self[LatticePoint(x, y)])]
            grid += [row]

        new_grid = type(self)(grid)
        new_grid.offset = self.offset
        return new_grid

    def conditional_update(self, predicate_function: Callable[[LatticePoint], T]) -> 'Grid[T]':
        """
        This method can be used to set cells based on the results of a function
        which takes in a LatticePoint and returns a new value for that cell.
        """

        new = self.copy()
        for y in range(self.offset.y, self.offset.y+new.height):
            for x in range(self.offset.x, self.offset.x+new.width):
                pt = LatticePoint(x, y)
                if value := predicate_function(pt):
                    new[pt] = value
        return new

    def draw_search(self, path: list[LatticePoint], path_char: str = '*',
                    explored: Optional[set[LatticePoint]] = None,
                    explored_char: Optional[str] = None) -> Self:
        """
        This function can be used to draw a search by passing in the path
        taken and the set of explored points
        """

        if explored is not None and explored_char is not None:
            for pt in explored:
                if pt in self:
                    self[pt].value = explored_char
        for pt in path:
            if pt in self:
                self[pt].value = path_char
        return self

    def overlay(self, other: 'Grid[T]', empty_value: T) -> 'Grid[T]':
        """
        Overlay the self grid over top of another grid. Only non-empty values
        from the other grid will be copied over
        """

        if other.bounds[0] not in self or other.bounds[1]-LatticePoint(1, 1) not in self:
            raise ValueError('Other grid not fully within bounds')
        # if self.size != other.size or self.offset != other.offset:
        #     raise ValueError('Other grid not fully within bounds')

        new = self.copy()
        for loc in other:
            loc: Cell
            if loc.rep != empty_char:
                new[loc] = loc
        return new

    def to_string(self, separator: str = ' ') -> str:
        """
        Returns a string representation with an arbitrary separator. For a
        well-formatted grid, values across all cells should have the same length
        """

        return '\n'.join([separator.join([str(col) for col in row]) for row in self.grid])

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(offset={self.offset},size={self.size})'

    def subgrid(self, lower_bound: Optional[LatticePoint] = None,
                upper_bound: Optional[LatticePoint] = None,
                reference: bool = False) -> 'Grid[T]':
        """
        Generate a grid based on the sub-selection between "lower_bound" and
        "upper_bound"
        """

        if lower_bound is None:
            lower_bound = self.offset
        if upper_bound is None:
            upper_bound = self.bounds[1]

        if not isinstance(lower_bound, LatticePoint):
            raise TypeError(f'{self.__class__.__name__}.subgrid lower_bound '
                            f'should be of type LatticePoint, '
                            f'{type(lower_bound)=} provided')

        if not isinstance(upper_bound, LatticePoint):
            raise TypeError(f'{self.__class__.__name__}.subgrid upper_bound '
                            f'should be of type LatticePoint, '
                            f'{type(upper_bound)=} provided')

        if lower_bound.is_above(upper_bound) or lower_bound.is_right_of(upper_bound):
            raise ValueError('Lower bound should be less than or equal to'
                             'upper bound')

        grid = []
        for row in self.grid[lower_bound.y:upper_bound.y]:
            row: list[Cell]
            if reference:
                grid.append(row[lower_bound.x:upper_bound.x])
            else:
                grid.append([cell.copy() for cell in row[lower_bound.x:upper_bound.x]])

        g = type(self)(grid)
        g.offset = lower_bound
        return g

    def shift(self, step: Vector2D) -> 'Self':
        """Translate the entire grid in the direction of the step vector"""

        if not isinstance(step.x, int) or not isinstance(step.y, int):
            raise TypeError('Cannot shift grid by non-integer amount')

        for pt in self:
            pt: Cell
            pt.x += step.x
            pt.y += step.y
        self.offset += step

        return self

    def flood_fill(self, start: LatticePoint,
                   predicate_function: Callable[[LatticePoint], bool]) -> set[LatticePoint]:
        """
        This methods performs a flood fill from the start location, walled off
        by predicate_function
        """

        seen: set[LatticePoint] = set()
        q: Queue[LatticePoint] = Queue()
        q.put(start)

        while not q.empty():
            pos: LatticePoint = q.get()
            if pos in seen or predicate_function(pos):
                continue
            seen.add(pos)

            for adj in pos.get_adjacent_points(lower_bound=self.offset,
                                               upper_bound=self.offset+self.size):
                q.put(adj)
        return seen

    def draw_line(self, character: str, start: LatticePoint, step: Vector2D, count: int) -> 'Self':
        """Write a number of characters to a grid in a single line"""
        for i in range(count+1):
            pos = start + step*i
            if pos in self:
                self[pos].rep = character
        return self

    def row(self, index: int) -> Optional[list[Cell[T]]]:
        if 0 <= (index + self.offset.y) < self.height:
            return self.grid[index + self.offset.y]
        return None
    
    def col(self, index: int) -> Optional[list[Cell[T]]]:
        if 0 <= (index + self.offset.x) < self.width:
            return [row[index + self.offset.x] for row in self.grid]
        return None
            
        
