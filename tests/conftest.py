import logging
from os import getenv
from unittest.mock import Mock

from peewee import SqliteDatabase
from pytest import fixture

from cibo.actions import Connect, Disconnect, Error
from cibo.actions.commands import (
    Close,
    Drop,
    Exits,
    Finalize,
    Get,
    Inventory,
    Login,
    Logout,
    Look,
    Move,
    Open,
    Quit,
    Register,
    Say,
)
from cibo.actions.scheduled import EveryMinute, EverySecond
from cibo.command import CommandProcessor
from cibo.events import ConnectEvent, DisconnectEvent, InputEvent, SpawnEvent
from cibo.models import (
    Client,
    ClientLoginState,
    Direction,
    Door,
    DoorFlag,
    EntityDescription,
    Item,
    Npc,
    Region,
    Room,
    RoomDescription,
    RoomExit,
    RoomFlag,
    Sector,
    Spawn,
    SpawnType,
)
from cibo.models.data import Item as ItemData
from cibo.models.data import Npc as NpcData
from cibo.models.data import Player
from cibo.models.server_config import ServerConfig
from cibo.output import OutputProcessor
from cibo.outputs import Private as OutputPrivate
from cibo.outputs import Region as OutputRegion
from cibo.outputs import Room as OutputRoom
from cibo.outputs import Sector as OutputSector
from cibo.outputs import Server as OutputServer
from cibo.password import Password
from cibo.resources import World


class BaseFactory:
    @fixture(autouse=True)
    def fixture_base(self):
        self.telnet = Mock()
        self.output = Mock()
        self.server_config = ServerConfig(self.telnet, Mock(), self.output)
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
    def fixture_mock_clients(self):
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


class OutputFactory(BaseFactory, ClientFactory, WorldFactory):
    @fixture(autouse=True)
    def fixture_output(self):
        self.output = OutputProcessor(self.telnet, self.world)
        self.private = OutputPrivate(self.telnet, self.world)
        self.room = OutputRoom(self.telnet, self.world)
        self.sector = OutputSector(self.telnet, self.world)
        self.region = OutputRegion(self.telnet, self.world)
        self.server = OutputServer(self.telnet, self.world)
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]
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


class SpawnFactory(WorldFactory):
    @fixture(autouse=True)
    def _fixture_spawn(self):
        self.spawns = [
            Spawn(type_=SpawnType.ITEM, entity_id=1, room_id=2, amount=1),
            Spawn(type_=SpawnType.ITEM, entity_id=2, room_id=1, amount=1),
            Spawn(type_=SpawnType.NPC, entity_id=1, room_id=1, amount=1),
        ]
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


class ConnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect_event(self):
        self.connect = ConnectEvent(self.server_config)
        yield


class DisconnectEventFactory(BaseFactory, ClientFactory):
    @fixture(autouse=True)
    def fixture_disconnect_event(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.disconnect = DisconnectEvent(self.server_config)
        self.default_message_args = {
            "justify": None,
            "style": None,
            "highlight": False,
            "terminal_width": 76,
        }
        yield


class SpawnEventFactory(BaseFactory, WorldFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_spawn_event(self):
        self.server_config = ServerConfig(self.telnet, self.world, self.output)
        self.spawn = SpawnEvent(self.server_config)
        yield


class InputEventFactory(CommandProcessorFactory, ClientFactory):
    @fixture(autouse=True)
    def fixture_input_event(self):
        self.input = InputEvent(self.server_config, self.command_processor)
        self.default_message_args = {
            "justify": None,
            "style": None,
            "highlight": False,
            "terminal_width": 76,
        }
        yield


class ActionFactory(ClientFactory, WorldFactory):
    def get_message_panel(self):
        return self.output.send_to_client.call_args.args[0].message.body

    @fixture
    def _fixture_action(self, _fixture_world):
        self.server_config = ServerConfig(self.telnet, self.world, self.output)
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.default_message_args = {
            "justify": None,
            "style": None,
            "highlight": False,
            "terminal_width": 76,
        }
        yield


class ConnectActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_connect(self, _fixture_action):
        self.connect = Connect(self.server_config)
        yield


class DisconnectActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_disconnect(self, _fixture_action):
        self.disconnect = Disconnect(self.server_config)
        yield


class ErrorActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_error(self, _fixture_action):
        self.error = Error(self.server_config)
        yield


class CloseActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_close(self, _fixture_action):
        self.close = Close(self.server_config)
        yield


class OpenActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_open(self, _fixture_action):
        self.open = Open(self.server_config)
        yield


class MoveActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_move(self, _fixture_action):
        self.telnet.get_connected_clients.return_value = []
        self.move = Move(self.server_config)
        yield


class LookActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_look(self, _fixture_action):
        self.look = Look(self.server_config)
        yield


class ExitsActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_exits(self, _fixture_action):
        self.exits = Exits(self.server_config)
        yield


class SayActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_say(self, _fixture_action):
        self.say = Say(self.server_config)
        yield


class QuitActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_quit(self, _fixture_action):
        self.quit = Quit(self.server_config)
        yield


class LogoutActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_logout(self, _fixture_action):
        self.logout = Logout(self.server_config)
        yield


class RegisterActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_register(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.register = Register(self.server_config)
        yield


class FinalizeActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_finalize(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.client.registration = Player()
        self.finalize = Finalize(self.server_config)
        yield


class LoginActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_login(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.login = Login(self.server_config)
        yield


class InventoryActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_inventory(self, _fixture_action):
        self.inventory = Inventory(self.server_config)
        yield


class DropActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_drop(self, _fixture_action):
        self.drop = Drop(self.server_config)
        yield


class GetActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_get(self, _fixture_action):
        self.get = Get(self.server_config)
        yield


class EveryMinuteActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_every_minute(self, _fixture_action):
        self.every_minute = EveryMinute(self.server_config)
        yield


class EverySecondActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_every_second(self, _fixture_action):
        self.every_second = EverySecond(self.server_config)
        yield
