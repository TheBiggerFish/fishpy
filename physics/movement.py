"""
This module provides a class to represent moving physics objects 
"""

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

    def step(self) -> None:
        """Step forward one unit of time, updating position and velocity"""

        if self._update_position_first:
            self.position += self.velocity
            self.velocity += self.acceleration
        else:
            self.velocity += self.acceleration
            self.position += self.velocity
