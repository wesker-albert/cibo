from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import MoveActionFactory


class TestMoveAction(MoveActionFactory):
    # pylint: disable=duplicate-code
    def test_action_move_aliases(self):
        assert self.move.aliases == [
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
        assert not self.move.required_args

    def test_action_move_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.move.process(self.client, "n", [])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_move_process_exit_not_found(self):
        self.move.process(self.client, "u", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="You can't go that way.", **self.default_message_args),
                client=self.client,
            )
        )

    def test_action_move_process_door_is_closed(self):
        self.move.process(self.client, "n", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="A wooden door is closed.", **self.default_message_args),
                client=self.client,
            )
        )

    def test_action_move_process_door_is_locked(self):
        self.move.process(self.client, "s", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A steel security door is closed.", **self.default_message_args
                ),
                client=self.client,
            )
        )

    def test_action_move_process(self, _fixture_database):
        self.move.process(self.client, "w", [])

        assert self.client.user.current_room_id == 5

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(body="You head west.", **self.default_message_args),
                client=self.client,
                send_prompt=False,
            ),
            MessageRoute(
                Message(body="[cyan]frank[/] arrives.", **self.default_message_args),
                ids=[5],
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] leaves west.", **self.default_message_args
                ),
                ids=[1],
            ),
        )

        panel = self.get_message_panel()

        assert panel.title == "[blue]A Room Marked #5[/]"
