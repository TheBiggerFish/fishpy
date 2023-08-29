"""This module provides a class for storing and evaluating rectangles"""

from .point2d import Point2D


class Rectangle:
    """This class stores and provides methods for evaluating rectangles"""

    def __init__(self, p1: Point2D, p2: Point2D):
        self._low = Point2D(min(p1.x, p2.x), min(p1.y, p2.y))
        self._high = Point2D(max(p1.x, p2.x), max(p1.y, p2.y))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(low={self._low}, high={self._high})'

    def corners(self) -> tuple[Point2D, Point2D, Point2D, Point2D]:
        """Returns a tuple containing all the corners of the rectangle"""
        return (self._low, Point2D(self._low.x, self._high.y),
                Point2D(self._low.y, self._high.x), self._high)

    def overlap(self, other: 'Rectangle') -> bool:
        """
        Predicate method which returns whether two provided rectangles overlap
        """

        l1, _, _, r1 = self.corners()
        l2, _, _, r2 = other.corners()

        # if rectangle has area 0, no overlap
        if l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
            return False

        # If one rectangle is on left side of other
        if l1.x > r2.x or l2.x > r1.x:
            return False

        # If one rectangle is above other
        if r1.y > l2.y or r2.y > l1.y:
            return False

        return True
