import socket as socket_
from unittest.mock import Mock

from pytest import fixture

from cibo.client import Client, ClientLoginState


@fixture(name="mock_client")
def fixture_mock_client() -> Client:
    return Client(
        socket=Mock(),
        address="127.0.0.1",
        encoding="utf-8",
        buffer="",
        last_check=2.5,
        login_state=ClientLoginState.PRE_LOGIN,
        registration=None,
        player=None,
    )


def test_client_is_logged_in(mock_client: Client):
    mock_client.log_in(Mock())

    assert mock_client.is_logged_in


def test_client_is_logged_out(mock_client: Client):
    mock_client.login_state = ClientLoginState.LOGGED_IN
    mock_client.player = Mock()

    mock_client.log_out()

    assert not mock_client.is_logged_in
    assert mock_client.login_state is ClientLoginState.PRE_LOGIN
    assert not mock_client.player


def test_client_prompt(mock_client: Client):
    assert mock_client.prompt == "> "


def test_client_send_message(mock_client: Client):
    mock_client.send_message("Hey guys!")

    mock_client.socket.sendall.assert_called_once_with(bytearray(b"Hey guys!"))


def test_client_send_message_error(mock_client: Client):
    mock_client.socket.sendall.side_effect = OSError

    mock_client.send_message("Hey guys!")


def test_client_disconnect(mock_client: Client):
    mock_client.disconnect()

    mock_client.socket.shutdown.assert_called_once_with(socket_.SHUT_RDWR)
    mock_client.socket.close.assert_called_once()
