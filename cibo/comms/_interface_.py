"""Commss are types of messages that can be send to clients, connected to the server.
Different comms types will target different clients, depending on the routing
supplied.
"""

from typing import Optional

from cibo.comms.private import Private
from cibo.comms.region import Region
from cibo.comms.room import Room
from cibo.comms.sector import Sector
from cibo.comms.server import Server
from cibo.comms.vicinity import Vicinity
from cibo.entities._interface_ import EntityInterface
from cibo.exceptions import MessageRouteMissingParameters
from cibo.models.client import Client
from cibo.models.message import MessageRoute
from cibo.telnet import TelnetServer


class CommsInterface:
    """Comms interface layer. Exposes the different comms types that can be used to
    send messages to clients.

    Additionally offers a place to create reusable "comms chain" methods for
    specific use cases, where multiple comms types and routes may be necessary.

    Args:
        telnet (TelnetServer): The configured telnet server to use.
        entity_interface (EntityInterface): The interface instance to use, when
            referencing entities in a comms message.
    """

    def __init__(self, telnet: TelnetServer, entity_interface: EntityInterface) -> None:
        self._telnet = telnet
        self._entities = entity_interface

        self._private = Private(self._telnet, self._entities)
        self._room = Room(self._telnet, self._entities)
        self._sector = Sector(self._telnet, self._entities)
        self._region = Region(self._telnet, self._entities)
        self._server = Server(self._telnet, self._entities)
        self._vicinity = Vicinity(self._telnet, self._entities)

    def send_prompt(self, client: Client) -> None:
        """Sends a prompt to the specified client."""

        client.send_prompt()

    def send_to_client(self, message: MessageRoute) -> None:
        """Sends a private message, to a specific client.

        Requires a `client` is specific within the routing object.
        """
        if not message.client:
            raise MessageRouteMissingParameters

        self._private.send(message)

    def send_to_room(self, message: MessageRoute) -> None:
        """Sends a message to clients whose player is currently located within the
        supplied room ID(s).

        Requires `ids` are specified within the routing object.
        """
        if not message.ids:
            raise MessageRouteMissingParameters

        self._room.send(message)

    def send_to_sector(self, message: MessageRoute) -> None:
        """Sends a message to clients whose player is currently located within the
        supplied sector ID(s).

        Requires `ids` are specified within the routing object.
        """
        if not message.ids:
            raise MessageRouteMissingParameters

        self._sector.send(message)

    def send_to_region(self, message: MessageRoute) -> None:
        """Sends a message to clients whose player is currently located within the
        supplied region ID(s).

        Requires `ids` are specified within the routing object.
        """

        if not message.ids:
            raise MessageRouteMissingParameters

        self._region.send(message)

    def send_to_server(self, message: MessageRoute) -> None:
        """Sends a server-wide message to clients who are currently logged into a
        player session.
        """

        self._server.send(message)

    def send_to_vicinity(
        self,
        message: MessageRoute,
        room_message: Optional[MessageRoute] = None,
        adjoining_room_message: Optional[MessageRoute] = None,
    ) -> None:
        """Sends individually specified messages to the appropriate clients, within
        the general vicinity.

        Requires a `client` is specific within the `message` object.

        Requires `ids` are specified within the `room_message` object, as well as the
        `adjoining_room_message` object (if included).

        Args:
            message (MessageRoute): Message intended for the client who is the
                origin of the comms.
            room_message (Optional[MessageRoute], optional): Message send to any
                clients that are in the same room as the origin client.
                Defaults to None.
            adjoining_room_message (Optional[MessageRoute], optional): An optional
                message to be sent to specified adjoining rooms. Defaults to None.
        """

        self._vicinity.send(message, room_message, adjoining_room_message)
