"""Say Action"""

from typing import List

from cibo.actions import Action
from cibo.models.client import Client


class Say(Action):
    """Say something to the current room."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        for connected_client in self._telnet.get_connected_clients():
            connected_client.send_message(
                f'{client.address} says, "{self._join_args(args)}"'
            )
