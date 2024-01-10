from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import DisconnectActionFactory


class TestDisconnectAction(DisconnectActionFactory):
    def test_action_disconnect_aliases(self):
        assert not self.disconnect.aliases()

    def test_action_disconnect_required_args(self):
        assert not self.disconnect.required_args()

    def test_action_disconnect_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.disconnect.process(self.client, None, [])

        self.comms.send_to_client.assert_not_called()

    def test_action_disconnect_process(self):
        self.disconnect.process(self.client, None, [])

        self.client.player.save.assert_called_once()
        self.comms.send_to_room.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You watch in horror as [cyan]frank[/] proceeds to slowly eat their own head. They eventually disappear into nothingness.",
                    **self.default_message_args,
                ),
                ids=[1],
                ignored_clients=[self.client],
            )
        )
