from typing import List

from cibo.client import Client
from cibo.messages.__message__ import Message
from cibo.messages.prompt import Prompt
from cibo.telnet import TelnetServer


class Room:
    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet

        self._prompt = Prompt()

    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def get(self, client: Client, message: Message) -> List[str]:
        return [self._format(message)] + self._prompt.get(client)

    def send(
        self, room_id: int, message: Message, ignored_clients: List[Client]
    ) -> None:
        """Prints a message to all clients whose player are within the room."""

        for client in self._telnet.get_connected_clients():
            if (
                client.is_logged_in
                and client.player
                and client.player.current_room_id == room_id
                and client not in ignored_clients
            ):
                client.send_message(self.get(client, message))
