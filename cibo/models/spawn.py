"""A Spawn is a rule that is used to manifest items or NPCS into a room, of specific
amounts.
"""

from dataclasses import dataclass
from enum import Enum


class SpawnType(str, Enum):
    """The type of spawn to create."""

    ITEM = "item"
    NPC = "npc"


@dataclass
class Spawn:
    """Represents an item or NPC spawning rule."""

    type_: SpawnType
    entity_id: int
    room_id: int
    amount: int
