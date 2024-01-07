from typing import Optional

from cibo.models.message import MessageRoute
from cibo.models.server_config import ServerConfig
from cibo.outputs.private import Private
from cibo.outputs.region import Region
from cibo.outputs.room import Room
from cibo.outputs.sector import Sector
from cibo.outputs.server import Server


class OutputProcessor:
    """Responsible for constructing messages that are sent to clients."""

    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

        self._private = Private(self._server_config)
        self._room = Room(self._server_config)
        self._sector = Sector(self._server_config)
        self._region = Region(self._server_config)
        self._server = Server(self._server_config)

    def send_to_client(self, message: MessageRoute) -> None:
        self._private.send(message)

    def send_to_room(self, message: MessageRoute) -> None:
        self._room.send(message)

    def send_to_sector(self, message: MessageRoute) -> None:
        self._sector.send(message)

    def send_to_region(self, message: MessageRoute) -> None:
        self._region.send(message)

    def send_to_server(self, message: MessageRoute) -> None:
        self._server.send(message)

    def send_to_vicinity(
        self,
        client_message: MessageRoute,
        room_message: MessageRoute,
        vicinity_message: Optional[MessageRoute] = None,
    ) -> None:
        if client_message.client:
            self.send_to_client(client_message)

            room_message.ignored_clients = [client_message.client]
            self.send_to_room(room_message)

            if vicinity_message:
                vicinity_message.ignored_clients = [client_message.client]
                self.send_to_room(vicinity_message)
