"""Outputs are types of messages that can be send to clients, connected to the server.
Different output types will target different clients, depending on the routing
supplied.
"""

from typing import Optional

from cibo.models.client import Client
from cibo.models.message import MessageRoute
from cibo.outputs.private import Private
from cibo.outputs.region import Region
from cibo.outputs.room import Room
from cibo.outputs.sector import Sector
from cibo.outputs.server import Server
from cibo.resources.world import World
from cibo.telnet import TelnetServer


class OutputProcessor:
    """Output processing abstraction layer. Exposes the different output types that
    can be used to send messages to clients.

    Additionally offers a place to create reusable "output chain" methods for
    specific use cases, where multiple output types and routes are necessary.
    """

    def __init__(self, telnet: TelnetServer, world: World) -> None:
        self._telnet = telnet
        self._world = world

        self._private = Private(self._telnet, self._world)
        self._room = Room(self._telnet, self._world)
        self._sector = Sector(self._telnet, self._world)
        self._region = Region(self._telnet, self._world)
        self._server = Server(self._telnet, self._world)

    def send_prompt(self, client: Client) -> None:
        """Sends a prompt to the specified client."""

        client.send_prompt()

    def send_to_client(self, message: MessageRoute) -> None:
        """Sends a private message, to a specific client.

        Requires a `client` is specific within the routing object.
        """

        self._private.send(message)

    def send_to_room(self, message: MessageRoute) -> None:
        """Sends a message to clients whose player is currently located within the
        supplied room ID(s).

        Requires `ids` are specified within the routing object.
        """

        self._room.send(message)

    def send_to_sector(self, message: MessageRoute) -> None:
        """Sends a message to clients whose player is currently located within the
        supplied sector ID(s).

        Requires `ids` are specified within the routing object.
        """

        self._sector.send(message)

    def send_to_region(self, message: MessageRoute) -> None:
        """Sends a message to clients whose player is currently located within the
        supplied region ID(s).

        Requires `ids` are specified within the routing object.
        """

        self._region.send(message)

    def send_to_server(self, message: MessageRoute) -> None:
        """Sends a server-wide message to clients who are currently logged into a
        player session.
        """

        self._server.send(message)

    def send_to_vicinity(
        self,
        client_message: MessageRoute,
        room_message: MessageRoute,
        adjoining_room_message: Optional[MessageRoute] = None,
    ) -> None:
        """Sends individually specified messages to the appropriate clients, within
        the general vicinity.

        Requires a `client` is specific within the `client_message` object.

        Requires `ids` are specified within the `room_message` object, as well as the
        `adjoining_room_message` object (if included).

        Args:
            client_message (MessageRoute): Message intended for the client who is the
                origin of the output.
            room_message (MessageRoute): Message send to any clients that are in the
                same room as the origin client.
            adjoining_room_message (Optional[MessageRoute], optional): An optional
                message to be sent to specified adjoining rooms. Defaults to None.
        """

        if client_message.client:
            self.send_to_client(client_message)

            room_message.ignored_clients = [client_message.client]
            self.send_to_room(room_message)

            if adjoining_room_message:
                adjoining_room_message.ignored_clients = [client_message.client]
                self.send_to_room(adjoining_room_message)
