from __future__ import annotations
from math import hypot

class Vector():
    """A 2-Dimensional vector used for position, velocity, and physics math."""

    def __init__(self: Vector, x: int | float, y: int | float) -> Vector:
        self.x = x
        self.y = y
    
    def dot_product(self: Vector, other: Vector) -> float:
        return self.x * other.x + self.y * other.y
    
    def get_unit(self: Vector) -> float:
        scale_reduction = 1 / self.magnitude()
        return self * scale_reduction

    def magnitude(self: Vector) -> float:
        return hypot(self.x, self.y)

    def normal(self: Vector) -> Vector:
        return Vector(-self.y, self.x)

    # builtin shenanigans:
    def __add__(self: Vector, other: Vector) -> Vector:
        return Vector(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self: Vector, other: Vector) -> Vector:
        return Vector(
            self.x - other.x,
            self.y - other.y
        )

    def __iadd__(self: Vector, other: Vector) -> None:
        self.x += other.x
        self.y += other.y
        return self
    
    def __isub__(self: Vector, other: Vector) -> None:
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self: Vector, other: int | float) -> Vector:
        if type(other) == Vector: raise NotImplemented
        return Vector(
            self.x * other,
            self.y * other
        )

    def __repr__(self: Vector) -> str:
        return "Vector(%s, %s)" % (self.x, self.y)

    def __str__(self: Vector) -> str:
        return "<%s, %s>" % (self.x, self.y)