from peewee import AutoField, IntegerField

from cibo.models.data.__model__ import Model


class Npc(Model):
    id_ = AutoField()
    spawn_room_id = IntegerField()
    current_room_id = IntegerField(null=True)
