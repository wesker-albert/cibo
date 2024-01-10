"""Abstraction to be used as a base class for every comms type."""

from abc import ABC, abstractmethod

from cibo.models import Message, MessageRoute
from cibo.entities import World
from cibo.telnet import TelnetServer


class Comms(ABC):
    """The base interface used by all Comms classes.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, telnet: TelnetServer, world: World):
        self._telnet = telnet
        self._world = world

    @abstractmethod
    def _format(self, message: Message) -> str:  # pytest: no cover
        """Formats the message, returning it as a string.

        Args:
            message (Message): The message object to format.

        Returns:
            str: The formatted and stringified message.
        """

        pass

    @abstractmethod
    def send(self, message: MessageRoute) -> None:  # pytest: no cover
        """Format and then send the message to the appropriate recipients, according
        to the comms type.

        Args:
            message (MessageRoute): The routing object, containing the message as well
                as the info required to route it to the right client(s).
        """

        pass
