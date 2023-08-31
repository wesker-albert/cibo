import socket as socket_
from unittest.mock import Mock

from cibo.client import ClientLoginState
from cibo.models.data.player import Player
from tests.conftest import ClientFactory


class TestClient(ClientFactory):
    def test_client_log_in(self):
        self.client.log_in(Mock())

        assert self.client.is_logged_in

    def test_client_log_out(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.client.log_out()

        assert not self.client.is_logged_in
        assert self.client.login_state is ClientLoginState.PRE_LOGIN
        assert not self.client.player.get_id()

    def test_client_prompt(self):
        assert self.client.prompt == "> "

    def test_client_send_message(self):
        self.client.send_message("Hey guys!")

        self.client.socket.sendall.assert_called_once_with(bytearray(b"Hey guys!"))

    def test_client_send_message_error(self):
        self.client.socket.sendall.side_effect = OSError

        self.client.send_message("Hey guys!")

    def test_client_disconnect(self):
        self.client.disconnect()

        self.client.socket.shutdown.assert_called_once_with(socket_.SHUT_RDWR)
        self.client.socket.close.assert_called_once()

    def test_client_is_registered(self):
        self.client.registration = Player(name="frank")

        assert self.client.is_registered
