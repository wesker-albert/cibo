import logging
from unittest.mock import Mock

from pytest import fixture

from cibo.client import Client, ClientLoginState
from cibo.command import CommandProcessor
from cibo.output import Output


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
    return CommandProcessor(Mock(), Mock(), [MockAction])


@fixture(name="output")
def fixture_output() -> Output:
    return Output(Mock())


class MockAction:
    def __init__(self, _telnet, _world):
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
