from cibo.models.client import ClientLoginState
from cibo.output import Announcement
from tests.conftest import SayActionFactory


class TestSayAction(SayActionFactory):
    def test_action_say_aliases(self):
        assert self.say.aliases() == ["say"]

    def test_action_say_required_args(self):
        assert not self.say.required_args()

    def test_action_say_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.say.process(self.client, "say", ["Hey you guys!"])

        self.output.send_prompt.assert_called_once_with(self.client)

    def test_action_say_process_missing_args(self):
        self.say.process(self.client, "say", [])

        self.output.private.send.assert_called_with(
            self.client, "You try to think of something clever to say, but fail."
        )

    def test_action_say_process(self):
        self.say.process(self.client, "say", ["Hey you guys!"])

        self.output.send_local_announcement.assert_called_once_with(
            Announcement(
                self_message='You say, "Hey you guys!"',
                room_message='[cyan]frank[/] says, "Hey you guys!"',
                adjoining_room_message=None,
            ),
            self.client,
            1,
        )
