"""Clients who have disconnected from the server, since last update poll."""

from cibo.actions._disconnect import _Disconnect
from cibo.events.__event__ import Event


class Disconnect(Event):
    """Clients who have disconnected from the server, since last update poll."""

    def process(self) -> None:
        for client in self._telnet.get_disconnected_clients():
            _Disconnect(self._telnet, self._world).process(client, None, [])