"""Clients who have connected to the server, since last update poll."""

from cibo.events import Event


class Connect(Event):
    """Clients who have connected to the server, since last update poll."""

    def process(self) -> None:
        """Process new client connection Events."""

        for client in self._telnet.get_new_clients():
            client.send_message(
                "Welcome to cibo.\n"
                "* Enter 'register name password' to create a new player.\n"
                "* Enter 'login name password' to log in to an existing player."
            )
