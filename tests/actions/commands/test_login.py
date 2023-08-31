from cibo.client import ClientLoginState
from cibo.output import Announcement
from tests.conftest import LoginActionFactory


class TestLoginAction(LoginActionFactory):
    def test_action_login_aliases(self):
        assert self.login.aliases() == ["login"]

    def test_action_login_required_args(self):
        assert self.login.required_args() == ["name", "password"]

    def test_action_login_process_already_logged_in(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.login.process(self.client, "login", ["frank", "password"])

        self.output.send_private_message.assert_called_with(
            self.client,
            "You login to Facebook, to make sure your ex isn't doing better than you are.",
        )

    def test_action_login_process_player_not_found(self, _fixture_database):
        self.login.process(self.client, "login", ["jennifer", "password"])

        self.output.send_private_message.assert_called_with(
            self.client,
            "A player by the name [cyan]jennifer[/] does not exist. If you want, you can [green]register[/] a new player with that name.",
        )

    def test_action_login_process_incorrect_password(self, _fixture_database):
        self.login.process(self.client, "login", ["frank", "wrongpassword"])

        self.output.send_private_message.assert_called_with(
            self.client, "[bright_red]Incorrect password.[/]"
        )

    def test_action_login_process_session_active(self, _fixture_database):
        self.mock_clients[0].player.name = "frank"
        self.telnet.get_connected_clients.return_value = [
            self.mock_clients[0],
        ]

        self.login.process(self.client, "login", ["frank", "abcd1234"])

        self.output.send_private_message.assert_called_with(
            self.client,
            "The player [cyan]frank[/] is already logged in. If this player belongs to you and you think it's been stolen, please contact the admin.",
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

        self.output.send_local_announcement.assert_called_once_with(
            Announcement(
                self_message="You take the [red]red pill[/]. You have a look around, to see how deep the rabbit hole goes...",
                room_message="[cyan]frank[/] falls from heaven. It looks like it hurt.",
                adjoining_room_message=None,
            ),
            self.client,
            1,
        )
