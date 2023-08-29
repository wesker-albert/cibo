import logging
from os import getenv
from unittest.mock import Mock

from pytest import fixture

from cibo.actions.commands.close import Close
from cibo.actions.connect import Connect
from cibo.actions.disconnect import Disconnect
from cibo.actions.error import Error
from cibo.actions.prompt import Prompt
from cibo.client import Client, ClientLoginState
from cibo.command import CommandProcessor
from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.models.data.player import Player
from cibo.models.door import Door, DoorFlag
from cibo.models.room import Direction, Room, RoomDescription, RoomExit
from cibo.output import Output
from cibo.password import Password
from cibo.resources.doors import Doors
from cibo.resources.items import Items
from cibo.resources.rooms import Rooms
from cibo.resources.world import World


class BaseFactory:
    @fixture(autouse=True)
    def fixture_base(self):
        self.telnet = Mock()
        self.output = Mock()
        yield


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
            player=Player(),
        )
        yield

    @fixture(autouse=True)
    def fixture_mock_client(self):
        self.mock_client = Mock()
        self.mock_client.login_state = ClientLoginState.PRE_LOGIN
        self.mock_client.player = Player()
        self.mock_client.prompt = "> "
        yield

    @fixture(autouse=True)
    def fixture_mock_client_additional(self):
        self.mock_client_additional = Mock()
        self.mock_client_additional.login_state = ClientLoginState.LOGGED_IN
        self.mock_client_additional.player = Mock(current_room_id=1)
        self.mock_client_additional.prompt = "> "
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


class OutputFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_output(self):
        self.output = Output(self.telnet)
        yield


class ConnectActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect(self):
        self.connect = Connect(self.telnet, Mock(), self.output)
        yield


class DisconnectActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_disconnect(self):
        self.disconnect = Disconnect(self.telnet, Mock(), self.output)
        yield


class ErrorActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_error(self):
        self.error = Error(self.telnet, Mock(), self.output)
        yield


class PromptActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_prompt(self):
        self.prompt = Prompt(self.telnet, Mock(), self.output)
        yield


class CloseActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_close(self):
        self.close = Close(self.telnet, Mock(), self.output)
        yield


class ConnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect_event(self):
        self.connect = ConnectEvent(self.telnet, Mock(), self.output)
        yield


class DisconnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_disconnect_event(self):
        self.disconnect = DisconnectEvent(self.telnet, Mock(), self.output)
        yield


class InputEventFactory(CommandProcessorFactory):
    @fixture(autouse=True)
    def fixture_input_event(self):
        self.input = InputEvent(
            self.telnet, Mock(), self.output, self.command_processor
        )
        yield


class WorldFactory:
    @fixture(autouse=True)
    def fixture_world(self):
        self.world = World()
        self.doors = Doors(getenv("DOORS_PATH", "/cibo/resources/doors.json"))
        self.rooms = Rooms(getenv("ROOMS_PATH", "/cibo/resources/rooms.json"))
        self.items = Items(getenv("ITEMS_PATH", "/cibo/resources/items.json"))
        yield


class DoorFactory:
    @fixture(autouse=True)
    def fixture_door(self):
        self.door_closed = Door(
            name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.CLOSED]
        )
        self.door_open = Door(
            name="small trapdoor", room_ids=[1, 7], flags=[DoorFlag.OPEN]
        )
        self.door_locked = Door(
            name="small trapdoor",
            room_ids=[1, 7],
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
                RoomExit(direction=Direction.UP, id_=6, description=None),
                RoomExit(direction=Direction.DOWN, id_=7, description=None),
            ],
        )
        yield


class PasswordFactory:
    @fixture(autouse=True)
    def fixture_password(self):
        self.password = Password()
        self.hashed_password = self.password.hash_("abc123")
        yield
