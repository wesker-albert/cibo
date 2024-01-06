from cibo.models.message import Message, MessageRoute
from cibo.output.__output__ import Output


class Sector(Output):
    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute) -> None:
        """Prints a message to all clients whose player are within the room."""

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.player:
                room = self.rooms.get_by_id(client.player.current_room_id)

                if (
                    room.sector.id_ in message.ids
                    and client not in message.ignored_clients
                ):
                    client.send_message(self._format(message.message))
                    client.send_prompt()
