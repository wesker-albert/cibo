import logging
from os import getenv
from unittest.mock import Mock

from pytest import fixture

from cibo.client import Client, ClientLoginState
from cibo.command import CommandProcessor
from cibo.decorator import load_environment_variables
from cibo.output import Output
from cibo.resources.doors import Doors
from cibo.resources.rooms import Rooms


@fixture(name="client")
def fixture_client() -> Client:
    return Client(
        socket=Mock(),
        address="127.0.0.1",
        encoding="utf-8",
        buffer="",
        last_check=2.5,
        login_state=ClientLoginState.PRE_LOGIN,
        registration=None,
        player=None,
    )


@fixture(name="mock_client")
def fixture_mock_client() -> Client:
    client = Mock()
    client.login_state = ClientLoginState.PRE_LOGIN
    client.player = None
    client.prompt = "> "

    return client


@fixture(name="command_processor")
def fixture_command_processor() -> CommandProcessor:
    return CommandProcessor(Mock(), Mock(), Mock(), [MockAction])


@fixture(name="output")
def fixture_output() -> Output:
    return Output(Mock())


@fixture(name="doors")
@load_environment_variables
def fixture_doors() -> Doors:
    return Doors(getenv("DOORS_PATH", "/cibo/resources/doors.json"))


@fixture(name="rooms")
@load_environment_variables
def fixture_rooms() -> Rooms:
    return Rooms(getenv("ROOMS_PATH", "/cibo/resources/rooms.json"))


class MockAction:
    def __init__(self, _telnet, _world, _output):
        pass

    def aliases(self):
        return ["login"]

    def required_args(self):
        return ["name", "password"]

    # pylint: disable=logging-too-many-args
    def process(self, _client, command, args):
        _name = args[0]
        _password = args[1]

        logging.info("Action processed", {"command": command, "args": args})
