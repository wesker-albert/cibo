"""Navigates a player between available rooms."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Move(Action):
    """Navigates a player between available rooms."""

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        _ = client, args
