from unittest.mock import Mock, call

from cibo.client import ClientLoginState
from cibo.output import Announcement
from tests.conftest import OutputFactory


class TestOutput(OutputFactory):
    def test_output_prompt(self):
        self.output.send_prompt(self.mock_clients[0])

        self.mock_clients[0].send_message.assert_called_once_with("\r\n> ")

    def test_output_private(self):
        self.output.send_private_message(self.mock_clients[0], "You are tired.")

        calls = [
            call(
                "\n  You are tired.                                                            \n"
            ),
            call("\r\n> "),
        ]

        self.mock_clients[0].send_message.assert_has_calls(calls)

    def test_output_private_no_prompt(self):
        self.output.send_private_message(
            self.mock_clients[0], "You are tired.", prompt=False
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )

    def test_output_local(self):
        self.mock_clients[0].login_state = ClientLoginState.LOGGED_IN
        self.mock_clients[0].player = Mock(current_room_id=1)

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_local_message(1, "John leaves.", [])

        calls = [
            call(
                "\r  John leaves.                                                              \n"
            ),
            call("\r\n> "),
        ]

        self.mock_clients[0].send_message.assert_has_calls(calls)

    def test_output_local_no_logged_in_clients(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_local_message(1, "John leaves.", [])

        self.mock_clients[0].send_message.assert_not_called()

    def test_output_local_no_client_in_room(self):
        self.mock_clients[0].login_state = ClientLoginState.LOGGED_IN
        self.mock_clients[0].player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_local_message(1, "John leaves.", [])

        self.mock_clients[0].send_message.assert_not_called()

    def test_output_local_client_ignored(self):
        self.mock_clients[0].login_state = ClientLoginState.LOGGED_IN
        self.mock_clients[0].player = Mock(current_room_id=1)

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_local_message(1, "John leaves.", [self.mock_clients[0]])

        self.mock_clients[0].send_message.assert_not_called()

    def test_output_local_announcement(self):
        announcement = Announcement("You died.", "John died.")

        self.mock_clients[0].login_state = ClientLoginState.LOGGED_IN
        self.mock_clients[0].player = Mock(current_room_id=1)

        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        self.output.send_local_announcement(announcement, self.mock_clients[0], 1)

        client_calls = [
            call(
                "\n  You died.                                                                 \n"
            ),
            call("\r\n> "),
        ]

        self.mock_clients[0].send_message.assert_has_calls(client_calls)

        additional_client_calls = [
            call(
                "\r  John died.                                                                \n"
            ),
            call("\r\n> "),
        ]

        self.mock_clients[1].send_message.assert_has_calls(additional_client_calls)

    def test_output_local_announcement_adjoining_room(self):
        announcement = Announcement(
            "You died.", "John died.", "Your hear a horrifying scream."
        )

        self.mock_clients[0].login_state = ClientLoginState.LOGGED_IN
        self.mock_clients[0].player = Mock(current_room_id=1)

        self.mock_clients[1].player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        self.output.send_local_announcement(announcement, self.mock_clients[0], 1, 2)

        additional_client_calls = [
            call(
                "\r  Your hear a horrifying scream.                                            \n"
            ),
            call("\r\n> "),
        ]

        self.mock_clients[1].send_message.assert_has_calls(additional_client_calls)
