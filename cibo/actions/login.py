"""Login Action"""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Login(Action):
    """Log in to an existing player on the server."""

    def required_args(self) -> List[str]:
        """Descriptions of the args required for the action."""

        return ["name", "password"]

    def process(self, client: Client, args: List[str]):
        """Process the logic for the action."""

        _ = client, args
