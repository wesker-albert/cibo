from unittest.mock import ANY

from tests.conftest import ClientFactory, ConnectActionFactory


class TestConnectAction(ClientFactory, ConnectActionFactory):
    def test_action_connect_aliases(self):
        assert not self.connect.aliases()

    def test_action_connect_required_args(self):
        assert not self.connect.required_args()

    def test_action_connect_process(self):
        self.connect.process(self.mock_client, None, [])

        self.output.send_private_message.assert_called_once_with(
            self.mock_client, ANY, justify="center"
        )
