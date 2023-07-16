"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class Direction(str, Enum):
    """Available directions of travel between Rooms."""

    NORTH = "n"
    SOUTH = "s"
    EAST = "e"
    WEST = "w"
    UP = "u"
    DOWN = "d"


@dataclass
class Sector:
    """A subset of Rooms with certain shared behaviors."""

    name: str
    # flags: List[Flags]


@dataclass
class Region:
    """A large group of Rooms."""

    name: str
    # flags: List[Flags]


@dataclass
class RoomDescription:
    """Descriptions of the Room from different perspectives."""

    normal: str
    # extra: Optional[str]
    # night: Optional[str]
    # under: Optional[str]
    # behind: Optional[str]
    # above: Optional[str]
    # smell: Optional[str]
    # listen: Optional[str]


@dataclass
class RoomExit:
    """Flags that govern exit behavior."""

    direction: Direction
    id_: int
    # description: str
    # door: str
    # door_flags: List[Flags]


@dataclass
class Room:
    """Represents a single Room within the world."""

    id_: int
    name: str
    description: RoomDescription
    exits: List[RoomExit]
    # sector: Sector
    # regions: List[Region]
    # flags: List[Flags]
