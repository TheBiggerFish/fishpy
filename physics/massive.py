"""
This module provides a class to represent moving physics objects with mass
"""

import math
from typing import Tuple

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

    def elastic_collision(self, other: 'MassiveObject') -> Tuple[Vector2D, Vector2D]:
        """Perform physics on ball if in contact with another ball"""

        m1 = self.mass
        s1 = self.speed
        d1 = self.direction

        m2 = other.mass
        s2 = other.speed
        d2 = other.direction

        # phi represents direction from position of self to position of other
        offset = self.position - other.position
        phi = math.atan2(offset.y, offset.x)

        # Equations of elastic collisions in a 2-dimensional space
        # https://williamecraver.wixsite.com/elastic-equations

        v1 = ((s1 * math.cos(d1 - phi) * (m1 - m2)) +
              (2 * m2 * s2 * math.cos(d2 - phi))) / (m1 + m2)
        v1Fx = (v1 * math.cos(phi)) + \
            (s1 * math.sin(d1 - phi) * math.cos(phi + (math.pi/2)))
        v1Fy = (v1 * math.sin(phi)) + \
            (s1 * math.sin(d1 - phi) * math.sin(phi + (math.pi/2)))
        v1F = Point2D(v1Fx, v1Fy)

        v2 = ((s2 * math.cos(d2 - phi) * (m2 - m1)) +
              (2 * m1 * s1 * math.cos(d1 - phi))) / (m2 + m1)
        v2Fx = (v2 * math.cos(phi)) + \
            (s2 * math.sin(d2 - phi) * math.cos(phi + (math.pi/2)))
        v2Fy = (v2 * math.sin(phi)) + \
            (s2 * math.sin(d2 - phi) * math.sin(phi + (math.pi/2)))
        v2F = Point2D(v2Fx, v2Fy)

        return v1F, v2F
