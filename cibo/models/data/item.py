"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a user.
"""


from typing import List, Self

from peewee import AutoField, ForeignKeyField, IntegerField

from cibo.models.data._base_ import Model
from cibo.models.data.user import User


class Item(Model):
    """Represents a persisted world item, that could belong to a user, located in
    a room, etc.
    """

    id_ = AutoField()
    item_id = IntegerField()
    spawn_room_id = IntegerField(null=True)
    current_room_id = IntegerField(null=True)
    user = ForeignKeyField(User, backref="inventory", null=True)

    @classmethod
    def get_by_current_room_id(cls, room_id: int) -> List[Self]:
        """Get any items that currently persist in the room with the given ID.

        Args:
            room_id (int): The ID of the room you want to check.

        Returns:
            List[Self]: The item(s) that are currently in the room specified, if any.
        """

        return [item for item in cls.select() if item.current_room_id == room_id]
