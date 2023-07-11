"""Say Action"""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Say(Action):
    """Say something to the current room."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return []

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        if not client.is_logged_in or not client.player:
            client.send_prompt()
            return

        if len(args) == 0:
            client.send_message(
                "You try to think of something clever to say, but fail."
            )
            return

        for connected_client in self._telnet.get_connected_clients():
            connected_client.send_message(
                f'{client.player.name} says, "{self._join_args(args)}"'
            )
