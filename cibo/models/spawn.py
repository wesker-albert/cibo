from dataclasses import dataclass
from enum import Enum
from typing import Union

from cibo.models.item import Item
from cibo.models.npc import Npc


class SpawnType(str, Enum):
    ITEM = "item"
    NPC = "npc"


@dataclass
class Spawn:
    type_: SpawnType
    entity: Union[Item, Npc]
    room_id: int
    amount: int
