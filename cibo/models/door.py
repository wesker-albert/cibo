"""A Door is an interactive object that separates two adjoining rooms. They can
commonly be opened and closed. Though some may be locked and need a key, or otherwise
be impassible until certain events are triggered.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List

from cibo.exceptions import DoorIsClosed, DoorIsLocked, DoorIsOpen


class DoorFlag(str, Enum):
    """States a door or object can be in."""

    OPEN = "open"
    CLOSED = "closed"
    LOCKED = "locked"


@dataclass
class Door:
    """Separates one room from another."""

    name: str
    room_ids: List[int]
    flags: List[DoorFlag]

    @property
    def is_closed(self) -> bool:
        """Check if the door is closed.

        Returns:
            bool: True, if closed.
        """

        return DoorFlag.CLOSED in self.flags

    @property
    def is_open(self) -> bool:
        """Check if the door is open.

        Returns:
            bool: True, if open.
        """

        return DoorFlag.OPEN in self.flags

    @property
    def is_locked(self) -> bool:
        """Check if the door is locked.

        Returns:
            bool: True, if locked.
        """

        return DoorFlag.LOCKED in self.flags

    def raise_status(self) -> None:
        """Raises the current status of the door as an Exception.

        Raises:
            DoorIsClosed: Given door is closed.
            DoorIsOpen: Given door is open.
            DoorIsLocked: Given door is locked.
        """

        if self.is_closed:
            raise DoorIsClosed

        if self.is_open:
            raise DoorIsOpen

        if self.is_locked:
            raise DoorIsLocked

    def close(self) -> None:
        """Close the given door."""

        self.flags.remove(DoorFlag.OPEN)
        self.flags.append(DoorFlag.CLOSED)

    def open_(self) -> None:
        """Open the given door."""

        self.flags.remove(DoorFlag.CLOSED)
        self.flags.append(DoorFlag.OPEN)
