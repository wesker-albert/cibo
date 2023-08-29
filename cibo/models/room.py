"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from cibo.exception import ExitNotFound


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

    id_: int
    name: str
    # flags: List[Flags]


@dataclass
class Region:
    """A large group of Rooms."""

    id_: int
    name: str
    # flags: List[Flags]


@dataclass
class RoomDescription:
    """Descriptions of the Room from different perspectives."""

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
    """Flags that govern exit behavior."""

    direction: Direction
    id_: int
    description: Optional[str]


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

    def get_exits(self) -> List[str]:
        """Get the text values of the exits for the given Room, in alphabetical order.
        Returns empty if the room has no exits.

        Returns:
            List[str]: The Room exits in str format.
        """

        return sorted([exit_.direction.name.lower() for exit_ in self.exits])

    def get_formatted_exits(self) -> str:
        """Formats the exits into a pretty, stylized string.

        Returns:
            str: The formatted exits.
        """

        exits = self.get_exits()

        # plurality is important...
        if not exits:
            return "[green]Exits:[/] none"

        if len(exits) == 1:
            return f"[green]Exit:[/] {exits[0]}"

        joined_exits = ", ".join([str(exit_) for exit_ in exits])
        return f"[green]Exits:[/] {joined_exits}"

    def get_direction_exit(self, direction: str) -> RoomExit:
        """Returns the Room exit in the direction given, if an exit exists that way.

        Args:
            direction (str): The direction to check.

        Returns:
            Optional[RoomExit]: The exit, if it exists.
        """

        for exit_ in self.exits:
            if (
                direction == exit_.direction.value
                or direction == exit_.direction.name.lower()
            ):
                return exit_

        raise ExitNotFound
