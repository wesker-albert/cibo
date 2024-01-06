from typing import Optional

from cibo.models.message import MessageRoute
from cibo.models.server_config import ServerConfig
from cibo.output.private import Private
from cibo.output.room import Room


class Vicinity:
    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

        self._private = Private(self._server_config)
        self._room = Room(self._server_config)

    def send(
        self,
        client_message: MessageRoute,
        room_message: MessageRoute,
        vicinity_message: Optional[MessageRoute] = None,
    ) -> None:
        if client_message.client:
            self._private.send(client_message)

            room_message.ignored_clients = [client_message.client]
            self._room.send(room_message)

            if vicinity_message:
                vicinity_message.ignored_clients = [client_message.client]
                self._room.send(vicinity_message)
