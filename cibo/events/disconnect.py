"""Clients who have disconnected from the server, since last update poll."""


from cibo.actions.disconnect import Disconnect
from cibo.events._base_ import Event


class DisconnectEvent(Event):
    """Clients who have disconnected from the server, since last update poll."""

    def process(self) -> None:
        for client in self._telnet.get_disconnected_clients():
            Disconnect(self._server_config).process(client, None, [])
