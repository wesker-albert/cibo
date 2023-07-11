"""Player model"""


from marshmallow import Schema, fields, validate
from peewee import AutoField, CharField, TextField

from cibo.helpers.models import field_is_alphanumeric
from cibo.models.database import DatabaseModel


class Player(DatabaseModel):
    """Represents a human-controlled player character."""

    id_ = AutoField()
    name = CharField(unique=True)
    password = TextField()


class PlayerSchema(Schema):
    """Schema for the Player model."""

    id_ = fields.Int()
    name = fields.Str(
        validate=[validate.Length(min=3, max=15), field_is_alphanumeric()]
    )
    password = fields.Str(validate=validate.Length(min=8))
