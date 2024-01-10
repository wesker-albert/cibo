"""Clients who have connected to the server, since last update poll."""

from cibo.actions import Connect
from cibo.events._base_ import Event


class ConnectEvent(Event):
    """Clients who have connected to the server, since last update poll."""

    def process(self) -> None:
        for client in self._telnet.get_new_clients():
            Connect(self._server_config).process(client, None, [])
