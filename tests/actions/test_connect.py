from tests.actions.conftest import ConnectActionFactory


class TestConnectAction(ConnectActionFactory):
    def test_action_connect_aliases(self):
        assert not self.connect.aliases

    def test_action_connect_required_args(self):
        assert not self.connect.required_args

    def test_action_connect_process(self):
        self.connect.process(self.client, None, [])

        panel = self.get_message_panel()

        assert (
            panel.renderable
            == "Welcome to the server!\n\nEnter [green]register name password[/] to create a new user.\nEnter [green]login name password[/] to log in to an existing user."
        )
