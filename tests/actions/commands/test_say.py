from cibo.models import ClientLoginState, Message, MessageRoute
from tests.actions.conftest import SayActionFactory


class TestSayAction(SayActionFactory):
    def test_action_say_aliases(self):
        assert self.say.aliases() == ["say"]

    def test_action_say_required_args(self):
        assert not self.say.required_args()

    def test_action_say_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.say.process(self.client, "say", ["Hey you guys!"])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_say_process_missing_args(self):
        self.say.process(self.client, "say", [])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="You try to think of something clever to say, but fail.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_say_process(self):
        self.say.process(self.client, "say", ["Hey you guys!"])

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(body='You say, "Hey you guys!"', **self.default_message_args),
                client=self.client,
            ),
            MessageRoute(
                Message(
                    body='[cyan]frank[/] says, "Hey you guys!"',
                    **self.default_message_args,
                ),
                ids=[1],
            ),
        )
