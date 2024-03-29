"""
This module provides a grid class which can be used in displaying 3D
pathfinding which follows a lattice grid
"""

from typing import Any, Dict, Iterable, List

from ...geometry import Point3D
from ..location3d import Location3D
from .grid import Grid


class Grid3D:
    """
    A class which can be used in displaying 3D pathfinding which follows a
    lattice grid
    """

    def __init__(self, grid: List[List[List[Location3D]]], offset: Point3D = Point3D(0, 0, 0)):
        self.grid = [Grid(sub, offset.copy()) for sub in grid]
        self._iter = Point3D(0, 0, 0)
        self.offset = offset

    def __getitem__(self, pt: Point3D) -> Location3D:
        if not isinstance(pt, Point3D):
            raise TypeError('Grid accessor must be of type Point3D')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        return self.grid[pt.z-self.offset.z][pt]

    def __setitem__(self, pt: Point3D, value: Any) -> None:
        if not isinstance(pt, Point3D):
            raise TypeError('Grid accessor must be of type Point3D')
        if pt not in self:
            raise KeyError('Point not located on the grid')
        self.grid[pt.z-self.offset.z][pt] = value

    def __contains__(self, pt: Point3D) -> bool:
        if not isinstance(pt, Point3D):
            raise TypeError('Grid accessor must be of type Point')
        return (0 <= pt.x-self.offset.x < self.width
                and 0 <= pt.y-self.offset.y < self.height
                and 0 <= pt.z-self.offset.z < self.depth)

    def __iter__(self) -> Iterable[Location3D]:
        for subgrid in self.grid:
            for pt in subgrid:
                yield pt

    @staticmethod
    def from_list_of_list_of_strings(rows: List[List[str]],
                                     wall_char: str = '#',
                                     offset: Point3D = Point3D(0, 0, 0)
                                     ) -> 'Grid3D':
        """Build a grid from a list of list strings of equal length"""

        bounds = Point3D(len(rows[0][0]), len(rows[0]), len(rows))
        grid = Grid3D.blank(bounds, offset)
        for x in range(bounds.x):
            for y in range(bounds.y):
                for z in range(bounds.z):
                    if rows[z][y][x] == wall_char:
                        is_wall = Location3D.IMPASSABLE
                    else:
                        is_wall = Location3D.OPEN
                    loc = Location3D(x+offset.x, y+offset.y,
                                     z+offset.z, is_wall, rows[z][y][x])
                    grid[Point3D(x+offset.x, y+offset.y, z+offset.z)] = loc
        return grid

    @staticmethod
    def blank(bounds: Point3D, offset: Point3D = Point3D(0, 0, 0)) -> 'Grid3D':
        """Return a blank grid of the given size "bounds" """

        cube = []
        for z in range(bounds.z):
            subgrid = []
            for y in range(bounds.y):
                row = []
                for x in range(bounds.x):
                    row += [Location3D(x+offset.x, y+offset.y,
                                       z+offset.z, Location3D.OPEN, '.')]
                subgrid += [row]
            cube += [subgrid]
        return Grid3D(cube, offset)

    @property
    def width(self) -> int:
        """This property represents the width of the grid"""
        return self.grid[0].width

    @property
    def height(self) -> int:
        """This property represents the height of the grid"""
        if self.depth == 0:
            return 0
        return self.grid[0].height

    @property
    def depth(self) -> int:
        """This property represents the depth of the grid"""
        return len(self.grid)

    @property
    def bounds(self) -> Point3D:
        """This property represents the width and height of the grid"""
        return Point3D(self.width, self.height, self.depth)

    def __str__(self) -> str:
        return '\n\n'.join([str(subgrid) for subgrid in self.grid])

    def copy(self) -> 'Grid3D':
        """This method returns a deep copy of self"""
        return Grid3D([subgrid.copy().grid for subgrid in self.grid], offset=self.offset.copy())

    @staticmethod
    def _assert_positive_integer(n: int) -> bool:
        if isinstance(n, int) and n > 0:
            return True
        raise ValueError('Can only expand with positive integers')

    def expand_up(self, steps: int, fill_char: str = '.') -> None:
        """
        Add "steps" additional layers to the top of the grid, using "fill_char"
        as the character to fill in the layers
        """

        Grid3D._assert_positive_integer(steps)
        self.offset.y -= steps
        for z in range(self.depth):
            self.grid[z].offset.y -= steps
            for y in range(self.offset.y, self.offset.y+steps):
                row = []
                for x in range(self.width):
                    row.append(Location3D(self.offset.x+x, y, self.offset.z+z,
                                          Location3D.OPEN, fill_char))
                self.grid[z].grid = [row] + self.grid[z].grid

    def expand_down(self, steps: int, fill_char: str = '.') -> None:
        """
        Add "steps" additional layers to the bottom of the grid, using "fill_char"
        as the character to fill in the layers
        """

        Grid3D._assert_positive_integer(steps)
        low_y = self.offset.y + self.height
        for z in range(self.depth):
            for y in range(low_y, low_y+steps):
                row = []
                for x in range(self.width):
                    row.append(Location3D(self.offset.x+x, y, self.offset.z+z,
                                          Location3D.OPEN, fill_char))
                self.grid[z].grid.append(row)

    def expand_left(self, steps: int, fill_char: str = '.') -> None:
        """
        Add "steps" additional layers to the left of the grid, using "fill_char"
        as the character to fill in the layers
        """

        Grid3D._assert_positive_integer(steps)
        self.offset.x -= steps
        for z in range(self.depth):
            self.grid[z].offset.x -= steps
            for y in range(self.height):
                for x in range(self.offset.x, self.offset.x+steps):
                    self.grid[z].grid[y] = [Location3D(x, self.offset.y+y, self.offset.z+z,
                                                       Location3D.OPEN, fill_char)
                                            ] + self.grid[z].grid[y]

    def expand_right(self, steps: int, fill_char: str = '.') -> None:
        """
        Add "steps" additional layers to the right of the grid, using "fill_char"
        as the character to fill in the layers
        """

        Grid3D._assert_positive_integer(steps)
        low_x = self.offset.x + self.width
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(low_x, low_x+steps):
                    self.grid[z].grid[y] = [Location3D(x, self.offset.y+y, self.offset.z+z,
                                                       Location3D.OPEN, fill_char)
                                            ] + self.grid[z].grid[y]

    def expand_in(self, steps: int, fill_char: str = '.') -> None:
        """
        Add "steps" additional layers to the back of the grid, using "fill_char"
        as the character to fill in the layers
        """

        Grid3D._assert_positive_integer(steps)
        self.offset.z -= steps
        for z in range(self.offset.z, self.offset.z+steps):
            new_subgrid = []
            for y in range(self.height):
                new_row = []
                for x in range(self.width):
                    new_row.append(Location3D(self.offset.x+x, self.offset.y+y, z,
                                              Location3D.OPEN, fill_char))
                new_subgrid.append(new_row)
            self.grid = [Grid(new_subgrid, self.offset.copy())] + self.grid

    def expand_out(self, steps: int, fill_char: str = '.') -> None:
        """
        Add "steps" additional layers to the front of the grid, using "fill_char"
        as the character to fill in the layers
        """

        Grid3D._assert_positive_integer(steps)
        low_z = self.offset.z + self.depth
        for z in range(low_z, low_z+steps):
            new_subgrid = []
            for y in range(self.height):
                new_row = []
                for x in range(self.width):
                    new_row.append(Location3D(self.offset.x+x, self.offset.y+y, z,
                                              Location3D.OPEN, fill_char))
                new_subgrid.append(new_row)
            self.grid.append(Grid(new_subgrid, self.offset.copy()))

    def char_positions(self, chars: List[str]) -> Dict[str, List[Point3D]]:
        """
        Return a list of points for each character passed in the "chars" list
        which represents the list of positions in which that character can be
        found on the grid
        """

        positions = {}
        for char in chars:
            positions[char] = []
        for z in range(self.depth):
            rcvd = self.grid[z].char_positions(chars)
            for char in rcvd:
                for i, pt in enumerate(rcvd[char]):
                    rcvd[char][i] = Point3D(pt.x, pt.y, self.offset.z+z)
                positions[char] += rcvd[char]
        return positions
