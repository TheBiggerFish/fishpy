"""
This module provides a class to represent moving physics objects with mass
"""

from ..geometry import Point2D, Vector2D
from .movement import MovingObject


class MassiveObject(MovingObject):
    """This class is used to represent objects with mass and movement physics"""

    def __init__(self, mass: int,
                 position: Point2D = Point2D(0, 0),
                 velocity: Vector2D = Vector2D(0, 0),
                 acceleration: Vector2D = Vector2D(0, 0),
                 update_position_first: bool = True):
        self.mass = mass
        super().__init__(position, velocity, acceleration, update_position_first)

    def __repr__(self):
        return (f'{self.__class__.__name__}(mass={self.mass},pos={self.position},'
                f'vel={self.velocity},acc={self.acceleration})')

    def gravitational_acceleration(self, other: 'MassiveObject',
                                   G: float = 6.674*10**-11) -> Vector2D:
        """Calculate the acceleration due to gravity of self towards other"""

        dist = self.position.euclidean_distance(other.position)
        force = G * self.mass * other.mass / dist**2
        directional_vector = (other.position - self.position).normalize()
        return directional_vector * force / self.mass
