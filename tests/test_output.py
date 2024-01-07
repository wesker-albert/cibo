from unittest.mock import Mock

from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutput(OutputFactory):
    def test_output_send_private_mesage(self):
        self.output.send_to_client(
            MessageRoute(Message("You are tired."), client=self.mock_clients[0])
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_private_message_no_prompt(self):
        self.output.send_to_client(
            MessageRoute(
                Message("You are tired."),
                client=self.mock_clients[0],
                send_prompt=False,
            ),
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_send_room_message(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  frank leaves.                                                             \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_room_message_no_logged_in_clients(self):
        self.mock_clients[0].login_state = ClientLoginState.PRE_LOGIN
        self.mock_clients[0].player = Mock()

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_send_room_message_no_client_in_room(self):
        self.mock_clients[0].player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_send_room_message_client_ignored(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(
            MessageRoute(
                Message("frank leaves."),
                ids=[1],
                ignored_clients=[self.mock_clients[0]],
            )
        )

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    # def test_output_send_local_announcement(self):
    #     announcement = Announcement("You died.", "frank died.")

    #     self.telnet.get_connected_clients.return_value = [
    #         self.mock_clients[0],
    #         self.mock_clients[1],
    #     ]

    #     self.output.send_local_announcement(announcement, self.mock_clients[0], 1)

    #     client_calls = [
    #         call(
    #             "\n  You died.                                                                 \n"
    #         ),
    #         call("\r\n> "),
    #     ]

    #     self.mock_clients[0].send_message.assert_has_calls(client_calls)

    #     additional_client_calls = [
    #         call(
    #             "\r  frank died.                                                               \n"
    #         ),
    #         call("\r\n> "),
    #     ]

    #     self.mock_clients[1].send_message.assert_has_calls(additional_client_calls)

    # def test_output_send_local_announcement_adjoining_room(self):
    #     announcement = Announcement(
    #         "You died.", "frank died.", "Your hear a horrifying scream."
    #     )

    #     self.mock_clients[1].player = Mock(current_room_id=2)

    #     self.telnet.get_connected_clients.return_value = [
    #         self.mock_clients[0],
    #         self.mock_clients[1],
    #     ]

    #     self.output.send_local_announcement(announcement, self.mock_clients[0], 1, 2)

    #     additional_client_calls = [
    #         call(
    #             "\r  Your hear a horrifying scream.                                            \n"
    #         ),
    #         call("\r\n> "),
    #     ]

    #     self.mock_clients[1].send_message.assert_has_calls(additional_client_calls)
