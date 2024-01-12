from cibo.models.message import Message, MessageRoute
from tests.comms.conftest import CommsFactory


class TestCommsRegion(CommsFactory):
    def test_comms_region_send(self):
        self.region.send(MessageRoute(Message("The ground begins to rumble."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The ground begins to rumble.                                              \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_comms_region_send_no_prompt(self):
        self.region.send(
            MessageRoute(
                Message("The ground begins to rumble."), ids=[1], send_prompt=False
            )
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The ground begins to rumble.                                              \n"
        )
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_region_send_no_logged_in_clients(self):
        self.mock_clients[0].is_logged_in = False

        self.region.send(MessageRoute(Message("The ground begins to rumble."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_region_send_client_ignored(self):
        self.region.send(
            MessageRoute(
                Message("The ground beings to rumble."),
                ids=[1],
                ignored_clients=[self.mock_clients[0]],
            )
        )

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_region_send_route_missing_ids(self):
        self.region.send(MessageRoute(Message("The ground beings to rumble.")))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()
