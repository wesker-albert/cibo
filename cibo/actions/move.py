"""Navigates a player between available rooms."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Move(Action):
    """Navigates a player between available rooms."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, _client: Client, _command: str, _args: List[str]):
        pass
