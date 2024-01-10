from cibo.models import Message, MessageRoute
from tests.conftest import OutputFactory


class TestOutputServer(OutputFactory):
    def test_output_server_send(self):
        self.server.send(MessageRoute(Message("The server is reboting.")))

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The server is reboting.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_server_send_no_prompt(self):
        self.server.send(
            MessageRoute(Message("The server is reboting."), ids=[1], send_prompt=False)
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\r  The server is reboting.                                                   \n"
        )
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_server_send_client_ignored(self):
        self.server.send(
            MessageRoute(
                Message("The server is rebooting."),
                ids=[1],
                ignored_clients=[self.mock_clients[0]],
            )
        )

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_server_send_no_logged_in_clients(self):
        self.mock_clients[0].is_logged_in = False

        self.server.send(MessageRoute(Message("The server is reboting."), ids=[1]))

        self.mock_clients[0].send_message.assert_not_called()
        self.mock_clients[0].send_prompt.assert_not_called()
