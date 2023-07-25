"""Say something to the current room."""

from typing import List

from cibo.actions.__action__ import Action
from cibo.client import Client


class Say(Action):
    """Say something to the current room."""

    def aliases(self) -> List[str]:
        return ["say"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: str, args: List[str]):
        if not client.is_logged_in:
            self.send.prompt(client)
            return

        if not args:
            self.send.private(
                client, "You try to think of something clever to say, but fail."
            )
            return

        self.send.local(
            client.player.current_room_id,
            f'[cyan]{client.player.name}[/] says, "{self._join_args(args)}"',
            [client],
        )

        self.send.private(client, f'You say, "{self._join_args(args)}"')