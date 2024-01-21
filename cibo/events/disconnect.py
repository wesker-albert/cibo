"""Clients who have disconnected from the server, since last update poll."""


from typing import Any

from cibo.actions.disconnect import Disconnect
from cibo.events._base_ import Event
from cibo.server_config import ServerConfig


class DisconnectEvent(Event):
    """Clients who have disconnected from the server, since last update poll."""

    def __init__(
        self,
        server_config: ServerConfig,
    ) -> None:
        super().__init__(server_config)

        self._process.connect(self.process)

    def process(self, _sender: Any) -> None:
        for client in self._telnet.get_disconnected_clients():
            Disconnect(self._server_config).process(client, None, [])
