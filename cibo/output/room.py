from typing import List

from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute
from cibo.output.__output__ import Output


class Room(Output):
    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute, ignored_clients: List[Client]) -> None:
        """Prints a message to all clients whose player are within the room."""

        for client in self._telnet.get_connected_clients():
            if (
                client.is_logged_in
                and client.player
                and client.player.current_room_id in message.room_ids
                and client not in ignored_clients
            ):
                client.send_message(self._format(message.message))
                client.send_prompt()
