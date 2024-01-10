import logging

from cibo.models import Message, MessageRoute
from tests.conftest import InputEventFactory


class TestInputEevent(InputEventFactory):
    def test_event_input_process(self, caplog):
        self.telnet.get_client_input.return_value = [
            (self.client, "login frank ClevaGuhl!")
        ]

        with caplog.at_level(logging.INFO):
            self.input.process()

            assert caplog.records[0].args == {
                "args": ["frank", "ClevaGuhl!"],
                "command": "login",
            }

    def test_event_input_process_no_input(self):
        self.telnet.get_client_input.return_value = [(self.client, None)]

        self.input.process()

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_event_input_process_missing_args(self):
        self.telnet.get_client_input.return_value = [(self.client, "login frank")]

        self.input.process()

        self.output.send_to_client.assert_called_once_with(
            MessageRoute(
                Message(
                    body="[bright_red]Command is missing required arguments.\nExpected syntax: [green]login name password[/][/]",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )
