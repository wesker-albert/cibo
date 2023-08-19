"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a player.
"""


from typing import List, Self

from peewee import AutoField, ForeignKeyField, IntegerField

from cibo.models.data.__model__ import Model
from cibo.models.data.player import Player


class Item(Model):
    id_ = AutoField()
    item_id = IntegerField()
    room_id = IntegerField(null=True)
    player = ForeignKeyField(Player, backref="inventory", null=True)

    @classmethod
    def get_by_room_id(cls, room_id: int) -> List[Self]:
        return [item for item in cls.select() if item.room_id == room_id]
