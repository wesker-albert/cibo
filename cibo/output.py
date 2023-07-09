"""Output module"""

from textwrap import TextWrapper

from cibo.models.client import Client
from cibo.telnet import TelnetServer


class Output:
    """Responsible for constructing messages that are sent to a client."""

    def __init__(self, telnet: TelnetServer) -> None:
        self.telnet = telnet

        self.textwrap = TextWrapper(
            width=76,
            replace_whitespace=False,
            drop_whitespace=True,
            initial_indent="  ",
            subsequent_indent="  ",
        )

    def _wrap(self, value: str) -> str:
        return self.textwrap.fill(value)

    def prompt(self, client: Client) -> None:
        """Prints a command prompt to the specified client."""

        self.telnet.send_message(client, "> \n")

    def private(self, client: Client, body: str) -> None:
        """Prints a message only to the specified client."""

        self.telnet.send_message(client, body)

    def local(self):
        """Prints a message to all clients within the room."""
        return

    def sector(self):
        """Prints a message to all clients within the sector."""
        return

    def region(self):
        """Prints a message to all clients within the sector."""
        return

    def server(self):
        """Prints a message to all clients on the server."""
        return
