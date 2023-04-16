from textwrap import TextWrapper

from cibo.models.messages import Messages


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

    def prompt(self):
        """Prints a command prompt to the specified client"""
        return

    def private(self):
        """Prints a message only to the specified client"""
        return

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
