from cibo.models import ClientLoginState, Message, MessageRoute
from tests.conftest import CloseActionFactory


class TestCloseAction(CloseActionFactory):
    def test_action_close_aliases(self):
        assert self.close.aliases() == ["close"]

    def test_action_close_required_args(self):
        assert not self.close.required_args()

    def test_action_close_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.close.process(self.client, "close", ["n"])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_close_process_missing_args(self):
        self.close.process(self.client, "close", [])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You close your eyes and daydream about money and success.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_close_process_door_is_closed(self):
        self.close.process(self.client, "close", ["n"])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A wooden door is already closed.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_close_process_door_is_locked(self):
        self.close.process(self.client, "close", ["s"])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A steel security door is already closed.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_close_process_door_not_found(self):
        self.close.process(self.client, "close", ["w"])

        self.output.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="There's nothing to close.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_close_process_close_door(self):
        self.close.process(self.client, "close", ["e"])

        door = self.close.doors.get_by_room_ids(1, 3)
        assert door.is_closed

        self.output.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You close a propped-open door.", **self.default_message_args
                ),
                client=self.client,
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] closes a propped-open door.",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
            MessageRoute(
                Message(
                    body="A propped-open door closes.", **self.default_message_args
                ),
                ids=[3],
            ),
        )
