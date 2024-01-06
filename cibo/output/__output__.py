from abc import ABC, abstractmethod

from cibo.models.message import Message, MessageRoute
from cibo.models.server_config import ServerConfig


class Output(ABC):
    def __init__(self, server_config: ServerConfig):
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._world = self._server_config.world

    @abstractmethod
    def _format(self, message: Message) -> str:
        pass

    @abstractmethod
    def send(self, message: MessageRoute) -> None:
        pass
