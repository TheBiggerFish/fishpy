"""
This module provides a grid class which can be used in displaying 2D
pathfinding which follows a lattice grid
"""


from queue import Queue
from typing import (Any, Callable, Dict, Iterable, List, Optional, Set, Tuple,
                    Union)

from fishpy.geometry import LatticePoint, Vector2D

from ...geometry import LatticePoint
from ..location import Location


class Grid:
    """
    A class which can be used in displaying 2D pathfinding which follows a
    lattice grid
    """

    def __init__(self, grid: List[List[Location]], offset: LatticePoint = LatticePoint(0, 0)):
        self.grid = grid
        self.offset = offset
        self._iter = LatticePoint(0, 0)

    def __getitem__(self, key: Union[LatticePoint, slice]
                    ) -> Union[Location, 'Grid']:
        if isinstance(key, LatticePoint):
            if key not in self:
                raise KeyError('Point not located on the grid')
            return self.grid[key.y-self.offset.y][key.x-self.offset.x]
        if isinstance(key, slice):
            if key.step is not None:
                raise NotImplementedError(f'{self.__class__.__name__}.__getitem__ '
                                          'cannot accept slices with a step value')
            start, stop = key.start, key.stop
            return self.subgrid(start, stop)
        raise TypeError(f'{self.__class__.__name__}.__getitem__ cannot '
                        f'accept accessors of type {type(key)}')

    def __setitem__(self, pt: LatticePoint, value: Any) -> None:
        if not isinstance(pt, LatticePoint):
            raise TypeError(
                f'Grid accessor must be of type Point, type {type(pt)} provided')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        self.grid[pt.y-self.offset.y][pt.x-self.offset.x] = value

    def __contains__(self, pt: LatticePoint) -> bool:
        if not isinstance(pt, LatticePoint):
            raise TypeError(
                f'Grid accessor must be of type Point, type {type(pt)} provided')
        return 0 <= pt.x-self.offset.x < self.width and 0 <= pt.y-self.offset.y < self.height

    def __iter__(self) -> Iterable[Location]:
        for row in self.grid:
            for col in row:
                yield col

    def __eq__(self, other: 'Grid') -> bool:
        if self.size != other.size or self.offset != other.offset:
            return False
        for pt in self:
            if self[pt] != other[pt]:
                return False
        return True

    def char_positions(self, chars: Iterable[str]) -> Dict[str, List[LatticePoint]]:
        """
        Return a list of points for each character passed in the "chars" list
        which represents the list of positions in which that character can be
        found on the grid
        """

        mapping: Dict[str, List[LatticePoint]] = {char: [] for char in chars}
        for x in range(self.offset.x, self.offset.x+self.width):
            for y in range(self.offset.y, self.offset.y+self.height):
                pt = LatticePoint(x, y)
                if self[pt].rep in mapping:
                    mapping[self[pt].rep].append(pt)
        return mapping

    @classmethod
    def from_list_of_strings(cls, rows: List[str], wall_char: str = '#',
                             offset: LatticePoint = LatticePoint(0, 0)):
        """Build a grid from a list of strings of equal length"""

        bounds = LatticePoint(len(rows[0]), len(rows))
        grid = cls.blank(bounds, offset)
        for x in range(bounds.x):
            for y in range(bounds.y):
                is_wall = Location.IMPASSABLE if rows[y][x] == wall_char else Location.OPEN
                loc = Location(x+offset.x, y+offset.y, is_wall, rows[y][x])
                grid[LatticePoint(x+offset.x, y+offset.y)] = loc
        return grid

    @classmethod
    def from_list_of_locations(cls, locations: List[Location]):
        """Build a grid of sufficient size for all of the included locations"""

        min_, max_ = LatticePoint(
            10**64, 10**64), LatticePoint(-10**64, -10**64)
        for location in locations:
            if location.x < min_.x:
                min_.x = location.x
            if location.x > max_.x:
                max_.x = location.x
            if location.y < min_.y:
                min_.y = location.y
            if location.y > max_.y:
                max_.y = location.y

        grid = cls.blank(max_-min_+LatticePoint(1, 1), min_)
        for location in locations:
            grid[location] = location
        return grid

    @classmethod
    def blank(cls, bounds: LatticePoint, offset: LatticePoint = LatticePoint(0, 0)):
        """Return a blank grid of the given size "bounds" """

        grid = []
        for y in range(bounds.y):
            row = []
            for x in range(bounds.x):
                row += [Location(x+offset.x, y+offset.y, Location.OPEN, '.')]
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

    def copy(self):
        """This method returns a deep copy of self"""

        grid = []
        for y in range(self.offset.y, self.offset.y+self.height):
            row = []
            for x in range(self.offset.x, self.offset.x+self.width):
                row += [self[LatticePoint(x, y)].copy()]
            grid += [row]

        new_grid = type(self)(grid)
        new_grid.offset = self.offset
        return new_grid

    def conditional_walls(self, predicate_function: Callable[[LatticePoint], bool],
                          char: str) -> 'Grid':
        """
        This method can be used to add walls based on the results of a
        function which takes in a Point and returns a boolean for whether
        there should be a wall at that point
        """

        new = self.copy()
        for y in range(self.offset.y, self.offset.y+new.height):
            for x in range(self.offset.x, self.offset.x+new.width):
                pt = LatticePoint(x, y)
                if predicate_function(pt):
                    new[pt] = Location(x, y, Location.IMPASSABLE, char)
        return new

    def draw_search(self, path: List[LatticePoint], path_char: str = '*',
                    explored: Optional[Set[LatticePoint]] = None,
                    explored_char: Optional[str] = None) -> None:
        """
        This function can be used to draw a search by passing in the path
        taken and the set of explored points
        """

        if explored is not None and explored_char is not None:
            for pt in explored:
                if pt in self:
                    self[pt].rep = explored_char
        for pt in path:
            if pt in self:
                self[pt].rep = path_char

    def overlay(self, other: 'Grid', empty_char: str = '.'):
        """Overlay the self grid over top of another grid"""

        if other.bounds[0] not in self or other.bounds[1]-LatticePoint(1, 1) not in self:
            raise ValueError('Other grid not fully within bounds')
        # if self.size != other.size or self.offset != other.offset:
        #     raise ValueError('Other grid not fully within bounds')

        new = self.copy()
        for loc in other:
            loc: Location
            if loc.rep != empty_char:
                new[loc] = loc
        return new

    def to_string(self, separator: str = ' '):
        """Returns a string representation with an arbitrary separator"""

        return '\n'.join([separator.join([str(col) for col in row]) for row in self.grid])

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(offset={self.offset},size={self.size})'

    def subgrid(self, lower_bound: Optional[LatticePoint] = None,
                upper_bound: Optional[LatticePoint] = None,
                reference: bool = False):
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
            row: list[Location]
            if reference:
                grid.append(row[lower_bound.x:upper_bound.x])
            else:
                grid.append([col.copy()
                            for col in row[lower_bound.x:upper_bound.x]])

        g = type(self)(grid)
        g.offset = lower_bound
        return g

    def shift(self, step: Vector2D):
        """Translate the entire grid in the direction of the step vector"""

        if not isinstance(step.x, int) or not isinstance(step.y, int):
            raise TypeError('Cannot shift grid by non-integer amount')

        for pt in self:
            pt: Location
            pt.x += step.x
            pt.y += step.y
        self.offset += step

        return self

    def flood_fill(self, start: Location,
                   predicate_function: Callable[[Location], bool]) -> List[Location]:
        """
        This methods performs a flood fill from the start location, walled off
        by predicate_function
        """

        seen = set()
        q = Queue()
        q.put(start)

        size = 0
        while not q.empty():
            loc: Location = q.get()
            if loc in seen or predicate_function(loc):
                continue
            seen.add(loc)
            size += 1

            for adj in loc.get_adjacent_points(lower_bound=self.offset,
                                               upper_bound=self.offset+self.size):
                q.put(self[adj])
        return seen

    def draw(self, character: str, start: LatticePoint, step: Vector2D, count: int):
        """Write a number of characters to a grid in a single line"""
        for i in range(count+1):
            pos = start + step*i
            if pos in self:
                self[pos].rep = character
