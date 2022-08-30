from __future__ import annotations
from .ball import Ball
from pygame import mouse
from pygame.math import Vector2

class Playerball(Ball):
    """
    Balls created by the player on click.
    They have variable radius, abide by gravity, and have different rules based on how recently they were created. 
    """
    def __init__(self: Playerball, x: int, y: int) -> Playerball:
        super().__init__()
        # The circle MUST start out with a size of 0.
        self._r: float = 0
        # The color of the ball. Off-purple. 
        self.color = (127, 0, 127)
        # Whether or not this ball grows currently. These balls are initialized on a click, 
        # and only grow while the mouse is held down, so the initial value is true. 
        self.is_growing: bool = True
        # The speed of growth, in change in radius per second. 
        self.grow_speed: int = 100
        # The vertical acceleration of the ball in px/s^2. 
        self.gravity: float = 735 # Random guesses. 75 * g feels good.
        # The positon of the ball. Follows the position of the mouse, which is passed to this as an xy parameter.
        self.pos: Vector2 = Vector2(x, y)
        self.vel: Vector2 = Vector2(0, 0)

    def follow_mouse(self: Playerball) -> None:
        self.pos: Vector2 = Vector2(*mouse.get_pos())

    def increase_radius(self: Playerball, dt: float) -> None:
        self._r += self.grow_speed * dt / 1000
        # If the ball's growth has hit a wall...
        if abs(self.pos.x - 500) + self.radius() > 500 or abs(self.pos.y - 500) + self.radius() > 500:
            # Then immediately stop growing. 
            self.is_growing = False

    def move(self: Playerball, dt: float) -> None:
        if self.pos.y != 1000 - self.radius():
            self.vel.y += self.gravity * dt / 1000
            self.pos.y = min(self.pos.y + self.vel.y * dt / 1000, 1000 - self.radius())
        else:
            self.vel.y = 0
        
        if abs(self.pos.x - 500) + self.radius() > 500:
            self.pos.x = max(min(self.pos.x, 1000 - self.radius()), self.radius())
            self.vel.x *= -1

    def onmouseup(self: Playerball) -> None:
        self.is_growing = False

    def tick(self: Playerball, dt: float) -> None:
        if self.is_growing:
            self.follow_mouse()
            self.increase_radius(dt)
        else:
            self.move(dt)