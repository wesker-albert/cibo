from cibo.client import ClientLoginState
from tests.conftest import ExitsActionFactory


class TestExitsAction(ExitsActionFactory):
    def test_action_exits_aliases(self):
        assert self.exits.aliases() == ["exits"]

    def test_action_exits_required_args(self):
        assert not self.exits.required_args()

    def test_action_exits_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.exits.process(self.client, "exits", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_exits_process(self):
        self.exits.process(self.client, "exits", [])

        self.output.send_private_message.assert_called_with(
            self.client, "[green]Exits:[/] east, north, south, west"
        )
