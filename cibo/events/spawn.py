from typing import List

from cibo.events.__event__ import Event
from cibo.models.data.item import Item
from cibo.models.data.npc import Npc
from cibo.models.spawn import Spawn, SpawnType


class SpawnEvent(Event):
    def _generate_item_model_list(self, spawn: Spawn) -> List[Item]:
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
        existing_npcs = Npc.get_by_spawn_room_id(spawn.room_id)

        return [
            Npc(
                npc_id=spawn.entity_id,
                spawn_room_id=spawn.room_id,
                current_room_id=spawn.room_id,
            )
            for _npc in range(spawn.amount - len(existing_npcs))
        ]

    def process(self) -> None:
        for spawn in self._world.spawns.get_all():
            if spawn.type_ is SpawnType.ITEM:
                Item.bulk_create(self._generate_item_model_list(spawn), batch_size=100)

            if spawn.type_ is SpawnType.NPC:
                Npc.bulk_create(self._generate_npc_model_list(spawn), batch_size=100)
