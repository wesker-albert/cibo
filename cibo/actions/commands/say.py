"""Say something to the current room."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import ActionMissingArguments, ClientNotLoggedIn
from cibo.models.object.announcement import Announcement


class Say(Action):
    """Say something to the current room."""

    def aliases(self) -> List[str]:
        return ["say"]

    def required_args(self) -> List[str]:
        return []

    @property
    def missing_args_msg(self) -> str:
        """No arguments were provided."""

        return "You try to think of something clever to say, but fail."

    def speech_msg(self, player_name: str, player_message: str) -> Announcement:
        """Player is successfully saying something."""

        return Announcement(
            f'You say, "{player_message}"',
            f'[cyan]{player_name}[/] says, "{player_message}"',
        )

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise ClientNotLoggedIn

            if not args:
                raise ActionMissingArguments

        except ClientNotLoggedIn:
            self.send.prompt(client)

        except ActionMissingArguments:
            self.send.private(client, self.missing_args_msg)

        else:
            speech_msg = self.speech_msg(client.player.name, self._join_args(args))

            self.send.local(
                client.player.current_room_id,
                speech_msg.to_room,
                [client],
            )

            self.send.private(client, speech_msg.to_self)
