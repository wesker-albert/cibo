from unittest.mock import Mock, call

from cibo.client import ClientLoginState
from tests.conftest import ClientFactory, OutputFactory


class TestOutput(ClientFactory, OutputFactory):
    def test_output_prompt(self):
        self.output.prompt(self.mock_client)

        self.mock_client.send_message.assert_called_once_with("\r\n> ")

    def test_output_private(self):
        self.output.private(self.mock_client, "You are tired.")

        calls = [
            call(
                "\n  You are tired.                                                            \n"
            ),
            call("\r\n> "),
        ]

        self.mock_client.send_message.assert_has_calls(calls)

    def test_output_private_no_prompt(self):
        self.output.private(self.mock_client, "You are tired.", prompt=False)

        self.mock_client.send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )

    def test_output_local(self):
        self.mock_client.login_state = ClientLoginState.LOGGED_IN
        self.mock_client.player = Mock(current_room_id=1)

        self.telnet.get_connected_clients.return_value = [self.mock_client]

        self.output.local(1, "John leaves.", [])

        calls = [
            call(
                "\r  John leaves.                                                              \n"
            ),
            call("\r\n> "),
        ]

        self.mock_client.send_message.assert_has_calls(calls)

    def test_output_local_no_logged_in_clients(self):
        self.telnet.get_connected_clients.return_value = [self.mock_client]

        self.output.local(1, "John leaves.", [])

        self.mock_client.send_message.assert_not_called()

    def test_output_local_no_client_in_room(self):
        self.mock_client.login_state = ClientLoginState.LOGGED_IN
        self.mock_client.player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [self.mock_client]

        self.output.local(1, "John leaves.", [])

        self.mock_client.send_message.assert_not_called()

    def test_output_local_client_ignored(self):
        self.mock_client.login_state = ClientLoginState.LOGGED_IN
        self.mock_client.player = Mock(current_room_id=1)

        self.telnet.get_connected_clients.return_value = [self.mock_client]

        self.output.local(1, "John leaves.", [self.mock_client])

        self.mock_client.send_message.assert_not_called()
