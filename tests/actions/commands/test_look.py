from unittest.mock import ANY

from cibo.client import ClientLoginState
from tests.conftest import LookActionFactory


class TestLookAction(LookActionFactory):
    def test_action_look_aliases(self):
        assert self.look.aliases() == ["l", "look"]

    def test_action_look_required_args(self):
        assert not self.look.required_args()

    def test_action_look_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.look.process(self.client, "look", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_look_process(self, _fixture_database):
        self.mock_clients[0].player.name = "jennifer"
        self.telnet.get_connected_clients.return_value = [self.mock_clients[0]]

        self.look.process(self.client, "look", [])

        self.output.send_private_message.assert_called_with(self.client, ANY)

        panel = self.get_private_message_panel()

        assert panel.title == "[blue]A Room Marked #1[/]"
        assert panel.subtitle == "[green]Exits:[/] east, north, south, west"
        assert (
            panel.renderable
            == "  The walls and floor of this room are a bright, sterile white. You feel as if you are inside a simulation.\n\nLooking around you see:\n• [bright_blue]A metal fork glistens in the dirt.\n• A large jukebox is plugged into the wall.[/]\n• [bright_green][cyan]jennifer[/] is standing here.[/]"
        )
