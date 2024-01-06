from abc import ABC, abstractmethod

from cibo.models.message import Message, MessageRoute
from cibo.models.server_config import ServerConfig
from cibo.resources.rooms import Rooms


class Output(ABC):
    def __init__(self, server_config: ServerConfig):
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._world = self._server_config.world

    @property
    def rooms(self) -> Rooms:
        """All the rooms in the world.

        Returns:
            Rooms: The rooms.
        """
        return self._world.rooms

    @abstractmethod
    def _format(self, message: Message) -> str:
        pass

    @abstractmethod
    def send(self, message: MessageRoute) -> None:
        pass
