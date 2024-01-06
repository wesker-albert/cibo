from cibo.models.client import ClientLoginState
from cibo.output import Announcement
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

        self.output.send_private_message.assert_called_with(
            self.client, "You close your eyes and daydream about money and success."
        )

    def test_action_close_process_door_is_closed(self):
        self.close.process(self.client, "close", ["n"])

        self.output.send_private_message.assert_called_with(
            self.client, "A wooden door is already closed."
        )

    def test_action_close_process_door_is_locked(self):
        self.close.process(self.client, "close", ["s"])

        self.output.send_private_message.assert_called_with(
            self.client, "A steel security door is already closed."
        )

    def test_action_close_process_door_not_found(self):
        self.close.process(self.client, "close", ["w"])

        self.output.send_private_message.assert_called_with(
            self.client, "There's nothing to close."
        )

    def test_action_close_process_close_door(self):
        self.close.process(self.client, "close", ["e"])

        door = self.close.doors.get_by_room_ids(1, 3)
        assert door.is_closed

        self.output.send_local_announcement.assert_called_once_with(
            Announcement(
                self_message="You close a propped-open door.",
                room_message="[cyan]frank[/] closes a propped-open door.",
                adjoining_room_message="A propped-open door closes.",
            ),
            self.client,
            1,
            3,
        )
