"""Quits the game and disconnects the client."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Quit(Action):
    """Quits the game and disconnects the client."""

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        _ = client, args
