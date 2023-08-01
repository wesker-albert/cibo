import logging
from unittest.mock import Mock

from cibo.client import Client
from cibo.command import CommandProcessor
from cibo.events.input import InputEvent


def test_process(caplog, client: Client, command_processor: CommandProcessor):
    telnet = Mock()
    telnet.get_client_input.return_value = [(client, "login john ClevaGuhl!")]

    output = Mock()

    input_ = InputEvent(telnet, Mock(), output, command_processor)

    with caplog.at_level(logging.INFO):
        input_.process()

        assert caplog.records[0].args == {
            "args": ["john", "ClevaGuhl!"],
            "command": "login",
        }


def test_process_no_input(client: Client, command_processor: CommandProcessor):
    telnet = Mock()
    telnet.get_client_input.return_value = [(client, None)]

    output = Mock()

    input_ = InputEvent(telnet, Mock(), output, command_processor)

    input_.process()

    output.prompt.assert_called_once()


def test_process_exception(client: Client, command_processor: CommandProcessor):
    telnet = Mock()
    telnet.get_client_input.return_value = [(client, "login john")]

    output = Mock()

    input_ = InputEvent(telnet, Mock(), output, command_processor)

    input_.process()

    output.private.assert_called_once_with(
        client,
        "[bright_red]Command is missing required arguments.\nExpected syntax: [green]login name password[/][/]",
    )
