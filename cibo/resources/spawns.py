"""A Spawn is a rule that is used to manifest items or NPCS into a room, of specific
amounts.

This is a collection of all the spawn rules in the world.
"""
from typing import List

from cibo.models.spawn import Spawn, SpawnType
from cibo.resources.__resource__ import Resource
from cibo.resources.items import Items
from cibo.resources.npcs import Npcs


class Spawns(Resource):
    """All the spawn rules that exist."""

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
        """Get all the spawn rules.

        Returns:
            List[Spawn]: All existing spawn rules.
        """

        return self._spawns
