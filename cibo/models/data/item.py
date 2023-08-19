"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a player.
"""


from typing import List, Self

from peewee import AutoField, ForeignKeyField, IntegerField

from cibo.models.data.__model__ import Model
from cibo.models.data.player import Player


class Item(Model):
    """Represents a persisted World Item, that could belong to a Player, located in
    a Room, etc.
    """

    id_ = AutoField()
    item_id = IntegerField()
    room_id = IntegerField(null=True)
    player = ForeignKeyField(Player, backref="inventory", null=True)

    @classmethod
    def get_by_room_id(cls, room_id: int) -> List[Self]:
        """Get any Items that currently persist in the Room with the given ID.

        Args:
            room_id (int): The ID of the Room you want to check.

        Returns:
            List[Self]: The Item(s) that are currently in the room specified, if any.
        """

        return [item for item in cls.select() if item.room_id == room_id]