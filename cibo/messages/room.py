from typing import List

from cibo.client import Client
from cibo.messages.__message__ import Message as MessageAbstract
from cibo.models.message import Message


class Room(MessageAbstract):
    def _format(self, message: Message) -> str:
        return f"\r{message}"

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
                client.send_message(self._format(message))
                client.send_prompt()
