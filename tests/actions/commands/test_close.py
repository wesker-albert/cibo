from unittest.mock import Mock

from cibo.client import ClientLoginState
from tests.conftest import ClientFactory, CloseActionFactory


class TestCloseAction(ClientFactory, CloseActionFactory):
    def test_action_close_aliases(self):
        assert self.close.aliases() == ["close"]

    def test_action_close_required_args(self):
        assert not self.close.required_args()

    def test_action_close_process_door_is_closed(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.client.player = Mock(current_room_id=1)

        self.close.process(self.client, "close", ["down"])

        self.output.send_private_message.assert_called_with(
            self.client, "A small trapdoor is already closed."
        )

    def test_action_close_process_door_not_found(self):
        self.client.login_state = ClientLoginState.LOGGED_IN
        self.client.player = Mock(current_room_id=1)

        self.close.process(self.client, "close", ["north"])

        self.output.send_private_message.assert_called_with(
            self.client, "There's nothing to close."
        )
