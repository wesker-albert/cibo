"""A client is created by the server any time a user connection is established. It
contains nonpersistent session information and relationships, necessary to carry
out interactions between the user and the server.
"""

import socket as socket_
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from cibo.models import Player


class ClientLoginState(int, Enum):
    """The different login states a client can be in."""

    PRE_LOGIN = 1
    LOGGED_IN = 2


@dataclass
class Client:
    """Represents a client connected to the server."""

    socket: socket_.socket
    address: str
    encoding: str
    buffer: str
    last_check: float
    login_state: ClientLoginState
    registration: Optional[Player]
    player: Optional[Player]

    @property
    def is_logged_in(self) -> bool:
        """Check if the client is logged in.

        Returns:
            bool: Is the client logged in or not
        """

        return self.login_state is ClientLoginState.LOGGED_IN

    @property
    def _prompt(self) -> str:
        """The prompt that appears before the client's terminal input.

        Returns:
            str: The prompt text
        """

        return "> "

    def _send_message(self, message: str) -> None:
        """Sends the message text to the client. The text will be printed out in
        the client's terminal.

        Args:
            message (str): The body text of the message
        """

        try:
            self.socket.sendall(bytearray(message, self.encoding))

        # a socket error will be raised if the client has already disconnected,
        # in which case we want to silently fail
        except socket_.error:
            return

    def send_message(self, message: str) -> None:
        """Sends the message text to the client, and apends a prompt at the end.

        Args:
            message (str): The body text of the message
        """

        self._send_message(f"\n\r\n\r{message}\n\r\n\r{self._prompt}")

    def send_prompt(self) -> None:
        """Sends a prompt to the client."""

        self._send_message(f"\n\r{self._prompt}")

    def disconnect(self) -> None:
        """Disconnect the client from the server."""

        self.socket.shutdown(socket_.SHUT_RDWR)
        self.socket.close()
