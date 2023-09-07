"""A Spawn is a rule that is used to manifest Items or NPCS into a room, of specific
amounts.
"""

from dataclasses import dataclass
from enum import Enum


class SpawnType(str, Enum):
    """The type of Spawn to create."""

    ITEM = "item"
    NPC = "npc"


@dataclass
class Spawn:
    """Represents an Item or NPC spawning rule."""

    type_: SpawnType
    entity_id: int
    room_id: int
    amount: int
