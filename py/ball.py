from __future__ import annotations
from random import random, randint, choice
from math import sqrt

class Ball():
    """
    Generic ball object. 
    """

    def __init__(self: Ball) -> Ball:
        # The radius of the ball, in pixels
        self._r: int = 1
        # The mass of the ball, required for momentum calculations
        self._m = 1.0
        # The position of the ball. 
        self.pos: dict[str, float] = {"x": randint(100, 900), "y": randint(100, 900)}
        # The velocity and velocity vector of the ball.
        self.velocity: int = 100
        # This value is randomly generated such that the velocity vector has constant magnitude but variable direction. 
        x_component = self.velocity * random()
        self.vel: dict[str, float] = {
            "x": x_component * choice([1, -1]), 
            "y": sqrt(self.velocity ** 2 - x_component ** 2) * choice([1, -1])
        }

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
            if abs(self.pos[key] - 500) > 400:
                self.vel[key] *= -1

    def radius(self: Ball) -> int:
        """Get the radius of the ball"""
        return self._r