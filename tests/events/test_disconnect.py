from unittest.mock import Mock

from tests.conftest import ClientFactory, DisconnectEventFactory


class TestDisconnectEvent(ClientFactory, DisconnectEventFactory):
    def test_event_disconnect_process(self):
        self.telnet.get_disconnected_clients.return_value = [self.mock_client]

        self.mock_client.player = Mock()
        self.mock_client.player.name = "John"
        self.mock_client.player.current_room_id = 1
        self.mock_client.is_logged_in.return_value = True

        self.disconnect.process()

        self.mock_client.player.save.assert_called_once()
        self.output.local.assert_called_once()
