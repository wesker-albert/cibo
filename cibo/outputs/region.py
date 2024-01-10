"""Sends a message to clients whose player is currently located within the
supplied region ID(s)."""

from cibo.models import Message, MessageRoute
from cibo.outputs.__output__ import Output


class Region(Output):
    """Sends a message to clients whose player is currently located within the
    supplied region ID(s)."""

    def _format(self, message: Message) -> str:
        return f"\r{message}"

    def send(self, message: MessageRoute) -> None:
        for client in self._telnet.get_connected_clients():
            if client.is_logged_in:
                room = self._world.rooms.get_by_id(client.player.current_room_id)
                sector = self._world.sectors.get_by_id(room.sector.id_)

                if (
                    sector.region.id_ in message.ids
                    and client not in message.ignored_clients
                ):
                    client.send_message(self._format(message.message))

                    if message.send_prompt:
                        client.send_prompt()