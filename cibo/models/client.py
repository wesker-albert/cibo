"""Client models"""

import socket as socket_
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from cibo.models.player import Player


class ClientLoginState(int, Enum):
    """The different login states a client can be in."""

    PRE_LOGIN = 1
    ACCOUNT_CREATION = 2
    LOGGED_IN = 3


@dataclass
class Client:
    """Represents a client connected to the server."""

    id_: UUID
    socket: socket_.socket
    address: str
    buffer: str
    last_check: float
    login_state: ClientLoginState
    player: Optional[Player]

    @property
    def is_logged_in(self) -> bool:
        """Check if the client is logged in.

        Returns:
            bool: Is the client logged in or not
        """

        return self.login_state is ClientLoginState.LOGGED_IN

    def send_message(self, message: str) -> None:
        """Sends the message text to the client. The text will be printed out in
        the client's terminal.

        Args:
            message (str): The body text of the message
        """

        try:
            self.socket.sendall(bytearray(f"{message}\n\r", "utf-8"))

        # a socket error will be raised if the client has already disconnected,
        # in which case we want to silently fail
        except socket_.error:
            return
