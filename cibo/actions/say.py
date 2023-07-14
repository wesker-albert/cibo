"""Say something to the current room."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Say(Action):
    """Say something to the current room."""

    def aliases(self) -> List[str]:
        return ["say"]

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        if not client.is_logged_in or not client.player:
            client.send_prompt()
            return

        if len(self._join_args(args)) == 0:
            self._send.private(
                client, "You try to think of something clever to say, but fail."
            )
            return

        self._send.local(
            f'#MAGENTA#{client.player.name}#NOCOLOR# says, "{self._join_args(args)}"',
            [client],
        )

        self._send.private(client, f'You say, "{self._join_args(args)}"')
