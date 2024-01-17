import socket as socket_
from unittest.mock import Mock

from cibo.models.client import ClientLoginState
from cibo.models.data.user import User
from cibo.models.prompt import Prompt
from tests.conftest import ClientFactory


class TestClient(ClientFactory):
    def test_client_log_in(self):
        self.client.log_in(Mock())

        assert self.client.is_logged_in

    def test_client_log_out(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.client.log_out()

        assert not self.client.is_logged_in
        assert not self.client.user.get_id()

    def test_client_prompt(self):
        assert self.client.prompt == Prompt(body="> ", terminal_width=76)

    def test_client_send_prompt(self):
        self.client.send_prompt()

        self.client.socket.sendall.assert_called_once_with(bytearray(b"\r\n> "))

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
        self.client.registration = User(name="frank")

        assert self.client.is_registered
