import logging
from unittest.mock import Mock

from pytest import raises

from cibo.command import CommandProcessor
from cibo.exception import CommandMissingArguments, UnrecognizedCommand


def test_process(caplog, command_processor: CommandProcessor):
    with caplog.at_level(logging.INFO):
        command_processor.process(Mock(), "login john ClevaGuhl!")

        assert caplog.records[0].args == {
            "args": ["john", "ClevaGuhl!"],
            "command": "login",
        }


def test_process_unrecognized_command(command_processor: CommandProcessor):
    with raises(UnrecognizedCommand):
        command_processor.process(Mock(), "say")


def test_process_missing_args(command_processor: CommandProcessor):
    with raises(CommandMissingArguments):
        command_processor.process(Mock(), "login john")
