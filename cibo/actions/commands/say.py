"""Say something to the current room."""

from typing import List, Tuple

from cibo.actions._base_ import Action
from cibo.exceptions import ActionMissingArguments, ClientNotLoggedIn
from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute


class Say(Action):
    """Say something to the current room."""

    def aliases(self) -> List[str]:
        return ["say"]

    def required_args(self) -> List[str]:
        return []

    @property
    def _missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You try to think of something clever to say, but fail.")

    def _speech_message(
        self, player_name: str, player_message: str
    ) -> Tuple[Message, Message]:
        """Player is successfully saying something."""

        return (
            Message(f'You say, "{player_message}"'),
            Message(f'[cyan]{player_name}[/] says, "{player_message}"'),
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
                client.player.name, self._join_args(args)
            )

            self.comms.send_to_vicinity(
                MessageRoute(speech_message[0], client=client),
                MessageRoute(speech_message[1], ids=[client.player.current_room_id]),
            )
