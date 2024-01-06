from unittest.mock import ANY

from cibo.models.client import ClientLoginState
from cibo.output import Announcement
from tests.conftest import LogoutActionFactory


class TestLogoutAction(LogoutActionFactory):
    def test_action_logout_aliases(self):
        assert self.logout.aliases() == ["logout"]

    def test_action_logout_required_args(self):
        assert not self.logout.required_args()

    def test_action_logout_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.logout.process(self.client, "logout", [])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_logout_process(self):
        self.logout.process(self.client, "logout", [], 0)

        assert self.client.login_state is ClientLoginState.PRE_LOGIN

        self.output.send_local_announcement.assert_called_once_with(
            Announcement(
                self_message="You slowly fade away into obscurity, like you always feared you would...",
                room_message="A black van pulls up, and 2 large men in labcoats abduct [cyan]frank[/]. The van speeds away. You wonder if you'll ever see them again...",
                adjoining_room_message=None,
            ),
            self.client,
            1,
            prompt=False,
        )

        self.output.private.send.assert_called_once_with(
            self.client, ANY, justify="center"
        )
