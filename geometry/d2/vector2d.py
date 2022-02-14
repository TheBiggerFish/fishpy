"""This module provides a class for storing vectors on an x-y plane"""

from math import atan, cos, degrees, radians, sin

from ..point import Point


class Vector2D(Point):
    """Class for storing vectors on an 2-dimensional plane"""

    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def cross(self, other: 'Vector2D') -> float:
        """Returns the cross product of self and other"""
        return (self.x*other.y) - (self.y*other.x)

    def dot(self, other: 'Vector2D') -> float:
        """Returns the dot product of self and other"""
        return (self.x*other.x) + (self.y*other.y)

    def normalize(self) -> 'Vector2D':
        """Normalize self, setting self to have a magnitude of 1"""
        return self / self.magnitude()

    def rotate(self, degree: float) -> 'Vector2D':
        """Create a new vector of magnitude 1, rotated \"degree\" degrees"""
        return Vector2D.from_vel(self.angle()+degree, 1)

    def area(self) -> float:
        """Returns the area created by self"""
        return self.x*self.y

    @staticmethod
    def from_vel(angle: float, step: float):
        """Create a new vector from an angle (radians) and a magnitude"""
        return Vector2D(step*cos(angle), step*sin(angle))

    @staticmethod
    def from_vel_degree(degree: float, step: float) -> 'Vector2D':
        """Create a new vector from an angle (degrees) and a magnitude"""
        return Vector2D.from_vel(radians(degree), step)

    @staticmethod
    def from_point(point: Point) -> 'Vector2D':
        """Create a new vector from a point"""
        return Vector2D(point.x, point.y)

    def angle(self) -> float:
        """Returns the angle of self"""

        if self.x == 0:
            if self.y == 0:
                raise ValueError('Zero vector (0,0) does not have an angle')
            return 90.0 if self.y > 0 else 270.0
        return degrees(atan(self.y/self.x)) + (180 if self.x < 0 else 360 if self.y < 0 else 0)


UP = Vector2D(0, 1)
DOWN = Vector2D(0, -1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)
