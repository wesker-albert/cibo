from cibo.models import Message, MessageRoute
from tests.conftest import CommsFactory


class TestCommsSector(CommsFactory):
    def test_comms_sector_send(self):
        self.sector.send(MessageRoute(Message("Someone screams nearby."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  Someone screams nearby.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_comms_sector_send_no_prompt(self):
        self.sector.send(
            MessageRoute(Message("Someone screams nearby."), ids=[1], send_prompt=False)
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  Someone screams nearby.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_sector_send_no_logged_in_clients(self):
        self.mock_clients[0].is_logged_in = False

        self.sector.send(MessageRoute(Message("Someone screams nearby."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_sector_send_client_ignored(self):
        self.sector.send(
            MessageRoute(
                Message("Someone screams nearboy."),
                ids=[1],
                ignored_clients=[self.mock_clients[0]],
            )
        )

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_comms_sector_send_route_missing_ids(self):
        self.sector.send(MessageRoute(Message("Someone screams nearby.")))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()
