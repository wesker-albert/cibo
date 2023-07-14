"""Returns the available exits."""

from typing import List

from cibo.actions import Action
from cibo.client import Client


class Exits(Action):
    """Returns the available exits."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, args: List[str]):
        _ = client, args
