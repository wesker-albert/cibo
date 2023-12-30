"""A Description contains various strings, that are used to describe an entity from
different perspectives and contexts.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EntityDescription:
    """Descriptions of an NPC or item, depending on context."""

    room: str
    look: str


@dataclass
class RoomDescription:
    """Descriptions of the room from different perspectives."""

    normal: str
    extra: Optional[str]
    night: Optional[str]
    smell: Optional[str]
    listen: Optional[str]
