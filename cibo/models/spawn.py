from dataclasses import dataclass
from enum import Enum


class SpawnType(str, Enum):
    ITEM = "item"
    NPC = "npc"


@dataclass
class Spawn:
    type_: SpawnType
    entity_id: int
    room_id: int
    amount: int
