from cibo.models.message import Message, MessageRoute
from tests.conftest import OutputFactory


class TestPrivateOutput(OutputFactory):
    def test_output_private_send(self):
        self.private.send(
            MessageRoute(Message("You are tired."), client=self.mock_clients[0])
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )
        self.mock_clients[0].send_prompt.assert_called_once()

    def test_output_private_send_no_prompt(self):
        self.private.send(
            MessageRoute(
                Message("You are tired."),
                client=self.mock_clients[0],
                send_prompt=False,
            ),
        )

        self.mock_clients[0].send_message.assert_called_once_with(
            "\n  You are tired.                                                            \n"
        )
        self.mock_clients[0].send_prompt.assert_not_called()

    def test_output_private_send_route_missing_client(self):
        self.private.send(MessageRoute(Message("You are tired.")))
