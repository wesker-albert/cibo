from cibo.models import ClientLoginState, Message, MessageRoute
from tests.actions.conftest import RegisterActionFactory


class TestRegisterAction(RegisterActionFactory):
    def test_action_register_aliases(self):
        assert self.register.aliases() == ["register"]

    def test_action_register_required_args(self):
        assert self.register.required_args() == ["name", "password"]

    def test_action_register_process_logged_in(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.register.process(self.client, "register", ["frank", "password"])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You register to vote, even though both candidates aren't that great.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_register_process_player_already_exists(self, _fixture_database):
        self.register.process(self.client, "register", ["frank", "password"])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="Sorry, turns out the name [cyan]frank[/] is already taken. Please [green]register[/] again with a different name.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_register_process_player_validation_error(self, _fixture_database):
        self.register.process(self.client, "register", ["jennifer", "123"])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="[bright_red]Your player name or password don't meet criteria.[/]\n\nNames must be 3-15 chars and only contain letters, numbers, or underscores. They are case-sensitive.\n\nPasswords must be minimum 8 chars.\n\nPlease [green]register[/] again.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_register_process_player_registered(self, _fixture_database):
        self.register.process(self.client, "register", ["jennifer", "password"])

        assert self.client.registration.name == "jennifer"
        assert self.client.registration.current_room_id == 1

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="Are you sure you want to create the player named [cyan]jennifer[/]?\n\nType [green]finalize[/] to finalize the player creation. If you want to use a different name or password, you can [green]register[/] again.\n\nOtherwise, feel free to [green]login[/] to an already existing player.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )
