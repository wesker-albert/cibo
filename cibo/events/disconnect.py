from cibo.events import Event


class Disconnect(Event):
    """Client disconnection Event."""

    def process(self) -> None:
        """Process client disconnection events."""

        for dc_client in self._telnet.get_disconnected_clients():
            for client in self._telnet.get_connected_clients():
                client.send_message(f"Client {dc_client.address} disconnected.")
