"""Send the client only a prompt."""

from typing import List, Optional

from cibo.actions import Action
from cibo.client import Client


class _Prompt(Action):
    """Send the client only a prompt."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        self._send.prompt(client)
