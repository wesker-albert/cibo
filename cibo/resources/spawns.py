from typing import List

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

    def get_all(self) -> List[Spawn]:
        return self._spawns
