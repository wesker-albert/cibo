"""A Spawn is a rule that is used to manifest items or NPCS into a room, of specific
amounts.

This is a collection of all the spawn rules in the world.
"""
from typing import List

from cibo.entities import Entity
from cibo.entities.items import Items
from cibo.entities.npcs import Npcs
from cibo.models.spawn import Spawn, SpawnType


class Spawns(Entity):
    """All the spawn rules that exist."""

    def __init__(self, spawns_file: str, items: Items, npcs: Npcs):
        self._items = items
        self._npcs = npcs
        self._spawns: List[Spawn] = self._generate_entities(spawns_file)

    def _create_entity_from_dict(self, entity: dict) -> Spawn:
        spawn = entity
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
