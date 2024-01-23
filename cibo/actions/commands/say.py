"""Say something to the current room."""

from typing import List, Tuple

from cibo.actions import Action
from cibo.exceptions import ActionMissingArguments, ClientNotLoggedIn
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Say(Action):
    """Say something to the current room."""

    @property
    def aliases(self) -> List[str]:
        return ["say"]

    @property
    def required_args(self) -> List[str]:
        return []

    @property
    def _missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You try to think of something clever to say, but fail.")

    def _speech_message(
        self, user_name: str, user_message: str
    ) -> Tuple[Message, Message]:
        """User is successfully saying something."""

        return (
            Message(f'You say, "{user_message}"'),
            Message(f'[cyan]{user_name}[/] says, "{user_message}"'),
        )

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

        except ClientNotLoggedIn:
            self.comms.send_prompt(client)

        except ActionMissingArguments:
            self.comms.send_to_client(
                MessageRoute(self._missing_args_message, client=client)
            )

        else:
            speech_message = self._speech_message(
                client.user.name, self._join_args(args)
            )

            self.comms.send_to_vicinity(
                MessageRoute(speech_message[0], client=client),
                MessageRoute(speech_message[1], ids=[client.user.current_room_id]),
            )
