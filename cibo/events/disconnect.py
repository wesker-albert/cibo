"""Clients who have disconnected from the server, since last update poll."""

from cibo.events import Event


class Disconnect(Event):
    """Clients who have disconnected from the server, since last update poll."""

    def process(self) -> None:
        """Process client disconnection Events."""

        for dc_client in self._telnet.get_disconnected_clients():
            for client in self._telnet.get_connected_clients():
                client.send_message(f"Client {dc_client.address} disconnected.")
