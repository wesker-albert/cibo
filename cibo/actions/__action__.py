"""Abstraction to be used as a base class for every action."""

from abc import ABC, abstractmethod
from typing import List

from cibo.models.client import Client
from cibo.models.server_config import ServerConfig
from cibo.output.private import Private
from cibo.output.room import Room
from cibo.output.vicinity import Vicinity
from cibo.password import Password
from cibo.resources.doors import Doors
from cibo.resources.items import Items
from cibo.resources.npcs import Npcs
from cibo.resources.resources import Resources
from cibo.resources.rooms import Rooms


class Action(ABC):
    """The base interface used by all Action classes.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    class Output:
        """Responsible for constructing messages that are sent to clients.

        Args:
            telnet (TelnetServer): The telnet server to use when outputting messages.
        """

        def __init__(self, server_config: ServerConfig) -> None:
            self._server_config = server_config

            self.send_private_message = Private(self._server_config).send
            self.send_room_message = Room(self._server_config).send
            self.send_vicinity_message = Vicinity(self._server_config).send

    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._world = self._server_config.world

        self._output = self.Output(self._server_config)

        self._password_hasher = Password()

    @property
    def resources(self) -> Resources:
        """Resource helper methods that aren't necesarily associated with just one
        resource type.

        Returns:
            Resources: The helper methods.
        """

        return self._world.resources

    @property
    def rooms(self) -> Rooms:
        """All the rooms in the world.

        Returns:
            Rooms: The rooms.
        """
        return self._world.rooms

    @property
    def doors(self) -> Doors:
        """All the doors in the world.

        Returns:
            Doors: The doors, without Jim Morrison.
        """

        return self._world.doors

    @property
    def items(self) -> Items:
        """All the items in the world.

        Returns:
            Items: The items.
        """

        return self._world.items

    @property
    def npcs(self) -> Npcs:
        """All the NPCs in the world.

        Returns:
            Npcs: The NPCs.
        """

        return self._world.npcs

    @property
    def output(self) -> Output:
        """Access the output formatter, to send messages to clients.

        Returns:
            Output: The output formatter instance, and its methods.
        """

        return self._output

    def _join_args(self, args: List[str]) -> str:
        """Join the list of args into a singular string, using a space as the
        delimiter.

        Args:
            args (List[str]): The list of args.

        Returns:
            str: All the args as one big string.
        """

        return " ".join([str(x) for x in args])

    @abstractmethod
    def aliases(self) -> List[str]:  # pytest: no cover
        """Command aliases mapped to the action. Clients can input these text
        commands, to trigger this action.

        If the action isn't intended to be directly available as a client command,
        returns an empty list.

        Returns:
            List[str]: Aliases associated with the action.
        """

        pass

    @abstractmethod
    def required_args(self) -> List[str]:  # pytest: no cover
        """Descriptions of the args required for the action.

        If no arguments are necessary for the action, returns an empty list.

        Returns:
            List[str]: Descriptions for each required argument.
        """

        pass

    @abstractmethod
    def process(
        self, client: Client, command: str, args: List[str]
    ) -> None:  # pytest: no cover
        """Process the logic for the action.

        Args:
            client (Client): The client who triggered the action.
            command (str): The command that the client sent.
            args (List[str]): The args necessary to the action.
        """

        pass
