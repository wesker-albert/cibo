"""Repetative logic that is carried out every minute."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client


class _EveryMinute(Action):
    """Repetative logic that is carried out every minute."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        if client.is_logged_in and client.player:
            client.player.save()
