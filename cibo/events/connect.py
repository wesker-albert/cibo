"""Clients who have connected to the server, since last update poll."""

from typing import Any

from cibo.actions.connect import Connect
from cibo.events._base_ import Event
from cibo.server_config import ServerConfig


class ConnectEvent(Event):
    """Clients who have connected to the server, since last update poll."""

    def __init__(
        self,
        server_config: ServerConfig,
    ) -> None:
        super().__init__(server_config)

        self._process.connect(self.process)

    def process(self, _sender: Any) -> None:
        for client in self._telnet.get_new_clients():
            Connect(self._server_config).process(client, None, [])
