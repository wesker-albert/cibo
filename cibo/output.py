"""Output module"""

from textwrap import TextWrapper

from cibo.models.messages import Messages
from cibo.telnet import TelnetServer


class Output:
    """Responsible for constructing messages thar are sent to a client"""

    def __init__(self, messages: Messages):
        super().__init__()

        self.textwrap = TextWrapper(
            width=76,
            replace_whitespace=False,
            drop_whitespace=True,
            initial_indent="  ",
            subsequent_indent="  ",
        )

        self.messages = messages

    def _wrap(self, value: str) -> str:
        return self.textwrap.fill(value)

    def prompt(self, telnet: TelnetServer, client):
        """Prints a command prompt to the specified client"""

        telnet.send_message(client, self.messages.prompt)

    def private(self, telnet: TelnetServer, client, body: str):
        """Prints a message only to the specified client"""

        telnet.send_message(client, body)

    def local(self):
        """Prints a message to all clients within the room"""
        return

    def sector(self):
        """Prints a message to all clients within the sector"""
        return

    def region(self):
        """Prints a message to all clients within the sector"""
        return

    def server(self):
        """Prints a message to all clients on the server"""
        return
