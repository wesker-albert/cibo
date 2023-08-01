import logging
from unittest.mock import Mock

from pytest import raises

from cibo.exception import CommandMissingArguments, UnrecognizedCommand
from tests.conftest import CommandProcessorFactory


class TestCommandProcessor(CommandProcessorFactory):
    def test_process(self, caplog):
        with caplog.at_level(logging.INFO):
            self.command_processor.process(Mock(), "login john ClevaGuhl!")

            assert caplog.records[0].args == {
                "args": ["john", "ClevaGuhl!"],
                "command": "login",
            }

    def test_process_unrecognized_command(self):
        with raises(UnrecognizedCommand):
            self.command_processor.process(Mock(), "say")

    def test_process_missing_args(self):
        with raises(CommandMissingArguments):
            self.command_processor.process(Mock(), "login john")
