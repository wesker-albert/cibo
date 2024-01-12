"""Repetative logic that is carried out every second."""

from typing import List, Optional

from cibo.actions._base_ import Action
from cibo.models.client import Client


class EverySecond(Action):
    """Repetative logic that is carried out every second."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(
        self, _client: Client, _command: Optional[str], _args: List[str]
    ) -> None:
        pass
