from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Direction(str, Enum):
    """Available directions of travel between rooms"""

    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"


@dataclass
class Sector:
    """A subset of rooms with certain shared behaviors"""

    name: str
    # flags: List[Flags]


@dataclass
class Region:
    """A large group of rooms"""

    name: str
    # flags: List[Flags]


@dataclass
class RoomDescription:
    """Descriptions of the room from different perspectives"""

    normal: str
    extra: Optional[str]
    night: Optional[str]
    under: Optional[str]
    behind: Optional[str]
    above: Optional[str]
    smell: Optional[str]
    listen: Optional[str]


@dataclass
class RoomExit:
    """Flags that govern exit behavior"""

    direction: Direction
    to_: int
    description: str
    # door: str
    # door_flags: List[Flags]


@dataclass
class Room:
    """Represents a single room within the world"""

    id_: int
    name: str
    description: RoomDescription
    exits: List[RoomExit]
    sector: Sector
    regions: List[Region]
    # flags: List[Flags]
