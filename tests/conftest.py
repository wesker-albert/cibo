import logging
from os import getenv
from unittest.mock import Mock

from peewee import SqliteDatabase
from pytest import fixture

from cibo.actions.commands._processor_ import CommandProcessor
from cibo.entities.world import World
from cibo.models.client import Client, ClientLoginState
from cibo.models.data.item import Item as ItemData
from cibo.models.data.npc import Npc as NpcData
from cibo.models.data.player import Player
from cibo.models.description import EntityDescription, RoomDescription
from cibo.models.direction import Direction
from cibo.models.door import Door, DoorFlag
from cibo.models.flag import RoomFlag
from cibo.models.item import Item
from cibo.models.npc import Npc
from cibo.models.region import Region
from cibo.models.room import Room, RoomExit
from cibo.models.sector import Sector
from cibo.models.spawn import Spawn, SpawnType
from cibo.server_config import ServerConfig
from cibo.utils.password import Password


class BaseFactory:
    @fixture(autouse=True)
    def fixture_base(self):
        self.telnet = Mock()
        self.comms = Mock()
        self.server_config = ServerConfig(self.telnet, Mock(), self.comms)
        yield


class DatabaseFactory:
    def give_item_to_player(self, item_id: int, player: Player) -> None:
        item = ItemData.get_by_id(item_id)
        item.player = player
        item.save()

    @fixture(scope="module")
    def _fixture_database(self):
        database = SqliteDatabase(getenv("DATABASE_PATH"))
        tables = (Player, ItemData, NpcData)

        with database.bind_ctx(tables):
            database.create_tables(tables)

            hashed_password = Password().hash_("abcd1234")
            players = [
                {
                    "name": "frank",
                    "password": hashed_password,
                    "current_room_id": 1,
                },
                {
                    "name": "john",
                    "password": hashed_password,
                    "current_room_id": 1,
                },
            ]

            items = [
                {"item_id": 1, "current_room_id": 1},
                {"item_id": 1},
                {"item_id": 2, "current_room_id": 1},
            ]

            npcs = [{"npc_id": 1, "spawn_room_id": 1, "current_room_id": 1}]

            # pylint: disable=no-value-for-parameter
            with database.atomic():
                Player.insert_many(players).execute()
                ItemData.insert_many(items).execute()
                NpcData.insert_many(npcs).execute()

            yield

            database.drop_tables(tables)
            database.close()


class ClientFactory:
    @fixture(autouse=True)
    def fixture_client(self):
        self.client = Client(
            socket=Mock(),
            address="127.0.0.1",
            encoding="utf-8",
            buffer="",
            last_check=2.5,
            login_state=ClientLoginState.PRE_LOGIN,
            registration=None,
            player=Mock(current_room_id=1),
        )
        self.client.player.name = "frank"
        yield

    @fixture(autouse=True)
    def _fixture_mock_clients(self):
        default_client_params = {
            "login_state": ClientLoginState.LOGGED_IN,
            "player": Mock(current_room_id=1),
            "prompt": "> ",
        }
        self.mock_clients = [
            Mock(**default_client_params),
            Mock(**default_client_params),
        ]
        yield


class CommandProcessorFactory(BaseFactory):
    class MockAction:
        def __init__(self, _server_config):
            pass

        def aliases(self):
            return ["login"]

        def required_args(self):
            return ["name", "password"]

        def process(self, _client, command, args):
            _name = args[0]
            _password = args[1]

            logging.info("Action processed", {"command": command, "args": args})

    @fixture(autouse=True)
    def fixture_command_processor(self):
        self.command_processor = CommandProcessor(self.server_config, [self.MockAction])
        yield


class PasswordFactory:
    @fixture(autouse=True)
    def fixture_password(self):
        self.password = Password()
        self.hashed_password = self.password.hash_("abc123")
        yield


class WorldFactory:
    @fixture(autouse=True)
    def _fixture_world(self):
        self.world = World()
        yield


class MessageFactory:
    @fixture(autouse=True)
    def _fixture_message(self):
        self.default_message_args = {
            "justify": None,
            "style": None,
            "highlight": False,
            "terminal_width": 76,
        }
        yield


class DoorFactory(WorldFactory):
    @fixture(autouse=True)
    def fixture_door(self):
        self.door_closed = Door(
            name="a wooden door", room_ids=[1, 2], flags=[DoorFlag.CLOSED]
        )
        self.door_open = Door(
            name="a wooden door", room_ids=[1, 2], flags=[DoorFlag.OPEN]
        )
        self.door_locked = Door(
            name="a steel security door",
            room_ids=[1, 4],
            flags=[DoorFlag.LOCKED],
        )
        yield


class ItemFactory(WorldFactory):
    @fixture(autouse=True)
    def fixture_item(self):
        self.item = Item(
            id_=1,
            name="a metal fork",
            description=EntityDescription(
                room="glistens in the dirt.",
                look="A pronged, metal eating utensil.",
            ),
            is_stationary=False,
            carry_limit=0,
            weight=0,
        )
        yield


class NpcFactory(WorldFactory):
    @fixture(autouse=True)
    def fixture_npc(self):
        self.npc = Npc(
            id_=1,
            name="a faceless businessman",
            description=EntityDescription(
                room="sits at his desk.",
                look="His face is smooth and amorphis, like putty. He is wearing a suit, tie, and carrying a briefcase. Though he has no eyes, he seems to be aware of your presence.",
            ),
        )
        yield


class RegionFactory(WorldFactory):
    @fixture(autouse=True)
    def _fixture_region(self):
        self.region = Region(
            id_=1,
            name="The Simulation",
            description="It's powered by people, but not in a good way.",
            flags=[],
        )
        yield


class SectorFactory(RegionFactory):
    @fixture(autouse=True)
    def _fixture_sector(self, _fixture_region):
        self.sector = Sector(
            id_=1,
            name="The Backrooms",
            description="A handful of rooms that make you feel uneasy.",
            region=self.region,
            flags=[RoomFlag.INSIDE],
        )
        yield


class RoomFactory(SectorFactory):
    @fixture(autouse=True)
    def fixture_room(self, _fixture_sector):
        self.room = Room(
            id_=1,
            name="A Room Marked #1",
            description=RoomDescription(
                normal="The walls and floor of this room are a bright, sterile white. You feel as if you are inside a simulation.",
                extra=None,
                night=None,
                smell=None,
                listen=None,
            ),
            exits=[
                RoomExit(direction=Direction.NORTH, id_=2, description=None),
                RoomExit(direction=Direction.EAST, id_=3, description=None),
                RoomExit(direction=Direction.SOUTH, id_=4, description=None),
                RoomExit(direction=Direction.WEST, id_=5, description=None),
            ],
            sector=self.sector,
            flags=[],
        )
        yield


class SpawnFactory(WorldFactory):
    @fixture(autouse=True)
    def _fixture_spawn(self):
        self.spawns = [
            Spawn(type_=SpawnType.ITEM, entity_id=1, room_id=2, amount=1),
            Spawn(type_=SpawnType.ITEM, entity_id=2, room_id=1, amount=1),
            Spawn(type_=SpawnType.NPC, entity_id=1, room_id=1, amount=1),
        ]
        yield
