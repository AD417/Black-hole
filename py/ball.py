from __future__ import annotations
from random import random, randint, choice
from math import sqrt, hypot
from typing import Any
from .vector import Vector

class Ball():
    """
    Generic ball object. 
    """

    def __init__(self: Ball) -> Ball:
        # The color of the ball, for rendering.
        self.color: tuple[int] = (0, 127, 255)
        # The radius of the ball, in pixels
        self._r: float = 25.0
        # The density of the ball, required for momentum calculations
        self._d = 1.0
        # The position of the ball. 
        self.pos: Vector = Vector(randint(100, 900), randint(100, 900))
        # The velocity and velocity vector of the ball.
        self.velocity: int = 500
        # This value is randomly generated such that the velocity vector has constant magnitude but variable direction. 
        x_component = self.velocity * random()
        self.vel: Vector = Vector(
            x_component * choice([1, -1]), 
            sqrt(self.velocity ** 2 - x_component ** 2) * choice([1, -1])
        )

    def distance_to(self: Ball, other: Ball) -> float:
        return (self.pos - other.pos).magnitude()

    def collides_with(self: Ball, other: Ball) -> bool:
        return self.distance_to(other) < self.radius() + other.radius()

    def mass(self: Ball) -> float:
        """Calculate the mass of the ball, given the area and density of the ball"""
        return self.radius() ** 2 * self._d

    def momentum(self: Ball) -> float:
        """Calculate the momentum of the ball, using p = mv"""
        return self.mass() * self.velocity

    def move(self: Ball, dt: float) -> None:
        """
        Move the ball, based on the amount of time since the last tick
        :param dt: the amount of time, in milliseconds, that has passed since the last move
        """
        self.pos += self.vel * (dt / 1000)
        if abs(self.pos.x - 500) + self.radius() > 500:
            self.pos.x = max(min(self.pos.x, 1000 - self.radius()), self.radius())
            self.vel.x *= -1
        if abs(self.pos.y - 500) + self.radius() > 500:
            self.pos.y = max(min(self.pos.y, 1000 - self.radius()), self.radius())
            self.vel.y *= -1
    
    def process_collision_with(self: Ball, other: Ball) -> None:
        """
        Compute the outcome of 2 balls that have collided with each other. 
        """
        self.resolve_intersection_with(other)
        self.resolve_velocity_with(other)

    def radius(self: Ball) -> int:
        """Get the current radius of the ball"""
        return self._r

    def render(self: Ball) -> dict[str, Any]:
        """
        Produce data required for the rendering of the ball.
        :return: a kwarg dictionary containing values important for Pygame rendering.
        """
        return {
            "color": self.color,
            "center": (self.pos.x, self.pos.y),
            "radius": self.radius()
        }

    def resolve_intersection_with(self: Ball, other: Ball) -> None:
        """
        Displace 2 balls that hit each other such that they are no longer intersecting. 
        Credit for this goes to OneLoneCoder, https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_Balls1.cpp 
        """

        distance = self.distance_to(other)

        overlap = 0.5 * (distance - self.radius() - other.radius())

        self.pos -= (self.pos - other.pos) * (overlap / distance)
        other.pos += (self.pos - other.pos) * (overlap / distance)


    
    def resolve_velocity_with(self: Ball, other: Ball) -> None:
        """
        Compute the resulting velocities of 2 balls that hit each other. 
        Credit for this goes to OneLoneCoder, https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_Balls1.cpp 
        """

        normal_position_vector: Vector = (self.pos - other.pos).get_unit()
        normal_velocity_vector: Vector = (self.vel - other.vel).get_unit()

        # I could not determine what this represents just by reading the code. 
        # Best guess is something related to some kind of momentum factor. 
        magic_number: float = normal_position_vector.dot_product(normal_velocity_vector) / (self.mass() + other.mass())

        self.vel -= normal_position_vector * magic_number * other.mass()
        other.vel -= normal_position_vector * magic_number * self.mass()

    def tick(self: Ball, dt: float) -> None:
        """
        Perform updates for this entity for this frame/tick.
        """
        self.move(dt)