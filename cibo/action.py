"""Actions module"""


from cibo.models.client import Client
from cibo.telnet import TelnetServer


class ActionProcessor:
    """Available interactions with the world."""

    def __init__(self, telnet: TelnetServer) -> None:
        """Creates the action processor instance.

        Args:
            telnet (TelnetServer): The Telnet server which supplies us with logic
                to help process the actions
        """

        self.telnet = telnet

    def register(self, _client: Client, _args: str):
        """Register a new player with the server."""
        return

    def login(self, _client: Client, _args: str):
        """Log in to an existing player on the server."""
        return

    def say(self, client: Client, args: str):
        """Say something to the current room."""

        for connected_client in self.telnet.get_connected_clients():
            connected_client.send_message(f'{client.address} says, "{args}"')

    def move(self, _client: Client, _args: str):
        """Moves a client between available rooms."""
        return

    def look(self, _client: Client, _args: str):
        """Returns information about the room or object targeted."""
        return

    def exits(self, _client: Client, _args: str):
        """Returns the available exits."""
        return

    def quit_(self, _client: Client, _args: str):
        """Quits the game and disconnects the client."""
        return

    def spawn(self, _client: Client, _args: str):
        """Spawns the character into the world."""
        return
