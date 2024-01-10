from unittest.mock import ANY

from cibo.models import ClientLoginState, Message, MessageRoute
from tests.actions.conftest import LogoutActionFactory


class TestLogoutAction(LogoutActionFactory):
    def test_action_logout_aliases(self):
        assert self.logout.aliases() == ["logout"]

    def test_action_logout_required_args(self):
        assert not self.logout.required_args()

    def test_action_logout_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.logout.process(self.client, "logout", [])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_logout_process(self):
        self.logout.process(self.client, "logout", [], 0)

        assert self.client.login_state is ClientLoginState.PRE_LOGIN

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You slowly fade away into obscurity, like you always feared you would...",
                    **self.default_message_args,
                ),
                client=self.client,
                send_prompt=False,
            ),
            MessageRoute(
                Message(
                    body="A black van pulls up, and 2 large men in labcoats abduct [cyan]frank[/]. The van speeds away. You wonder if you'll ever see them again...",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
        )

        self.comms.send_to_client.assert_called_once_with(
            MessageRoute(
                Message(
                    body=ANY,
                    justify="center",
                    style=None,
                    highlight=False,
                    terminal_width=76,
                ),
                client=self.client,
            )
        )
