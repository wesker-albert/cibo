from cibo.models.message import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutputServer(OutputFactory):
    def test_output_server_send(self):
        self.server.send(MessageRoute(Message("The server is reboting.")))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The server is reboting.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()
