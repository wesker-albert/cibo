"""A client is created by the server any time a user connection is established. It
contains nonpersistent session information and relationships, necessary to carry
out interactions between the user and the server.
"""

import socket as socket_
from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import List, Optional, Self

from cibo.models.command import CommandFlowState, CommandHistoryEntry
from cibo.models.data.character import Character
from cibo.models.data.user import User
from cibo.models.prompt import Prompt


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
    last_check: float
    buffer: str = ""
    login_state: ClientLoginState = ClientLoginState.PRE_LOGIN
    registration: User = User()  # TODO: deprecate
    user: User = User()
    character: Character = Character()
    command_history: List[CommandHistoryEntry] = field(default_factory=lambda: [])
    command_flow_state: Optional[CommandFlowState] = None

    @classmethod
    def create_new_client(
        cls, socket: socket_.socket, address: str, encoding: str
    ) -> Self:
        """Create a brand new client, in a pre-login state.

        Args:
            socket (socket_.socket): Socket to attach the client to.
            address (str): Return address for the client.
            encoding (str): Character encoding to use.

        Returns:
            Self: A fresh, new client object.
        """

        return cls(
            socket=socket,
            address=address,
            encoding=encoding,
            last_check=time(),
        )

    @property
    def is_logged_in(self) -> bool:
        """Check if the client is logged in.

        Returns:
            bool: Is the client logged in or not.
        """

        return self.login_state is ClientLoginState.LOGGED_IN

    @property
    def is_registered(self) -> bool:
        """Check if the client has registration information.

        Returns:
            bool: Does the client have user regisration info.
        """

        return bool(self.registration.is_dirty())

    @property
    def prompt(self) -> Prompt:
        """The prompt that appears before the client's terminal input.

        Returns:
            Prompt: The prompt object.
        """

        return Prompt("> ")

    def send_message(self, message: str) -> None:
        """Sends the message text to the client. The text will be printed out in
        the client's terminal.

        Args:
            message (str): The body text of the message.
        """

        try:
            self.socket.sendall(bytearray(message, self.encoding))

        # a socket error will be raised if the client has already disconnected,
        # in which case we want to silently fail
        except socket_.error:
            return

    def send_prompt(self) -> None:
        """Sends the prompt text to the client."""

        self.send_message(str(self.prompt))

    def disconnect(self) -> None:
        """Disconnect the client from the server."""

        self.socket.shutdown(socket_.SHUT_RDWR)
        self.socket.close()

    def log_out(self) -> None:
        """Log the client out of their current user session."""

        self.login_state = ClientLoginState.PRE_LOGIN

        self.user.save()

        self.user = User()

    def log_in(self, user: User) -> None:
        """Log the client in as the given user.

        Args:
            user (User): The user the client will assume.
        """

        self.user = user
        self.login_state = ClientLoginState.LOGGED_IN

    def add_command_history_entry(self, entry: CommandHistoryEntry) -> None:
        """Add an entry to the input history, and trim the list so that it is never
        larger than the last 50 entries.

        Args:
            entry (CommandHistoryEntry): The entry, including the command and arguments.
        """

        del self.command_history[:-50]

        self.command_history.append(entry)
