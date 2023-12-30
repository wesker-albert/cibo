"""An NPC is a non-player character, that a player might encounter while exploring
the world. Some NPCs can be interacted with, in varying ways.
"""

from typing import List, Self

from peewee import AutoField, IntegerField

from cibo.models.data.__model__ import Model


class Npc(Model):
    """Represents a non-player character that has been spawned into the world,
    and may be interacted with.
    """

    id_ = AutoField()
    npc_id = IntegerField()
    spawn_room_id = IntegerField()
    current_room_id = IntegerField(null=True)

    @classmethod
    def get_by_spawn_room_id(cls, room_id: int) -> List[Self]:
        """Get any NPCs that are set to spawn in the room with the given ID.

        Args:
            room_id (int): The room ID to check against.

        Returns:
            List[Self]: The NPC(s) with the given spawn room ID, if any.
        """

        return [npc for npc in cls.select() if npc.spawn_room_id == room_id]

    @classmethod
    def get_by_current_room_id(cls, room_id: int) -> List[Self]:
        """Get any NPCs that are currently located in the room with the given ID.

        Args:
            room_id (int): The room ID to check against.

        Returns:
            List[Self]: The NPC(s) currently located in the given room ID, if any.
        """

        return [npc for npc in cls.select() if npc.current_room_id == room_id]
