"""Make others aware that a player has abruptly disconnected."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class _Disconnect(Action):
    """Make others aware that a player has abruptly disconnected."""

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        if client.player:
            self._send.local(
                f"You watch in horror as #MAGENTA#{client.player.name}#NOCOLOR# "
                "proceeds to slowly eat their own head. They eventually disappear "
                "into nothingness.",
                [client],
            )
