from typing import Optional

from cibo.models.client import Client
from cibo.models.message import Message, MessageRoute
from cibo.models.server_config import ServerConfig
from cibo.output.__output__ import Output
from cibo.output.private import Private
from cibo.output.room import Room


class Vicinity(Output):
    def __init__(self, server_config: ServerConfig) -> None:
        super().__init__(server_config)

        self._private = Private(self._server_config)
        self._room = Room(self._server_config)

    def send(
        self,
        client: Client,
        client_message: Message,
        room_message: MessageRoute,
        vicinity_message: Optional[MessageRoute] = None,
    ) -> None:
        self._private.send(client, client_message)
        self._room.send(room_message, [client])

        if vicinity_message:
            self._room.send(vicinity_message, [client])
