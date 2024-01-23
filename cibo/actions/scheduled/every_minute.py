"""Repetative logic that is carried out every minute."""

from typing import List, Optional

from cibo.actions import Action
from cibo.models.client import Client


class EveryMinute(Action):
    """Repetative logic that is carried out every minute."""

    @property
    def aliases(self) -> List[str]:
        return []

    @property
    def required_args(self) -> List[str]:
        return []

    def process(
        self, client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        if client.is_logged_in:
            client.user.save()
