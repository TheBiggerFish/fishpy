"""
This module provides an extension of Grid which can be expanded in every direction
"""

from typing import Optional

from ...geometry import LatticePoint
from ..location import Location
from .grid import Grid


class ExpandableGrid(Grid):
    """An extension of Grid which can be expanded in every direction"""

    @staticmethod
    def _assert_positive_integer(n:int) -> bool:
        if isinstance(n,int) and n > 0:
            return True
        raise ValueError('Can only expand with positive integers')

    def expand_up(self,steps:int,fill_char:str='.') -> 'ExpandableGrid':
        """
        Add "steps" additional rows to the top of the grid, using "fill_char"
        as the character to fill in the rows
        """

        if steps == 0:
            return self

        ExpandableGrid._assert_positive_integer(steps)
        self.offset.y -= steps
        for y in range(self.offset.y,self.offset.y+steps):
            row = []
            for x in range(self.width):
                row.append(Location(self.offset.x+x,y,Location.OPEN,fill_char))
            self.grid = [row] + self.grid
        return self

    def expand_down(self,steps:int,fill_char:str='.') -> 'ExpandableGrid':
        """
        Add "steps" additional rows to the bottom of the grid, using "fill_char"
        as the character to fill in the rows
        """

        if steps == 0:
            return self

        ExpandableGrid._assert_positive_integer(steps)
        low_y = self.offset.y + self.height
        for y in range(low_y,low_y+steps):
            row = []
            for x in range(self.width):
                row.append(Location(self.offset.x+x,y,Location.OPEN,fill_char))
            self.grid.append(row)
        return self

    def expand_left(self,steps:int,fill_char:str='.') -> 'ExpandableGrid':
        """
        Add "steps" additional columns to the left of the grid, using
        "fill_char" as the character to fill in the columns
        """

        if steps == 0:
            return self

        ExpandableGrid._assert_positive_integer(steps)
        self.offset.x -= steps
        for y in range(self.height):
            for x in range(self.offset.x,self.offset.x+steps):
                self.grid[y] = [Location(x,self.offset.y+y,Location.OPEN,fill_char)] + self.grid[y]
        return self

    def expand_right(self,steps:int,fill_char:str='.') -> 'ExpandableGrid':
        """
        Add "steps" additional columns to the right of the grid, using
        "fill_char" as the character to fill in the columns
        """

        if steps == 0:
            return self

        ExpandableGrid._assert_positive_integer(steps)
        low_x = self.offset.x + self.width
        for y in range(self.height):
            for x in range(low_x,low_x+steps):
                self.grid[y] = self.grid[y] + [Location(x,self.offset.y+y,Location.OPEN,fill_char)]
        return self

    def mirror_x(self,x_value:Optional[int]=None) -> 'ExpandableGrid':
        """
        Mirror the entire grid around the x-value provided
        If no x-value provided, mirror within current bounds
        """

        low_bound,high_bound = self.bounds
        if x_value is None:
            newoffset = self.offset
        else:
            newoffset = LatticePoint(2*x_value-high_bound.x+1,low_bound.y)
        new_grid:ExpandableGrid = ExpandableGrid.blank(self.size,newoffset)

        for y in range(low_bound.y,high_bound.y):
            for x in range(low_bound.x,high_bound.x):
                loc = self[LatticePoint(x,y)].copy()
                if x_value is None:
                    new_pos = LatticePoint(low_bound.x+high_bound.x-x-1,y)
                else:
                    new_pos = LatticePoint(2*x_value-x,y)
                loc.x,loc.y = new_pos.x,new_pos.y
                new_grid[new_pos] = loc
        self.offset = newoffset
        self.grid = new_grid.grid
        return self

    def mirror_y(self,y_value:Optional[int]=None) -> 'ExpandableGrid':
        """
        Mirror the entire grid around the y-value provided
        If no y-value provided, mirror within current bounds
        """

        low_bound,high_bound = self.bounds
        if y_value is None:
            newoffset = self.offset
        else:
            newoffset = LatticePoint(low_bound.x,2*y_value-high_bound.y+1)
        new_grid:ExpandableGrid = ExpandableGrid.blank(self.size,newoffset)

        for y in range(low_bound.y,high_bound.y):
            for x in range(low_bound.x,high_bound.x):
                loc = self[LatticePoint(x,y)].copy()
                if y_value is None:
                    new_pos = LatticePoint(x,low_bound.y+high_bound.y-1-y)
                else:
                    new_pos = LatticePoint(x,2*y_value-y)
                loc.x,loc.y = new_pos.x,new_pos.y
                new_grid[new_pos] = loc
        self.offset = newoffset
        self.grid = new_grid.grid
        return self

    def overlay(self,other:'ExpandableGrid',empty_char:str='.'):
        self_bounds,other_bounds = self.bounds,other.bounds

        new_grid = self.copy()
        new_grid = new_grid.expand_left(max(0,self_bounds[0].x-other_bounds[0].x))
        new_grid = new_grid.expand_down(max(0,other_bounds[1].y-self_bounds[1].y))
        new_grid = new_grid.expand_right(max(0,other_bounds[1].x-self_bounds[1].x))
        new_grid = new_grid.expand_up(max(0,self_bounds[0].y-other_bounds[0].y))

        for loc in other:
            loc:Location
            if loc.rep != empty_char:
                new_grid[loc] = loc
        return new_grid
