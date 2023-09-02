"""A Room is a space that exists within the world, and which Players and Npcs can
occupy as well as navigate through.
"""

from dataclasses import dataclass
from typing import List, Optional

from cibo.exception import ExitNotFound
from cibo.models.direction import Direction
from cibo.models.flag import RoomFlag


@dataclass
class RoomDescription:
    """Descriptions of the Room from different perspectives."""

    normal: str
    extra: Optional[str]
    night: Optional[str]
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
    flags: List[RoomFlag]

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
