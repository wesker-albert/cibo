"""Clients who have disconnected from the server, since last update poll."""

from cibo.actions import _Disconnect
from cibo.events import Event


class Disconnect(Event):
    """Clients who have disconnected from the server, since last update poll."""

    def process(self) -> None:
        for client in self._telnet.get_disconnected_clients():
            _Disconnect(self._telnet).process(client, None, [])
