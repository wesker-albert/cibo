from cibo.models.message import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutputSector(OutputFactory):
    def test_output_sector_send(self):
        self.sector.send(MessageRoute(Message("Someone screams nearby."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  Someone screams nearby.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_sector_send_route_missing_ids(self):
        self.sector.send(MessageRoute(Message("Someone screams nearby.")))
