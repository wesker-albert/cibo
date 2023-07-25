"""Clients who have connected to the server, since last update poll."""

from cibo.actions.connect import Connect
from cibo.events.__event__ import Event


class ConnectEvent(Event):
    """Clients who have connected to the server, since last update poll."""

    def process(self) -> None:
        for client in self._telnet.get_new_clients():
            Connect(self._telnet, self._world).process(client, None, [])
