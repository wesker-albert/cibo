from unittest.mock import Mock

from pytest import raises

from cibo.exception import MessageRouteMissingParameters
from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutput(OutputFactory):
    def test_output_send_prompt(self):
        self.output.send_prompt(self.mock_clients[0])

        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_client(self):
        self.output.send_to_client(
            MessageRoute(Message("You are tired."), client=self.mock_clients[0])
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_client_no_prompt(self):
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

    def test_output_send_to_client_route_missing_client(self):
        with raises(MessageRouteMissingParameters):
            self.output.send_to_client(MessageRoute(Message("You are tired.")))

    def test_output_send_to_room(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  frank leaves.                                                             \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_room_no_logged_in_clients(self):
        self.mock_clients[0].login_state = ClientLoginState.PRE_LOGIN
        self.mock_clients[0].player = Mock()

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_send_to_room_no_client_in_room(self):
        self.mock_clients[0].player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_send_to_room_client_ignored(self):
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

    def test_output_send_to_room_route_missing_ids(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        with raises(MessageRouteMissingParameters):
            self.output.send_to_room(MessageRoute(Message("frank leaves.")))

    def test_output_send_sector(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_sector(
            MessageRoute(Message("Someone screams nearby."), ids=[1])
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  Someone screams nearby.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_sector_route_missing_ids(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        with raises(MessageRouteMissingParameters):
            self.output.send_to_sector(MessageRoute(Message("Someone screams nearby.")))

    def test_output_send_region(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_region(
            MessageRoute(Message("The ground begins to rumble."), ids=[1])
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The ground begins to rumble.                                              \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_region_route_missing_ids(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        with raises(MessageRouteMissingParameters):
            self.output.send_to_region(
                MessageRoute(Message("The ground beings to rumble."))
            )

    def test_output_send_server(self):
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.output.send_to_server(MessageRoute(Message("The server is reboting.")))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The server is reboting.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_vicinity(self):
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        self.output.send_to_vicinity(
            MessageRoute(Message(body="You died."), client=self.mock_clients[0]),
            MessageRoute(
                Message(body="frank died."),
                ids=[1],
            ),
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You died.                                                                 \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

        self.mock_clients[1].send_message.assert_called_once_with(
            "\r  frank died.                                                               \n"
        )
        self.mock_clients[1].send_prompt.assert_called_once()

    def test_output_send_to_vicinity_adjoining_room(self):
        self.mock_clients[1].player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        self.output.send_to_vicinity(
            MessageRoute(Message(body="You died."), client=self.mock_clients[0]),
            MessageRoute(
                Message(body="frank died."),
                ids=[1],
            ),
            MessageRoute(
                Message(body="You hear a horrifying scream."),
                ids=[2],
            ),
        )

        self.mock_clients[1].send_message.assert_called_once_with(
            "\r  You hear a horrifying scream.                                             \n"
        )
        self.mock_clients[1].send_prompt.assert_called_once()

    def test_output_send_to_vicinity_route_missing_client(self):
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        with raises(MessageRouteMissingParameters):
            self.output.send_to_vicinity(
                MessageRoute(Message(body="You died.")),
                MessageRoute(
                    Message(body="frank died."),
                    ids=[1],
                ),
            )
