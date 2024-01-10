"""Alert the client an error occurred."""

from typing import List, Optional

from cibo.actions.__action__ import Action
from cibo.models import Client, Message, MessageRoute


class Error(Action):
    """Alert the client an error occurred."""

    def aliases(self) -> List[str]:
        return []

    def required_args(self) -> List[str]:
        return ["message"]

    def _error_message(self, message: str) -> Message:
        """An error occurred."""

        return Message(f"[bright_red]{message}[/]")

    def process(self, client: Client, _command: Optional[str], args: List[str]) -> None:
        self.output.send_to_client(
            MessageRoute(self._error_message(args[0]), client=client)
        )
