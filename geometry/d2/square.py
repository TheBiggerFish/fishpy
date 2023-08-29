"""This module provides a class for storing and evaluating squares"""

from .lattice import LatticePoint
from .point2d import Point2D
from .rectangle import Rectangle


class Square(Rectangle):
    """This class stores and provides methods for evaluating squares"""

    def __init__(self, center: Point2D, side: float):
        self.center = center
        self.side = side

        side_offset = Point2D(side/2, side/2)
        if side_offset.is_lattice():
            side_offset = LatticePoint.floor(side_offset)
        super().__init__(center-side_offset, center+side_offset)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(center={self.center}, side={self.side})'
