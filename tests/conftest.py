import logging
from os import getenv
from unittest.mock import Mock

from pytest import fixture

from cibo.actions.connect import Connect
from cibo.actions.disconnect import Disconnect
from cibo.actions.error import Error
from cibo.actions.prompt import Prompt
from cibo.client import Client, ClientLoginState
from cibo.command import CommandProcessor
from cibo.decorator import load_environment_variables
from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.output import Output
from cibo.resources.doors import Doors
from cibo.resources.rooms import Rooms


class BaseFactory:
    @fixture(autouse=True)
    def fixture_base(self) -> None:
        self.telnet = Mock()
        self.output = Mock()


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
            player=None,
        )
        yield

    @fixture(autouse=True)
    def fixture_mock_client(self) -> Client:
        self.mock_client = Mock()
        self.mock_client.login_state = ClientLoginState.PRE_LOGIN
        self.mock_client.player = None
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


@fixture(name="doors")
@load_environment_variables
def fixture_doors() -> Doors:
    return Doors(getenv("DOORS_PATH", "/cibo/resources/doors.json"))


@fixture(name="rooms")
@load_environment_variables
def fixture_rooms() -> Rooms:
    return Rooms(getenv("ROOMS_PATH", "/cibo/resources/rooms.json"))
