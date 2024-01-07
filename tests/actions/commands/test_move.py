from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.conftest import MoveActionFactory


class TestMoveAction(MoveActionFactory):
    # pylint: disable=duplicate-code
    def test_action_move_aliases(self):
        assert self.move.aliases() == [
            "d",
            "down",
            "e",
            "east",
            "n",
            "north",
            "s",
            "south",
            "u",
            "up",
            "w",
            "west",
        ]

    def test_action_move_required_args(self):
        assert not self.move.required_args()

    def test_action_move_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.move.process(self.client, "n", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_move_process_exit_not_found(self):
        self.move.process(self.client, "u", [])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="You can't go that way.", **self.default_message_args),
                client=self.client,
            )
        )

    def test_action_move_process_door_is_closed(self):
        self.move.process(self.client, "n", [])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="A wooden door is closed.", **self.default_message_args),
                client=self.client,
            )
        )

    def test_action_move_process_door_is_locked(self):
        self.move.process(self.client, "s", [])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A steel security door is closed.", **self.default_message_args
                ),
                client=self.client,
            )
        )

    # def test_action_move_process(self, _fixture_database):
    #     self.move.process(self.client, "w", [])

    #     assert self.client.player.current_room_id == 5

    #     self.output.send_local_announcement.assert_called_once_with(
    #         Announcement(
    #             self_message="You head west.",
    #             room_message="[cyan]frank[/] arrives.",
    #             adjoining_room_message="[cyan]frank[/] leaves west.",
    #         ),
    #         self.client,
    #         5,
    #         1,
    #         prompt=False,
    #     )

    #     panel = self.get_private_message_panel()

    #     assert panel.title == "[blue]A Room Marked #5[/]"
