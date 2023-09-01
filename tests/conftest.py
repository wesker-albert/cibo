import logging
from os import getenv
from unittest.mock import Mock

from peewee import SqliteDatabase
from pytest import fixture

from cibo.actions.commands.close import Close
from cibo.actions.commands.drop import Drop
from cibo.actions.commands.exits import Exits
from cibo.actions.commands.finalize import Finalize
from cibo.actions.commands.get import Get
from cibo.actions.commands.inventory import Inventory
from cibo.actions.commands.login import Login
from cibo.actions.commands.logout import Logout
from cibo.actions.commands.open import Open
from cibo.actions.commands.quit import Quit
from cibo.actions.commands.register import Register
from cibo.actions.commands.say import Say
from cibo.actions.connect import Connect
from cibo.actions.disconnect import Disconnect
from cibo.actions.error import Error
from cibo.actions.prompt import Prompt
from cibo.client import Client, ClientLoginState
from cibo.command import CommandProcessor
from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.models.data.item import Item
from cibo.models.data.player import Player
from cibo.models.door import Door, DoorFlag
from cibo.models.room import Direction, Room, RoomDescription, RoomExit
from cibo.output import Output
from cibo.password import Password
from cibo.resources.world import World


class BaseFactory:
    @fixture(autouse=True)
    def fixture_base(self):
        self.telnet = Mock()
        self.output = Mock()
        yield


class DatabaseFactory:
    def give_item_to_player(self, item_id: int, player: Player) -> None:
        item = Item.get_by_id(item_id)
        item.player = player
        item.save()

    @fixture(scope="module")
    def _fixture_database(self):
        database = SqliteDatabase(getenv("DATABASE_PATH"))
        tables = (Player, Item)

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
                {"item_id": 1, "room_id": 1},
                {"item_id": 1},
                {"item_id": 2, "room_id": 1},
            ]

            # pylint: disable=no-value-for-parameter
            with database.atomic():
                Player.insert_many(players).execute()
                Item.insert_many(items).execute()

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
        def __init__(self, _telnet, _world, _output):
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
        self.command_processor = CommandProcessor(
            self.telnet, Mock(), self.output, [self.MockAction]
        )
        yield


class OutputFactory(BaseFactory, ClientFactory):
    @fixture(autouse=True)
    def fixture_output(self):
        self.output = Output(self.telnet)
        yield


class PasswordFactory:
    @fixture(autouse=True)
    def fixture_password(self):
        self.password = Password()
        self.hashed_password = self.password.hash_("abc123")
        yield


class WorldFactory:
    @fixture(autouse=True)
    def fixture_world(self):
        self.world = World()
        yield


class DoorFactory:
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


class RoomFactory:
    @fixture(autouse=True)
    def fixture_room(self):
        self.room = Room(
            id_=1,
            name="A Room Marked #1",
            description=RoomDescription(
                normal="The walls and floor of this room are a bright, sterile white. You feel as if you are inside a simulation.",
                extra=None,
                night=None,
                under=None,
                behind=None,
                above=None,
                smell=None,
                listen=None,
            ),
            exits=[
                RoomExit(direction=Direction.NORTH, id_=2, description=None),
                RoomExit(direction=Direction.EAST, id_=3, description=None),
                RoomExit(direction=Direction.SOUTH, id_=4, description=None),
                RoomExit(direction=Direction.WEST, id_=5, description=None),
            ],
        )
        yield


class ConnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect_event(self):
        self.connect = ConnectEvent(self.telnet, Mock(), self.output)
        yield


class DisconnectEventFactory(BaseFactory, ClientFactory):
    @fixture(autouse=True)
    def fixture_disconnect_event(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.disconnect = DisconnectEvent(self.telnet, Mock(), self.output)
        yield


class InputEventFactory(CommandProcessorFactory, ClientFactory):
    @fixture(autouse=True)
    def fixture_input_event(self):
        self.input = InputEvent(
            self.telnet, Mock(), self.output, self.command_processor
        )
        yield


class ActionFactory(ClientFactory, WorldFactory):
    @fixture
    def _fixture_action(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.world = World()
        yield


class ConnectActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_connect(self, _fixture_action):
        self.connect = Connect(self.telnet, Mock(), self.output)
        yield


class DisconnectActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_disconnect(self, _fixture_action):
        self.disconnect = Disconnect(self.telnet, Mock(), self.output)
        yield


class ErrorActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_error(self, _fixture_action):
        self.error = Error(self.telnet, Mock(), self.output)
        yield


class PromptActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_prompt(self, _fixture_action):
        self.prompt = Prompt(self.telnet, Mock(), self.output)
        yield


class CloseActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_close(self, _fixture_action):
        self.close = Close(self.telnet, self.world, self.output)
        yield


class OpenActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_open(self, _fixture_action):
        self.open = Open(self.telnet, self.world, self.output)
        yield


class ExitsActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_exits(self, _fixture_action):
        self.exits = Exits(self.telnet, self.world, self.output)
        yield


class SayActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_say(self, _fixture_action):
        self.say = Say(self.telnet, self.world, self.output)
        yield


class QuitActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_quit(self, _fixture_action):
        self.quit = Quit(self.telnet, self.world, self.output)
        yield


class LogoutActionFactory(BaseFactory, ActionFactory):
    @fixture(autouse=True)
    def fixture_logout(self, _fixture_action):
        self.logout = Logout(self.telnet, self.world, self.output)
        yield


class RegisterActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_register(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.register = Register(self.telnet, self.world, self.output)
        yield


class FinalizeActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_finalize(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.client.registration = Player()
        self.finalize = Finalize(self.telnet, self.world, self.output)
        yield


class LoginActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_login(self, _fixture_action):
        self.client.login_state = ClientLoginState.PRE_LOGIN
        self.login = Login(self.telnet, self.world, self.output)
        yield


class InventoryActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_inventory(self, _fixture_action):
        self.inventory = Inventory(self.telnet, self.world, self.output)
        yield


class DropActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_drop(self, _fixture_action):
        self.drop = Drop(self.telnet, self.world, self.output)
        yield


class GetActionFactory(BaseFactory, ActionFactory, DatabaseFactory):
    @fixture(autouse=True)
    def fixture_get(self, _fixture_action):
        self.get = Get(self.telnet, self.world, self.output)
        yield
