from __future__ import annotations

class Vector():
    """A 2-Dimensional vector used for position, velocity, and physics math."""

    def __init__(self: Vector, x: int | float, y: int | float) -> Vector:
        self.x = x
        self.y = y

    

    # Built in shenanigans: