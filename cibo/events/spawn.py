"""A spawner that iterates over all the existiting spawn rules, translates them, then
spawns the appropriate entity and amount into the world.
"""

from typing import Any, List

from cibo.events._base_ import Event
from cibo.models.data.item import Item
from cibo.models.data.npc import Npc
from cibo.models.spawn import Spawn, SpawnType


class SpawnEvent(Event):
    """A spawner that iterates over all the existiting spawn rules, translates them,
    then spawns the specified amount of the appropriate entity into the world.
    """

    def _generate_item_model_list(self, spawn: Spawn) -> List[Item]:
        """Queries the items of the given spawn model, that already exist in the
        specified room. If there are less than the amount specified by the rule,
        it creates as many are missing.

        Args:
            spawn (Spawn): The item spawn rule.

        Returns:
            List[Item]: The missing items, as data model instances.
        """

        existing_items = Item.get_by_current_room_id(spawn.room_id)

        return [
            Item(
                item_id=spawn.entity_id,
                spawn_room_id=spawn.room_id,
                current_room_id=spawn.room_id,
            )
            for _item in range(spawn.amount - len(existing_items))
        ]

    def _generate_npc_model_list(self, spawn: Spawn) -> List[Npc]:
        """Queries the NPCs of the given spawn model, that already exist with the
        specified spawn room. If there are less than the amount specified by the rule,
        it creates as many are missing.

        Args:
            spawn (Spawn): The NPC spawn rule.

        Returns:
            List[Npc]: The missing NPCs, as data model instances.
        """

        existing_npcs = Npc.get_by_spawn_room_id(spawn.room_id)

        return [
            Npc(
                npc_id=spawn.entity_id,
                spawn_room_id=spawn.room_id,
                current_room_id=spawn.room_id,
            )
            for _npc in range(spawn.amount - len(existing_npcs))
        ]

    def process(self, _sender: Any = None) -> None:
        for spawn in self._entities.spawns.get_all():
            if spawn.type_ is SpawnType.ITEM:
                Item.bulk_create(self._generate_item_model_list(spawn), batch_size=100)

            if spawn.type_ is SpawnType.NPC:
                Npc.bulk_create(self._generate_npc_model_list(spawn), batch_size=100)
