"""The Output class provides message formatting and isolation logic, ensuring
that messages have a uniform style and reach only the clients they are intended to.
"""

from enum import Enum
from textwrap import TextWrapper
from typing import List

from cibo.client import Client
from cibo.telnet import TelnetServer


class Color(str, Enum):
    """Codes to display color in terminal output."""

    BLACK = "\033[30m"
    RED = "\033[31m"
    LRED = "\033[91m"
    GREEN = "\033[32m"
    LGREEN = "\033[92m"
    YELLOW = "\033[33m"
    LYELLOW = "\033[93m"
    BLUE = "\033[34m"
    LBLUE = "\033[94m"
    MAGENTA = "\033[35m"
    LMAGENTA = "\033[95m"
    CYAN = "\033[36m"
    LCYAN = "\033[96m"
    GRAY = "\033[37m"
    DGRAY = "\033[90m"
    WHITE = "\033[97m"
    NOCOLOR = "\033[0m\033[49m"


class Style(str, Enum):
    """Codes to display text styles in terminal output."""

    BOLD = "\033[1m"
    NOSTYLE = "\033[22m"


class Output:
    """Responsible for constructing messages that are sent to clients."""

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet

    def _wrap_message(self, message: str) -> str:
        """Wrap the text to a certain width, and include indentation.

        Args:
            message (str): The message body to wrap

        Returns:
            str: The wrapped text
        """

        text_wrapper = TextWrapper(
            width=76,
            replace_whitespace=False,
            drop_whitespace=True,
            initial_indent="  ",
            subsequent_indent="  ",
        )

        return text_wrapper.fill(message)

    def _format_message(self, message: str) -> str:
        """Format the message. First wrap the message, then replace any color or style
        flags with the correspending ANSI escape sequences.

        Color and style flags can be indicated with leading and trailing hash (#)
        characters.

        Args:
            message (str): The message to format

        Returns:
            str: The formatted message.
        """
        formatted_message = self._wrap_message(message)

        for color in Color:
            formatted_message = formatted_message.replace(
                f"#{color.name}#", color.value
            )

        for style in Style:
            formatted_message = formatted_message.replace(
                f"#{style.name}#", style.value
            )

        return formatted_message

    def private(
        self, client: Client, message: str, newline: bool = True, prompt: bool = True
    ) -> None:
        """Prints a message only to the client specified.

        Args:
            client (Client): The client to send the message to
            message (str): The body of the message
            newline (bool, optional): If the message should be prepended with a new
                line. Defaults to True.
            prompt (bool, optional): If a prompt should be included immediately after
                the message. Defaults to True.
        """

        formatted_message = self._format_message(message)

        client.send_message(
            f"\r\n{formatted_message}\r\n" if newline else f"{formatted_message}\r\n"
        )

        if prompt:
            client.send_prompt()

    # TODO: when we implement the concept of "rooms", make this method only send to
    # the clients in the room specified
    def local(self, message: str, ignore_clients: List[Client]):
        """Prints a message to all clients whose plater are within the room.

        Args:
            message (str): The body of the message
            ignore_clients (List[Client]): Clients that should not receive the message
        """

        formatted_message = self._format_message(message)

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client not in ignore_clients:
                client.send_message(f"\r{formatted_message}\r\n")
                client.send_prompt()

    def sector(self, _sector: int, _message: str, _ignore_clients: List[Client]):
        """Prints a message to all clients within the sector."""

        pass

    def region(self, _region: int, _message: str, _ignore_clients: List[Client]):
        """Prints a message to all clients within the sector."""

        pass

    def server(self, _message: str, _ignore_clients: List[Client]):
        """Prints a message to all clients on the server."""

        pass
