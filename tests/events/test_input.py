import logging

from cibo.models.event import EventPayload
from cibo.models.message import Message, MessageRoute
from tests.events.conftest import InputEventFactory


class TestInputEvent(InputEventFactory):
    def test_event_input_process(self, caplog):
        with caplog.at_level(logging.INFO):
            self.signal.send(
                self, payload=EventPayload(self.client, "login frank ClevaGuhl!")
            )

        assert caplog.records[0].args == {
            "args": ["frank", "ClevaGuhl!"],
            "command": "login",
        }

    def test_event_input_process_no_input(self):
        self.signal.send(self, payload=EventPayload(self.client, None))

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_event_input_process_missing_args(self):
        self.signal.send(self, payload=EventPayload(self.client, "login frank"))

        self.comms.send_to_client.assert_called_once_with(
            MessageRoute(
                Message(
                    body="[bright_red]Command is missing required arguments.\nExpected syntax: [green]login name password[/][/]",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_event_input_process_no_payload(self):
        self.signal.send(self, payload=None)

        self.comms.send_prompt.assert_not_called()
        self.comms.send_to_client.assert_not_called()
