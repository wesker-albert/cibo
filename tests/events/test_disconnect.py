from tests.conftest import DisconnectEventFactory


class TestDisconnectEvent(DisconnectEventFactory):
    def test_event_disconnect_process(self):
        self.telnet.get_disconnected_clients.return_value = [self.client]

        self.disconnect.process()

        self.client.player.save.assert_called_once()
        self.output.send_to_room.assert_called_once_with(
            1,
            "You watch in horror as [cyan]frank[/] proceeds to slowly eat their own head. They eventually disappear into nothingness.",
            [self.client],
        )
