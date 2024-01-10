from unittest.mock import ANY

from cibo.models import ClientLoginState, Message, MessageRoute
from cibo.models.data import Player
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

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(body=ANY, **self.default_message_args),
                client=self.client,
            )
        )

        panel = self.get_message_panel()

        assert panel.title == "[blue]A Room Marked #1[/]"
        assert panel.subtitle == "[green]Exits:[/] east, north, south, west"
        assert (
            panel.renderable
            == "  The walls and floor of this room are a bright, sterile white. You feel as if you are inside a simulation.\n\nLooking around you see:\n• [bright_blue]A metal fork glistens in the dirt.\n• A large jukebox is plugged into the wall.[/]\n• [bright_green][cyan]jennifer[/] is standing here.\n• A faceless businessman sits at his desk.[/]"
        )

    def test_action_look_process_items_and_npcs(self, _fixture_database):
        self.client.player = Player.get_by_name("frank")
        self.give_item_to_player(2, self.client.player)

        # the resource doesn't exist in player inventory or room items and NPCs
        self.look.process(self.client, "look", ["macguffin"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="You don't see that...", **self.default_message_args),
                client=self.client,
            )
        )

        # the item exists, but we don't process zero indexes
        self.look.process(self.client, "look", ["0.fork"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="You don't see that...", **self.default_message_args),
                client=self.client,
            )
        )

        # the item exists in the room
        self.look.process(self.client, "look", ["fork"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You look at a metal fork:\n\n  A pronged, metal eating utensil.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

        # the item exists in the room, specified with index
        self.look.process(self.client, "look", ["1.fork"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You look at a metal fork:\n\n  A pronged, metal eating utensil.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

        # the item exists in the player inventory, specified with index
        self.look.process(self.client, "look", ["2.fork"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You look at a metal fork:\n\n  A pronged, metal eating utensil.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

        # the item doesn't exist, because the index is out of range
        self.look.process(self.client, "look", ["3.fork"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="You don't see that...", **self.default_message_args),
                client=self.client,
            )
        )

        # the npc exists in the room
        self.look.process(self.client, "look", ["man"])
        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You look at a faceless businessman:\n\n  His face is smooth and amorphis, like putty. He is wearing a suit, tie, and carrying a briefcase. Though he has no eyes, he seems to be aware of your presence.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )
