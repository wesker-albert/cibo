from abc import ABC, abstractmethod
from typing import Any

from cibo.models.message import Message, MessageRoute
from cibo.models.server_config import ServerConfig
from cibo.output.private import Private
from cibo.output.room import Room


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


class OutputChain(ABC):
    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

        self._private = Private(self._server_config)
        self._room = Room(self._server_config)

    @abstractmethod
    def send(self, *args: Any, **kwargs: Any) -> None:
        pass
