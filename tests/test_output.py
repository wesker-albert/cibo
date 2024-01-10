from unittest.mock import Mock

from pytest import raises

from cibo.exception import MessageRouteMissingParameters
from cibo.models import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutput(OutputFactory):
    def test_output_send_prompt(self):
        self.output.send_prompt(self.mock_clients[0])

        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_send_to_client(self):
        self.output.send_to_client(
            MessageRoute(Message("You are tired."), client=self.mock_clients[0])
        )

    def test_output_send_to_client_route_missing_client(self):
        with raises(MessageRouteMissingParameters):
            self.output.send_to_client(MessageRoute(Message("You are tired.")))

    def test_output_send_to_room(self):
        self.output.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

    def test_output_send_to_room_route_missing_ids(self):
        with raises(MessageRouteMissingParameters):
            self.output.send_to_room(MessageRoute(Message("frank leaves.")))

    def test_output_send_to_sector(self):
        self.output.send_to_sector(
            MessageRoute(Message("Someone screams nearby."), ids=[1])
        )

    def test_output_send_to_sector_route_missing_ids(self):
        with raises(MessageRouteMissingParameters):
            self.output.send_to_sector(MessageRoute(Message("Someone screams nearby.")))

    def test_output_send_to_region(self):
        self.output.send_to_region(
            MessageRoute(Message("The ground begins to rumble."), ids=[1])
        )

    def test_output_send_to_region_route_missing_ids(self):
        with raises(MessageRouteMissingParameters):
            self.output.send_to_region(
                MessageRoute(Message("The ground beings to rumble."))
            )

    def test_output_send_to_server(self):
        self.output.send_to_server(MessageRoute(Message("The server is reboting.")))

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
