"""Send the client only a prompt."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client


class Prompt(Action):
    """Send the client only a prompt."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return []

    def process(self, client: Client, _command: Optional[str], _args: List[str]):
        self.send.prompt(client)
