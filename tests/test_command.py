import logging
from unittest.mock import Mock

from pytest import fixture, raises

from cibo.command import CommandProcessor
from cibo.exception import CommandMissingArguments, UnrecognizedCommand


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


@fixture(name="mock_command_processor")
def fixture_mock_command_processor() -> CommandProcessor:
    return CommandProcessor(Mock(), Mock(), [MockAction])


def test_process(caplog, mock_command_processor: CommandProcessor):
    with caplog.at_level(logging.INFO):
        mock_command_processor.process(Mock(), "login john ClevaGuhl!")

        assert caplog.records[0].args == {
            "args": ["john", "ClevaGuhl!"],
            "command": "login",
        }


def test_process_unrecognized_command(mock_command_processor: CommandProcessor):
    with raises(UnrecognizedCommand):
        mock_command_processor.process(Mock(), "say")


def test_process_missing_args(mock_command_processor: CommandProcessor):
    with raises(CommandMissingArguments):
        mock_command_processor.process(Mock(), "login john")
