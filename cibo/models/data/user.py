"""A User represents a playable character, which a client logs into and assumes in
order to interact with the world. User information is persistent, allowing the client
to resume their adventure where they left off.
"""


from typing import Self

from marshmallow import Schema, fields, validate
from peewee import AutoField, CharField, DoesNotExist, IntegerField, TextField

from cibo.exceptions import UserNotFound
from cibo.models.data._base_ import Model


class User(Model):
    """Represents a human-controlled user character."""

    id_ = AutoField()
    name = CharField(unique=True)
    password = TextField()
    current_room_id = IntegerField()

    @classmethod
    def get_by_name(cls, name: str) -> Self:
        """Find a user by name, if they already exist.

        Args:
            name (str): The user name to search.

        Returns:
            Self: The user, if one exists with the given name.
        """

        try:
            user: Self = cls.get(cls.name == name)
            return user

        # a User doesn't exist with the entered name
        except DoesNotExist as ex:
            raise UserNotFound from ex


class UserSchema(Schema):
    """Schema for the user model."""

    id_ = fields.Int()
    name = fields.Str(
        validate=[validate.Length(min=3, max=15), validate.Regexp("^[a-zA-Z0-9_]*$")]
    )
    password = fields.Str(validate=validate.Length(min=8))
    current_room_id = fields.Int()
