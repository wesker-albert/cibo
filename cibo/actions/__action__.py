"""Abstraction to be used as a base class for every Action."""

from abc import ABC, abstractmethod
from typing import List, Optional

from cibo.client import Client
from cibo.output import Output
from cibo.password import Password
from cibo.telnet import TelnetServer


class Action(ABC):
    """The base interface used by all Action classes."""

    def __init__(self, telnet: TelnetServer) -> None:
        self._telnet = telnet
        self._send = Output(self._telnet)
        self._password_hasher = Password()

    def _join_args(self, args: List[str]) -> str:
        """Join the list of args into a singular string, using a space as the
        delimiter.

        Args:
            args (List[str]): The list of args

        Returns:
            str: All the args as one big string
        """

        return " ".join([str(x) for x in args])

    @abstractmethod
    def aliases(self) -> List[str]:
        """Command aliases mapped to the Action. Clients can input these text
        commands, to trigger this Action.

        If the action isn't intended to be directly available as a client Command,
        returns an empty list.

        Returns:
            List[str]: Aliases associated with the Action
        """

        pass

    @abstractmethod
    def required_args(self) -> List[str]:
        """Descriptions of the args required for the Action.

        If no arguments are necessary for the Action, returns an empty list.

        Returns:
            List[str]: Descriptions for each required argument
        """

        pass

    @abstractmethod
    def process(self, client: Client, command: Optional[str], args: List[str]) -> None:
        """Process the logic for the Action.

        Args:
            client (Client): The client who triggered the Action
            command (str): The command that the client sent
            args (List[str]): The args necessary to the Action
        """

        pass
