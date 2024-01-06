"""Say something to the current room."""

from typing import List, Tuple

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ActionMissingArguments, ClientNotLoggedIn
from cibo.models.message import Message, MessageRoute


class Say(Action):
    """Say something to the current room."""

    def aliases(self) -> List[str]:
        return ["say"]

    def required_args(self) -> List[str]:
        return []

    @property
    def missing_args_message(self) -> Message:
        """No arguments were provided."""

        return Message("You try to think of something clever to say, but fail.")

    def speech_message(
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
            self.output.send_prompt(client)

        except ActionMissingArguments:
            self.output.send_private_message(client, self.missing_args_message)

        else:
            speech_message = self.speech_message(
                client.player.name, self._join_args(args)
            )

            self.output.send_vicinity_message(
                client,
                speech_message[0],
                MessageRoute(client.player.current_room_id, speech_message[1]),
            )
