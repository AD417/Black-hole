from __future__ import annotations
from random import random, randint, choice
from math import sqrt, hypot
from typing import Any

class Ball():
    """
    Generic ball object. 
    """

    def __init__(self: Ball) -> Ball:
        # The color of the ball, for rendering.
        self.color: tuple[int] = (0, 127, 255)
        # The radius of the ball, in pixels
        self._r: float = 25.0
        # The mass of the ball, required for momentum calculations
        self._m = 1.0
        # The position of the ball. 
        self.pos: dict[str, float] = {"x": randint(100, 900), "y": randint(100, 900)}
        # The velocity and velocity vector of the ball.
        self.velocity: int = 500
        # This value is randomly generated such that the velocity vector has constant magnitude but variable direction. 
        x_component = self.velocity * random()
        self.vel: dict[str, float] = {
            "x": x_component * choice([1, -1]), 
            "y": sqrt(self.velocity ** 2 - x_component ** 2) * choice([1, -1])
        }

    def distance_to(self: Ball, other: Ball) -> float:
        return hypot(
            self.pos["x"] - other.pos["x"],
            self.pos["y"] - other.pos["y"]
        )

    def collides_with(self: Ball, other: Ball) -> bool:
        return self.distance_to(other) < self.radius() + other.radius()

    def momentum(self: Ball) -> float:
        """Calculate the momentum of the ball, using p = mv"""
        return self._m * self.velocity

    def move(self: Ball, dt: int) -> None:
        """
        Move the ball, based on the amount of time since the last tick
        :param dt: the amount of time, in milliseconds, that has passed since the last move.
        """
        for key in self.vel:
            self.pos[key] += self.vel[key] * (dt / 1000)
            if abs(self.pos[key] - 500) + self.radius() > 500:
                self.pos[key] = max(min(self.pos[key], 1000 - self.radius()), self.radius())
                self.vel[key] *= -1

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
            "center": (self.pos["x"], self.pos["y"]),
            "radius": self.radius()
        }

    def tick(self: Ball, dt: int) -> None:
        """
        Perform updates for this entity for this frame/tick.
        """
        self.move(dt)