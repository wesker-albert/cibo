"""Returns information about the room or object targeted."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Look(Action):
    """Returns information about the room or object targeted."""

    def aliases(self) -> List[str]:
        return ["l", "look"]

    def required_args(self) -> List[str]:
        return []

    def process(self, _client: Client, _command: str, args: List[str]):
        if not args:
            # TODO: return the room details
            return
