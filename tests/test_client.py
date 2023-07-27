import socket as socket_
from unittest.mock import Mock

from cibo.client import Client, ClientLoginState


def test_client_is_logged_in(client: Client):
    client.log_in(Mock())

    assert client.is_logged_in


def test_client_is_logged_out(client: Client):
    client.login_state = ClientLoginState.LOGGED_IN
    client.player = Mock()

    client.log_out()

    assert not client.is_logged_in
    assert client.login_state is ClientLoginState.PRE_LOGIN
    assert not client.player


def test_client_prompt(client: Client):
    assert client.prompt == "> "


def test_client_send_message(client: Client):
    client.send_message("Hey guys!")

    client.socket.sendall.assert_called_once_with(bytearray(b"Hey guys!"))


def test_client_send_message_error(client: Client):
    client.socket.sendall.side_effect = OSError

    client.send_message("Hey guys!")


def test_client_disconnect(client: Client):
    client.disconnect()

    client.socket.shutdown.assert_called_once_with(socket_.SHUT_RDWR)
    client.socket.close.assert_called_once()
