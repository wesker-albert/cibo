from abc import ABC

from cibo.config import ServerConfig


class Output(ABC):
    def __init__(self, server_config: ServerConfig):
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._world = self._server_config.world
