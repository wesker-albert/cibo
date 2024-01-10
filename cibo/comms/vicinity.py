"""Sends individually specified messages to the appropriate clients, within
the general vicinity.
"""

from typing import Optional

from cibo.comms._base_ import Comms
from cibo.comms.private import Private
from cibo.comms.room import Room
from cibo.entities.world import World
from cibo.exceptions import MessageRouteMissingParameters
from cibo.models.message import Message, MessageRoute
from cibo.telnet import TelnetServer


class Vicinity(Comms):
    """Sends individually specified messages to the appropriate clients, within
    the general vicinity.
    """

    def __init__(self, telnet: TelnetServer, world: World) -> None:
        super().__init__(telnet, world)

        self._private = Private(telnet, world)
        self._room = Room(telnet, world)

    def _format(self, _message: Message) -> str:  # pytest: no cover
        return str()

    def send(
        self,
        message: MessageRoute,
        room_message: Optional[MessageRoute] = None,
        adjoining_room_message: Optional[MessageRoute] = None,
    ) -> None:
        if not message.client or not room_message:
            raise MessageRouteMissingParameters

        self._private.send(message)

        room_message.ignored_clients = [message.client]
        self._room.send(room_message)

        if adjoining_room_message:
            adjoining_room_message.ignored_clients = [message.client]
            self._room.send(adjoining_room_message)
