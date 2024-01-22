"""Sends a message to clients whose user is currently located within the
supplied room ID(s)."""

from cibo.comms import Comm
from cibo.models.message import Message, MessageRoute


class Room(Comm):
    """Sends a message to clients whose user is currently located within the
    supplied room ID(s)."""

    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute) -> None:
        for client in self._telnet.get_connected_clients():
            if (
                client.is_logged_in
                and client.user.current_room_id in message.ids
                and client not in message.ignored_clients
            ):
                client.send_message(self._format(message.message))

                if message.send_prompt:
                    client.send_prompt()
