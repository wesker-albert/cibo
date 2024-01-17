from cibo.models.message import Message, MessageRoute
from tests.events.conftest import DisconnectEventFactory


class TestDisconnectEvent(DisconnectEventFactory):
    def test_event_disconnect_process(self):
        self.telnet.get_disconnected_clients.return_value = [self.client]

        self.disconnect.process()

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
