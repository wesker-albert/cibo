"""Say something to the current room."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.exception import MissingArguments, NotLoggedIn
from cibo.models.announcement import Announcement


class Say(Action):
    """Say something to the current room."""

    def aliases(self) -> List[str]:
        return ["say"]

    def required_args(self) -> List[str]:
        return []

    @property
    def no_args_msg(self) -> str:
        """No arguments were provided."""

        return "You try to think of something clever to say, but fail."

    def speaking_msg(self, player_name: str, player_message: str) -> Announcement:
        """Player is successfully saying something."""

        return Announcement(
            f'You say, "{player_message}"',
            f'[cyan]{player_name}[/] says, "{player_message}"',
        )

    def process(self, client: Client, _command: str, args: List[str]) -> None:
        try:
            if not client.is_logged_in:
                raise NotLoggedIn

            if not args:
                raise MissingArguments

        except NotLoggedIn:
            self.send.prompt(client)

        except MissingArguments:
            self.send.private(client, self.no_args_msg)

        else:
            speaking_msg = self.speaking_msg(client.player.name, self._join_args(args))

            self.send.local(
                client.player.current_room_id,
                speaking_msg.to_room,
                [client],
            )

            self.send.private(client, speaking_msg.to_self)
