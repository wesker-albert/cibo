from cibo.models.message import Message, MessageRoute
from cibo.outputs.__output__ import Output


class Room(Output):
    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute) -> None:
        """Prints a message to all clients whose player are within the room."""

        for client in self._telnet.get_connected_clients():
            if client.is_logged_in and client.player:
                if (
                    client.player.current_room_id in message.ids
                    and client not in message.ignored_clients
                ):
                    client.send_message(self._format(message.message))

                    if message.send_prompt:
                        client.send_prompt()
