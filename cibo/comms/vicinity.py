"""Sends individually specified messages to the appropriate clients, within
the general vicinity.
"""

from typing import Optional

from cibo.comms import Comm
from cibo.comms.private import Private
from cibo.comms.room import Room
from cibo.entities._interface_ import EntityInterface
from cibo.exceptions import MessageRouteMissingParameters
from cibo.models.message import Message, MessageRoute
from cibo.telnet import TelnetServer


class Vicinity(Comm):
    """Sends individually specified messages to the appropriate clients, within
    the general vicinity.
    """

    def __init__(self, telnet: TelnetServer, entity_interface: EntityInterface) -> None:
        super().__init__(telnet, entity_interface)

        self._private = Private(telnet, entity_interface)
        self._room = Room(telnet, entity_interface)

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
