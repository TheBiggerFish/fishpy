"""
This module provides an extension of Grid which can be expanded in every direction
"""

from ...geometry import Vector2D

from ..location import Location
from .grid import Grid


class ExpandableGrid(Grid):
    """An extension of Grid which can be expanded in every direction"""

    @staticmethod
    def _assert_positive_integer(n:int) -> bool:
        if isinstance(n,int) and n > 0:
            return True
        raise ValueError('Can only expand with positive integers')

    def expand_up(self,steps:int,fill_char:str='.') -> None:
        """
        Add "steps" additional rows to the top of the grid, using "fill_char"
        as the character to fill in the rows
        """

        ExpandableGrid._assert_positive_integer(steps)
        self._offset.y -= steps
        for y in range(self._offset.y,self._offset.y+steps):
            row = []
            for x in range(self.width):
                row.append(Location(self._offset.x+x,y,Location.OPEN,fill_char))
            self.grid = [row] + self.grid

    def expand_down(self,steps:int,fill_char:str='.') -> None:
        """
        Add "steps" additional rows to the bottom of the grid, using "fill_char"
        as the character to fill in the rows
        """

        ExpandableGrid._assert_positive_integer(steps)
        low_y = self._offset.y + self.height
        for y in range(low_y,low_y+steps):
            row = []
            for x in range(self.width):
                row.append(Location(self._offset.x+x,y,Location.OPEN,fill_char))
            self.grid.append(row)

    def expand_left(self,steps:int,fill_char:str='.') -> None:
        """
        Add "steps" additional columns to the left of the grid, using
        "fill_char" as the character to fill in the columns
        """

        ExpandableGrid._assert_positive_integer(steps)
        self._offset.x -= steps
        for y in range(self.height):
            for x in range(self._offset.x,self._offset.x+steps):
                self.grid[y] = [Location(x,self._offset.y+y,Location.OPEN,fill_char)] + self.grid[y]

    def expand_right(self,steps:int,fill_char:str='.') -> None:
        """
        Add "steps" additional columns to the right of the grid, using
        "fill_char" as the character to fill in the columns
        """

        ExpandableGrid._assert_positive_integer(steps)
        low_x = self._offset.x + self.width
        for y in range(self.height):
            for x in range(low_x,low_x+steps):
                self.grid[y] = self.grid[y] + [Location(x,self._offset.y+y,Location.OPEN,fill_char)]

    def shift(self,step:Vector2D) -> None:
        """Translate the entire grid in the direction of the step vector"""

        for pt in self:
            pt.x += step.x
            pt.y += step.y
        self._offset += step
