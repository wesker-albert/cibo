from cibo.client import ClientLoginState
from tests.conftest import QuitActionFactory


class TestQuitAction(QuitActionFactory):
    def test_action_quit_aliases(self):
        assert self.quit.aliases() == ["quit"]

    def test_action_quit_required_args(self):
        assert not self.quit.required_args()

    def test_action_quit_process_logged_in(self):
        self.quit.process(self.client, "quit", [])

        assert self.client.login_state is ClientLoginState.PRE_LOGIN

        self.output.send_local_message.assert_called_once_with(
            1,
            '[cyan]frank[/] yells, "Thank you Wisconsin!" They then proceed to drop their microphone, and walk off the stage.',
            [self.client],
        )
        self.output.send_private_message.assert_called_once_with(
            self.client,
            "You take the [blue]blue pill[/]. You wake up in your bed and believe whatever you want to believe. You choose to believe that your parents are proud of you.\n",
            prompt=False,
        )

        self.client.socket.close.assert_called_once()

    def test_action_quit_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.quit.process(self.client, "quit", [])

        self.output.send_private_message.assert_called_once_with(
            self.client,
            "You take the [blue]blue pill[/]. You wake up in your bed and believe whatever you want to believe. You choose to believe that your parents are proud of you.\n",
            prompt=False,
        )

        self.client.socket.close.assert_called_once()
