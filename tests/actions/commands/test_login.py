from cibo.models import ClientLoginState, Message, MessageRoute
from tests.actions.conftest import LoginActionFactory


class TestLoginAction(LoginActionFactory):
    def test_action_login_aliases(self):
        assert self.login.aliases() == ["login"]

    def test_action_login_required_args(self):
        assert self.login.required_args() == ["name", "password"]

    def test_action_login_process_already_logged_in(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.login.process(self.client, "login", ["frank", "password"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You login to Facebook, to make sure your ex isn't doing better than you are.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_login_process_player_not_found(self, _fixture_database):
        self.login.process(self.client, "login", ["jennifer", "password"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A player by the name [cyan]jennifer[/] does not exist. If you want, you can [green]register[/] a new player with that name.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_login_process_incorrect_password(self, _fixture_database):
        self.login.process(self.client, "login", ["frank", "wrongpassword"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="[bright_red]Incorrect password.[/]",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_login_process_session_active(self, _fixture_database):
        self.mock_clients[0].player.name = "frank"
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
        ]

        self.login.process(self.client, "login", ["frank", "abcd1234"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="The player [cyan]frank[/] is already logged in. If this player belongs to you and you think it's been stolen, please contact the admin.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_login_process_logging_in(self, _fixture_database):
        self.mock_clients[0].player.name = "jennifer"
        self.mock_clients[0].login_state = ClientLoginState.PRE_LOGIN
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
        ]

        self.login.process(self.client, "login", ["frank", "abcd1234"])

        assert self.client.player.name == "frank"
        assert self.client.is_logged_in

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You take the [red]red pill[/]. You have a look around, to see how deep the rabbit hole goes...",
                    **self.default_message_args,
                ),
                client=self.client,
                send_prompt=False,
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] falls from heaven. It looks like it hurt.",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
        )

        panel = self.get_message_panel()

        assert panel.title == "[blue]A Room Marked #1[/]"
