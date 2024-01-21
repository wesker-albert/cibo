"""Actions are blocks of logic that are individually processed when an event calls
them directly, or a client sends the server a particular command, associated with that
specific action.

Any newly added Action classes that will be driven by a command from the client will
need to have their files created in the `cibo.actions.commands` path. Only then will
the new action be available to clients.
"""

from abc import ABC, abstractmethod
from typing import List

from cibo.comms._interface_ import CommsInterface
from cibo.entities.doors import Doors
from cibo.entities.items import Items
from cibo.entities.npcs import Npcs
from cibo.entities.rooms import Rooms
from cibo.models.client import Client
from cibo.server_config import ServerConfig
from cibo.utils.password import Password


class Action(ABC):
    """The base interface used by all Action classes.

    Args:
        server_config (ServerConfig): The server configuration object.
    """

    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

        self._telnet = self._server_config.telnet
        self._entities = self._server_config.entity_interface
        self._comms = self._server_config.comms_interface

        self._password_hasher = Password()

    @property
    def rooms(self) -> Rooms:
        """All the rooms in the world.

        Returns:
            Rooms: The rooms.
        """
        return self._entities.rooms

    @property
    def doors(self) -> Doors:
        """All the doors in the world.

        Returns:
            Doors: The doors, without Jim Morrison.
        """

        return self._entities.doors

    @property
    def items(self) -> Items:
        """All the items in the world.

        Returns:
            Items: The items.
        """

        return self._entities.items

    @property
    def npcs(self) -> Npcs:
        """All the NPCs in the world.

        Returns:
            Npcs: The NPCs.
        """

        return self._entities.npcs

    @property
    def comms(self) -> CommsInterface:
        """Access the comms interface, to send messages to clients.

        Returns:
            CommsInterface: The comms interface, to make available its methods.
        """

        return self._comms

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
