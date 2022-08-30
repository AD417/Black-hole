from __future__ import annotations
from .ball import Ball

class BigBall(Ball):
    """
    A larger ball type, 2x as big, but 2x as slow. 
    """
    def __init__(self: BigBall) -> BigBall:
        super().__init__()
        # The color of the ball, for rendering.
        self.color: tuple[int] = (255, 127, 0) # Orange
        # The radius of the ball, in pixels
        self._r *= 2
        # The velocity and velocity vector of the ball.
        self.velocity /= 2
        self.vel.x /= 2
        self.vel.y /= 2

