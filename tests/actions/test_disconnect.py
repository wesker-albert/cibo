from unittest.mock import Mock

from cibo.actions.disconnect import Disconnect
from cibo.client import Client


def test_aliases():
    connect = Disconnect(Mock(), Mock(), Mock())

    assert not connect.aliases()


def test_required_args():
    connect = Disconnect(Mock(), Mock(), Mock())

    assert not connect.required_args()


def test_process_not_logged_in(mock_client: Client):
    output = Mock()
    connect = Disconnect(Mock(), Mock(), output)

    mock_client.player = Mock()

    connect.process(mock_client, None, [])

    mock_client.player.send.assert_not_called()
    output.private.assert_not_called()


def test_process_no_player(mock_client: Client):
    output = Mock()
    connect = Disconnect(Mock(), Mock(), output)

    connect.process(mock_client, None, [])

    output.private.assert_not_called()


def test_process(mock_client: Client):
    output = Mock()
    connect = Disconnect(Mock(), Mock(), output)

    mock_client.player = Mock()
    mock_client.player.name = "John"
    mock_client.player.current_room_id = 1
    mock_client.is_logged_in.return_value = True

    connect.process(mock_client, None, [])

    mock_client.player.save.assert_called_once()
    output.local.assert_called_once_with(
        1,
        "You watch in horror as [cyan]John[/] proceeds to slowly eat their own head. They eventually disappear into nothingness.",
        [mock_client],
    )
