from fishpy.geometry import Point

from ..location import Location
from .grid import Grid


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
