"""A Character represents a playable character, which a user logs into and assumes in
order to interact with the world. Character information is persistent, allowing the
user to resume their adventure where they left off.
"""


from typing import Self

from marshmallow import Schema, fields, validate
from peewee import AutoField, CharField, DoesNotExist, ForeignKeyField, IntegerField

from cibo.exceptions import CharacterNotFound
from cibo.models.data import Model
from cibo.models.data.user import User, UserSchema


class Character(Model):
    """Represents a human-controlled user character."""

    id_ = AutoField()
    user = ForeignKeyField(User, backref="character")
    name = CharField(unique=True)
    current_room_id = IntegerField()

    @classmethod
    def get_by_name(cls, name: str) -> Self:
        """Find a character by name, if they already exist.

        Args:
            name (str): The character name to search.

        Returns:
            Self: The character, if one exists with the given name.
        """

        try:
            character: Self = cls.get(cls.name == name)
            return character

        # a User doesn't exist with the entered name
        except DoesNotExist as ex:
            raise CharacterNotFound from ex


class CharacterSchema(Schema):
    """Schema for the character model."""

    id_ = fields.Int()
    user = fields.Nested(UserSchema)
    name = fields.Str(
        validate=[validate.Length(min=3, max=15), validate.Regexp("^[a-zA-Z0-9_]*$")]
    )
    current_room_id = fields.Int()
