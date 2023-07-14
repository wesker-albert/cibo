"""Returns information about the room or object targeted."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        _ = client, args
