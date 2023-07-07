"""Player model"""

from peewee import AutoField, CharField, TextField

from cibo.models.database import DatabaseModel


class Player(DatabaseModel):
    """Represents a human-controlled player character"""

    id_ = AutoField()
    name = CharField(max_length=15)
    password = TextField()
