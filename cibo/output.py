"""Output module"""

from textwrap import TextWrapper
from typing import List

from cibo.models import Client

# TODO: figure out what to do with this


class Output:
    """Responsible for constructing messages that are sent to a client."""

    def __init__(self) -> None:
        self.textwrap = TextWrapper(
            width=76,
            replace_whitespace=False,
            drop_whitespace=True,
            initial_indent="  ",
            subsequent_indent="  ",
        )

    def _wrap(self, value: str) -> str:
        return self.textwrap.fill(value)

    def local(self, _clients: List[Client]):
        """Prints a message to all clients within the room."""
        return

    def sector(self, _clients: List[Client]):
        """Prints a message to all clients within the sector."""
        return

    def region(self, _clients: List[Client]):
        """Prints a message to all clients within the sector."""
        return

    def server(self, _clients: List[Client]):
        """Prints a message to all clients on the server."""
        return
