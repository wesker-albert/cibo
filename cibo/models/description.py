"""A Description contains various strings, that are used to describe an entity from
different perspectives and contexts.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EntityDescription:
    """Descriptions of an Npc or Item, depending on context."""

    room: str
    look: str


@dataclass
class RoomDescription:
    """Descriptions of the Room from different perspectives."""

    normal: str
    extra: Optional[str]
    night: Optional[str]
    smell: Optional[str]
    listen: Optional[str]
