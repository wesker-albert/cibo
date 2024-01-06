from cibo.models.client import ClientLoginState
from cibo.models.data.player import Player
from tests.conftest import FinalizeActionFactory


class TestFinalizeAction(FinalizeActionFactory):
    def test_action_finalize_aliases(self):
        assert self.finalize.aliases() == ["finalize"]

    def test_action_finalize_required_args(self):
        assert not self.finalize.required_args()

    def test_action_finalize_process_logged_in(self):
        self.client.login_state = ClientLoginState.LOGGED_IN

        self.finalize.process(self.client, "finalize", [])

        self.output.private.send.assert_called_with(
            self.client,
            "You finalize your written will, leaving your whole estate to your cat.",
        )

    def test_action_finalize_process_not_registered(self):
        self.finalize.process(self.client, "finalize", [])

        self.output.private.send.assert_called_with(
            self.client,
            "You'll need to [green]register[/] before you can [green]finalize[/].",
        )

    def test_action_finalize_process_player_already_exists(self, _fixture_database):
        self.client.registration = Player(
            name="frank", password="abcd1234", current_room_id=1
        )

        self.finalize.process(self.client, "finalize", [])

        self.output.private.send.assert_called_with(
            self.client,
            "Sorry, turns out the name [cyan]frank[/] is already taken. Please [green]register[/] again with a different name.",
        )

    def test_action_finalize_process_create_player(self, _fixture_database):
        self.client.registration = Player(
            name="jennifer", password="abcd1234", current_room_id=1
        )

        self.finalize.process(self.client, "finalize", [])

        assert not self.client.is_registered
        player = Player.get_by_name("jennifer")
        assert len(player.inventory) == 1

        self.output.private.send.assert_called_with(
            self.client,
            "[cyan]jennifer[/] has been created. You can now [green]login[/] with this player.",
        )
