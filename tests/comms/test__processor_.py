from pytest import raises

from cibo.exceptions import MessageRouteMissingParameters
from cibo.models.message import Message, MessageRoute
from tests.comms.conftest import CommsFactory


class TestCommsProcessor(CommsFactory):
    def test_comms_processor_send_prompt(self):
        self.comms.send_prompt(self.mock_clients[0])

        self.mock_clients[0].send_prompt.assert_called_once()

    def test_comms_processor_send_to_client(self):
        self.comms.send_to_client(
            MessageRoute(Message("You are tired."), client=self.mock_clients[0])
        )

    def test_comms_processor_send_to_client_route_missing_client(self):
        with raises(MessageRouteMissingParameters):
            self.comms.send_to_client(MessageRoute(Message("You are tired.")))

    def test_comms_processor_send_to_room(self):
        self.comms.send_to_room(MessageRoute(Message("frank leaves."), ids=[1]))

    def test_comms_processor_send_to_room_route_missing_ids(self):
        with raises(MessageRouteMissingParameters):
            self.comms.send_to_room(MessageRoute(Message("frank leaves.")))

    def test_comms_processor_send_to_sector(self):
        self.comms.send_to_sector(
            MessageRoute(Message("Someone screams nearby."), ids=[1])
        )

    def test_comms_processor_send_to_sector_route_missing_ids(self):
        with raises(MessageRouteMissingParameters):
            self.comms.send_to_sector(MessageRoute(Message("Someone screams nearby.")))

    def test_comms_processor_send_to_region(self):
        self.comms.send_to_region(
            MessageRoute(Message("The ground begins to rumble."), ids=[1])
        )

    def test_comms_processor_send_to_region_route_missing_ids(self):
        with raises(MessageRouteMissingParameters):
            self.comms.send_to_region(
                MessageRoute(Message("The ground beings to rumble."))
            )

    def test_comms_processor_send_to_server(self):
        self.comms.send_to_server(MessageRoute(Message("The server is reboting.")))

    def test_comms_processor_send_to_vicinity(self):
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
