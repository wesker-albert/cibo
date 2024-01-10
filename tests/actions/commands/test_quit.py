from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import QuitActionFactory


class TestQuitAction(QuitActionFactory):
    def test_action_quit_aliases(self):
        assert self.quit.aliases() == ["quit"]

    def test_action_quit_required_args(self):
        assert not self.quit.required_args()

    def test_action_quit_process_logged_in(self):
        self.quit.process(self.client, "quit", [], 0)

        assert self.client.login_state is ClientLoginState.PRE_LOGIN

        self.comms.send_to_room.assert_called_once_with(
            MessageRoute(
                Message(
                    body='[cyan]frank[/] yells, "Thank you Wisconsin!" They then proceed to drop their microphone, and walk off the stage.',
                    **self.default_message_args,
                ),
                ids=[1],
                ignored_clients=[self.client],
            )
        )
        self.comms.send_to_client.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You take the [blue]blue pill[/]. You wake up in your bed and believe whatever you want to believe. You choose to believe that your parents are proud of you.\n",
                    **self.default_message_args,
                ),
                client=self.client,
                send_prompt=False,
            )
        )

        self.client.socket.close.assert_called_once()

    def test_action_quit_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.quit.process(self.client, "quit", [], 0)

        self.comms.send_to_client.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You take the [blue]blue pill[/]. You wake up in your bed and believe whatever you want to believe. You choose to believe that your parents are proud of you.\n",
                    **self.default_message_args,
                ),
                client=self.client,
                send_prompt=False,
            )
        )

        self.client.socket.close.assert_called_once()
