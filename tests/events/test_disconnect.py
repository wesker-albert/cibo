from unittest.mock import Mock

from cibo.client import Client
from cibo.events.disconnect import DisconnectEvent


def test_process(mock_client: Client):
    telnet = Mock()
    telnet.get_disconnected_clients.return_value = [mock_client]

    output = Mock()

    connect = DisconnectEvent(telnet, Mock(), output)

    mock_client.player = Mock()
    mock_client.player.name = "John"
    mock_client.player.current_room_id = 1
    mock_client.is_logged_in.return_value = True

    connect.process()

    mock_client.player.save.assert_called_once()
    output.local.assert_called_once()
