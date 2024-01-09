from cibo.models.message import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutputRegion(OutputFactory):
    def test_output_region_send(self):
        self.region.send(MessageRoute(Message("The ground begins to rumble."), ids=[1]))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The ground begins to rumble.                                              \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_region_send_route_missing_ids(self):
        self.region.send(MessageRoute(Message("The ground beings to rumble.")))
