"""A door is an interactive object that separates two adjoining rooms. They can
commonly be opened and closed. Though some may be locked and need a key, or otherwise
be impassible until certain events are triggered.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


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
