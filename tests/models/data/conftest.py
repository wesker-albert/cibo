from os import getenv, remove

from peewee import SqliteDatabase
from pytest import fixture

from cibo.models.data.item import Item
from cibo.models.data.player import Player
from cibo.password import Password


@fixture(scope="session", autouse=True)
def fixture_database():
    # we have to remove the db before populating it again, if it exists
    try:
        remove(getenv("DATABASE_PATH"))

    except FileNotFoundError:
        pass

    database = SqliteDatabase(getenv("DATABASE_PATH"))
    database.connect()
    database.create_tables([Player, Item])

    player = Player(
        name="frank", password=Password().hash_("abc123"), current_room_id=1
    )
    player.save()

    Item(item_id=1, room_id=1).save()
    Item(item_id=1, player=player).save()

    yield
