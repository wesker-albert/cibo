"""A Direction is just that-- a direction in which a player or NPC can travel."""

from enum import Enum


class Direction(str, Enum):
    """Available directions of travel between Rooms."""

    NORTH = "n"
    SOUTH = "s"
    EAST = "e"
    WEST = "w"
    UP = "u"
    DOWN = "d"
