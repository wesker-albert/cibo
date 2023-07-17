"""A Player represents a playable character, which a client logs into and assumes in
order to interact with the world. Player information is persistent, allowing the client
to resume their adventure where they left off.
"""


from marshmallow import Schema, fields, validate
from peewee import AutoField, CharField, IntegerField, TextField

from cibo.models.__model__ import Model


class Player(Model):
    """Represents a human-controlled player character."""

    id_ = AutoField()
    name = CharField(unique=True)
    password = TextField()
    current_room_id = IntegerField()


class PlayerSchema(Schema):
    """Schema for the Player model."""

    id_ = fields.Int()
    name = fields.Str(
        validate=[validate.Length(min=3, max=15), validate.Regexp("^[a-zA-Z0-9_]*$")]
    )
    password = fields.Str(validate=validate.Length(min=8))
    current_room_id = fields.Int()
