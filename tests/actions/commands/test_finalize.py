from cibo.models.client import ClientLoginState
from cibo.models.data.user import User
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import FinalizeActionFactory


class TestFinalizeAction(FinalizeActionFactory):
    def test_action_finalize_aliases(self):
        assert self.finalize.aliases() == ["finalize"]

    def test_action_finalize_required_args(self):
        assert not self.finalize.required_args()

    def test_action_finalize_process_logged_in(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.finalize.process(self.client, "finalize", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You finalize your written will, leaving your whole estate to your cat.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_finalize_process_not_registered(self):
        self.finalize.process(self.client, "finalize", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You'll need to [green]register[/] before you can [green]finalize[/].",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_finalize_process_user_already_exists(self, _fixture_database):
        self.client.registration = User(
            name="frank", password="abcd1234", current_room_id=1
        )

        self.finalize.process(self.client, "finalize", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="Sorry, turns out the name [cyan]frank[/] is already taken. Please [green]register[/] again with a different name.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_finalize_process_create_user(self, _fixture_database):
        self.client.registration = User(
            name="jennifer", password="abcd1234", current_room_id=1
        )

        self.finalize.process(self.client, "finalize", [])

        assert not self.client.is_registered
        user = User.get_by_name("jennifer")
        assert len(user.inventory) == 1

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="[cyan]jennifer[/] has been created. You can now [green]login[/] with this user.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )
