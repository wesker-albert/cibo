from cibo.models.client import ClientLoginState
from cibo.models.message import Message, MessageRoute
from tests.actions.conftest import OpenActionFactory


class TestOpenAction(OpenActionFactory):
    def test_action_open_aliases(self):
        assert self.open.aliases() == ["open"]

    def test_action_open_required_args(self):
        assert not self.open.required_args()

    def test_action_open_process_not_logged_in(self):
        self.client.login_state = ClientLoginState.PRE_LOGIN

        self.open.process(self.client, "open", ["n"])

        self.comms.send_prompt.assert_called_once_with(self.client)

    def test_action_open_process_missing_args(self):
        self.open.process(self.client, "open", [])

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(
                    body="You open your mouth and let out a loud belch. If anyone else is in the room, they probably heard it...",
                    **self.default_message_args,
                ),
                client=self.client,
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] burps loudly. How disgusting...",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
        )

    def test_action_open_process_door_is_open(self):
        self.open.process(self.client, "open", ["e"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A propped-open door is already open.",
                    **self.default_message_args,
                ),
                client=self.client,
            )
        )

    def test_action_open_process_door_is_locked(self):
        self.open.process(self.client, "open", ["s"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(
                    body="A steel security door is locked.", **self.default_message_args
                ),
                client=self.client,
            )
        )

    def test_action_open_process_door_not_found(self):
        self.open.process(self.client, "open", ["w"])

        self.comms.send_to_client.assert_called_with(
            MessageRoute(
                Message(body="There's nothing to open.", **self.default_message_args),
                client=self.client,
            )
        )

    def test_action_open_process_open_door(self):
        self.open.process(self.client, "open", ["n"])

        door = self.open.doors.get_by_room_ids(1, 2)
        assert door.is_open

        self.comms.send_to_vicinity.assert_called_once_with(
            MessageRoute(
                Message(body="You open a wooden door.", **self.default_message_args),
                client=self.client,
            ),
            MessageRoute(
                Message(
                    body="[cyan]frank[/] opens a wooden door.",
                    **self.default_message_args,
                ),
                ids=[1],
            ),
            MessageRoute(
                Message(body="A wooden door opens.", **self.default_message_args),
                ids=[2],
            ),
        )
