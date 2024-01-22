"""A Direction is just that-- a direction in which a user or NPC can travel."""

from enum import Enum


class Direction(str, Enum):
    """Available directions of travel between rooms."""

    NORTH = "n"
    SOUTH = "s"
    EAST = "e"
    WEST = "w"
    UP = "u"
    DOWN = "d"

    def __str__(self) -> str:
        return self.value
