"""A User represents an account that a client can log into. They then can do things
such as create playable characters associated with the user account.
"""


from typing import Self

from marshmallow import Schema, fields, validate
from peewee import AutoField, CharField, DoesNotExist, TextField

from cibo.exceptions import UserNotFound
from cibo.models.data._base_ import Model


class User(Model):
    """Represents a user account."""

    id_ = AutoField()
    name = CharField(unique=True)
    password = TextField()

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
