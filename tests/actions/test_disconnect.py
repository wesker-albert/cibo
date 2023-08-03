from unittest.mock import Mock

from tests.conftest import ClientFactory, DisconnectActionFactory


class TestDisconnectAction(ClientFactory, DisconnectActionFactory):
    def test_aliases(self):
        assert not self.disconnect.aliases()

    def test_required_args(self):
        assert not self.disconnect.required_args()

    def test_process_not_logged_in(self):
        self.mock_client.player = Mock()

        self.disconnect.process(self.mock_client, None, [])

        self.mock_client.player.send.assert_not_called()
        self.output.private.assert_not_called()

    def test_process(self):
        self.mock_client.player = Mock()
        self.mock_client.player.name = "John"
        self.mock_client.player.current_room_id = 1
        self.mock_client.is_logged_in.return_value = True

        self.disconnect.process(self.mock_client, None, [])

        self.mock_client.player.save.assert_called_once()
        self.output.local.assert_called_once_with(
            1,
            "You watch in horror as [cyan]John[/] proceeds to slowly eat their own head. They eventually disappear into nothingness.",
            [self.mock_client],
        )
