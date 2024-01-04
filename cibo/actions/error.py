"""Alert the client an error occurred."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.client import Client
from cibo.output import Message


class Error(Action):
    """Alert the client an error occurred."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return ["message"]

    def error_message(self, message: str) -> Message:
        return Message(f"[bright_red]{message}[/]")

    def process(self, client: Client, _command: Optional[str], args: List[str]) -> None:
        self.output.send_private_message(client, self.error_message(args[0]))
