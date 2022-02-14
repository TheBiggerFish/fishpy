"""This module provides a class to represent moving physics objects"""

from math import atan2

from ..geometry import Point2D, Vector2D


class MovingObject:
    """This class is used to represent objects with movement physics"""

    def __init__(self, position: Point2D = Point2D(0, 0),
                 velocity: Vector2D = Vector2D(0, 0),
                 acceleration: Vector2D = Vector2D(0, 0),
                 update_position_first: bool = True):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self._update_position_first = update_position_first

    def __repr__(self):
        return (f'{self.__class__.__name__}(pos={self.position},'
                f'vel={self.velocity},acc={self.acceleration})')

    @property
    def speed(self) -> float:
        """Represents the speed of the object in units per step"""
        return self.velocity.magnitude()

    @property
    def direction(self) -> float:
        """Represents the direction of the object in radians"""
        return atan2(self.velocity.y, self.velocity.x)

    def step(self, count: int = 1) -> None:
        """Step forward 'count' units of time, updating position and velocity"""

        for _ in range(count):
            if self._update_position_first:
                self.position += self.velocity
                self.velocity += self.acceleration
            else:
                self.velocity += self.acceleration
                self.position += self.velocity
