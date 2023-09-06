from typing import List, Self

from peewee import AutoField, IntegerField

from cibo.models.data.__model__ import Model


class Npc(Model):
    id_ = AutoField()
    npc_id = IntegerField()
    spawn_room_id = IntegerField()
    current_room_id = IntegerField(null=True)

    @classmethod
    def get_by_spawn_room_id(cls, room_id: int) -> List[Self]:
        return [npc for npc in cls.select() if npc.spawn_room_id == room_id]

    @classmethod
    def get_by_current_room_id(cls, room_id: int) -> List[Self]:
        return [npc for npc in cls.select() if npc.current_room_id == room_id]
