import logging

from pytest import raises

from cibo.exception import InputNotReceived
from tests.conftest import ClientFactory, InputEventFactory


class TestInputEevent(ClientFactory, InputEventFactory):
    def test_event_input_process(self, caplog):
        self.telnet.get_client_input.return_value = [
            (self.mock_client, "login john ClevaGuhl!")
        ]

        with caplog.at_level(logging.INFO):
            self.input.process()

            assert caplog.records[0].args == {
                "args": ["john", "ClevaGuhl!"],
                "command": "login",
            }

    def test_event_input_process_no_input(self):
        self.telnet.get_client_input.return_value = [(self.mock_client, None)]

        with raises(InputNotReceived):
            self.input.process()

    def test_event_input_process_exception(self):
        self.telnet.get_client_input.return_value = [(self.mock_client, "login john")]

        self.input.process()

        self.output.private.assert_called_once_with(
            self.mock_client,
            "[bright_red]Command is missing required arguments.\nExpected syntax: [green]login name password[/][/]",
        )
