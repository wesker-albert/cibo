"""An item is an in-game piece of inventory, that can be picked up, carried, and
often used by a player.
"""

from dataclasses import dataclass

from peewee import AutoField, ForeignKeyField, IntegerField

from cibo.models.__model__ import Model
from cibo.models.player import Player


@dataclass
class Item:
    """Represents an interactive item."""

    id_: int
    name: str
    description: str
    is_stationary: bool
    carry_limit: int
    weight: int


class PlayerItem(Model):
    id_ = AutoField()
    item_id = IntegerField()
    room_id = IntegerField()
    player = ForeignKeyField(Player, backref="inventory")
