"""Quit Action"""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Quit(Action):
    """Quits the game and disconnects the client."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args
