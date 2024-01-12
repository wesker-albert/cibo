from unittest.mock import Mock

from pytest import raises

from cibo.exceptions import MessageRouteMissingParameters
from cibo.models.message import Message, MessageRoute
from tests.comms.conftest import CommsFactory


class TestCommsVicinity(CommsFactory):
    def test_comms_vicinity_send(self):
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        self.comms.send_to_vicinity(
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

    def test_comms_vicinity_send_adjoining_room(self):
        self.mock_clients[1].player = Mock(current_room_id=2)

        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        self.comms.send_to_vicinity(
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

    def test_comms_vicinity_send_route_missing_client(self):
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        with raises(MessageRouteMissingParameters):
            self.comms.send_to_vicinity(
                MessageRoute(Message(body="You died.")),
                MessageRoute(
                    Message(body="frank died."),
                    ids=[1],
                ),
            )

    def test_comms_vicinity_send_missing_room_message(self):
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
            self.mock_clients[1],
        ]

        with raises(MessageRouteMissingParameters):
            self.comms.send_to_vicinity(
                MessageRoute(Message(body="You died.")),
            )
