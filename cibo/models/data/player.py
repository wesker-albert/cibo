"""A Player represents a playable character, which a client logs into and assumes in
order to interact with the world. Player information is persistent, allowing the client
to resume their adventure where they left off.
"""


from typing import Self

from marshmallow import Schema, fields, validate
from peewee import AutoField, CharField, DoesNotExist, IntegerField, TextField

from cibo.exceptions import PlayerNotFound
from cibo.models.data import Model


class Player(Model):
    """Represents a human-controlled player character."""

    id_ = AutoField()
    name = CharField(unique=True)
    password = TextField()
    current_room_id = IntegerField()

    @classmethod
    def get_by_name(cls, name: str) -> Self:
        """Find a player by name, if they already exist.

        Args:
            name (str): The player name to search.

        Returns:
            Self: The player, if one exists with the given name.
        """

        try:
            player: Self = cls.get(cls.name == name)
            return player

        # a Player doesn't exist with the entered name
        except DoesNotExist as ex:
            raise PlayerNotFound from ex


class PlayerSchema(Schema):
    """Schema for the player model."""

    id_ = fields.Int()
    name = fields.Str(
        validate=[validate.Length(min=3, max=15), validate.Regexp("^[a-zA-Z0-9_]*$")]
    )
    password = fields.Str(validate=validate.Length(min=8))
    current_room_id = fields.Int()
