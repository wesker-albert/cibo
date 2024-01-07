"""Abstraction to be used as a base class for every output type."""

from abc import ABC, abstractmethod

from cibo.models.message import Message, MessageRoute
from cibo.models.server_config import ServerConfig


class Output(ABC):
    """The base interface used by all Output classes.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig):
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._world = self._server_config.world

    @abstractmethod
    def _format(self, message: Message) -> str:
        """Formats the message, returning it as a string.

        Args:
            message (Message): The message object to format.

        Returns:
            str: The formatted and stringified message.
        """

        pass

    @abstractmethod
    def send(self, message: MessageRoute) -> None:
        """Format and then send the message to the appropriate recipients, according
        to the output type.

        Args:
            message (MessageRoute): The routing object, containing the message as well
                as the info required to route it to the right client(s).
        """

        pass
