from cibo.client import ClientLoginState
from tests.conftest import EveryMinuteActionFactory


class TestEveryMinuteAction(EveryMinuteActionFactory):
    def test_action_every_minute_aliases(self):
        assert not self.every_minute.aliases()

    def test_action_every_minute_required_args(self):
        assert not self.every_minute.required_args()

    def test_action_every_minute_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.every_minute.process(self.client, None, [])

        self.client.player.save.assert_not_called()

    def test_action_every_minute_process(self):
        self.every_minute.process(self.client, None, [])

        self.client.player.save.assert_called_once()
