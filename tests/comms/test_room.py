from unittest.mock import Mock

from cibo.models import Message, MessageRoute
from tests.conftest import CommsFactory


class TestCommsRoom(CommsFactory):
    def test_comms_room_send(self):
        self.room.send(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  frank leaves.                                                             \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_comms_room_send_no_prompt(self):
        self.room.send(
            MessageRoute(Message("frank leaves."), ids=[1], send_prompt=False)
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  frank leaves.                                                             \n"
        )
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_room_send_no_logged_in_clients(self):
        self.mock_clients[0].is_logged_in = False

        self.room.send(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_room_send_no_client_in_room(self):
        self.mock_clients[0].player = Mock(current_room_id=2)

        self.room.send(MessageRoute(Message("frank leaves."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_room_send_client_ignored(self):
        self.room.send(
            MessageRoute(
                Message("frank leaves."),
                ids=[1],
                ignored_clients=[self.mock_clients[0]],
            )
        )

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_room_send_route_missing_ids(self):
        self.room.send(MessageRoute(Message("frank leaves.")))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()
