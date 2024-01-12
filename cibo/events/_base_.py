"""Abstraction to be used as a base class for every event."""

from abc import ABC, abstractmethod

from cibo.server_config import ServerConfig


class Event(ABC):
    """The base interface used by all Event classes.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._world = self._server_config.world
        self._comms = self._server_config.comms_interface

    @abstractmethod
    def process(self) -> None:  # pytest: no cover
        """Processes the logic for the specific event type."""

        pass