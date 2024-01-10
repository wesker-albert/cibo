from cibo.models import ClientLoginState, Message, MessageRoute
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

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="[green]Exits:[/] east, north, south, west",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )
