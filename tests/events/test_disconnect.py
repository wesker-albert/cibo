from cibo.models.event import EventPayload
from cibo.models.message import Message, MessageRoute
from tests.events.conftest import DisconnectEventFactory


class TestDisconnectEvent(DisconnectEventFactory):
    def test_event_disconnect_process(self):
        self.signal.send(self, payload=EventPayload(self.client))

        self.client.user.save.assert_called_once()
        self.comms.send_to_room.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You watch in horror as [cyan]frank[/] proceeds to slowly eat their own head. They eventually disappear into nothingness.",
                    **self.default_message_args,
                ),
                ids=[1],
                ignored_clients=[self.client],
            )
        )

    def test_event_disconnect_process_no_payload(self):
        self.signal.send(self, payload=None)

        self.client.user.save.assert_not_called()
        self.comms.send_to_room.assert_not_called()
