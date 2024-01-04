from typing import Optional

from cibo.client import Client
from cibo.messages.__message__ import Message, MessageRoute
from cibo.messages.private import Private
from cibo.messages.room import Room
from cibo.telnet import TelnetServer


class Vicinity:
    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet

        self._private = Private()
        self._room = Room(self._telnet)

    def send(
        self,
        client: Client,
        client_message: Message,
        room_message: MessageRoute,
        vicinity_message: Optional[MessageRoute] = None,
    ) -> None:
        self._private.send(client, client_message)
        self._room.send(room_message.room_id, room_message.message, [client])

        if vicinity_message:
            self._room.send(
                vicinity_message.room_id,
                vicinity_message.message,
                [client],
            )
