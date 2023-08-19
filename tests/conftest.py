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
from cibo.models.object.room import Direction, Room, RoomDescription, RoomExit
from cibo.output import Output
from cibo.resources.doors import Doors
from cibo.resources.rooms import Rooms
from cibo.resources.world import World


class BaseFactory:
    @fixture(autouse=True)
    def fixture_base(self) -> None:
        self.telnet = Mock()
        self.output = Mock()
        yield


class ClientFactory:
    @fixture(autouse=True)
    def fixture_client(self) -> Client:
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
    def fixture_mock_client(self) -> Client:
        self.mock_client = Mock()
        self.mock_client.login_state = ClientLoginState.PRE_LOGIN
        self.mock_client.player = Player()
        self.mock_client.prompt = "> "
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
    def fixture_command_processor(self) -> CommandProcessor:
        self.command_processor = CommandProcessor(
            self.telnet, Mock(), self.output, [self.MockAction]
        )
        yield


class OutputFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_output(self) -> Output:
        self.output = Output(self.telnet)
        yield


class ConnectActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect(self) -> Connect:
        self.connect = Connect(self.telnet, Mock(), self.output)
        yield


class DisconnectActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_disconnect(self) -> Disconnect:
        self.disconnect = Disconnect(self.telnet, Mock(), self.output)
        yield


class ErrorActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_error(self) -> Error:
        self.error = Error(self.telnet, Mock(), self.output)
        yield


class PromptActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_prompt(self) -> Prompt:
        self.prompt = Prompt(self.telnet, Mock(), self.output)
        yield


class CloseActionFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_close(self) -> Close:
        self.close = Close(self.telnet, Mock(), self.output)
        yield


class ConnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_connect_event(self) -> ConnectEvent:
        self.connect = ConnectEvent(self.telnet, Mock(), self.output)
        yield


class DisconnectEventFactory(BaseFactory):
    @fixture(autouse=True)
    def fixture_disconnect_event(self) -> DisconnectEvent:
        self.disconnect = DisconnectEvent(self.telnet, Mock(), self.output)
        yield


class InputEventFactory(CommandProcessorFactory):
    @fixture(autouse=True)
    def fixture_input_event(self) -> InputEvent:
        self.input = InputEvent(
            self.telnet, Mock(), self.output, self.command_processor
        )
        yield


class WorldFactory:
    @fixture(autouse=True)
    def fixture_world(self) -> World:
        self.world = World()
        yield

    @fixture(autouse=True)
    def fixture_doors(self) -> Doors:
        self.doors = Doors(getenv("DOORS_PATH", "/cibo/resources/doors.json"))
        yield

    @fixture(autouse=True)
    def fixture_rooms(self) -> Rooms:
        self.rooms = Rooms(getenv("ROOMS_PATH", "/cibo/resources/rooms.json"))
        yield

    @fixture(name="room")
    def fixture_room(self) -> Room:
        yield Room(
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
            spawned_items=[2],
        )
