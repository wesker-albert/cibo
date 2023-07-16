"""Make others aware that a player has abruptly disconnected."""

from typing import List, Optional

from cibo.actions import Action
from cibo.client import Client


class _Disconnect(Action):
    """Make others aware that a player has abruptly disconnected."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        if client.player:
            self._send.local(
                client.player.room,
                f"You watch in horror as [cyan]{client.player.name}[/] "
                "proceeds to slowly eat their own head. They eventually disappear "
                "into nothingness.",
                [client],
            )
