"""Alert the client an error occurred."""

from typing import List, Optional

from cibo.actions import Action
from cibo.client import Client


class _Error(Action):
    """Alert the client an error occurred."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return ["message"]

    def process(self, client: Client, _command: Optional[str], args: List[str]):
        self._send.private(client, f"[bright_red]{args[0]}[/]")
