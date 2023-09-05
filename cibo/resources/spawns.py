from typing import List, Union

from cibo.exception import SpawnNotFound, SpawnTypeUnknown
from cibo.models.item import Item
from cibo.models.npc import Npc
from cibo.models.spawn import Spawn, SpawnType
from cibo.resources.__resource__ import Resource
from cibo.resources.items import Items
from cibo.resources.npcs import Npcs


class Spawns(Resource):
    def __init__(self, spawns_file: str, items: Items, npcs: Npcs):
        self._items = items
        self._npcs = npcs
        self._spawns: List[Spawn] = self._generate_resources(spawns_file)

    def _create_resource_from_dict(self, resource: dict) -> Spawn:
        spawn = resource
        type_ = SpawnType(spawn["type"])

        return Spawn(
            type_=type_,
            entity_id=spawn["entity_id"],
            room_id=spawn["room_id"],
            amount=spawn["amount"],
        )

    def _get_entity_by_id(self, type_: SpawnType, id_: int) -> Union[Item, Npc]:
        if type_ is SpawnType.ITEM:
            return self._items.get_by_id(id_)

        if type_ is SpawnType.NPC:
            return self._npcs.get_by_id(id_)

        raise SpawnTypeUnknown

    def get_by_room_id(self, id_: int) -> Spawn:
        for spawn in self._spawns:
            if spawn.room_id == id_:
                return spawn

        raise SpawnNotFound

    def get_all(self) -> List[Spawn]:
        return self._spawns
