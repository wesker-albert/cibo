"""Output module"""

from enum import Enum
from textwrap import TextWrapper
from typing import List

from cibo.client import Client

# TODO: figure out what to do with this


class TerminalColors(str, Enum):
    """Codes to display color in terminal output."""

    BLACK = "\033[30m"
    RED = "\033[31m"
    LIGHT_RED = "\033[91m"
    GREEN = "\033[32m"
    LIGHT_GREEN = "\033[92m"
    YELLOW = "\033[33m"
    LIGHT_YELLOW = "\033[93m"
    BLUE = "\033[34m"
    LIGHT_BLUE = "\033[94m"
    MAGENTA = "\033[35m"
    LIGHT_MAGENTA = "\033[95m"
    CYAN = "\033[36m"
    LIGHTCYAN = "\033[96m"
    GRAY = "\033[37m"
    DARK_GRAY = "\033[90m"
    WHITE = "\033[97m"
    NO_COLOR = "\033[0m\033[49m"


class TerminalStyle(str, Enum):
    """Codes to display text styles in terminal output."""

    BOLD = "\033[1m"
    NO_STYLE = "\033[22m"


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
