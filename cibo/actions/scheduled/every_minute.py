"""Repetative logic that is carried out every minute."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client


class EveryMinute(Action):
    """Repetative logic that is carried out every minute."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        if client.is_logged_in:
            client.player.save()
