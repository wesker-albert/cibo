import logging
from unittest.mock import Mock

from pytest import raises

from cibo.exceptions import CommandMissingArguments, CommandUnrecognized
from tests.conftest import CommandProcessorFactory


class TestCommandProcessor(CommandProcessorFactory):
    def test_command_processor_process(self, caplog):
        with caplog.at_level(logging.INFO):
            self.command_processor.process(Mock(), "login frank ClevaGuhl!")

            assert caplog.records[0].args == {
                "args": ["frank", "ClevaGuhl!"],
                "command": "login",
            }

    def test_command_processor_process_unrecognized_command(self):
        with raises(CommandUnrecognized):
            self.command_processor.process(Mock(), "say")

    def test_command_processor_process_missing_args(self):
        with raises(CommandMissingArguments):
            self.command_processor.process(Mock(), "login frank")
